param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
Write-Output 'WINDOWS_TUNNEL_PREFLIGHT_R2_PASS'
Write-Output ('HOST='+$env:COMPUTERNAME)
Write-Output ('IDENTITY='+[Security.Principal.WindowsIdentity]::GetCurrent().Name)
$root='C:\AI\GPT-Windows-Bridge-B'
$items=@(
 (Join-Path $root 'Launch-OpenAI-Real-MCP.ps1'),
 (Join-Path $root 'tunnel\v0.0.16\tunnel-client.exe'),
 (Join-Path $root 'mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js'),
 (Join-Path $root 'persistence\Restore-Interactive.ps1'),
 (Join-Path $root 'persistence\Show-Current-Tunnel-Console.ps1')
)
foreach($f in $items){
 $isHere=Test-Path -LiteralPath $f -ErrorAction Stop
 Write-Output ('EXISTS='+$isHere+';FILE='+$f)
 if(!$isHere){throw ('MISSING_LAUNCH_COMPONENT='+$f)}
 if($f.EndsWith('.ps1')){$tok=$null;$err=$null;[void][System.Management.Automation.Language.Parser]::ParseFile($f,[ref]$tok,[ref]$err);Write-Output ('PARSE_ERRORS='+$err.Count+';FILE='+$f);if($err.Count -ne 0){throw 'PARSE_FAILURE'}}
}
Write-Output 'USER_A_DESKTOP_NOT_CHECKED_NETWORK_SERVICE_ACCESS_DENIED'
$all=@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
Write-Output ('TOTAL_TUNNEL_CLIENTS='+$all.Count)
$target='tunnel_6acbeee2ce888191b775cd53429c7597'
$matching=@($all | Where-Object {$_.CommandLine -like "*$target*"})
Write-Output ('EXPECTED_TUNNEL_COUNT='+$matching.Count)
Write-Output ('EXPECTED_TUNNEL_PIDS='+($matching.ProcessId -join ','))
Write-Output ('OLD_POWERSHELL_PID_27920_ALIVE='+[bool](Get-Process -Id 27920 -ErrorAction SilentlyContinue))
$svc=@(Get-CimInstance Win32_Service | Where-Object {$_.Name -like 'actions.runner.cuiqinggang*'})
foreach($s in $svc){Write-Output ('RUNNER_SERVICE='+$s.State+';STARTMODE='+$s.StartMode)}
Write-Output 'PREFLIGHT_R2_READ_ONLY_COMPLETE'
exit 0
