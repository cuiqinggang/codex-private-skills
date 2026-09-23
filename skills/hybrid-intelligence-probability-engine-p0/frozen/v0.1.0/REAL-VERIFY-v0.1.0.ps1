param([int]$Runs=10)
$ErrorActionPreference='Stop'
$start=[System.Diagnostics.Stopwatch]::GetTimestamp()
$freq=[System.Diagnostics.Stopwatch]::Frequency
$ts=[DateTimeOffset]::Now.ToString('o')
Write-Host "REAL_START_TIMESTAMP=$ts"
Write-Host "REAL_START_TICK=$start"
Write-Host "STOPWATCH_FREQUENCY=$freq"
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$runner=Join-Path $root 'HIPE-P0-v0.1.0-real-verify.py'
$out=Join-Path $root 'HIPE-P0-REAL-RESULT.json'
python $runner --mode live --runs $Runs --out $out
$code=$LASTEXITCODE
$end=[System.Diagnostics.Stopwatch]::GetTimestamp()
$endts=[DateTimeOffset]::Now.ToString('o')
$ms=[math]::Round(1000.0*($end-$start)/$freq,3)
Write-Host "REAL_END_TIMESTAMP=$endts"
Write-Host "REAL_PROCESS_MS=$ms"
if(Test-Path -LiteralPath $out){ Write-Host "RESULT_SHA256=$((Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash)" }
exit $code