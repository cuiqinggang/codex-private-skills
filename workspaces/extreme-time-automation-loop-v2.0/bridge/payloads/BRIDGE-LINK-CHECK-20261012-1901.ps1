param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference = 'Stop'
Write-Output 'GH_TO_WINDOWS_REALITY_PROBE_PASS'
Write-Output ('PROBE_ID=BRIDGE-LINK-CHECK-20261012-1901')
Write-Output ('WINDOWS_HOST=' + $env:COMPUTERNAME)
Write-Output ('RUNNER_NAME=' + $env:RUNNER_NAME)
Write-Output ('WINDOWS_IDENTITY=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name)
$services = @(Get-CimInstance Win32_Service | Where-Object { $_.Name -like 'actions.runner.cuiqinggang-codex-private-skills*' })
foreach ($s in $services) { Write-Output ('RUNNER_SERVICE=' + $s.State + ';STARTMODE=' + $s.StartMode) }
$listener = @(Get-Process -Name 'Runner.Listener' -ErrorAction SilentlyContinue)
Write-Output ('RUNNER_LISTENER_COUNT=' + $listener.Count)
$tunnelId='tunnel_6acbeee2ce888191b775cd53429c7597'
$tunnels = @(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'" | Where-Object { $_.CommandLine -like "*$tunnelId*" })
Write-Output ('OPENAI_TUNNEL_MATCH_COUNT=' + $tunnels.Count)
Write-Output ('OPENAI_TUNNEL_PID=' + ($tunnels.ProcessId -join ','))
Write-Output ('PROBE_UTC=' + [DateTime]::UtcNow.ToString('o'))
exit 0
