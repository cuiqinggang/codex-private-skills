[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel).Trim()
if (-not $repoRoot) { throw 'VERIFY=BLOCKED: not inside the repository.' }

$relativeBase = 'skills\first-principles-physical-limit-convergence\components\jev-probability-engine-p0-extreme\virtual-attacks\v0.5.0'
$base = Join-Path $repoRoot $relativeBase

$sourcePath = Join-Path $base 'candidate-reality-challenge-v3.cs'
$frozenPath = Join-Path $base 'FROZEN-CANDIDATE-v0.5.0.json'
$contractPath = Join-Path $base 'REAL-VERIFY-CONTRACT.md'
$virtualPath = Join-Path $base 'VIRTUAL-99-FREEZE.md'

$baselineCert = Join-Path $repoRoot 'skills\first-principles-physical-limit-convergence\components\jev-probability-engine-p0-extreme\certifications\v0.4.0\REALITY_CERTIFICATION.md'
$baselineManifest = Join-Path $repoRoot 'skills\first-principles-physical-limit-convergence\components\jev-probability-engine-p0-extreme\certifications\v0.4.0\manifest.json'

$expected = @{
    $sourcePath = '66de96b172c50efea8f3f520c0c31669d6122c67'
    $frozenPath = '4b273b74a7d74851d1e99715a72cb52e168d7752'
    $contractPath = 'f89584f72bafe04f61d347bfc2960ecbfbbde997'
    $virtualPath = 'e2333b65d87486247223f62a881a1eef4b3f5613'
    $baselineCert = '1c8edbf4834a69dd4cc037211bf3d29b44f16ea4'
    $baselineManifest = '88cbe180ff6f6c78e99072b393f4ad4dee038179'
}

foreach ($path in $expected.Keys) {
    if (-not (Test-Path -LiteralPath $path)) { throw "VERIFY=BLOCKED_MISSING_FILE: $path" }
    $actual = (git hash-object -- $path).Trim().ToLowerInvariant()
    if ($actual -ne $expected[$path]) {
        throw "VERIFY=BLOCKED_FROZEN_HASH_MISMATCH: $path expected=$($expected[$path]) actual=$actual"
    }
}

$frozen = Get-Content -LiteralPath $frozenPath -Raw | ConvertFrom-Json
if ($frozen.candidate_id -ne 'JPE-P0-S2-PROJECTED-EARLY-RELEASE-V3' -or
    $frozen.gates.virtual_99 -ne 'PASS' -or
    $frozen.gates.solution_frozen -ne 'YES' -or
    $frozen.gates.real_verify -ne 'NOT_YET' -or
    $frozen.gates.codex_design_authority -ne 'NO' -or
    $frozen.gates.codex_executor_only -ne 'YES' -or
    [double]$frozen.baseline.t_p0_ms -ne 560.9819) {
    throw 'VERIFY=BLOCKED_FROZEN_CONTRACT_MISMATCH'
}

if ($PSVersionTable.PSEdition -ne 'Core' -or $PSVersionTable.PSVersion.Major -lt 7) {
    throw 'VERIFY=BLOCKED_RUNTIME: PowerShell 7+ required.'
}

if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) {
    throw 'VERIFY=BLOCKED: OPENROUTER_API_KEY missing from current process.'
}

$commandPack = 'C:\Users\A\Desktop\jev-probability-engine-p0-v0.2.2-command-pack\jev-probability-engine-p0-v0.2.2-command-pack'
$anchorPath = Join-Path $commandPack 'scripts\reality-anchor.mjs'
$oldResultPath = Join-Path $commandPack 'reality-test\results\RESULT.json'
$expectedAnchorHash = 'B132E06971FC4A2546A93A531054383ABE98BF27E33DDB00545294F4C432C20C'
$expectedResultHash = '7D093D354D6FE6554899DCB7E4D06F251C7D7860D9AE68F73D0B7AB93CB47E51'

if (-not (Test-Path -LiteralPath $anchorPath) -or -not (Test-Path -LiteralPath $oldResultPath)) {
    throw 'VERIFY=BLOCKED_BASELINE_FIXTURE_MISSING'
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $anchorPath).Hash -ne $expectedAnchorHash -or
    (Get-FileHash -Algorithm SHA256 -LiteralPath $oldResultPath).Hash -ne $expectedResultHash) {
    throw 'VERIFY=BLOCKED_BASELINE_SOURCE_INTEGRITY_FAIL'
}

$workspace = 'C:\Users\A\Documents\Codex\2026-09-21\jev-probability-engine-p0-v050-frozen-real-verify-r2'
if (Test-Path -LiteralPath $workspace) {
    throw "VERIFY=BLOCKED_OUTPUT_ALREADY_EXISTS: $workspace"
}
New-Item -ItemType Directory -Path $workspace | Out-Null

$localSource = Join-Path $workspace 'candidate-reality-challenge-v3.cs'
Copy-Item -LiteralPath $sourcePath -Destination $localSource

$resultsRoot = Join-Path $workspace 'reality-challenge-v3'
$finalResult = Join-Path $workspace 'REALITY_CHALLENGE_V3_RESULT.json'
$acceptance = Join-Path $workspace 'REALITY_CHALLENGE_V3_ACCEPTANCE.md'

Add-Type -Path $localSource -ErrorAction Stop

$publicFixture = Join-Path $commandPack 'fixtures\public\pe-p0-general-01.input.json'
$privateOracle = Join-Path $commandPack 'fixtures\private\pe-p0-general-01.oracle.json'
$executorOutcomes = Join-Path $commandPack 'fixtures\private\executor-outcomes.json'

$exitCode = [JevP0V3.RealityChallenge]::RunAsync(
    $publicFixture,
    $privateOracle,
    $executorOutcomes,
    $resultsRoot,
    $finalResult,
    $acceptance
).GetAwaiter().GetResult()

$result = Get-Content -LiteralPath $finalResult -Raw | ConvertFrom-Json

Write-Host "CANDIDATE=$($result.candidate_id)"
Write-Host "MEASURED_RUNS=$($result.measured_runs)"
Write-Host "PASS_RUNS=$($result.pass_runs)"
Write-Host "FAIL_RUNS=$($result.fail_runs)"
Write-Host "COMMERCIAL_GATE_SERIES=$($result.commercial_gate_series)"
Write-Host "EXPECTED_HTTP_REQUESTS=$($result.expected_http_requests)"
Write-Host "ACTUAL_HTTP_REQUESTS=$($result.actual_http_requests)"
Write-Host "REQUEST_COUNT_MATCH=$($result.request_count_match)"
Write-Host "PREVIOUS_REAL_P0_VERSION=v0.4.0"
Write-Host "PREVIOUS_T_P0_MS=560.9819"
Write-Host "MIN_MS=$($result.min_ms)"
Write-Host "P50_MS=$($result.p50_ms)"
Write-Host "P95_MS=$($result.p95_ms)"
Write-Host "MAX_MS=$($result.max_ms)"
Write-Host "BASELINE_BEATEN=$($result.baseline_beaten)"
Write-Host "NEW_REAL_P0_ELIGIBLE=$($result.new_real_p0_eligible)"
Write-Host "RESULT_PATH=$finalResult"

$pass = (
    $exitCode -eq 0 -and
    [int]$result.measured_runs -eq 30 -and
    [int]$result.pass_runs -eq 30 -and
    [int]$result.fail_runs -eq 0 -and
    $result.commercial_gate_series -eq 'PASS' -and
    $result.request_count_match -eq 'PASS' -and
    $result.baseline_beaten -eq 'YES' -and
    [double]$result.min_ms -lt 560.9819
)

if ($pass) {
    Write-Host 'STATUS=V0.5.0_REAL_P0_ELIGIBLE'
    Write-Host 'NEXT_ACTION=RETURN_TO_GPT_FOR_APPEND_ONLY_CERTIFICATION'
    exit 0
}

Write-Host 'STATUS=KEEP_V0.4.0'
Write-Host 'NEXT_ACTION=REALITY_DELTA_STOP'
exit 3
