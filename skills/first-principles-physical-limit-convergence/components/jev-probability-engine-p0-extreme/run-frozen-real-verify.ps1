param(
  [Parameter(Mandatory=$true)]
  [string]$FixtureRoot
)
# TASK_STEP=3_REAL_VERIFY
$ErrorActionPreference='Stop'
$FixtureRoot=(Resolve-Path -LiteralPath $FixtureRoot).Path
Write-Host 'METHOD=first-principles-physical-limit-convergence v3.1.6'
Write-Host 'SOLUTION_FROZEN=YES'
Write-Host 'EXECUTOR_ROLE=EXECUTE_VERIFY_REPORT_STOP'
Write-Host "FIXTURE_ROOT=$FixtureRoot"

$expected=@{
  'fixtures\public\pe-p0-general-01.input.json'='a002824c2da64f005819469b2e0b3ae9683c9ea2f5b8d0b8a59384785c04d3a7'
  'fixtures\private\pe-p0-general-01.oracle.json'='ec6e70aab43fc0c98b8d5c44ffce015bc0516ea4ce1891f654c2c8020b845ccb'
  'fixtures\private\executor-outcomes.json'='3e20d211220f33984e05e6721f1e3dd0c552ef4da0bb6ab0dd14dac8a22cf0da'
}
foreach($rel in $expected.Keys){
  $p=Join-Path $FixtureRoot $rel
  if(-not (Test-Path -LiteralPath $p)){ throw "FIXTURE_MISSING=$rel" }
  $h=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
  if($h -ne $expected[$rel]){ throw "FIXTURE_HASH_MISMATCH=$rel GOT=$h" }
}
Write-Host 'FIXTURE_HASH_GATE=PASS'

$root=Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $root
try {
  if (-not $env:OPENROUTER_API_KEY) {
    $secure=Read-Host 'OpenRouter Key' -AsSecureString
    $b=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { $env:OPENROUTER_API_KEY=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($b) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b) }
  }
  if (-not (Test-Path node_modules\undici)) {
    npm install --ignore-scripts --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw "NPM_INSTALL_FAILED exit=$LASTEXITCODE" }
  }
  $env:PE_P0_FIXTURE_ROOT=$FixtureRoot
  node .\frozen-reality-verify.mjs
  $exit=$LASTEXITCODE
  if ($exit -ne 0) {
    Write-Host "REALITY_DELTA=YES EXIT=$exit"
    Write-Host 'ACTION=STOP_RETURN_TO_GPT'
    exit $exit
  }
  Write-Host 'ACTION=REPORT_STOP'
} finally {
  Remove-Item Env:PE_P0_FIXTURE_ROOT -ErrorAction SilentlyContinue
  Pop-Location
}
