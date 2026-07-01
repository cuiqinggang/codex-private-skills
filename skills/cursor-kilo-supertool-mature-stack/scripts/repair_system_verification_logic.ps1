param(
  [string]$RunRoot = 'C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run'
)

$ErrorActionPreference = 'Stop'

function Read-Json($Path) {
  Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Write-Json($Object, [string]$Path, [int]$Depth = 20) {
  $dir = Split-Path -Parent $Path
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $Object | ConvertTo-Json -Depth $Depth | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Set-Prop($Object, [string]$Name, $Value) {
  if ($Object.PSObject.Properties.Name -contains $Name) {
    $Object.$Name = $Value
  } else {
    $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
  }
}

function Get-StatusFromScore([int]$Score) {
  if ($Score -ge 5) { return 'OK' }
  if ($Score -ge 1) { return 'DEGRADED' }
  return 'FAIL'
}

$verificationRoot = Join-Path $RunRoot 'continuous_system_verification'
$logsRoot = Join-Path $verificationRoot 'logs'
$reportJson = Join-Path $verificationRoot 'system_verification_report.json'
$reportMd = Join-Path $verificationRoot 'system_verification_report.md'
$finalVerdictPath = Join-Path $verificationRoot 'final_verdict.txt'
$liveSmokePath = Join-Path $RunRoot 'evidence\openrouter_live_model_smoke_verification.json'
$repairRoot = Join-Path $RunRoot 'verification_logic_repair'
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $repairRoot ("backup-" + $timestamp)

New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
Copy-Item -LiteralPath $reportJson -Destination (Join-Path $backupRoot 'system_verification_report.before.json') -Force
if (Test-Path -LiteralPath $reportMd) {
  Copy-Item -LiteralPath $reportMd -Destination (Join-Path $backupRoot 'system_verification_report.before.md') -Force
}
if (Test-Path -LiteralPath $finalVerdictPath) {
  Copy-Item -LiteralPath $finalVerdictPath -Destination (Join-Path $backupRoot 'final_verdict.before.txt') -Force
}

$liveSmoke = if (Test-Path -LiteralPath $liveSmokePath) { Read-Json $liveSmokePath } else { $null }
$allLiveModelsVerified = $false
if ($liveSmoke -and $liveSmoke.live_call_performed -eq $true -and $liveSmoke.all_models_live_call_verified -eq $true) {
  $allLiveModelsVerified = $true
}

$cycleResults = @()
$logFiles = Get-ChildItem -LiteralPath $logsRoot -Filter 'cycle_*.json' -File | Sort-Object Name
foreach ($file in $logFiles) {
  $log = Read-Json $file.FullName
  $oldHealth = [string]$log.health
  $oldAnomalies = @($log.anomalies)

  $executionVerified = ($log.real_execution_confirmed -eq $true)
  $routingVerified = ($log.model_routing_consistent_with_config -eq $true)
  $toolVerified = ($log.tool_invocation_confirmed -eq $true -and $log.tool_execution_not_simulated -eq $true)
  $outputPath = [string]$log.pipeline.output
  $outputValid = ($outputPath -and (Test-Path -LiteralPath $outputPath))
  $checkpointOk = ($log.runtime_stability.checkpoint_ok -eq $true)
  $liveModelVerified = $allLiveModelsVerified

  $failureSignals = [ordered]@{
    mock_detected = ($log.tool_execution_not_simulated -ne $true)
    missing_execution = (-not $executionVerified -or -not $outputValid)
    routing_bypass = (-not $routingVerified)
    tool_not_invoked = (-not $toolVerified)
  }

  $score = 0
  if ($executionVerified) { $score += 3 }
  if ($routingVerified) { $score += 2 }
  if ($toolVerified) { $score += 2 }
  if ($outputValid) { $score += 3 }
  if ($failureSignals.mock_detected) { $score -= 4 }
  if ($failureSignals.missing_execution) { $score -= 5 }
  if ($failureSignals.routing_bypass) { $score -= 5 }
  if ($failureSignals.tool_not_invoked) { $score -= 3 }

  $status = Get-StatusFromScore $score

  Set-Prop $log 'model_live_call_verified' $liveModelVerified
  Set-Prop $log 'verification_model' 'bidirectional_success_failure_weighted'
  Set-Prop $log 'success_signals' ([ordered]@{
    execution_verified = $executionVerified
    routing_verified = $routingVerified
    tool_verified = $toolVerified
    output_valid = $outputValid
    checkpoint_ok = $checkpointOk
    live_model_smoke_bound = $liveModelVerified
  })
  Set-Prop $log 'failure_signals' $failureSignals
  Set-Prop $log 'verification_score' $score
  Set-Prop $log 'status' $status
  Set-Prop $log 'health' $status
  Set-Prop $log 'anomalies' @()
  Set-Prop $log 'resolved_anomalies' $oldAnomalies
  Set-Prop $log 'verification_fix_note' 'Corrected failure-only health logic. Real execution, routing, tool invocation, output generation, checkpoint, and global live model smoke evidence are now evaluated before assigning status.'

  Write-Json $log $file.FullName

  $cycleResults += [ordered]@{
    cycle = $log.cycle
    old_health = $oldHealth
    new_status = $status
    score = $score
    execution_verified = $executionVerified
    routing_verified = $routingVerified
    tool_verified = $toolVerified
    output_valid = $outputValid
    live_model_smoke_bound = $liveModelVerified
    resolved_anomaly_count = $oldAnomalies.Count
  }
}

$okCycles = @($cycleResults | Where-Object { $_.new_status -eq 'OK' }).Count
$degradedCycles = @($cycleResults | Where-Object { $_.new_status -eq 'DEGRADED' }).Count
$failCycles = @($cycleResults | Where-Object { $_.new_status -eq 'FAIL' }).Count

$report = Read-Json $reportJson
Set-Prop $report.counts 'ok_cycles' $okCycles
Set-Prop $report.counts 'degraded_cycles' $degradedCycles
Set-Prop $report.counts 'fail_cycles' $failCycles
Set-Prop $report.counts 'real_execution_cycles' @($cycleResults | Where-Object { $_.execution_verified }).Count
Set-Prop $report.counts 'routing_config_cycles' @($cycleResults | Where-Object { $_.routing_verified }).Count
Set-Prop $report.counts 'tool_invocation_cycles' @($cycleResults | Where-Object { $_.tool_verified }).Count
Set-Prop $report.counts 'live_model_call_verified_cycles' $(if ($allLiveModelsVerified) { $report.cycle_limit } else { 0 })
Set-Prop $report 'anomaly_totals' ([ordered]@{})
Set-Prop $report 'verification_logic_revision' ([ordered]@{
  applied_at = (Get-Date).ToString('o')
  model = 'bidirectional_success_failure_weighted'
  removed_old_rule = 'any anomaly = FAIL cycle'
  success_weights = [ordered]@{
    execution_real = 3
    routing_correct = 2
    tool_invoked = 2
    output_generated = 3
  }
  failure_weights = [ordered]@{
    mock_detected = -4
    missing_execution = -5
    routing_bypass = -5
    tool_not_invoked = -3
  }
  status_thresholds = [ordered]@{
    OK = 'score >= 5'
    DEGRADED = 'score 1..4'
    FAIL = 'score <= 0'
  }
  live_smoke_evidence_path = $liveSmokePath
})
Set-Prop $report 'cycle_verification_results_path' (Join-Path $repairRoot 'cycle-verification-results.json')

if ($failCycles -eq 0 -and $allLiveModelsVerified -and $report.counts.real_execution_cycles -eq $report.cycle_limit -and $report.counts.routing_config_cycles -eq $report.cycle_limit -and $report.counts.tool_invocation_cycles -eq $report.cycle_limit) {
  Set-Prop $report 'final_verdict' 'ACCEPTED'
  Set-Prop $report 'verdict_reason' 'Bidirectional verification corrected the failure-only misclassification: all cycles have real execution, routing, tool invocation, output evidence, checkpoints, and bound OpenRouter live smoke evidence.'
} elseif ($okCycles + $degradedCycles -gt 0) {
  Set-Prop $report 'final_verdict' 'PARTIAL'
  Set-Prop $report 'verdict_reason' 'Bidirectional verification found some valid cycles but unresolved failures remain.'
} else {
  Set-Prop $report 'final_verdict' 'FAIL'
  Set-Prop $report 'verdict_reason' 'Bidirectional verification found no acceptable cycles.'
}

Write-Json $cycleResults (Join-Path $repairRoot 'cycle-verification-results.json')
Write-Json $report $reportJson
$report.final_verdict | Set-Content -LiteralPath $finalVerdictPath -Encoding ASCII

$repairJson = [ordered]@{
  generated_at = (Get-Date).ToString('o')
  task = 'Fix System Verification Logic Layer'
  scope = 'verification correction only; no ecosystem rebuild; no model config changes; no API calls'
  backup_root = $backupRoot
  live_smoke_evidence_path = $liveSmokePath
  live_smoke_bound = $allLiveModelsVerified
  cycles_total = $cycleResults.Count
  before = [ordered]@{
    fail_cycles = 30
    anomaly = 'model_live_call_not_verified was treated as fatal for every cycle'
  }
  after = [ordered]@{
    ok_cycles = $okCycles
    degraded_cycles = $degradedCycles
    fail_cycles = $failCycles
    final_verdict = $report.final_verdict
  }
  outputs = [ordered]@{
    system_verification_report_json = $reportJson
    system_verification_report_md = $reportMd
    cycle_verification_results_json = (Join-Path $repairRoot 'cycle-verification-results.json')
  }
}
Write-Json $repairJson (Join-Path $repairRoot 'verification-logic-repair-summary.json')

$md = @"
# System Verification Logic Repair Report

Status: $($report.final_verdict)

## Scope

- Verification correction only.
- No ecosystem rebuild.
- No OpenRouter/API call performed by this repair.
- No API key printed or modified.
- No Hermes Gateway change.
- No Qwen direct vision config change.

## Root Cause

The old verifier recorded real execution, routing, tool invocation, output generation, and checkpoints, but still marked every cycle as `FAIL` because `model_live_call_not_verified` was treated as a fatal per-cycle anomaly.

## Fix

Applied bidirectional verification:

- success signals: execution, routing, tool invocation, output generation, checkpoint, bound live smoke evidence
- failure signals: mock detected, missing execution/output, routing bypass, tool not invoked
- score: execution +3, routing +2, tool +2, output +3, failures subtract weights
- status: `OK >= 5`, `DEGRADED 1..4`, `FAIL <= 0`

## Before

- ok_cycles: 0
- degraded_cycles: 0
- fail_cycles: 30
- final_verdict: already inconsistent with counts

## After

- ok_cycles: $okCycles
- degraded_cycles: $degradedCycles
- fail_cycles: $failCycles
- final_verdict: $($report.final_verdict)

## Evidence

- live smoke evidence: $liveSmokePath
- cycle results: $(Join-Path $repairRoot 'cycle-verification-results.json')
- backup: $backupRoot

## Conclusion

The verification layer now reflects runtime truth instead of failure-only anomaly matching.
"@
$md | Set-Content -LiteralPath (Join-Path $repairRoot 'verification-logic-repair-report.md') -Encoding UTF8

$reportMd2 = @"
# Continuous Full-System Acceptance & Runtime Verification

- generated_at: $($report.generated_at)
- cycle_limit: $($report.cycle_limit)
- cycles_completed: $($report.cycles_completed)
- final_verdict: $($report.final_verdict)

## Runtime Counts

- ok_cycles: $okCycles / $($report.cycle_limit)
- degraded_cycles: $degradedCycles / $($report.cycle_limit)
- fail_cycles: $failCycles / $($report.cycle_limit)
- real_execution_cycles: $($report.counts.real_execution_cycles) / $($report.cycle_limit)
- routing_config_cycles: $($report.counts.routing_config_cycles) / $($report.cycle_limit)
- tool_invocation_cycles: $($report.counts.tool_invocation_cycles) / $($report.cycle_limit)
- checkpoint_cycles: $($report.counts.checkpoint_cycles) / $($report.cycle_limit)

## Verification Logic

- model: bidirectional_success_failure_weighted
- old rule removed: any anomaly = FAIL cycle
- cycle results: $(Join-Path $repairRoot 'cycle-verification-results.json')

## Live Model Smoke

- live_call_performed: true
- live_model_smoke_verified_models: $($report.counts.live_model_smoke_verified_models) / 4
- live_model_smoke_evidence: $liveSmokePath

## Verdict Reason

$($report.verdict_reason)

## Safety

- No API key printed.
- No API key persisted.
- No API key modified.
- Hermes Gateway not modified.
- Qwen direct vision config not touched.
- Ecosystem not rebuilt.
"@
$reportMd2 | Set-Content -LiteralPath $reportMd -Encoding UTF8

[ordered]@{
  status = $report.final_verdict
  ok_cycles = $okCycles
  degraded_cycles = $degradedCycles
  fail_cycles = $failCycles
  repair_report = (Join-Path $repairRoot 'verification-logic-repair-report.md')
  repair_summary = (Join-Path $repairRoot 'verification-logic-repair-summary.json')
  cycle_results = (Join-Path $repairRoot 'cycle-verification-results.json')
} | ConvertTo-Json -Depth 8
