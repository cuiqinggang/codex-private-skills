[CmdletBinding()]
param(
    [ValidateSet('Initialize','Continue','Status')]
    [string]$Action = 'Continue',
    [string]$LoopRoot,
    [string]$ResumeStatePath
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Run this fixture only in a disposable Windows VM.' }
if ([string]::IsNullOrWhiteSpace($LoopRoot)) {
    $LoopRoot = Join-Path $env:ProgramData 'RebootResumeAdapterFixture\loop'
}

$contractPath = Join-Path $LoopRoot 'LOOP-CONTRACT.json'
$statePath = Join-Path $LoopRoot 'STATE.json'
$logPath = Join-Path $LoopRoot 'RUN-LOG.jsonl'

function Get-BootIdentity {
    (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')
}

function Write-AtomicJson([string]$Path, [object]$Value) {
    $directory = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    $temporary = Join-Path $directory ('.{0}.{1}.tmp' -f ([IO.Path]::GetFileName($Path)), [guid]::NewGuid().ToString('N'))
    $json = $Value | ConvertTo-Json -Depth 12
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($json)
    $stream = [IO.File]::Open($temporary, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try {
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush($true)
    } finally {
        $stream.Dispose()
    }
    if (Test-Path -LiteralPath $Path) {
        [IO.File]::Replace($temporary, $Path, $null, $true)
    } else {
        [IO.File]::Move($temporary, $Path)
    }
}

function Read-Json([string]$Path) {
    Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Add-RunLog([object]$Event) {
    $line = ($Event | ConvertTo-Json -Compress -Depth 8) + [Environment]::NewLine
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($line)
    $stream = [IO.File]::Open($logPath, [IO.FileMode]::Append, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    try {
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush($true)
    } finally {
        $stream.Dispose()
    }
}

function Assert-State([object]$State) {
    $expected = @(
        'schemaVersion','loopId','status','phase','rebootCount','maxReboots',
        'previousBootId','bootIds','nextAction','updatedAt','lastErrorCode'
    ) | Sort-Object
    $actual = @($State.PSObject.Properties.Name | Sort-Object)
    if (($actual -join '|') -ne ($expected -join '|')) { throw 'Fixture state schema mismatch.' }
    if ([string]$State.loopId -ne 'two-reboot-loop-fixture') { throw 'Fixture loop identity mismatch.' }
    if ([int]$State.maxReboots -ne 2) { throw 'Fixture reboot budget changed.' }
    if ([int]$State.rebootCount -lt 0 -or [int]$State.rebootCount -gt 2) { throw 'Fixture reboot count is invalid.' }
    if ([string]$State.status -notin @('WAITING','CLOSED','BLOCKED')) { throw 'Fixture status is invalid.' }
}

if ($Action -eq 'Initialize') {
    if (Test-Path -LiteralPath $statePath) {
        $existing = Read-Json $statePath
        Assert-State $existing
        [pscustomobject]$existing
        return
    }
    New-Item -ItemType Directory -Path $LoopRoot -Force | Out-Null
    $contract = [ordered]@{
        loop_id = 'two-reboot-loop-fixture'
        mode = 'goal'
        goal = 'Prove exact continuation across two externally controlled guest reboots.'
        success_criteria = @('three distinct boot ids','exactly two reboot requests','final CLOSED state')
        boundaries = [ordered]@{
            allowed = @('write fixture state and append fixture log')
            forbidden = @('restart host','restart guest','run arbitrary commands','use network')
        }
        budget = [ordered]@{max_runs=3;max_repair_rounds=0;max_runtime_minutes=30}
        stop_conditions = @('same boot id','state schema mismatch','more than two reboot requests')
    }
    Write-AtomicJson $contractPath $contract
    $boot = Get-BootIdentity
    $state = [ordered]@{
        schemaVersion = 1
        loopId = 'two-reboot-loop-fixture'
        status = 'WAITING'
        phase = 0
        rebootCount = 0
        maxReboots = 2
        previousBootId = $boot
        bootIds = @($boot)
        nextAction = 'REBOOT_REQUIRED'
        updatedAt = [DateTime]::UtcNow.ToString('o')
        lastErrorCode = $null
    }
    Write-AtomicJson $statePath $state
    Add-RunLog ([ordered]@{
        run=0;utc=$state.updatedAt;bootId=$boot;decision='REBOOT_REQUIRED'
        outputCursor=0;nextAction='REBOOT_REQUIRED'
    })
    Write-Output 'FIXTURE_REBOOT_REQUIRED_1'
    return
}

if (-not (Test-Path -LiteralPath $statePath)) { throw 'Initialize the two-reboot Loop fixture first.' }
$state = Read-Json $statePath
Assert-State $state

if ($Action -eq 'Status') {
    [pscustomobject]$state
    return
}

if ([string]$state.status -eq 'CLOSED') {
    Write-Output 'TWO_REBOOT_LOOP_FIXTURE_ALREADY_PASS'
    return
}
if ([string]$state.status -eq 'BLOCKED') { throw "Fixture is blocked: $($state.lastErrorCode)" }

$boot = Get-BootIdentity
if ($boot -eq [string]$state.previousBootId) {
    $state.status = 'BLOCKED'
    $state.nextAction = 'NONE'
    $state.lastErrorCode = 'BOOT_ID_UNCHANGED'
    $state.updatedAt = [DateTime]::UtcNow.ToString('o')
    Write-AtomicJson $statePath $state
    Add-RunLog ([ordered]@{
        run=([int]$state.rebootCount + 1);utc=$state.updatedAt;bootId=$boot
        decision='BLOCKED';outputCursor=$state.rebootCount;nextAction='NONE'
        errorCode='BOOT_ID_UNCHANGED'
    })
    throw 'Guest boot identity did not change; refusing same-boot replay.'
}

$state.rebootCount = [int]$state.rebootCount + 1
$state.phase = [int]$state.phase + 1
$state.previousBootId = $boot
$state.bootIds = @($state.bootIds) + $boot
$state.updatedAt = [DateTime]::UtcNow.ToString('o')
$state.lastErrorCode = $null

if ([int]$state.rebootCount -lt [int]$state.maxReboots) {
    $state.status = 'WAITING'
    $state.nextAction = 'REBOOT_REQUIRED'
    Write-AtomicJson $statePath $state
    Add-RunLog ([ordered]@{
        run=$state.rebootCount;utc=$state.updatedAt;bootId=$boot;decision='REBOOT_REQUIRED'
        outputCursor=$state.rebootCount;nextAction='REBOOT_REQUIRED'
    })
    Write-Output 'FIXTURE_REBOOT_REQUIRED_2'
    return
}

$state.status = 'CLOSED'
$state.nextAction = 'NONE'
Write-AtomicJson $statePath $state
Add-RunLog ([ordered]@{
    run=$state.rebootCount;utc=$state.updatedAt;bootId=$boot;decision='PASS'
    outputCursor=$state.rebootCount;nextAction='NONE'
})
Write-Output 'TWO_REBOOT_LOOP_FIXTURE_PASS'
