param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)
$ErrorActionPreference='Continue'
Write-Output ('IDENTITY=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name)
Write-Output ('INTERACTIVE_USER=' + (Get-CimInstance Win32_ComputerSystem).UserName)
Write-Output ('NOW=' + (Get-Date).ToString('o'))
Write-Output '---TASK---'
try {
  $t=Get-ScheduledTask -TaskName 'GPT-DesktopCommander-Remote-Autostart' -ErrorAction Stop
  $t | Select-Object TaskName,State,TaskPath,
    @{N='Actions';E={($_.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }) -join ' | '}},
    @{N='PrincipalUser';E={$_.Principal.UserId}},
    @{N='LogonType';E={$_.Principal.LogonType}} |
    ConvertTo-Json -Depth 5
  Get-ScheduledTaskInfo -TaskName 'GPT-DesktopCommander-Remote-Autostart' |
    Select-Object LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns |
    ConvertTo-Json -Depth 4
} catch {
  Write-Output ('TASK_ERROR=' + $_.Exception.Message)
}
$paths=@(
 'C:\actions-runner-etal\_local-tools\DesktopCommanderRemote\remote.log',
 'C:\actions-runner-etal\_local-tools\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1'
)
foreach($p in $paths){
  Write-Output ('---PATH '+$p+' EXISTS='+(Test-Path -LiteralPath $p)+'---')
  if(Test-Path -LiteralPath $p){
    if($p -like '*.log'){ Get-Content -LiteralPath $p -Tail 120 -ErrorAction Continue }
    else { Get-Content -LiteralPath $p -Raw -ErrorAction Continue }
  }
}
Write-Output '---NODE_POWERSHELL_PROCS---'
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -in @('node.exe','powershell.exe','pwsh.exe','cmd.exe') } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine |
  ConvertTo-Json -Depth 4
exit 0
