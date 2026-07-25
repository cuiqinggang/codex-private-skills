[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory)]
    [ValidateSet('Install','Arm','Resume','Complete','Disarm','Status')]
    [string]$Action,
    [Parameter(Mandatory)]
    [string]$ConfigPath,
    [string]$StatePath,
    [string]$EntryPointManifestPath,
    [string]$CodeCommit,
    [ValidatePattern('^[a-fA-F0-9]{64}$')]
    [string]$PackageSha256,
    [string]$RunId,
    [string]$ResumeStep,
    [string]$EntryPointId,
    [ValidateRange(1, 20)]
    [int]$MaxAttempts = 3,
    [string]$RemoteStateUri,
    [ValidateRange(0, 3600)]
    [int]$NetworkWaitSeconds = 120,
    [string]$TaskName = 'RebootResumeAdapter'
)

$ErrorActionPreference = 'Stop'
$script:AllowedStatuses = @('READY','REBOOT_PENDING','RESUMING','COMPLETED','BLOCKED')
$script:StateFields = @(
    'schemaVersion','runId','status','resumeStep','entryPointId','previousBootId',
    'attempt','maxAttempts','codeCommit','packageSha256','stateRevision','updatedAt','lastErrorCode'
)

function Assert-Windows {
    if ($env:OS -ne 'Windows_NT') { throw 'This action requires native Windows.' }
}

function Get-BootIdentity {
    (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')
}

function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Required JSON file not found: $Path" }
    Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Write-AtomicJson([string]$Path, [object]$Value) {
    $directory = Split-Path -Parent $Path
    if (-not $directory) { throw 'State path must have a parent directory.' }
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    $temporary = Join-Path $directory ('.checkpoint-{0}.tmp' -f [guid]::NewGuid().ToString('N'))
    try {
        $json = $Value | ConvertTo-Json -Depth 8
        $stream = [IO.File]::Open($temporary, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        try {
            $bytes = [Text.UTF8Encoding]::new($false).GetBytes($json)
            $stream.Write($bytes, 0, $bytes.Length)
            $stream.Flush($true)
        } finally { $stream.Dispose() }
        if (Test-Path -LiteralPath $Path) {
            [IO.File]::Replace($temporary, $Path, $null)
        } else {
            [IO.File]::Move($temporary, $Path)
        }
    } finally {
        if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
    }
}

function Get-ProtectedRoot {
    if ([string]::IsNullOrWhiteSpace($env:ProgramData)) { throw 'ProgramData is unavailable.' }
    [IO.Path]::GetFullPath((Join-Path $env:ProgramData 'RebootResumeAdapter'))
}

function Assert-InProtectedRoot([string]$Path, [string]$Root) {
    $rootPrefix = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
    $full = [IO.Path]::GetFullPath($Path)
    if ($full -ne $rootPrefix.TrimEnd('\') -and -not $full.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes protected root: $Path" }
    $full
}

function Set-ProtectedRootAcl([string]$Root) {
    $administrators = [Security.Principal.SecurityIdentifier]::new('S-1-5-32-544')
    $system = [Security.Principal.SecurityIdentifier]::new('S-1-5-18')
    $acl = [Security.AccessControl.DirectorySecurity]::new()
    $acl.SetAccessRuleProtection($true, $false)
    $inherit = [Security.AccessControl.InheritanceFlags]'ContainerInherit, ObjectInherit'
    $propagate = [Security.AccessControl.PropagationFlags]::None
    foreach ($sid in @($administrators,$system)) {
        $rule = [Security.AccessControl.FileSystemAccessRule]::new(
            $sid,[Security.AccessControl.FileSystemRights]::FullControl,$inherit,$propagate,[Security.AccessControl.AccessControlType]::Allow)
        $acl.AddAccessRule($rule) | Out-Null
    }
    $acl.SetOwner($administrators)
    Set-Acl -LiteralPath $Root -AclObject $acl
}

function Set-ProtectedFileAcl([string]$Path) {
    $administrators = [Security.Principal.SecurityIdentifier]::new('S-1-5-32-544')
    $system = [Security.Principal.SecurityIdentifier]::new('S-1-5-18')
    $acl = [Security.AccessControl.FileSecurity]::new()
    $acl.SetAccessRuleProtection($true, $false)
    foreach ($sid in @($administrators,$system)) {
        $rule = [Security.AccessControl.FileSystemAccessRule]::new(
            $sid,[Security.AccessControl.FileSystemRights]::FullControl,[Security.AccessControl.AccessControlType]::Allow)
        $acl.AddAccessRule($rule) | Out-Null
    }
    $acl.SetOwner($administrators)
    Set-Acl -LiteralPath $Path -AclObject $acl
}

function Assert-ProtectedPath([string]$Path, [string]$Root) {
    $full = Assert-InProtectedRoot $Path $Root
    if (-not (Test-Path -LiteralPath $full)) { throw "Protected path is missing: $full" }
    $item = Get-Item -LiteralPath $full -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "Reparse point is forbidden: $full" }
    $acl = Get-Acl -LiteralPath $full
    $allowed = @('S-1-5-18','S-1-5-32-544')
    foreach ($rule in @($acl.Access)) {
        if ($rule.AccessControlType -ne 'Allow') { continue }
        $sid = $rule.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
        $writeMask = [Security.AccessControl.FileSystemRights]'Write,Modify,FullControl,ChangePermissions,TakeOwnership'
        if (($rule.FileSystemRights -band $writeMask) -ne 0 -and $allowed -notcontains $sid) {
            throw "Unapproved write ACL on protected path: $sid"
        }
    }
    if ($full -eq [IO.Path]::GetFullPath($Root) -and -not $acl.AreAccessRulesProtected) { throw "Protected root ACL inheritance is enabled: $full" }
    $full
}

function Assert-State([object]$State, [object]$Config) {
    $actualFields = @($State.PSObject.Properties.Name | Sort-Object)
    $expectedFields = @($script:StateFields | Sort-Object)
    if (($actualFields -join '|') -ne ($expectedFields -join '|')) { throw 'Checkpoint contains missing or unapproved fields.' }
    if ([int]$State.schemaVersion -ne 1) { throw 'Unsupported checkpoint schema.' }
    if ($script:AllowedStatuses -notcontains [string]$State.status) { throw 'Invalid checkpoint status.' }
    foreach ($field in @('runId','resumeStep','entryPointId','previousBootId','codeCommit','packageSha256','stateRevision')) {
        if ($null -eq $State.$field -or [string]::IsNullOrWhiteSpace([string]$State.$field)) { throw "Missing checkpoint field: $field" }
    }
    if ([string]$State.codeCommit -ne [string]$Config.codeCommit) { throw 'Checkpoint code commit mismatch.' }
    if ([string]$State.packageSha256 -ne [string]$Config.packageSha256) { throw 'Checkpoint package hash mismatch.' }
    if ([int]$State.attempt -gt [int]$State.maxAttempts) { throw 'Checkpoint attempt count is invalid.' }
    if ([string]$State.entryPointId -notmatch '^[A-Za-z0-9._-]{1,64}$') { throw 'Checkpoint EntryPointId is invalid.' }
    foreach ($value in @([string]$State.runId,[string]$State.resumeStep)) {
        if ($value -match '[\x00-\x1f]') { throw 'Checkpoint text contains control characters.' }
    }
}

function Confirm-RemotePendingState([object]$Config, [object]$LocalState) {
    if ([string]$LocalState.status -ne 'REBOOT_PENDING') { return }
    if ([string]::IsNullOrWhiteSpace([string]$Config.remoteStateUri)) { return }
    $deadline = [DateTime]::UtcNow.AddSeconds([int]$Config.networkWaitSeconds)
    do {
        try {
            $remote = Invoke-RestMethod -Uri ([string]$Config.remoteStateUri) -Method Get
            Assert-State $remote $Config
            if ([string]$remote.status -ne 'REBOOT_PENDING') { throw 'Remote checkpoint is not pending.' }
            foreach ($field in @('runId','stateRevision','codeCommit','packageSha256','entryPointId','resumeStep','previousBootId')) {
                if ([string]$remote.$field -ne [string]$LocalState.$field) { throw "Remote checkpoint mismatch: $field" }
            }
            return
        } catch {
            if ([DateTime]::UtcNow -ge $deadline) { throw }
            Start-Sleep -Seconds 5
        }
    } while ($true)
}

function Get-ManifestEntry([object]$Manifest, [string]$Id) {
    if ($Id -notmatch '^[A-Za-z0-9._-]{1,64}$') { throw 'EntryPointId has unsafe characters.' }
    $entry = @($Manifest.entryPoints | Where-Object { [string]$_.id -eq $Id })
    if ($entry.Count -ne 1) { throw 'EntryPointId is absent or ambiguous in the installed allowlist.' }
    $entryFields = @($entry[0].PSObject.Properties.Name | Sort-Object)
    if (($entryFields -join '|') -ne ((@('id','scriptPath','sha256') | Sort-Object) -join '|')) {
        throw 'Entrypoint contains unapproved fields.'
    }
    if ([string]$entry[0].scriptPath -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Entrypoint path traversal is forbidden.' }
    if ([IO.Path]::GetExtension([string]$entry[0].scriptPath) -ne '.ps1') { throw 'Entrypoint must be one PowerShell script.' }
    if ([string]$entry[0].sha256 -notmatch '^[a-fA-F0-9]{64}$') { throw 'Entrypoint hash is invalid.' }
    $entry[0]
}

function Read-ProtectedConfig([string]$Path, [bool]$RequireState) {
    $root = Get-ProtectedRoot
    if ([IO.Path]::GetFullPath($Path) -ne [IO.Path]::GetFullPath((Join-Path $root 'config.json'))) { throw 'Config path is outside the fixed protected root.' }
    $null = Assert-ProtectedPath $root $root
    $null = Assert-ProtectedPath $Path $root
    $config = Read-JsonFile $Path
    $expected = @{
        installRoot=$root
        statePath=(Join-Path $root 'state.json')
        manifestPath=(Join-Path $root 'entrypoints.json')
        bootstrapPath=(Join-Path $root 'Invoke-RebootResumeAdapter.ps1')
    }
    foreach ($name in $expected.Keys) {
        if ([IO.Path]::GetFullPath([string]$config.$name) -ne [IO.Path]::GetFullPath([string]$expected[$name])) { throw "Protected config path changed: $name" }
    }
    foreach ($critical in @([string]$config.manifestPath,[string]$config.bootstrapPath,(Split-Path -Parent ([string]$config.manifestPath)))) {
        $null = Assert-ProtectedPath $critical $root
    }
    if ($RequireState) { $null = Assert-ProtectedPath ([string]$config.statePath) $root }
    if ((Get-FileHash -LiteralPath ([string]$config.bootstrapPath) -Algorithm SHA256).Hash.ToLowerInvariant() -ne [string]$config.packageSha256) {
        throw 'Protected bootstrap hash changed.'
    }
    $config
}

switch ($Action) {
    'Install' {
        Assert-Windows
        foreach ($required in @($StatePath,$EntryPointManifestPath,$CodeCommit,$PackageSha256)) {
            if ([string]::IsNullOrWhiteSpace($required)) { throw 'Install requires state, manifest, commit, and package hash.' }
        }
        $protectedRoot = Get-ProtectedRoot
        $expectedConfig = Join-Path $protectedRoot 'config.json'
        $expectedState = Join-Path $protectedRoot 'state.json'
        if ([IO.Path]::GetFullPath($ConfigPath) -ne [IO.Path]::GetFullPath($expectedConfig) -or
            [IO.Path]::GetFullPath($StatePath) -ne [IO.Path]::GetFullPath($expectedState)) {
            throw 'ConfigPath and StatePath must use the fixed ProgramData protected root.'
        }
        $actualBootstrapHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualBootstrapHash -ne $PackageSha256.ToLowerInvariant()) { throw 'PackageSha256 must equal the current bootstrap script SHA-256.' }
        $manifest = Read-JsonFile $EntryPointManifestPath
        if (@($manifest.entryPoints).Count -lt 1) { throw 'Entrypoint manifest is empty.' }
        $root = $protectedRoot
        $bootstrap = Join-Path $root 'Invoke-RebootResumeAdapter.ps1'
        $installedManifest = Join-Path $root 'entrypoints.json'
        $entriesRoot = Join-Path $root 'entries'
        $installedEntries = @()
        $sourceRoot = Split-Path -Parent ([IO.Path]::GetFullPath($EntryPointManifestPath))
        foreach ($sourceEntry in @($manifest.entryPoints)) {
            $null = Get-ManifestEntry $manifest ([string]$sourceEntry.id)
            $sourcePath = [IO.Path]::GetFullPath((Join-Path $sourceRoot ([string]$sourceEntry.scriptPath)))
            $sourcePrefix = $sourceRoot.TrimEnd('\') + '\'
            if (-not $sourcePath.StartsWith($sourcePrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Source entry escapes manifest directory.' }
            $sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($sourceHash -ne ([string]$sourceEntry.sha256).ToLowerInvariant()) { throw 'Source entrypoint hash mismatch.' }
            $installedEntries += [ordered]@{id=[string]$sourceEntry.id;scriptPath=("entries\{0}.ps1" -f $sourceEntry.id);sha256=$sourceHash}
        }
        $config = [ordered]@{
            schemaVersion = 1; statePath = $StatePath; manifestPath = $installedManifest
            codeCommit = $CodeCommit; packageSha256 = $PackageSha256.ToLowerInvariant()
            remoteStateUri = $RemoteStateUri; networkWaitSeconds = $NetworkWaitSeconds; taskName = $TaskName
            installRoot=$root;bootstrapPath=$bootstrap
        }
        if ($PSCmdlet.ShouldProcess($TaskName, 'Install reboot resume bootstrap and AtStartup task')) {
            New-Item -ItemType Directory -Path $root -Force | Out-Null
            New-Item -ItemType Directory -Path $entriesRoot -Force | Out-Null
            Copy-Item -LiteralPath $PSCommandPath -Destination $bootstrap -Force
            for ($index=0; $index -lt $installedEntries.Count; $index++) {
                $sourceEntry = @($manifest.entryPoints)[$index]
                $sourcePath = [IO.Path]::GetFullPath((Join-Path $sourceRoot ([string]$sourceEntry.scriptPath)))
                Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $root ([string]$installedEntries[$index].scriptPath)) -Force
            }
            [ordered]@{entryPoints=$installedEntries} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $installedManifest -Encoding UTF8
            Write-AtomicJson $ConfigPath $config
            Set-ProtectedRootAcl $root
            Set-ProtectedRootAcl $entriesRoot
            foreach ($criticalFile in @($bootstrap,$installedManifest,$ConfigPath)+@($installedEntries | ForEach-Object { Join-Path $root ([string]$_.scriptPath) })) {
                Set-ProtectedFileAcl $criticalFile
            }
            foreach ($critical in @($root,$entriesRoot,$bootstrap,$installedManifest,$ConfigPath)+@($installedEntries | ForEach-Object { Join-Path $root ([string]$_.scriptPath) })) {
                $null = Assert-ProtectedPath $critical $root
            }
            if ((Get-FileHash -LiteralPath $bootstrap -Algorithm SHA256).Hash.ToLowerInvariant() -ne $actualBootstrapHash) { throw 'Installed bootstrap hash mismatch.' }
            $argument = "-NoProfile -File `"$bootstrap`" -Action Resume -ConfigPath `"$ConfigPath`""
            $taskAction = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument $argument
            $trigger = New-ScheduledTaskTrigger -AtStartup
            $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
            Register-ScheduledTask -TaskName $TaskName -Action $taskAction -Trigger $trigger -Principal $principal -Force | Out-Null
        }
        [pscustomobject]@{status='INSTALLED';taskName=$TaskName;configPath=$ConfigPath}
    }
    'Arm' {
        Assert-Windows
        $config = Read-ProtectedConfig $ConfigPath $false
        foreach ($required in @($RunId,$ResumeStep,$EntryPointId)) {
            if ([string]::IsNullOrWhiteSpace($required)) { throw 'Arm requires RunId, ResumeStep, and EntryPointId.' }
        }
        $null = Get-ManifestEntry (Read-JsonFile ([string]$config.manifestPath)) $EntryPointId
        $revision = 1
        if (Test-Path -LiteralPath ([string]$config.statePath)) {
            $old = Read-JsonFile ([string]$config.statePath)
            $revision = [int]$old.stateRevision + 1
        }
        $state = [ordered]@{
            schemaVersion=1;runId=$RunId;status='REBOOT_PENDING';resumeStep=$ResumeStep
            entryPointId=$EntryPointId;previousBootId=(Get-BootIdentity);attempt=0;maxAttempts=$MaxAttempts
            codeCommit=[string]$config.codeCommit;packageSha256=[string]$config.packageSha256
            stateRevision=$revision;updatedAt=[DateTime]::UtcNow.ToString('o');lastErrorCode=$null
        }
        Write-AtomicJson ([string]$config.statePath) $state
        Set-ProtectedFileAcl ([string]$config.statePath)
        $null = Assert-ProtectedPath ([string]$config.statePath) (Get-ProtectedRoot)
        $roundTrip = Read-JsonFile ([string]$config.statePath)
        Assert-State $roundTrip $config
        if (-not [string]::IsNullOrWhiteSpace([string]$config.remoteStateUri)) {
            try {
                Confirm-RemotePendingState $config $roundTrip
            } catch {
                $roundTrip.status='BLOCKED'; $roundTrip.lastErrorCode='REMOTE_CHECKPOINT_INVALID'
                $roundTrip.updatedAt=[DateTime]::UtcNow.ToString('o')
                Write-AtomicJson ([string]$config.statePath) $roundTrip
                throw 'Remote checkpoint verification failed; reboot is not armed.'
            }
        }
        [pscustomobject]$roundTrip
    }
    'Resume' {
        Assert-Windows
        $protectedRoot = Get-ProtectedRoot
        $config = Read-ProtectedConfig $ConfigPath $true
        $mutex = [Threading.Mutex]::new($false, 'Global\RebootResumeAdapter')
        if (-not $mutex.WaitOne(0)) { throw 'Another resume process owns the global mutex.' }
        try {
            $state = Read-JsonFile ([string]$config.statePath)
            Assert-State $state $config
            if ([string]$state.status -ne 'REBOOT_PENDING') { [pscustomobject]$state; break }
            try { Confirm-RemotePendingState $config $state }
            catch {
                $state.status='BLOCKED'; $state.lastErrorCode='REMOTE_CHECKPOINT_INVALID'
                $state.updatedAt=[DateTime]::UtcNow.ToString('o')
                Write-AtomicJson ([string]$config.statePath) $state
                throw
            }
            if ((Get-BootIdentity) -eq [string]$state.previousBootId) {
                $state.status='BLOCKED'; $state.lastErrorCode='BOOT_ID_UNCHANGED'
                $state.updatedAt=[DateTime]::UtcNow.ToString('o')
                Write-AtomicJson ([string]$config.statePath) $state
                throw 'Boot identity did not change; refusing replay.'
            }
            if ([int]$state.attempt -ge [int]$state.maxAttempts) {
                $state.status='BLOCKED'; $state.lastErrorCode='MAX_ATTEMPTS'
                $state.updatedAt=[DateTime]::UtcNow.ToString('o')
                Write-AtomicJson ([string]$config.statePath) $state
                throw 'Maximum resume attempts reached.'
            }
            $entry = Get-ManifestEntry (Read-JsonFile ([string]$config.manifestPath)) ([string]$state.entryPointId)
            $manifestRoot = Split-Path -Parent ([string]$config.manifestPath)
            $manifestRootWithSeparator = [IO.Path]::GetFullPath($manifestRoot).TrimEnd('\') + '\'
            $entryPath = [IO.Path]::GetFullPath((Join-Path $manifestRoot ([string]$entry.scriptPath)))
            if (-not $entryPath.StartsWith($manifestRootWithSeparator, [StringComparison]::OrdinalIgnoreCase)) { throw 'Entrypoint escapes manifest root.' }
            $null = Assert-ProtectedPath $entryPath $protectedRoot
            $actualHash = (Get-FileHash -LiteralPath $entryPath -Algorithm SHA256).Hash
            if ($actualHash -ne [string]$entry.sha256) { throw 'Entrypoint hash mismatch.' }
            $state.status='RESUMING'; $state.attempt=[int]$state.attempt+1; $state.lastErrorCode=$null
            $state.updatedAt=[DateTime]::UtcNow.ToString('o')
            Write-AtomicJson ([string]$config.statePath) $state
            $global:LASTEXITCODE = 0
            & $entryPath -ResumeStatePath ([string]$config.statePath)
            if (-not $? -or $LASTEXITCODE -ne 0) { throw "Entrypoint failed with exit code $LASTEXITCODE." }
            [pscustomobject]$state
        } catch {
            if (Test-Path -LiteralPath ([string]$config.statePath)) {
                $failed = Read-JsonFile ([string]$config.statePath)
                Assert-State $failed $config
                $failed.status='BLOCKED'
                if (-not $failed.lastErrorCode) { $failed.lastErrorCode='RESUME_FAILED' }
                $failed.updatedAt=[DateTime]::UtcNow.ToString('o')
                Write-AtomicJson ([string]$config.statePath) $failed
            }
            throw
        } finally {
            if ($mutex) { $mutex.ReleaseMutex(); $mutex.Dispose() }
        }
    }
    'Complete' {
        $config = Read-ProtectedConfig $ConfigPath $true
        $state = Read-JsonFile ([string]$config.statePath)
        Assert-State $state $config
        $state.status='COMPLETED'; $state.lastErrorCode=$null; $state.updatedAt=[DateTime]::UtcNow.ToString('o')
        Write-AtomicJson ([string]$config.statePath) $state
        if ($env:OS -eq 'Windows_NT' -and $PSCmdlet.ShouldProcess([string]$config.taskName, 'Unregister completed reboot resume task')) {
            Unregister-ScheduledTask -TaskName ([string]$config.taskName) -Confirm:$false -ErrorAction SilentlyContinue
        }
        [pscustomobject]$state
    }
    'Disarm' {
        Assert-Windows
        $config = Read-ProtectedConfig $ConfigPath $false
        if ($PSCmdlet.ShouldProcess([string]$config.taskName, 'Unregister reboot resume task')) {
            Unregister-ScheduledTask -TaskName ([string]$config.taskName) -Confirm:$false -ErrorAction SilentlyContinue
        }
        [pscustomobject]@{status='DISARMED';taskName=[string]$config.taskName}
    }
    'Status' {
        $config = Read-ProtectedConfig $ConfigPath $true
        $state = Read-JsonFile ([string]$config.statePath)
        Assert-State $state $config
        [pscustomobject]$state
    }
}
