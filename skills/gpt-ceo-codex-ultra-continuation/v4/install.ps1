param([switch]$NoWindow)
$ErrorActionPreference='Stop'
$monRoot='C:\AI\Polsia-Unified-V4'
$task='Polsia-Unified-Monitor-V4'
$pwsh='C:\Program Files\PowerShell\7\pwsh.exe'
$collector=Join-Path $monRoot 'collect.ps1'
$viewer=Join-Path $monRoot 'dashboard.ps1'
$result=[ordered]@{task=$task;task_register='NOT_ATTEMPTED';query='UNKNOWN';snapshot='UNKNOWN';desktop_shortcut='UNKNOWN';startup_shortcut='UNKNOWN';window='NOT_LAUNCHED';errors=@();utc=[DateTime]::UtcNow.ToString('o')}
if(-not (Test-Path -LiteralPath $pwsh)){throw 'NO_PWSH7_FOUND'}
try{
 $tr='"'+$pwsh+'" -NoLogo -NoProfile -NonInteractive -File "'+$collector+'"'
 $output=& schtasks.exe /Create /F /SC MINUTE /MO 1 /TN $task /TR $tr 2>&1
 if($LASTEXITCODE -eq 0){$result.task_register='PASS_NATIVE_SCHTASKS'}
 else{$result.errors+=('SCHTASKS_RETURN_'+$LASTEXITCODE+':'+($output -join ' '))}
}catch{$result.errors+=('SCHTASKS_EXCEPTION_'+$_.Exception.Message)}
if($result.task_register -ne 'PASS_NATIVE_SCHTASKS'){
 try{
  $a=New-ScheduledTaskAction -Execute $pwsh -Argument ('-NoLogo -NoProfile -NonInteractive -File "'+$collector+'"')
  $t=New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1)
  $s=New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew -StartWhenAvailable
  $null=Register-ScheduledTask -TaskName $task -Action $a -Trigger $t -Settings $s -Description 'Polsia V4 read-only native 1-min status snapshot, no second Codex' -Force -ErrorAction Stop
  $result.task_register='PASS_NATIVE_REGISTER_SCHEDULEDTASK'
 }catch{$result.errors+=('REGISTER_FALLBACK_'+$_.Exception.Message)}
}
try{
 $item=Get-ScheduledTask -TaskName $task -ErrorAction Stop
 $result.query=[string]$item.State
 if($result.task_register -like 'PASS_*'){
  try{Start-ScheduledTask -TaskName $task -ErrorAction Stop}catch{$result.errors+=('FIRST_TRIGGER_'+$_.Exception.Message)}
 }
}catch{$result.errors+=('VERIFY_TASK_'+$_.Exception.Message)}
try{
 $null=(& $collector -Once)
 $state=Get-Content -LiteralPath (Join-Path $monRoot 'snapshot.json') -Raw -Encoding utf8|ConvertFrom-Json
 if($state.schema -eq 'POLSIA_UNIFIED_MONITOR_V4' -and @($state.branches).Count -eq 10){$result.snapshot='PASS_10_BRANCHES'}else{$result.snapshot='FAIL_INCOMPLETE'}
}catch{$result.errors+=('COLLECT_'+$_.Exception.Message)}
if($result.task_register -like 'PASS_*' -and $result.snapshot -eq 'PASS_10_BRANCHES'){
 try{
  $desk=[Environment]::GetFolderPath('Desktop')
  $old=Join-Path $desk 'Polsia Codex - Live Status.lnk'
  $backup=Join-Path $monRoot 'Original-Live-Status.before-V4.lnk'
  if((Test-Path -LiteralPath $old) -and -not (Test-Path -LiteralPath $backup)){Copy-Item -LiteralPath $old -Destination $backup -ErrorAction Stop}
  $shell=New-Object -ComObject WScript.Shell
  $lnk=$shell.CreateShortcut($old)
  $lnk.TargetPath=$pwsh
  $lnk.Arguments='-NoLogo -NoProfile -NoExit -File "'+$viewer+'"'
  $lnk.WorkingDirectory=$monRoot
  $lnk.Description='Polsia V4 unified 10-lane monitor. Read-only; original runner unchanged.'
  $lnk.WindowStyle=1
  $lnk.Save()
  $result.desktop_shortcut=if(Test-Path -LiteralPath $old){'PASS'}else{'FAIL'}
  $startup=[Environment]::GetFolderPath('Startup')
  if($startup -and (Test-Path -LiteralPath $startup)){
   Copy-Item -LiteralPath $old -Destination (Join-Path $startup 'Polsia Unified V4.lnk') -Force
   $result.startup_shortcut='PASS_ON_USER_LOGON'
  }else{$result.startup_shortcut='STARTUP_FOLDER_UNAVAILABLE'}
 }catch{$result.errors+=('SHORTCUT_'+$_.Exception.Message)}
 if(-not $NoWindow){
  try{
   Start-Process -FilePath $pwsh -ArgumentList @('-NoLogo','-NoProfile','-NoExit','-File',('"'+$viewer+'"')) -WorkingDirectory $monRoot -WindowStyle Normal
   $result.window='LAUNCH_REQUESTED'
  }catch{$result.errors+=('WINDOW_'+$_.Exception.Message)}
 }
}
($result | ConvertTo-Json -Depth 4) | Set-Content -LiteralPath (Join-Path $monRoot 'installation.json') -Encoding utf8
$result|ConvertTo-Json -Compress -Depth 4
if($result.task_register -notlike 'PASS_*' -or $result.snapshot -ne 'PASS_10_BRANCHES'){exit 2}