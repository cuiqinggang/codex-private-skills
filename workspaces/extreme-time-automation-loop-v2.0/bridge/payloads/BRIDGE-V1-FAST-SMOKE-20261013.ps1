param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
$timer=[Diagnostics.Stopwatch]::StartNew()
[long]$sum=0
for($i=0;$i -lt 100000;$i++){ $sum+=$i }
$timer.Stop()
if($sum -ne 4999950000){throw 'V1_FAST_SUM_MISMATCH'}
if(-not $BridgeWorkDir -or -not (Test-Path -LiteralPath $BridgeWorkDir)){throw 'V1_FAST_WORKDIR_MISSING'}
if(-not $TaskFile -or -not (Test-Path -LiteralPath $TaskFile)){throw 'V1_FAST_TASKFILE_MISSING'}
Write-Output ('BRIDGE_V1_FAST_TASK_REALITY_PASS;HOST='+$env:COMPUTERNAME+';RUNNER='+$env:RUNNER_NAME+';COMPUTE_MS='+[math]::Round($timer.Elapsed.TotalMilliseconds,3)+';UTC='+[DateTime]::UtcNow.ToString('o'))
