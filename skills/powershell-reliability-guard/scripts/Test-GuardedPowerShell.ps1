[CmdletBinding()]
param()

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('powershell-guard-test-' + [guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $testRoot)
try {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $runner = Join-Path $PSScriptRoot 'Invoke-GuardedPowerShell.ps1'
    $incidentLog = Join-Path $testRoot 'incidents.jsonl'
    $learnedCatalog = Join-Path $testRoot 'learned-errors.jsonl'
    $invalidScript = Join-Path $testRoot 'invalid.ps1'
    $marker = Join-Path $testRoot 'marker.txt'
    $hostExecutable = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
    $hostArguments = @('-NoLogo', '-NoProfile', '-NonInteractive')
    if ($PSVersionTable.PSVersion.Major -le 5) {
        $hostArguments += @('-ExecutionPolicy', 'Bypass')
    }

    function Invoke-RunnerChild([string]$TargetScript, [string[]]$AdditionalArguments = @()) {
        $childOutput = & $hostExecutable @hostArguments -File $runner -Path $TargetScript `
            -Target Current -Analyzer Skip -IncidentLogPath $incidentLog `
            -LearnedCatalogPath $learnedCatalog @AdditionalArguments 2>&1
        return [pscustomobject]@{
            ExitCode = $LASTEXITCODE
            Output = ($childOutput -join [Environment]::NewLine)
        }
    }

    [System.IO.File]::WriteAllText($invalidScript, "if (`$true) {`r`n[IO.File]::WriteAllText('$marker','BAD')", $encoding)

    $invalidRun = Invoke-RunnerChild -TargetScript $invalidScript
    if ($invalidRun.ExitCode -eq 0) { throw 'Invalid syntax was not blocked.' }
    if (Test-Path -LiteralPath $marker) { throw 'Blocked script still produced a side effect.' }
    $invalidResult = $invalidRun.Output | ConvertFrom-Json
    if ($invalidResult.Status -ne 'BLOCKED') { throw 'Blocked result was not reported.' }
    if ($invalidResult.Phase -ne 'PREFLIGHT') { throw 'Syntax failure used the wrong incident phase.' }

    $executionScript = Join-Path $testRoot 'execution.ps1'
    [System.IO.File]::WriteAllText($executionScript, "[Console]::Error.WriteLine('EXPECTED_FAILURE')`r`nexit 7", $encoding)
    $failureRun = Invoke-RunnerChild -TargetScript $executionScript
    if ($failureRun.ExitCode -eq 0) { throw 'Non-zero target exit was not blocked.' }
    $failureResult = $failureRun.Output | ConvertFrom-Json
    if ($failureResult.Phase -ne 'EXECUTION') { throw 'Execution failure used the wrong incident phase.' }

    [System.IO.File]::WriteAllText($executionScript, "[IO.File]::WriteAllText('$marker','PASS')`r`nexit 0", $encoding)
    $resolutionArguments = @(
        '-ResolveIncidentId', $failureResult.IncidentId,
        '-RootCause', 'Self-test intentional exit 7',
        '-Fix', 'Replace failing fixture with passing fixture',
        '-Prevention', 'Require zero exit code before acceptance'
    )
    $successRun = Invoke-RunnerChild -TargetScript $executionScript -AdditionalArguments $resolutionArguments
    if ($successRun.ExitCode -ne 0) { throw ('Valid script failed: ' + $successRun.Output) }
    $successResult = $successRun.Output | ConvertFrom-Json
    if ($successResult.Status -ne 'PASS') { throw 'Valid script did not report PASS.' }
    if ($successResult.VerifiedArchive -ne 'ADDED') { throw 'Verified repair was not archived.' }
    if ([System.IO.File]::ReadAllText($marker) -ne 'PASS') { throw 'Valid script postcondition failed.' }
    if (-not (Test-Path -LiteralPath $learnedCatalog)) { throw 'Learned error catalog was not created.' }

    $events = @([System.IO.File]::ReadAllLines($incidentLog, [Text.Encoding]::UTF8) | ForEach-Object { $_ | ConvertFrom-Json })
    if (@($events | Where-Object event -eq 'FAILURE_VERIFIED_RESOLVED').Count -ne 1) {
        throw 'Resolved incident event was not recorded exactly once.'
    }

    [pscustomobject]@{
        Status = 'PASS'
        SyntaxFailureBlocked = $true
        BlockedSideEffectAbsent = $true
        ValidExecutionPassed = $true
        AutomaticIncidentCreated = (Test-Path -LiteralPath $incidentLog)
        VerifiedRepairArchived = $true
    } | ConvertTo-Json -Compress
}
finally {
    if (Test-Path -LiteralPath $testRoot) {
        Remove-Item -LiteralPath $testRoot -Recurse -Force
    }
}
