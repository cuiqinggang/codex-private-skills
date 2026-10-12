$ErrorActionPreference='Stop'
$dir='C:\AI\Polsia-V5-Parallel-20261012\monitor'
$h=[IO.File]::ReadAllText((Join-Path $dir 'index.html'),[Text.Encoding]::UTF8)
$parts=[regex]::Matches($h,'(?s)<script(?:\s[^>]*)?>(.*?)</script>')
$n=0;$fail=0
foreach($m in $parts){
 $code=$m.Groups[1].Value
 if([string]::IsNullOrWhiteSpace($code)){continue}
 $n++;$temp=Join-Path $env:TEMP ('polsia-monitor-'+$n+'.js')
 [IO.File]::WriteAllText($temp,$code,[Text.UTF8Encoding]::new($false))
 & node --check $temp
 if($LASTEXITCODE -ne 0){$fail++}
}
$d=Invoke-RestMethod 'http://127.0.0.1:8766/status.json' -TimeoutSec 10
$r=Invoke-WebRequest 'http://127.0.0.1:8766/index.html' -TimeoutSec 10
$bytes=$r.RawContentStream.ToArray()
$html=[Text.Encoding]::UTF8.GetString($bytes)
$history=Invoke-RestMethod 'http://127.0.0.1:8766/status-pa5-history.json' -TimeoutSec 10
Write-Output ('JS_CHECKED='+$n+' JS_ERRORS='+$fail)
Write-Output ('HTTP='+$r.StatusCode+' HTML_V1='+$html.Contains('独立监控 V1.0')+' HTML_PCL='+$html.Contains('PCL 四路执行情况'))
Write-Output ('SCHEMA='+$d.schema+' BATCH='+$d.batch_id+' TASKS='+@($d.jobs).Count+' CONTRACTS_VERIFIED='+@($d.jobs|Where-Object source_verified).Count)
Write-Output ('RUNNING='+@($d.jobs|Where-Object status -eq RUNNING).Count+' NOT_STARTED='+@($d.jobs|Where-Object status -eq ASSIGNED_NOT_YET_STARTED).Count+' OLD_HISTORY='+@($history.jobs).Count)
if($fail -gt 0 -or $r.StatusCode -ne 200 -or $d.version -ne '1.0.0' -or @($d.jobs).Count -ne 4 -or @($history.jobs).Count -ne 5){throw 'MONITOR_V1_TEST_FAILED'}