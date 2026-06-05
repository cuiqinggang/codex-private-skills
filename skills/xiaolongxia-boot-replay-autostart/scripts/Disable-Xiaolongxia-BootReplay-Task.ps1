$ErrorActionPreference = 'Stop'
$taskName = 'Xiaolongxia_BootReplay_Logon'
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
  Disable-ScheduledTask -TaskName $taskName | Out-Null
  Write-Output "$taskName disabled"
} else {
  Write-Output "$taskName not found"
}
