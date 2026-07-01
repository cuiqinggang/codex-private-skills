param(
  [ValidateSet('Approval','Auto','ReportOnly')]
  [string]$Mode = 'Approval'
)

$ErrorActionPreference = 'Stop'
$TaskName = 'Codex_SystemEvolution_2h'
$Runner = 'C:\Users\A\.codex\skills\system-evolution\scripts\run-system-evolution.ps1'
if (-not (Test-Path $Runner)) { throw "Runner missing: $Runner" }

$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Runner`" -Mode $Mode"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration (New-TimeSpan -Days 3650)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -StartWhenAvailable
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
Write-Output "REGISTERED $TaskName Mode=$Mode"
