$ErrorActionPreference = 'Stop'
$tunnelId = 'tunnel_6acbeee2ce888191b775cd53429c7597'
$launcher = 'C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1'
$probe = 'C:\AI\GPT-Windows-Bridge-B\persistence\Watch-Tunnel-Health.ps1'
$all = @(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
$existing = @($all | Where-Object { ([string]$_.CommandLine).Contains($tunnelId) })
if ($all.Count -gt 0) {
    if ($all.Count -ne 1 -or !(Test-Path -LiteralPath $probe)) {
        Write-Warning 'Tunnel identity uncertain; refusing a duplicate start.'
        if ([Environment]::UserInteractive) { [void](Read-Host 'Press Enter to close') }
        exit 2
    }
    $firstPid = [int]$all[0].ProcessId
    $deadline = (Get-Date).AddSeconds(180)
    Write-Host 'Checking the existing tunnel; it may still be initializing. No second instance will start.'
    while ($true) {
        $now = @(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
        if ($now.Count -ne 1 -or [int]$now[0].ProcessId -ne $firstPid) {
            Write-Warning 'Tunnel process changed during readiness check; refusing a duplicate start.'
            break
        }
        try { $state = (& $probe | Select-Object -Last 1 | ConvertFrom-Json) }
        catch { Write-Warning 'Tunnel health probe failed; no new process will be started.'; break }
        if ([int]$state.pid -ne $firstPid -or [int]$state.clients -ne 1) {
            Write-Warning 'Probe identity changed or cannot be verified; no new process will be started.'
            break
        }
        if ($state.state -in @('HEALTHY','HEALTHY_PATH_ONLY')) {
            Write-Host ('Existing tunnel ready: '+$state.state+'; PID: '+$firstPid)
            Write-Host 'MCP is healthy. The tunnel remains active independently of this window.'
            Write-Host 'This is a status window only. No second instance was started.'
            if ([Environment]::UserInteractive) {
                try { [void](Read-Host 'Status HEALTHY. Press Enter to close this status window') }
                catch { Write-Host 'Interactive input unavailable; tunnel remains running.' }
            }
            exit 0
        }
        if ($state.state -notin @('MCP_NOT_INITIALIZED','NOT_READY')) {
            Write-Warning ('Tunnel requires diagnosis: '+$state.state+'; PID: '+$firstPid)
            break
        }
        if ((Get-Date) -ge $deadline) {
            Write-Warning ('Initialization still pending after 180 seconds; PID: '+$firstPid)
            break
        }
        Write-Host ('Waiting for existing MCP initialization; PID: '+$firstPid)
        Start-Sleep -Seconds 5
    }
    Write-Warning 'No duplicate tunnel was started. Keep this result visible for diagnosis.'
    if ([Environment]::UserInteractive) { [void](Read-Host 'Press Enter to close') }
    exit 2
}
if (!(Test-Path -LiteralPath $launcher)) { throw "Launcher missing: $launcher" }
Write-Host 'No tunnel-client process found. Starting the existing interactive launcher.'
Write-Host 'Enter the existing Runtime API key locally; never paste it into ChatGPT.'
& $launcher -Launch