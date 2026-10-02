param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)
$ErrorActionPreference='Continue'
Write-Output ('IDENTITY=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name)
Write-Output ('INTERACTIVE_USER=' + (Get-CimInstance Win32_ComputerSystem).UserName)
Write-Output ('NOW=' + (Get-Date).ToString('o'))
$ev='C:\AI\DCR-PROCESS-RECONNECT-R12.json'
Write-Output ('R12_EVIDENCE_EXISTS=' + (Test-Path -LiteralPath $ev))
if(Test-Path -LiteralPath $ev){
  Write-Output '---R12_EVIDENCE---'
  Get-Content -LiteralPath $ev -Raw
}
Write-Output '---DCR_PROCESSES---'
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -match '(?i)desktop-commander|Start-DesktopCommanderRemote' } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine |
  ConvertTo-Json -Depth 4
Write-Output '---WATCHDOG_28868---'
Get-CimInstance Win32_Process -Filter 'ProcessId=28868' -ErrorAction SilentlyContinue |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine |
  ConvertTo-Json -Depth 4
Write-Output '---SCHEDULED_TASK---'
try {
  Get-ScheduledTask -TaskName 'GPT-DesktopCommander-Remote-Autostart' -ErrorAction Stop |
    Select-Object TaskName,State,TaskPath |
    ConvertTo-Json -Depth 4
} catch {
  Write-Output ('TASK_QUERY_ERROR=' + $_.Exception.Message)
}
$startup='C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\GPT-DesktopCommander-Remote-Autostart.cmd'
Write-Output ('STARTUP_ENTRY_EXISTS=' + (Test-Path -LiteralPath $startup))
$launcher='C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1'
Write-Output ('USER_LAUNCHER_EXISTS=' + (Test-Path -LiteralPath $launcher))
if(Test-Path -LiteralPath $launcher){
  Write-Output '---USER_LAUNCHER---'
  Get-Content -LiteralPath $launcher -Raw
}
Write-Output '---RUNNER_SERVICE---'
Get-Service | Where-Object {$_.Name -like '*actions.runner*'} |
  Select-Object Name,Status,StartType |
  ConvertTo-Json -Depth 4
exit 0
