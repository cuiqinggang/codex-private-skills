param(
  [string]$TaskName = 'CodexChaosNormalizerDaily',
  [string]$DailyAt = '10:00',
  [int]$DaysInterval = 1,
${REDACTED_SECRET}
${REDACTED_SECRET}
)

$ErrorActionPreference = 'Stop'
if ($DaysInterval -lt 1) {
  throw 'DaysInterval must be 1 or greater.'
}

$script = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) 'run-codex-chaos-maintenance.ps1'
if (-not (Test-Path -LiteralPath $script)) {
  throw "Missing maintenance script: $script"
}

$time = [datetime]::ParseExact($DailyAt, 'HH:mm', [Globalization.CultureInfo]::InvariantCulture)
$actionArgs = @(
  '-NoProfile',
  '-ExecutionPolicy', 'Bypass',
  '-File', "`"$script`"",
  '-Workspace', "`"$Workspace`"",
  '-CodexHome', "`"$CodexHome`""
) -join ' '

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $actionArgs
$trigger = New-ScheduledTaskTrigger -Daily -At $time
if ($DaysInterval -gt 1) {
  $trigger.DaysInterval = $DaysInterval
}
$settings = New-ScheduledTaskSettingsSet `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries `
  -StartWhenAvailable `
  -MultipleInstances IgnoreNew `
  -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null

$task = Get-ScheduledTask -TaskName $TaskName
$info = Get-ScheduledTaskInfo -TaskName $TaskName
[pscustomobject]@{
  TaskName = $task.TaskName
  State = $task.State
  DailyAt = $DailyAt
  DaysInterval = $DaysInterval
  NextRunTime = $info.NextRunTime
  Action = $action.Execute
  Arguments = $action.Arguments
}
