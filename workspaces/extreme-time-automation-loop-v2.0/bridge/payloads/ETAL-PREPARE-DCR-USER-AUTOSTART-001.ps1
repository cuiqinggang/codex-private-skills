param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)

$ErrorActionPreference='Stop'
$root='C:\actions-runner-etal\_local-tools\DesktopCommanderRemote'
New-Item -ItemType Directory -Path $root -Force | Out-Null

$launcher=Join-Path $root 'Start-DesktopCommanderRemote.ps1'
$installer=Join-Path $root 'Install-Autostart-ForCurrentUser.ps1'

$launcherLines=@(
  "$" + "ErrorActionPreference='Continue'",
  "$" + "profile=[Environment]::GetFolderPath('UserProfile')",
  "$" + "env:USERPROFILE=$" + "profile",
  "$" + "HOME=$" + "profile",
  "$" + "npx=(Get-Command npx.cmd -ErrorAction Stop).Source",
  "$" + "log='C:\actions-runner-etal\_local-tools\DesktopCommanderRemote\remote.log'",
  "while ($" + "true) {",
  "  try { & $" + "npx -y '@wonderwhy-er/desktop-commander@latest' remote *>> $" + "log } catch { }",
  "  Start-Sleep -Seconds 5",
  "}"
)
Set-Content -LiteralPath $launcher -Value $launcherLines -Encoding UTF8

$installerLines=@(
  "$" + "ErrorActionPreference='Stop'",
  "$" + "taskName='GPT-DesktopCommander-Remote-Autostart'",
  "$" + "root='C:\actions-runner-etal\_local-tools\DesktopCommanderRemote'",
  "$" + "launcher=Join-Path $" + "root 'Start-DesktopCommanderRemote.ps1'",
  "$" + "user=[Security.Principal.WindowsIdentity]::GetCurrent().Name",
  "$" + "profile=[Environment]::GetFolderPath('UserProfile')",
  "$" + "session=Join-Path $" + "profile '.desktop-commander-device\device.json'",
  "if (-not (Test-Path -LiteralPath $" + "session)) { throw 'PERSISTED_DESKTOP_COMMANDER_SESSION_NOT_FOUND' }",
  "$" + "action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""'+$" + "launcher+'""')",
  "$" + "trigger=New-ScheduledTaskTrigger -AtLogOn -User $" + "user",
  "$" + "principal=New-ScheduledTaskPrincipal -UserId $" + "user -LogonType Interactive -RunLevel Limited",
  "$" + "settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable",
  "Register-ScheduledTask -TaskName $" + "taskName -Action $" + "action -Trigger $" + "trigger -Principal $" + "principal -Settings $" + "settings -Force | Out-Null",
  "Start-ScheduledTask -TaskName $" + "taskName",
  "Start-Sleep -Seconds 10",
  "$" + "task=Get-ScheduledTask -TaskName $" + "taskName",
  "Write-Output 'DCR_AUTOSTART=CONFIGURED'",
  "Write-Output ('TASK_NAME='+$" + "taskName)",
  "Write-Output ('TASK_STATE='+$" + "task.State)",
  "Write-Output ('USER='+$" + "user)"
)
Set-Content -LiteralPath $installer -Value $installerLines -Encoding UTF8

Write-Output "DCR_USER_INSTALLER_PREPARED=YES"
Write-Output "INSTALLER=$installer"
Write-Output "LAUNCHER=$launcher"
