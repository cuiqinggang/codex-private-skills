$ErrorActionPreference='Stop'
$root='C:\AI\Polsia-V5-Parallel-20261012\monitor'
$port=8766
$existing=@(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
if($existing.Count -gt 0){
 try{$ping=Invoke-WebRequest -Uri 'http://127.0.0.1:8766/index.html' -TimeoutSec 3 -ErrorAction Stop
 if($ping.StatusCode -eq 200){Write-Output 'ALREADY_RUNNING_HEALTHY';exit 0}}catch{}
 throw 'PORT_OCCUPIED_BY_UNVERIFIED_SERVICE'
}
$python=Get-Command python.exe -ErrorAction Stop
$stdout=Join-Path $root 'web-server.out.log'
$stderr=Join-Path $root 'web-server.err.log'
$proc=Start-Process -FilePath $python.Source -ArgumentList @('-m','http.server','8766','--bind','127.0.0.1','--directory',('"' + $root + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
Start-Sleep -Seconds 2
try{$r=Invoke-WebRequest -Uri 'http://127.0.0.1:8766/index.html' -TimeoutSec 5 -ErrorAction Stop
 $d=Invoke-RestMethod -Uri 'http://127.0.0.1:8766/status.json' -TimeoutSec 5
 if($r.StatusCode -ne 200 -or @($d.jobs).Count -ne 5){throw 'DASHBOARD_OR_5_LANES_MISSING'}
 [IO.File]::WriteAllText((Join-Path $root 'web-server-pid.txt'),([string]$proc.Id))
 Write-Output ('DASHBOARD_REAL_HTTP_PASS;PID='+$proc.Id+';TASKS='+@($d.jobs).Count)
}catch{
 if(-not $proc.HasExited){Stop-Process -Id $proc.Id -ErrorAction SilentlyContinue}
 throw
}