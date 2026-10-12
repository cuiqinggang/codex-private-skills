$ErrorActionPreference='Continue'
$base='C:\AI\Polsia-V5-Parallel-20261012'
& (Join-Path $base 'save-status.ps1') PA5-03 BLOCKED '业务工作流服务与模型桥均未监听，正在等待合法恢复' 3 'PA5-03-workflow-probe.json' 'HTTP无法连接；n8n端口5678及模型桥8788未监听'
$task='Polsia-V5-Process-Publish'
$pwsh='C:\Program Files\PowerShell\7\pwsh.exe'
try{
 $old=Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
 if(-not $old){
  $action=New-ScheduledTaskAction -Execute $pwsh -Argument '-NoLogo -NoProfile -NonInteractive -File "C:\AI\Polsia-V5-Parallel-20261012\monitor\publish-status.ps1"'
  $trig=New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(1)) -RepetitionInterval (New-TimeSpan -Minutes 1)
  $settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 1) -StartWhenAvailable
  $old=Register-ScheduledTask -TaskName $task -Action $action -Trigger $trig -Settings $settings -Description 'Polsia V5 readonly process snapshot each 60 seconds' -ErrorAction Stop
 }
 if($old.State -eq 'Disabled'){throw '任务被禁用，拒绝宣称持续更新'}
 Write-Output ('NATIVE_MINUTE_SAMPLING='+$old.State)
}catch{Write-Output ('SCHEDULE_NOT_CERTIFIED='+$_.Exception.Message)}
try{
 $shell=New-Object -ComObject WScript.Shell
 $startup=[Environment]::GetFolderPath('Startup')
 $target=Join-Path $startup 'Polsia V5 全流程状态服务.lnk'
 $sc=$shell.CreateShortcut($target)
 $sc.TargetPath=$pwsh
 $sc.Arguments='-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -File "C:\AI\Polsia-V5-Parallel-20261012\monitor\start-dashboard.ps1"'
 $sc.WorkingDirectory=(Join-Path $base 'monitor')
 $sc.Description='只启动轻量本地只读网页服务，不打开新浏览器、不执行业务'
 $sc.Save()
 Write-Output 'DASHBOARD_STARTUP_SHORTCUT=PASS'
}catch{Write-Output ('STARTUP_NOT_CERTIFIED='+$_.Exception.Message)}