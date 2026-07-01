$ErrorActionPreference = "SilentlyContinue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Panel = Join-Path $Root "CodexQuotaPanel.ps1"
$Log = Join-Path $Root "quota-panel.log"

function Write-WatchdogLog($Message) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $Log -Value "$stamp watchdog: $Message" -Encoding UTF8
}

Write-WatchdogLog "started"

while ($true) {
    $panelProcess = Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -like "*CodexQuotaPanel.ps1*" -and
            $_.CommandLine -notlike "*QuotaPanelWatchdog.ps1*"
        } |
        Select-Object -First 1

    if (-not $panelProcess) {
        Write-WatchdogLog "panel missing; restarting"
        Start-Process powershell.exe -ArgumentList "-STA","-NoProfile","-ExecutionPolicy","Bypass","-File",$Panel
    }

    Start-Sleep -Seconds 60
}
