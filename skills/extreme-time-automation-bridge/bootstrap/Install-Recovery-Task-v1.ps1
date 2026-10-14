$ErrorActionPreference='Stop'
$taskName='GPT-Windows-Tunnel-Recovery-v1'
$root='C:\AI\GPT-Windows-Bridge-B'
$supervisor=Join-Path $root 'persistence\Recovery-Supervisor-v1.ps1'
if(!(Test-Path -LiteralPath $supervisor)){throw 'SUPERVISOR_NOT_FOUND'}
$tokens=$null;$errors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($supervisor,[ref]$tokens,[ref]$errors)
if($errors.Count){throw ('SUPERVISOR_SYNTAX_INVALID='+$errors.Count)}
if(Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue){throw 'TASK_ALREADY_EXISTS_DO_NOT_OVERWRITE'}
$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
$action=New-ScheduledTaskAction -Execute "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument ('-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File "'+$supervisor+'"')
$logon=New-ScheduledTaskTrigger -AtLogOn -User $user
$repeat=New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(2)) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
$principal=New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($logon,$repeat) -Settings $settings -Principal $principal -Description 'Native Windows logon and repeating recovery supervisor; one official tunnel only; user-scope DPAPI key; no proxy changes.' -ErrorAction Stop | Out-Null
Start-ScheduledTask -TaskName $taskName -ErrorAction Stop
$task=Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
'RECOVERY_TASK_INSTALLED='+$task.TaskName
'RECOVERY_TASK_STATE='+$task.State
'USER='+$user
'CURRENT_TUNNEL_COUNT='+@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'").Count
'NO_SECRET_READ=TRUE'
