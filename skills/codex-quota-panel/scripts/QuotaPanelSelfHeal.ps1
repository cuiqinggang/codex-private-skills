param(
    [string]$RuntimeDir = "$env:USERPROFILE\.codex\quota-panel"
)

$ErrorActionPreference = "SilentlyContinue"
$Root = $RuntimeDir
${REDACTED_SECRET}
$Checker = Join-Path $Root "cclimits.py"
$Panel = Join-Path $Root "CodexQuotaPanel.ps1"
$Watchdog = Join-Path $Root "QuotaPanelWatchdog.ps1"
$Log = Join-Path $Root "quota-panel.log"
$LastGoodFile = Join-Path $Root "quota-panel-last-good.txt"
$TimeoutSeconds = 25
$MaxLastGoodAgeMinutes = 10

function Write-HealLog($Message) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $Log -Value "$stamp selfheal: $Message" -Encoding UTF8
}

function Stop-OldQuotaChildren {
    $cutoff = (Get-Date).AddMinutes(-2)
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -like "*cclimits.py*--codex*--json*" -and
            $_.CreationDate -lt $cutoff
        } |
        ForEach-Object {
            Write-HealLog "killing stale cclimits tree pid=$($_.ProcessId)"
            try { & taskkill.exe /PID $_.ProcessId /T /F | Out-Null } catch {}
        }
}

function Invoke-LiveQuotaJson {
    $stamp = [guid]::NewGuid().ToString("N")
    $stdoutPath = Join-Path $env:TEMP "codex-quota-selfheal-$stamp.out"
    $stderrPath = Join-Path $env:TEMP "codex-quota-selfheal-$stamp.err"
    try {
        $proc = Start-Process -FilePath $Python -ArgumentList @($Checker, "--codex", "--json") -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -WindowStyle Hidden -PassThru
        if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
            try { & taskkill.exe /PID $proc.Id /T /F | Out-Null } catch {}
            return [pscustomobject]@{ Ok = $false; Text = $null; Reason = "timeout after ${TimeoutSeconds}s" }
        }
        $output = if (Test-Path $stdoutPath) { Get-Content -Raw -Encoding UTF8 $stdoutPath } else { $null }
        $errorText = if (Test-Path $stderrPath) { Get-Content -Raw -Encoding UTF8 $stderrPath } else { $null }
        if (-not $output) {
            $reason = if ($errorText) { $errorText.Trim() } else { "no output" }
            return [pscustomobject]@{ Ok = $false; Text = $null; Reason = $reason }
        }
        $data = $output | ConvertFrom-Json
        $codex = $data.codex
        if (-not $codex -or $codex.status -ne "ok") {
            $reason = if ($codex -and $codex.error) { $codex.error } else { "status not ok" }
            return [pscustomobject]@{ Ok = $false; Text = $null; Reason = $reason }
        }

        $pReset = Convert-ResetClock $codex.primary_window.resets_in
        $sReset = Convert-ResetText $codex.secondary_window.resets_in
        $tian = [string][char]0x5929
        $text = "$($codex.primary_window.remaining) $pReset | 7$tian$($codex.secondary_window.remaining) $sReset"
        return [pscustomobject]@{ Ok = $true; Text = $text; Reason = "ok" }
    } catch {
        return [pscustomobject]@{ Ok = $false; Text = $null; Reason = $_.Exception.Message }
    } finally {
        Remove-Item -LiteralPath $stdoutPath,$stderrPath -Force -ErrorAction SilentlyContinue
    }
}

function Convert-ResetText($Text) {
    $wei = [string][char]0x672A
    $zhi = [string][char]0x77E5
    if (-not $Text) { return "$wei$zhi" }
    $tian = [string][char]0x5929
    $shi = [string][char]0x65F6
    $fen = [string][char]0x5206
    return ($Text -replace "\s+", "" -replace "d", $tian -replace "h", $shi -replace "m", $fen)
}

function Convert-ResetClock($Text) {
    if (-not $Text) { return "--:--" }
    $totalMinutes = 0
    if ($Text -match "(\d+)d") { $totalMinutes += [int]$Matches[1] * 24 * 60 }
    if ($Text -match "(\d+)h") { $totalMinutes += [int]$Matches[1] * 60 }
    if ($Text -match "(\d+)m") { $totalMinutes += [int]$Matches[1] }
    if ($totalMinutes -le 0) { return "00:00" }
    $hours = [math]::Floor($totalMinutes / 60)
    $minutes = $totalMinutes % 60
    return ("{0:00}:{1:00}" -f $hours, $minutes)
}

function Restart-QuotaPanel {
    Get-CimInstance Win32_Process |
        Where-Object { $_.CommandLine -like "*CodexQuotaPanel.ps1*" -and $_.ProcessId -ne $PID } |
        ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    Start-Process powershell.exe -ArgumentList "-STA","-NoProfile","-ExecutionPolicy","Bypass","-File",$Panel

    $watchdogProcess = Get-CimInstance Win32_Process |
        Where-Object { $_.CommandLine -like "*QuotaPanelWatchdog.ps1*" } |
        Select-Object -First 1
    if (-not $watchdogProcess) {
        Start-Process powershell.exe -WindowStyle Hidden -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File",$Watchdog
    }
}

New-Item -ItemType Directory -Force -Path $Root | Out-Null
Stop-OldQuotaChildren

$lastGoodAge = 999999
if (Test-Path $LastGoodFile) {
    $lastGoodAge = ((Get-Date) - (Get-Item $LastGoodFile).LastWriteTime).TotalMinutes
}

$panelProcess = Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -like "*CodexQuotaPanel.ps1*" -and $_.CommandLine -notlike "*QuotaPanelWatchdog.ps1*" } |
    Select-Object -First 1

if (-not $panelProcess -or $lastGoodAge -gt $MaxLastGoodAgeMinutes) {
    $live = Invoke-LiveQuotaJson
    if ($live.Ok) {
        Set-Content -Path $LastGoodFile -Value $live.Text -Encoding UTF8
        Write-HealLog "live quota ok; cache refreshed: $($live.Text)"
        Restart-QuotaPanel
        Write-HealLog "panel restarted after stale/missing check"
    } else {
        Write-HealLog "live quota unavailable; no restart loop: $($live.Reason)"
        if (-not $panelProcess) { Restart-QuotaPanel; Write-HealLog "panel restarted because missing" }
    }
} else {
    Write-HealLog "healthy; last good age=$([int]$lastGoodAge)m"
}
