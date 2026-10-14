$ErrorActionPreference = 'Stop'
$tunnelId = 'tunnel_6acbeee2ce888191b775cd53429c7597'
$launcher = 'C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1'
$probe = 'C:\AI\GPT-Windows-Bridge-B\persistence\Watch-Tunnel-Health.ps1'
$all = @(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
$existing = @($all | Where-Object { ([string]$_.CommandLine).Contains($tunnelId) })
if ($all.Count -gt 0) {
    if ($all.Count -ne 1 -or !(Test-Path -LiteralPath $probe)) {
        Write-Warning 'Tunnel process identity uncertain; refusing duplicate launch.'
        Start-Sleep -Seconds 2; exit 2
    }
    try { $state = (& $probe | Select-Object -Last 1 | ConvertFrom-Json) }
    catch { Write-Warning 'Health probe failed; refusing duplicate launch.'; Start-Sleep -Seconds 2; exit 2 }
    Write-Host ('Tunnel health: ' + $state.state + '; PID: ' + $state.pid)
    if ($state.state -in @('HEALTHY','HEALTHY_PATH_ONLY')) {
        if ($state.state -eq 'HEALTHY_PATH_ONLY') {
            Write-Warning 'Limited rights: Tunnel ID not independently verified.'
        }
        Write-Host 'Tunnel process is already running; no second instance will start.'
        Start-Sleep -Seconds 2; exit 0
    }
    Write-Warning ('Unhealthy or unverified tunnel: ' + $state.state + '. Do not start another instance.')
    Start-Sleep -Seconds 2; exit 2
}
if (!(Test-Path -LiteralPath $launcher)) { throw "Launcher missing: $launcher" }
Write-Host 'No tunnel-client process found. Starting the existing interactive launcher.'
Write-Host 'Enter the existing Runtime API key locally; never paste it into ChatGPT.'
& $launcher -Launch