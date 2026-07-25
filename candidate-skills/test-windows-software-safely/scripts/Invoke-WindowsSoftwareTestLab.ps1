[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory)]
    [ValidateSet('Prepare','ExecutePayload','RestartGuest','CollectEvidence','Restore','Status')]
    [string]$Action,
    [Parameter(Mandatory)]
    [string]$PlanPath,
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-fA-F0-9]{64}$')]
    [string]$ApprovePlanHash,
    [switch]$Execute,
    [Management.Automation.PSCredential]$GuestCredential,
    [ValidateRange(30, 1800)]
    [int]$GuestRestartTimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Lab execution requires native Windows with Hyper-V.' }

function Get-PlanHash([object]$Plan) {
    $copy = [ordered]@{}
    foreach ($property in $Plan.PSObject.Properties) {
        if ($property.Name -ne 'planHash') { $copy[$property.Name]=$property.Value }
    }
    $canonical = $copy | ConvertTo-Json -Depth 6 -Compress
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        ([BitConverter]::ToString($sha.ComputeHash([Text.UTF8Encoding]::new($false).GetBytes($canonical)))).Replace('-','').ToLowerInvariant()
    } finally { $sha.Dispose() }
}

function Write-LabEvent([System.Collections.IDictionary]$Event, [string]$RunRoot) {
    New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
    $path = Join-Path $RunRoot ("event-{0}-{1}.json" -f [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'),[guid]::NewGuid().ToString('N'))
    $Event | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $path -Encoding UTF8
    [ordered]@{path=$path;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
}

function Restore-And-Verify([object]$Plan, [object]$Vm, [Management.Automation.PSCredential]$Credential, [int]$TimeoutSeconds) {
    if ($null -eq $Credential) { throw 'GuestCredential is required to verify restoration.' }
    $snapshot = Get-VMSnapshot -VMName $Vm.Name -Name ([string]$Plan.baselineCheckpointName) -ErrorAction Stop
    Restore-VMSnapshot -VMSnapshot $snapshot -Confirm:$false
    $current = Get-VM -Name $Vm.Name
    if ([string]$current.State -ne 'Running') { Start-VM -Name $Vm.Name | Out-Null }
    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    $markerExists = $null
    do {
        try {
            $markerExists = [bool](Invoke-Command -VMName $Vm.Name -Credential $Credential -ScriptBlock {
                param($MarkerPath)
                Test-Path -LiteralPath $MarkerPath
            } -ArgumentList ([string]$Plan.testMarkerPath) -ErrorAction Stop)
        } catch { $markerExists = $null }
        if ($null -ne $markerExists) { break }
        Start-Sleep -Seconds 5
    } while ([DateTime]::UtcNow -lt $deadline)
    if ($null -eq $markerExists) { throw 'Restored guest did not become reachable for verification.' }
    if ($markerExists) { throw 'Baseline restore verification failed: test marker still exists.' }
    [ordered]@{checkpointId=[string]$snapshot.Id;markerAbsent=$true}
}

function Assert-NetworkIsolation([object]$Plan, [object]$Vm) {
    $adapters = @(Get-VMNetworkAdapter -VMName $Vm.Name -ErrorAction Stop)
    $actualIds = @($adapters | ForEach-Object {[string]$_.Id} | Sort-Object)
    $expectedIds = @($Plan.initialAdapterIds | ForEach-Object {[string]$_} | Sort-Object)
    if (($actualIds -join '|') -ne ($expectedIds -join '|')) { throw 'VM network adapter set drifted.' }
    if ([string]$Plan.networkMode -eq 'None') {
        foreach ($adapter in $adapters) {
            if (-not [string]::IsNullOrWhiteSpace([string]$adapter.SwitchName)) { throw 'None mode requires every adapter disconnected.' }
        }
        return
    }
    if ([string]$Plan.networkMode -ne 'Private') { throw 'Unsupported network isolation mode.' }
    $switch = Get-VMSwitch -Name ([string]$Plan.privateSwitchName) -ErrorAction Stop
    if ([string]$switch.SwitchType -ne 'Private' -or [string]$switch.Id -ne [string]$Plan.privateSwitchId) {
        throw 'Private switch identity or type drifted.'
    }
    foreach ($adapter in $adapters) {
        if ([string]$adapter.SwitchName -ne [string]$switch.Name) { throw 'Adapter is not connected only to the pinned Private switch.' }
    }
}

$plan = Get-Content -LiteralPath $PlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([int]$plan.schemaVersion -ne 1 -or [string]$plan.kind -ne 'windows-software-test-plan') { throw 'Unsupported lab plan.' }
if (-not [bool]$plan.disposableConfirmed) { throw 'Plan does not identify a disposable VM.' }
if ([string]$plan.host -ne $env:COMPUTERNAME) { throw 'Plan belongs to another host.' }
$actualHash = Get-PlanHash $plan
if ($actualHash -ne ([string]$plan.planHash).ToLowerInvariant() -or $actualHash -ne $ApprovePlanHash.ToLowerInvariant()) { throw 'Plan hash mismatch.' }
$vm = Get-VM -Name ([string]$plan.vmName) -ErrorAction Stop
if ([string]$vm.Id -ne [string]$plan.vmId) { throw 'VM identity changed.' }

$payloadHash = $null

$runRoot = Join-Path ([string]$plan.evidenceRoot) ([string]$plan.runId)
$runStatePath = Join-Path $runRoot 'run-state.json'
$event = [ordered]@{
    schemaVersion=1;runId=[string]$plan.runId;host=$env:COMPUTERNAME;vmName=$vm.Name;vmId=[string]$vm.Id
    action=$Action;mode=$(if ($Execute) {'Execute'} else {'Preview'});timestamp=[DateTime]::UtcNow.ToString('o')
    vmState=[string]$vm.State;guestPayloadSha256=[string]$plan.guestPayloadSha256;status='PREVIEW'
}

if (-not $Execute) { [pscustomobject]$event; return }

try {
    if ($Action -ne 'Restore' -and [DateTime]::Parse([string]$plan.expiresAt).ToUniversalTime() -lt [DateTime]::UtcNow) { throw 'Plan expired.' }
    if ($Action -notin @('Restore','Status','CollectEvidence')) {
        if (-not (Test-Path -LiteralPath ([string]$plan.guestPayloadPath) -PathType Leaf)) { throw 'Guest payload is missing.' }
        $payloadHash = (Get-FileHash -LiteralPath ([string]$plan.guestPayloadPath) -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($payloadHash -ne [string]$plan.guestPayloadSha256) { throw 'Guest payload hash changed.' }
    }
    switch ($Action) {
        'Prepare' {
            if ($PSCmdlet.ShouldProcess($vm.Name, 'Isolate VM and create baseline checkpoint')) {
                foreach ($adapter in @(Get-VMNetworkAdapter -VMName $vm.Name)) {
                    if ([string]$plan.networkMode -eq 'None') {
                        Disconnect-VMNetworkAdapter -VMNetworkAdapter $adapter
                    } else {
                        $switch = Get-VMSwitch -Name ([string]$plan.privateSwitchName) -ErrorAction Stop
                        if ([string]$switch.SwitchType -ne 'Private') { throw 'Private switch identity changed.' }
                        Connect-VMNetworkAdapter -VMNetworkAdapter $adapter -SwitchName $switch.Name
                    }
                }
                Assert-NetworkIsolation $plan $vm
                if (Get-VMSnapshot -VMName $vm.Name -Name ([string]$plan.baselineCheckpointName) -ErrorAction SilentlyContinue) {
                    throw 'Baseline checkpoint already exists.'
                }
                $snapshot = Checkpoint-VM -VMName $vm.Name -SnapshotName ([string]$plan.baselineCheckpointName) -Passthru
                New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
                [ordered]@{schemaVersion=1;runId=[string]$plan.runId;guestRebootCount=0;status='PREPARED';checkpointId=[string]$snapshot.Id} |
                    ConvertTo-Json | Set-Content -LiteralPath $runStatePath -Encoding UTF8
                $event.checkpointId=[string]$snapshot.Id; $event.status='PREPARED'
            }
        }
        'ExecutePayload' {
            if ($null -eq $GuestCredential) { throw 'GuestCredential is required to execute the payload.' }
            if (-not (Test-Path -LiteralPath $runStatePath -PathType Leaf)) { throw 'Run was not prepared.' }
            Assert-NetworkIsolation $plan $vm
            if ($PSCmdlet.ShouldProcess($vm.Name, 'Copy and execute the pinned guest payload')) {
                Copy-VMFile -VMName $vm.Name -SourcePath ([string]$plan.guestPayloadPath) `
                    -DestinationPath ([string]$plan.guestPayloadDestination) -FileSource Host -CreateFullPath -Force
                $guestResult = Invoke-Command -VMName $vm.Name -Credential $GuestCredential -ScriptBlock {
                    param($PayloadPath,$ExpectedHash,$RunId,$MarkerPath)
                    $ErrorActionPreference='Stop'
                    $actual=(Get-FileHash -LiteralPath $PayloadPath -Algorithm SHA256).Hash.ToLowerInvariant()
                    if ($actual -ne $ExpectedHash) { throw 'Guest payload hash mismatch.' }
                    $global:LASTEXITCODE=0
                    try {
                        & $PayloadPath -RunId $RunId
                        $exitCode=$(if ($LASTEXITCODE) {[int]$LASTEXITCODE} elseif ($?) {0} else {1})
                    } catch {
                        return [pscustomobject]@{exitCode=1;sha256=$actual;markerCreated=$false;errorCode='PAYLOAD_EXCEPTION'}
                    }
                    if ($exitCode -ne 0) { return [pscustomobject]@{exitCode=$exitCode;sha256=$actual;markerCreated=$false;errorCode='PAYLOAD_NONZERO_EXIT'} }
                    New-Item -ItemType File -Path $MarkerPath -Force | Out-Null
                    [pscustomobject]@{exitCode=0;sha256=$actual;markerCreated=(Test-Path -LiteralPath $MarkerPath)}
                } -ArgumentList ([string]$plan.guestPayloadDestination),([string]$plan.guestPayloadSha256),([string]$plan.runId),([string]$plan.testMarkerPath)
                $event.guestExitCode=[int]$guestResult.exitCode; $event.guestVerifiedSha256=[string]$guestResult.sha256
                $event.testMarkerCreated=[bool]$guestResult.markerCreated
                if ([int]$guestResult.exitCode -ne 0 -or -not [bool]$guestResult.markerCreated) { throw 'Guest payload execution failed.' }
                $event.status='PAYLOAD_EXECUTED'
            }
        }
        'RestartGuest' {
            if ($null -eq $GuestCredential) { throw 'GuestCredential is required at runtime for boot-id verification.' }
            if (-not (Test-Path -LiteralPath $runStatePath -PathType Leaf)) { throw 'Run was not prepared.' }
            Assert-NetworkIsolation $plan $vm
            $runState = Get-Content -LiteralPath $runStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
            if ([int]$runState.guestRebootCount -ge [int]$plan.maxGuestReboots) { throw 'Maximum guest reboot count reached.' }
            if ($PSCmdlet.ShouldProcess($vm.Name, 'Restart disposable guest VM')) {
                $bootScript = { (Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o') }
                $before = [string](Invoke-Command -VMName $vm.Name -Credential $GuestCredential -ScriptBlock $bootScript)
                Restart-VM -Name $vm.Name -Confirm:$false
                $deadline = [DateTime]::UtcNow.AddSeconds($GuestRestartTimeoutSeconds)
                $after = $null
                do {
                    Start-Sleep -Seconds 5
                    $current = Get-VM -Name $vm.Name
                    if ([string]$current.State -eq 'Running') {
                        try { $after = [string](Invoke-Command -VMName $vm.Name -Credential $GuestCredential -ScriptBlock $bootScript -ErrorAction Stop) }
                        catch { $after = $null }
                    }
                    if ($after -and $after -ne $before) { break }
                } while ([DateTime]::UtcNow -lt $deadline)
                if (-not $after -or $after -eq $before) { throw 'Guest restart or boot-id verification timed out.' }
                $runState.guestRebootCount=[int]$runState.guestRebootCount+1; $runState.status='GUEST_REBOOT_VERIFIED'
                $runState | ConvertTo-Json | Set-Content -LiteralPath $runStatePath -Encoding UTF8
                $event.previousGuestBootId=$before; $event.currentGuestBootId=$after
                $event.guestRebootCount=[int]$runState.guestRebootCount; $event.status='GUEST_REBOOT_VERIFIED'
            }
        }
        'CollectEvidence' { $event.status='EVIDENCE_COLLECTED' }
        'Restore' {
            if ($PSCmdlet.ShouldProcess($vm.Name, 'Restore and verify this run baseline checkpoint')) {
                $restored = Restore-And-Verify $plan $vm $GuestCredential $GuestRestartTimeoutSeconds
                $event.checkpointId=[string]$restored.checkpointId; $event.testMarkerAbsent=[bool]$restored.markerAbsent
                $event.status='RESTORE_VERIFIED'
            }
        }
        'Status' { $event.status='STATUS' }
    }
    $evidence = Write-LabEvent $event $runRoot
    $event.evidencePath=$evidence.path; $event.evidenceSha256=$evidence.sha256
    [pscustomobject]$event
} catch {
    $event.status='BLOCKED'; $event.errorCode=("$Action`_FAILED").ToUpperInvariant()
    $event.errorMessage=$_.Exception.Message; $event.restoreAttempted=$false
    if ($Action -notin @('Restore','Status')) {
        $event.restoreAttempted=$true
        try {
            $restored = Restore-And-Verify $plan $vm $GuestCredential $GuestRestartTimeoutSeconds
            $event.recoveryStatus='BASELINE_RESTORE_VERIFIED'; $event.recoveryCheckpointId=[string]$restored.checkpointId
        } catch {
            $event.recoveryStatus='BASELINE_RESTORE_FAILED'; $event.recoveryError=$_.Exception.Message
        }
    }
    try {
        $evidence = Write-LabEvent $event $runRoot
        $event.evidencePath=$evidence.path; $event.evidenceSha256=$evidence.sha256
    } catch {}
    throw
}
