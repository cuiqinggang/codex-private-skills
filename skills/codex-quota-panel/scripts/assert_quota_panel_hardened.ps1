param(
    [string]$RuntimeDir = "$env:USERPROFILE\.codex\quota-panel"
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Parent = Split-Path -Parent $Here
${REDACTED_SECRET}
$Problems = New-Object System.Collections.Generic.List[string]

function Add-Problem($Message) {
    $Problems.Add($Message) | Out-Null
}

function Test-FileContains($Path, $Pattern) {
    if (-not (Test-Path $Path)) {
        Add-Problem "Missing file: $Path"
        return $false
    }
    return [bool](Select-String -Path $Path -Pattern $Pattern -Quiet)
}

$runtimePanel = Join-Path $RuntimeDir "CodexQuotaPanel.ps1"
$runtimeLauncher = Join-Path $RuntimeDir "Start-CodexQuotaPanel.cmd"
$runtimeHiddenLauncher = Join-Path $RuntimeDir "Start-CodexQuotaPanel-Hidden.vbs"
$runtimeWatchdog = Join-Path $RuntimeDir "QuotaPanelWatchdog.ps1"
$runtimeSelfHeal = Join-Path $RuntimeDir "QuotaPanelSelfHeal.ps1"
$runtimeInstaller = Join-Path $RuntimeDir "install_or_repair_quota_panel.ps1"
$skillPanel = Join-Path $SkillDir "scripts\CodexQuotaPanel.ps1"
$skillLauncher = Join-Path $SkillDir "scripts\Start-CodexQuotaPanel.cmd"
$skillWatchdog = Join-Path $SkillDir "scripts\QuotaPanelWatchdog.ps1"
$skillSelfHeal = Join-Path $SkillDir "scripts\QuotaPanelSelfHeal.ps1"
$skillInstaller = Join-Path $SkillDir "scripts\install_or_repair_quota_panel.ps1"

if (Test-Path $runtimeHiddenLauncher) {
    Add-Problem "Obsolete hidden launcher still present: $runtimeHiddenLauncher"
}

foreach ($path in @($runtimeLauncher, $skillLauncher, $runtimeWatchdog, $skillWatchdog, $runtimeInstaller, $skillInstaller)) {
    if (Test-Path $path) {
        $content = Get-Content -Raw $path
        if ($path -notlike "*QuotaPanelWatchdog.ps1" -and ($content -match "CodexQuotaPanel\.ps1.*WindowStyle\s+Hidden|WindowStyle\s+Hidden.*CodexQuotaPanel\.ps1|/min.*CodexQuotaPanel\.ps1|CodexQuotaPanel\.ps1.*/min")) {
            Add-Problem "Panel launch hidden/minimized in: $path"
        }
        if ($path -like "*QuotaPanelWatchdog.ps1" -and $content -match "CodexQuotaPanel\.ps1.*WindowStyle\s+Hidden|WindowStyle\s+Hidden.*CodexQuotaPanel\.ps1") {
            Add-Problem "Watchdog restarts panel hidden in: $path"
        }
    } else {
        Add-Problem "Missing file: $path"
    }
}

foreach ($path in @($runtimeLauncher, $skillLauncher)) {
    if (Test-Path $path) {
        $content = Get-Content -Raw $path
        if ($content -notmatch "CodexQuotaPanel\.ps1") {
            Add-Problem "Startup launcher does not start the visible panel: $path"
        }
        if ($content -notmatch "QuotaPanelWatchdog\.ps1") {
            Add-Problem "Startup launcher does not start the watchdog: $path"
        }
    }
}

foreach ($path in @($runtimePanel, $skillPanel)) {
    if (Test-Path $path) {
        $content = Get-Content -Raw $path
        if ($content -notmatch "LastGoodMaxAgeMinutes\s*=\s*10") { Add-Problem "Missing 10-minute cache limit in: $path" }
        if ($content -notmatch "Interval\s*=\s*180000") { Add-Problem "Missing 3-minute refresh interval in: $path" }
        if ($content -notmatch 'for\s*\(\$attempt\s*=\s*1;\s*\$attempt\s*-le\s*3') { Add-Problem "Missing 3-attempt cclimits retry in: $path" }
        if ($content -notmatch "CclimitsTimeoutSeconds\s*=\s*20" -or $content -notmatch "WaitForExit") { Add-Problem "Missing bounded cclimits timeout in: $path" }
        if ($content -notmatch "taskkill\.exe" -or $content -notmatch "codex-quota-panel-") { Add-Problem "Missing robust timeout tree-kill/temp-output cclimits guard in: $path" }
        if ($content -notmatch "Show-StartupFallback") { Add-Problem "Missing visible startup fallback in: $path" }
        if ($content -notmatch "Hide-HostConsole" -or $content -notmatch "GetConsoleWindow" -or $content -notmatch "ShowWindow") { Add-Problem "Missing host-console hide guard in: $path" }
        if ($content -notmatch "AllowExpired") { Add-Problem "Missing stale cache fallback policy in: $path" }
        if ($content -match "0x65E7|oldPrefix") { Add-Problem "Visible stale prefix can reintroduce the old marker in: $path" }
        if ($content -match "quota refresh\.\.\.") { Add-Problem "Non-quota visible refresh text still present in: $path" }
    } else {
        Add-Problem "Missing file: $path"
    }
}

foreach ($path in @($runtimeSelfHeal, $skillSelfHeal)) {
    if (Test-Path $path) {
        $content = Get-Content -Raw $path
        if ($content -notmatch "MaxLastGoodAgeMinutes\s*=\s*10") { Add-Problem "Self-heal missing 10-minute stale threshold in: $path" }
        if ($content -notmatch "taskkill\.exe") { Add-Problem "Self-heal missing stale process tree kill in: $path" }
        if ($content -notmatch "Restart-QuotaPanel") { Add-Problem "Self-heal missing panel restart in: $path" }
    } else {
        Add-Problem "Missing self-heal script: $path"
    }
}

foreach ($path in @($runtimeInstaller, $skillInstaller)) {
    if (Test-Path $path) {
        $content = Get-Content -Raw $path
        if ($content -notmatch "CodexQuotaPanelSelfHeal") { Add-Problem "Installer does not register self-heal scheduled task: $path" }
        if ($content -notmatch "QuotaPanelSelfHeal\.ps1") { Add-Problem "Installer does not deploy self-heal script: $path" }
        if ($content -notmatch "ExecutionTimeLimit" -or $content -notmatch "MultipleInstances\s+IgnoreNew") { Add-Problem "Installer does not bound/non-reenter self-heal scheduled task: $path" }
        if ($content -notmatch "Start-CodexQuotaPanel-Hidden\.vbs") { Add-Problem "Installer does not remove obsolete hidden launcher: $path" }
    }
}

$task = Get-ScheduledTask -TaskName "CodexQuotaPanelSelfHeal" -ErrorAction SilentlyContinue
if (-not $task) {
    Add-Problem "Missing Windows scheduled task: CodexQuotaPanelSelfHeal"
} else {
    if ($task.State -eq "Disabled") { Add-Problem "Self-heal scheduled task is disabled" }
    if ($task.Settings.ExecutionTimeLimit -ne "PT2M") { Add-Problem "Self-heal scheduled task missing 2-minute execution limit" }
    if ($task.Settings.MultipleInstances -ne "IgnoreNew") { Add-Problem "Self-heal scheduled task missing IgnoreNew multiple-instance policy" }
}

$startup = [Environment]::GetFolderPath("Startup")
$shortcut = Join-Path $startup "Codex Quota Panel.lnk"
if (Test-Path $shortcut) {
    $shell = New-Object -ComObject WScript.Shell
    $s = $shell.CreateShortcut($shortcut)
    $expected = Join-Path $RuntimeDir "Start-CodexQuotaPanel.cmd"
    if ($s.TargetPath -ne $expected) {
        Add-Problem "Startup shortcut target mismatch: $($s.TargetPath)"
    }
} else {
    Add-Problem "Missing startup shortcut: $shortcut"
}

if ($Problems.Count -gt 0) {
    $Problems | ForEach-Object { Write-Output "FAIL: $_" }
    exit 1
}

Write-Output "PASS: quota panel hardened"
