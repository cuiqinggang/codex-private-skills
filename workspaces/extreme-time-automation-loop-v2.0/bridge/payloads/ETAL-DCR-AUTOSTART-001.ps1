param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)

$ErrorActionPreference='Stop'
$taskName='GPT-DesktopCommander-Remote-Autostart'
$root=Join-Path $env:LOCALAPPDATA 'DesktopCommanderRemote'
$launcher=Join-Path $root 'Start-DesktopCommanderRemote.ps1'
$log=Join-Path $root 'remote.log'
$session=Join-Path $HOME '.desktop-commander-device\device.json'

$npx=(Get-Command npx.cmd -ErrorAction Stop).Source
New-Item -ItemType Directory -Path $root -Force | Out-Null

$escapedNpx=$npx.Replace("'","''")
$escapedLog=$log.Replace("'","''")
$launcherLines=@(
  "$" + "ErrorActionPreference='Continue'",
  "$" + "npx='" + $escapedNpx + "'",
  "$" + "log='" + $escapedLog + "'",
  "& $" + "npx -y '@wonderwhy-er/desktop-commander@latest' remote *>> $" + "log",
  "exit $" + "LASTEXITCODE"
)
Set-Content -LiteralPath $launcher -Value $launcherLines -Encoding UTF8

$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "'+$launcher+'"')
$trigger=New-ScheduledTaskTrigger -AtLogOn -User $user
$principal=New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
try { Start-ScheduledTask -TaskName $taskName -ErrorAction Stop } catch {}

Start-Sleep -Seconds 12
$task=Get-ScheduledTask -TaskName $taskName
$proc=@(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
  $_.CommandLine -match '(?i)desktop-commander' -and $_.CommandLine -match '(?i)remote'
})

[ordered]@{
  status='DCR_AUTOSTART_CONFIGURED'
  task_name=$taskName
  task_state=$task.State.ToString()
  user=$user
  launcher=$launcher
  session_file_exists=(Test-Path -LiteralPath $session)
  matching_processes=$proc.Count
  process_ids=@($proc | ForEach-Object {$_.ProcessId})
  log=$log
  proxy_modified=$false
} | ConvertTo-Json -Depth 5
