param(
    [string]$RuntimeDir = "$env:USERPROFILE\.codex\quota-panel"
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $Here
$SourceDir = if (Test-Path (Join-Path $SkillDir "scripts\CodexQuotaPanel.ps1")) { Join-Path $SkillDir "scripts" } else { $Here }
$ScriptSource = Join-Path $SourceDir "CodexQuotaPanel.ps1"
$CclimitsSource = Join-Path $SourceDir "cclimits.py"
$LauncherSource = Join-Path $SourceDir "Start-CodexQuotaPanel.cmd"
$WatchdogSource = Join-Path $SourceDir "QuotaPanelWatchdog.ps1"
$SelfHealSource = Join-Path $SourceDir "QuotaPanelSelfHeal.ps1"
$InstallerSource = Join-Path $SourceDir "install_or_repair_quota_panel.ps1"
$AssertSource = Join-Path $SourceDir "assert_quota_panel_hardened.ps1"

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
Copy-Item -Force $ScriptSource (Join-Path $RuntimeDir "CodexQuotaPanel.ps1")
Copy-Item -Force $CclimitsSource (Join-Path $RuntimeDir "cclimits.py")
Copy-Item -Force $LauncherSource (Join-Path $RuntimeDir "Start-CodexQuotaPanel.cmd")
Copy-Item -Force $WatchdogSource (Join-Path $RuntimeDir "QuotaPanelWatchdog.ps1")
Copy-Item -Force $SelfHealSource (Join-Path $RuntimeDir "QuotaPanelSelfHeal.ps1")
Copy-Item -Force $InstallerSource (Join-Path $RuntimeDir "install_or_repair_quota_panel.ps1")
Copy-Item -Force $AssertSource (Join-Path $RuntimeDir "assert_quota_panel_hardened.ps1")
Remove-Item -LiteralPath (Join-Path $RuntimeDir "Start-CodexQuotaPanel-Hidden.vbs") -Force -ErrorAction SilentlyContinue

$startup = [Environment]::GetFolderPath("Startup")
$startupShortcut = Join-Path $startup "Codex Quota Panel.lnk"
$open = [string][char]0x6253 + [string][char]0x5F00
$codex = "Codex"
$quota = [string][char]0x989D + [string][char]0x5EA6
$display = [string][char]0x663E + [string][char]0x793A
$desktopShortcutName = "$open$codex$quota$display.lnk"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) $desktopShortcutName
$target = Join-Path $RuntimeDir "Start-CodexQuotaPanel.cmd"
$shell = New-Object -ComObject WScript.Shell

foreach ($shortcut in @($startupShortcut, $desktopShortcut)) {
    $s = $shell.CreateShortcut($shortcut)
    $s.TargetPath = $target
    $s.WorkingDirectory = $RuntimeDir
    $s.WindowStyle = 7
    $s.Description = "Show compact Codex quota panel"
    $s.Save()
}

Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -like "*CodexQuotaPanel.ps1*" -and $_.ProcessId -ne $PID } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -like "*QuotaPanelWatchdog.ps1*" -and $_.ProcessId -ne $PID } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

Start-Process powershell.exe -ArgumentList "-STA","-NoProfile","-ExecutionPolicy","Bypass","-File",(Join-Path $RuntimeDir "CodexQuotaPanel.ps1")
Start-Process powershell.exe -WindowStyle Hidden -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File",(Join-Path $RuntimeDir "QuotaPanelWatchdog.ps1")

$taskName = "CodexQuotaPanelSelfHeal"
$selfHealPath = Join-Path $RuntimeDir "QuotaPanelSelfHeal.ps1"
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
}
$taskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$selfHealPath`"" -WorkingDirectory $RuntimeDir
$taskTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$taskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $taskTrigger -Settings $taskSettings -Description "Self-heal the Codex quota panel if live quota works but the visible label is stale." -Force | Out-Null

powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RuntimeDir "assert_quota_panel_hardened.ps1") -RuntimeDir $RuntimeDir

[pscustomobject]@{
    RuntimeDir = $RuntimeDir
    StartupShortcut = $startupShortcut
    DesktopShortcut = $desktopShortcut
}
