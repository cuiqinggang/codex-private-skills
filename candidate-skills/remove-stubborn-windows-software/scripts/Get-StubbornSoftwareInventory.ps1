[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string[]]$DisplayName,
    [string[]]$Publisher = @(),
    [string]$BaselineInventoryPath,
    [string]$ComponentIdentityManifestPath,
    [Parameter(Mandatory)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Inventory requires native Windows.' }
if ($DisplayName.Count -lt 1 -or @($DisplayName | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count) {
    throw 'DisplayName values must be non-empty exact names.'
}

function Is-Exact([string]$Value, [string[]]$Allowed) {
    foreach ($candidate in $Allowed) {
        if ([string]::Equals($Value, $candidate, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

function Split-UninstallString([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    if ($Value -match '^\s*"([^"]+)"\s*(.*)$') {
        return [ordered]@{executable=$Matches[1];arguments=$Matches[2]}
    }
    if ($Value -match '^\s*([^\s]+)\s*(.*)$') {
        return [ordered]@{executable=$Matches[1];arguments=$Matches[2]}
    }
    return $null
}

$registryRoots = @(
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$products = @()
foreach ($root in $registryRoots) {
    foreach ($item in @(Get-ItemProperty -Path $root -ErrorAction SilentlyContinue)) {
        if (-not (Is-Exact ([string]$item.DisplayName) $DisplayName)) { continue }
        if ($Publisher.Count -and -not (Is-Exact ([string]$item.Publisher) $Publisher)) { continue }
        $parsed = Split-UninstallString ([string]($(if ($item.QuietUninstallString) {$item.QuietUninstallString} else {$item.UninstallString})))
        $signatureStatus = $null; $signer = $null; $signerThumbprint = $null; $sha256 = $null
        if ($parsed -and (Test-Path -LiteralPath ([string]$parsed.executable) -PathType Leaf)) {
            $sig = Get-AuthenticodeSignature -LiteralPath ([string]$parsed.executable)
            $signatureStatus = [string]$sig.Status
            $signer = [string]$sig.SignerCertificate.Subject
            $signerThumbprint = [string]$sig.SignerCertificate.Thumbprint
            $sha256 = (Get-FileHash -LiteralPath ([string]$parsed.executable) -Algorithm SHA256).Hash.ToLowerInvariant()
        }
        $products += [ordered]@{
            displayName=[string]$item.DisplayName;publisher=[string]$item.Publisher
            version=[string]$item.DisplayVersion;registryKey=[string]$item.PSPath
            windowsInstaller=([int]$item.WindowsInstaller -eq 1);productCode=[string]$item.PSChildName
            uninstall=$parsed;signatureStatus=$signatureStatus;signer=$signer;signerThumbprint=$signerThumbprint;sha256=$sha256
            installLocation=[string]$item.InstallLocation
        }
    }
}

$baseline = $null
$baselineSha256 = $null
$declared = $null
$declaredSha256 = $null
if ($ComponentIdentityManifestPath) {
    $declared = Get-Content -LiteralPath $ComponentIdentityManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $declaredFields = @($declared.PSObject.Properties.Name | Sort-Object)
    $expectedFields = @('schemaVersion','installRoots','processPaths','serviceNames','taskIds','startupIds') | Sort-Object
    if (($declaredFields -join '|') -ne ($expectedFields -join '|') -or [int]$declared.schemaVersion -ne 1) {
        throw 'Unsupported component identity manifest.'
    }
    foreach ($identity in @($declared.installRoots)+@($declared.processPaths)+@($declared.serviceNames)+@($declared.taskIds)+@($declared.startupIds)) {
        if ([string]::IsNullOrWhiteSpace([string]$identity) -or [string]$identity -match '[*?\x00-\x1f]') {
            throw 'Component identities must be exact and cannot contain wildcards or control characters.'
        }
    }
    $declaredSha256 = (Get-FileHash -LiteralPath $ComponentIdentityManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
if ($BaselineInventoryPath) {
    $baseline = Get-Content -LiteralPath $BaselineInventoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([int]$baseline.schemaVersion -ne 1 -or [string]$baseline.kind -ne 'stubborn-software-inventory') {
        throw 'Unsupported baseline inventory.'
    }
    if ([string]$baseline.computer -ne $env:COMPUTERNAME) { throw 'Baseline belongs to another computer.' }
    $baselineSha256 = (Get-FileHash -LiteralPath $BaselineInventoryPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

$rootCandidates = @($products.installLocation | Where-Object { $_ })
if ($declared) { $rootCandidates += @($declared.installRoots) }
if ($baseline) {
    $rootCandidates += @($baseline.installRoots | ForEach-Object { [string]$_.path } | Where-Object { $_ })
    $rootCandidates += @($baseline.products.installLocation | Where-Object { $_ })
}
$installRoots = @($rootCandidates | ForEach-Object { [IO.Path]::GetFullPath($_).TrimEnd('\') } | Sort-Object -Unique)
$baselineProcessPaths = @()
$baselineServiceNames = @()
$baselineTaskIds = @()
$baselineStartupIds = @()
if ($baseline) {
    $baselineProcessPaths = @($baseline.processes | ForEach-Object { [string]$_.path })
    $baselineServiceNames = @($baseline.servicesAndDrivers | ForEach-Object { [string]$_.name })
    $baselineTaskIds = @($baseline.scheduledTasks | ForEach-Object { "$($_.taskPath)|$($_.taskName)" })
    $baselineStartupIds = @($baseline.startupEntries | ForEach-Object { "$($_.location)|$($_.name)" })
    $baselineProcessPaths += @($baseline.declaredComponentIdentities.processPaths)
    $baselineServiceNames += @($baseline.declaredComponentIdentities.serviceNames)
    $baselineTaskIds += @($baseline.declaredComponentIdentities.taskIds)
    $baselineStartupIds += @($baseline.declaredComponentIdentities.startupIds)
}
if ($declared) {
    $baselineProcessPaths += @($declared.processPaths)
    $baselineServiceNames += @($declared.serviceNames)
    $baselineTaskIds += @($declared.taskIds)
    $baselineStartupIds += @($declared.startupIds)
}

function Is-UnderRoot([string]$Path, [string[]]$Roots) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    foreach ($root in $Roots) {
        if ($Path.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

$processes = @()
foreach ($process in @(Get-Process -ErrorAction SilentlyContinue)) {
    try {
        $path = [string]$process.Path
        if ((Is-UnderRoot $path $installRoots) -or (Is-Exact $path $baselineProcessPaths)) {
            $processes += [ordered]@{evidenceId=("process:" + $path.ToLowerInvariant());name=$process.Name;id=$process.Id;path=$path}
        }
    } catch {}
}

$services = @()
foreach ($className in @('Win32_SystemDriver','Win32_Service')) {
    foreach ($service in @(Get-CimInstance -ClassName $className -ErrorAction SilentlyContinue)) {
        $path = ([string]$service.PathName).Trim('"')
        if ((Is-UnderRoot $path $installRoots) -or (Is-Exact ([string]$service.Name) $baselineServiceNames)) {
            $services += [ordered]@{evidenceId=("service:" + ([string]$service.Name).ToLowerInvariant());name=[string]$service.Name;state=[string]$service.State;path=[string]$service.PathName}
        }
    }
}

$scheduledTasks = @()
foreach ($task in @(Get-ScheduledTask -ErrorAction SilentlyContinue)) {
    foreach ($action in @($task.Actions)) {
        $execute = [string]$action.Execute
        $taskId = "$($task.TaskPath)|$($task.TaskName)"
        if ((Is-UnderRoot $execute.Trim('"') $installRoots) -or (Is-Exact $taskId $baselineTaskIds)) {
            $scheduledTasks += [ordered]@{evidenceId=("task:" + $taskId.ToLowerInvariant());taskPath=[string]$task.TaskPath;taskName=[string]$task.TaskName;execute=$execute;state=[string]$task.State}
        }
    }
}

$startupEntries = @()
foreach ($entry in @(Get-CimInstance -ClassName Win32_StartupCommand -ErrorAction SilentlyContinue)) {
    $command = [string]$entry.Command
    $startupId = "$($entry.Location)|$($entry.Name)"
    if ((Is-UnderRoot $command.TrimStart('"') $installRoots) -or (Is-Exact $startupId $baselineStartupIds)) {
        $startupEntries += [ordered]@{evidenceId=("startup:" + $startupId.ToLowerInvariant());name=[string]$entry.Name;command=$command;location=[string]$entry.Location}
    }
}

$installRootEvidence = @($installRoots | ForEach-Object {
    [ordered]@{evidenceId=("root:" + $_.ToLowerInvariant());path=$_;exists=(Test-Path -LiteralPath $_)}
})
$result = [ordered]@{
    schemaVersion=1;kind='stubborn-software-inventory';computer=$env:COMPUTERNAME
    userSid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    capturedAt=[DateTime]::UtcNow.ToString('o');requestedDisplayNames=$DisplayName
    requestedPublishers=$Publisher;products=$products;processes=$processes;servicesAndDrivers=$services
    scheduledTasks=$scheduledTasks;startupEntries=$startupEntries;installRoots=$installRootEvidence
    baselineInventoryPath=$BaselineInventoryPath;baselineInventorySha256=$baselineSha256
    componentIdentityManifestSha256=$declaredSha256;declaredComponentIdentities=$declared
    classification=$(if ($products.Count -or $processes.Count -or $services.Count -or $scheduledTasks.Count -or $startupEntries.Count) {'ACTIVE_PRODUCT'} elseif (@($installRootEvidence | Where-Object {$_.exists}).Count) {'UNKNOWN_BLOCKER'} else {'ABSENT'})
}
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
[pscustomobject]$result
