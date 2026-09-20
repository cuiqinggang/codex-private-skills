[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$expectedAnchorHash = 'B132E06971FC4A2546A93A531054383ABE98BF27E33DDB00545294F4C432C20C'
$expectedResultHash = '7D093D354D6FE6554899DCB7E4D06F251C7D7860D9AE68F73D0B7AB93CB47E51'
$commandPack = 'C:\Users\A\Desktop\jev-probability-engine-p0-v0.2.2-command-pack\jev-probability-engine-p0-v0.2.2-command-pack'
$step3 = 'C:\Users\A\Documents\Codex\2026-09-21\jev-probability-engine-p0-step3-virtual99-v2'
$workspace = $PSScriptRoot
$sourcePath = Join-Path $workspace 'candidate-reality-challenge-v2.cs'
$resultsRoot = Join-Path $workspace 'reality-challenge-v2'
$finalResult = Join-Path $workspace 'REALITY_CHALLENGE_V2_RESULT.json'
$acceptance = Join-Path $workspace 'REALITY_CHALLENGE_V2_ACCEPTANCE.md'
$anchorPath = Join-Path $commandPack 'scripts\reality-anchor.mjs'
$oldResultPath = Join-Path $commandPack 'reality-test\results\RESULT.json'

if ($PSVersionTable.PSEdition -ne 'Core' -or $PSVersionTable.PSVersion.Major -lt 7) {
    throw 'CHALLENGE=BLOCKED_FROZEN_RUNTIME: PowerShell 7 is required.'
}

$virtual = Get-Content -LiteralPath (Join-Path $step3 'VIRTUAL_RESULT-V2.json') -Raw | ConvertFrom-Json
$frozen = Get-Content -LiteralPath (Join-Path $step3 '02-FROZEN-CANDIDATE-V2.json') -Raw | ConvertFrom-Json
if ($virtual.VIRTUAL_99_V2 -ne 'PASS' -or $virtual.SOLUTION_FROZEN_V2 -ne 'YES' -or $virtual.STEP4_ALLOWED -ne 'YES' -or
    $frozen.jev_decision_waves_per_run -ne 1 -or $frozen.http_requests_per_run -ne 2 -or
    $frozen.http_request_concurrency -ne 2 -or $frozen.local_execution_waves -ne 2) {
    throw 'CHALLENGE=BLOCKED: frozen Step 3 V2 gate mismatch.'
}

$anchorHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $anchorPath).Hash
$oldResultHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $oldResultPath).Hash
if ($anchorHash -ne $expectedAnchorHash -or $oldResultHash -ne $expectedResultHash) {
    throw 'BASELINE_SOURCE_INTEGRITY=FAIL CHALLENGE=BLOCKED'
}

foreach ($path in @($resultsRoot, $finalResult, $acceptance)) {
    if (Test-Path -LiteralPath $path) { throw "OUTPUT_ALREADY_EXISTS_NO_OVERWRITE: $path" }
}

Add-Type -Path $sourcePath -ErrorAction Stop

$publicFixture = Join-Path $commandPack 'fixtures\public\pe-p0-general-01.input.json'
$privateOracle = Join-Path $commandPack 'fixtures\private\pe-p0-general-01.oracle.json'
$executorOutcomes = Join-Path $commandPack 'fixtures\private\executor-outcomes.json'

$exitCode = [JevP0V2.RealityChallenge]::RunAsync(
    $publicFixture,
    $privateOracle,
    $executorOutcomes,
    $resultsRoot,
    $finalResult,
    $acceptance
).GetAwaiter().GetResult()

exit $exitCode
