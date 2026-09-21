[CmdletBinding()]
param(
  [string]$ResultRoot = 'C:\Users\A\Documents\Codex\2026-09-21\jev-probability-engine-p0-v051-frozen-real-verify'
)

Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'

$final = Join-Path $ResultRoot 'REALITY_CHALLENGE_V4_RESULT.json'
$acceptance = Join-Path $ResultRoot 'REALITY_CHALLENGE_V4_ACCEPTANCE.md'
$measuredRoot = Join-Path $ResultRoot 'reality-challenge-v4\measured'

if (-not (Test-Path -LiteralPath $final)) { throw 'POST_VERIFY=BLOCKED_RESULT_MISSING' }
if (-not (Test-Path -LiteralPath $acceptance)) { throw 'POST_VERIFY=BLOCKED_ACCEPTANCE_MISSING' }
if (-not (Test-Path -LiteralPath $measuredRoot)) { throw 'POST_VERIFY=BLOCKED_MEASURED_ROOT_MISSING' }

$r = Get-Content -LiteralPath $final -Raw | ConvertFrom-Json
$dirs = @(Get-ChildItem -LiteralPath $measuredRoot -Directory -ErrorAction Stop)
$runSummaries = @()
$manifests = @()

foreach($d in $dirs){
  $rs = Join-Path $d.FullName 'run-summary.json'
  $mf = Join-Path $d.FullName 'manifest.json'
  if (-not (Test-Path -LiteralPath $rs)) { throw "POST_VERIFY=BLOCKED_RUN_SUMMARY_MISSING:$($d.Name)" }
  if (-not (Test-Path -LiteralPath $mf)) { throw "POST_VERIFY=BLOCKED_MANIFEST_MISSING:$($d.Name)" }
  $runSummaries += Get-Content -LiteralPath $rs -Raw | ConvertFrom-Json
  $manifests += Get-Content -LiteralPath $mf -Raw | ConvertFrom-Json
}

$checks = [ordered]@{
  candidate_id = ($r.candidate_id -eq 'JPE-P0-S2-SEMANTIC-PROJECTION-V4')
  baseline_version = ($r.baseline_version -eq 'v0.4.0')
  baseline_ms = ([double]$r.baseline_T_P0_ms -eq 560.9819)
  measured_count = ([int]$r.measured_runs -eq 30 -and $dirs.Count -eq 30 -and $runSummaries.Count -eq 30)
  pass_count = ([int]$r.pass_runs -eq 30 -and @($runSummaries | Where-Object { -not $_.pass }).Count -eq 0)
  fail_count = ([int]$r.fail_runs -eq 0)
  commercial_gate_series = ($r.commercial_gate_series -eq 'PASS')
  per_run_commercial_gate = (@($manifests | Where-Object { $_.commercial_gate -ne 'PASS' }).Count -eq 0)
  request_count = ([int]$r.actual_http_requests -eq 67 -and [int]$r.expected_http_requests -eq 67 -and $r.request_count_match -eq 'PASS')
  per_run_request_count = (@($runSummaries | Where-Object { [int]$_.request_count -ne 2 }).Count -eq 0)
  baseline_beaten = ($r.baseline_beaten -eq 'YES' -and [double]$r.min_ms -lt 560.9819)
}

$failed = @($checks.GetEnumerator() | Where-Object { -not $_.Value })

Write-Host "CANDIDATE=$($r.candidate_id)"
Write-Host "MEASURED_RUNS=$($r.measured_runs)"
Write-Host "PASS_RUNS=$($r.pass_runs)"
Write-Host "FAIL_RUNS=$($r.fail_runs)"
Write-Host "COMMERCIAL_GATE_SERIES=$($r.commercial_gate_series)"
Write-Host "EXPECTED_HTTP_REQUESTS=$($r.expected_http_requests)"
Write-Host "ACTUAL_HTTP_REQUESTS=$($r.actual_http_requests)"
Write-Host "REQUEST_COUNT_MATCH=$($r.request_count_match)"
Write-Host "PREVIOUS_REAL_P0_VERSION=v0.4.0"
Write-Host "PREVIOUS_T_P0_MS=560.9819"
Write-Host "MIN_MS=$($r.min_ms)"
Write-Host "P50_MS=$($r.p50_ms)"
Write-Host "P95_MS=$($r.p95_ms)"
Write-Host "MAX_MS=$($r.max_ms)"
Write-Host "BASELINE_BEATEN=$($r.baseline_beaten)"

if($failed.Count -eq 0){
  Write-Host 'POST_RUN_VERIFY=PASS'
  Write-Host 'STATUS=V0.5.1_REAL_P0_ELIGIBLE'
  Write-Host 'NEXT_ACTION=RETURN_TO_GPT_FOR_APPEND_ONLY_CERTIFICATION'
  exit 0
}

Write-Host ('POST_RUN_VERIFY=FAIL FAILED_CHECKS=' + (($failed | ForEach-Object Key) -join ','))
Write-Host 'STATUS=KEEP_V0.4.0'
Write-Host 'NEXT_ACTION=REALITY_DELTA_STOP'
exit 3
