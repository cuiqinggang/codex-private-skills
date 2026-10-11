param([switch]$Once,[int]$RefreshSeconds=10)
$ErrorActionPreference='Continue'
$monRoot='C:\AI\Polsia-Unified-V4'
$lastAlert=''
try{$Host.UI.RawUI.WindowTitle='POLSIA V4 | All Tasks / Real Status'}catch{}
[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false)
while($true){
 $snap=$null;$readError=''
 try{$snap=Get-Content -LiteralPath (Join-Path $monRoot 'snapshot.json') -Raw -Encoding utf8 | ConvertFrom-Json -ErrorAction Stop}catch{$readError=$_.Exception.Message}
 if(-not $Once){Clear-Host}
 Write-Host '========================================================' -ForegroundColor Cyan
 Write-Host '     POLSIA V4  |  全任务监控台 (只读 / 可持久化)' -ForegroundColor Cyan
 Write-Host '========================================================' -ForegroundColor Cyan
 if(-not $snap){Write-Host ('监控数据不可读: '+$readError) -ForegroundColor Red}
 else{
  $age=999999
  try{$age=[math]::Round(([DateTime]::UtcNow-([DateTime]$snap.utc).ToUniversalTime()).TotalSeconds)}catch{}
  $online=$age -ge 0 -and $age -le 150
  $sev=if($snap.alert_keys.Count -gt 0 -or -not $online){'RED'}elseif($snap.root_status -eq 'WAITING_CEO' -or @($snap.branches|Where-Object {$_.status -eq 'BLOCKED'}).Count -gt 0){'YELLOW'}else{'GREEN'}
  $clr=if($sev -eq 'RED'){'Red'}elseif($sev -eq 'YELLOW'){'Yellow'}else{'Green'}
  Write-Host ('监控采样: '+$snap.utc+'  / '+$age+'秒前; 采样任务='+$(if($online){'正常'}else{'失联'})) -ForegroundColor $clr
  Write-Host ('母任务: '+$snap.root_status+' | 冻结: '+$snap.freeze+' | Codex PID: '+($snap.root_pid -join ', ')) -ForegroundColor $clr
  Write-Host ('当前节点: '+$snap.node)
  if($snap.root_reason){Write-Host ('等待/问题原因: '+$snap.root_reason) -ForegroundColor $(if($snap.root_status -eq 'WAITING_CEO'){'Yellow'}else{'Red'})}
  Write-Host ('原计划任务: '+$snap.scheduler+' | 业务INFLIGHT='+$snap.inflight)
  Write-Host '--------------------------------------------------------'
  Write-Host '模块            实际状态        说明/下一步'
  Write-Host '--------------------------------------------------------'
  foreach($b in $snap.branches){
   $line=('{0,-12} {1,-13} {2}' -f $b.id,$b.status,$b.detail)
   $col=if($b.status -in @('ERROR','STALE','ALERT')){'Red'}elseif($b.status -in @('BLOCKED','WAITING_CEO','READY')){'Yellow'}else{'Green'}
   if($line.Length -gt 110){$line=$line.Substring(0,110)}
   Write-Host $line -ForegroundColor $col
  }
  Write-Host '--------------------------------------------------------'
  if($snap.alert_keys.Count -gt 0){
   Write-Host ('! 当前故障 '+$snap.alert_keys.Count+': '+($snap.alert_keys -join '; ')) -ForegroundColor Red
  }elseif(-not $online){Write-Host '! 监控采样超过150秒未更新，检查监控计划任务' -ForegroundColor Red}
  else{Write-Host '当前无未解决故障；正常等待审批不属于宕机。' -ForegroundColor Green}
  if($snap.notes.Count -gt 0){Write-Host ('注意: '+($snap.notes -join '; ')) -ForegroundColor Yellow}
  Write-Host '最近异常及恢复记录 (即使故障已修复，历史仍保留):'
  $history=Join-Path $monRoot 'incidents.jsonl'
  if(Test-Path -LiteralPath $history){
   @(Get-Content -LiteralPath $history -Tail 4 -Encoding utf8) | ForEach-Object {
    try{$ev=$_|ConvertFrom-Json;Write-Host ('  '+$ev.utc+' '+$ev.event+' '+$ev.key)}catch{}
   }
  }else{Write-Host '  无异常记录'}
  $key=($snap.alert_keys -join '|')
  if((-not $online -or $key) -and ($key+'|'+$online) -ne $lastAlert){try{[Console]::Beep(920,350)}catch{}}
  $lastAlert=$key+'|'+$online
 }
 Write-Host '--------------------------------------------------------'
 Write-Host '关闭窗口不会停止Windows原生监控，未执行任何业务/自动重发。'
 if($Once){break}
 Start-Sleep -Seconds $RefreshSeconds
}