param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
Write-Output 'WINDOWS_TUNNEL_PREFLIGHT_20261012'
Write-Output ('HOST='+$env:COMPUTERNAME)
Write-Output ('IDENTITY='+[Security.Principal.WindowsIdentity]::GetCurrent().Name)
Write-Output ('BOOT='+((Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('o')))
$root='C:\AI\GPT-Windows-Bridge-B'
$items=@(
  (Join-Path $root 'Launch-OpenAI-Real-MCP.ps1'),
  (Join-Path $root 'tunnel\v0.0.16\tunnel-client.exe'),
  (Join-Path $root 'mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js'),
  (Join-Path $root 'persistence\Restore-Interactive.ps1'),
  (Join-Path $root 'persistence\Show-Current-Tunnel-Console.ps1'),
  'C:\Users\A\Desktop\GPT-Windows-MCP-一键恢复.lnk',
  'C:\Users\A\Desktop\GPT-Windows-MCP-Show-Console.lnk')
foreach($f in $items) {
  $present=Test-Path -LiteralPath $f
  Write-Output ('EXISTS='+$present+';FILE='+$f)
  if($present -and $f.EndsWith('.ps1')) {
     $tk=$null;$er=$null
     [void][System.Management.Automation.Language.Parser]::ParseFile($f,[ref]$tk,[ref]$er)
     Write-Output ('SCRIPT_PARSE_ERRORS='+$er.Count+';FILE='+$f)
  }
}
$all=@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
Write-Output ('ALL_TUNNEL_CLIENTS='+$all.Count)
$id='tunnel_6acbeee2ce888191b775cd53429c7597'
$matching=@($all|Where-Object {$_.CommandLine -like "*$id*"})
Write-Output ('EXPECTED_TUNNEL_COUNT='+$matching.Count)
Write-Output ('OLD_PARENT_POWER_SHELL_PID27920_EXISTS='+[bool](Get-Process -Id 27920 -ErrorAction SilentlyContinue))
$t=@(Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -eq 'GPT-Windows-Tunnel-Autostart'})
Write-Output ('TUNNEL_AUTOSTART_TASK_COUNT='+$t.Count)
$s=@(Get-CimInstance Win32_Service | Where-Object {$_.Name -like 'actions.runner.cuiqinggang*'})
foreach($v in $s){Write-Output ('GH_SERVICE='+$v.State+';MODE='+$v.StartMode)}
Write-Output 'PREFLIGHT_READ_ONLY_COMPLETE'
exit 0
