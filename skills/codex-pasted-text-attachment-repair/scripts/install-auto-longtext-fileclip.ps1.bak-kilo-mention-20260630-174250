param(
    [switch]$Start,
    [switch]$Stop,
    [int]$MinChars = 2000,
    [string]$TargetMode = "Codex"
)

$ErrorActionPreference = "Stop"

$skillScripts = Split-Path -Parent $PSCommandPath
$target = Join-Path $env:USERPROFILE ".codex\manual-paste-attachments"
$desktop = [Environment]::GetFolderPath("Desktop")
$startup = [Environment]::GetFolderPath("Startup")
$watchdogTaskName = "CodexAutoLongTextWatchdog"
New-Item -ItemType Directory -Force -Path $target | Out-Null

$files = @(
    "install-auto-longtext-fileclip.ps1",
    "auto-longtext-fileclip.ps1",
    "clipboard-to-txt.ps1",
    "fix-codex-longtext-attachment.ps1",
    "watch-auto-longtext-fileclip.ps1",
    "Run-AutoLongTextWatchdog-Hidden.vbs",
    "START_Auto_LongText_FileClip.cmd",
    "START_Auto_LongText_FileClip_Hidden.vbs",
    "STOP_Auto_LongText_FileClip.cmd",
    "STATUS_Auto_LongText_FileClip.cmd"
)

foreach ($file in $files) {
    $source = Join-Path $skillScripts $file
    $destination = Join-Path $target $file
    if (Test-Path -LiteralPath $source) {
        if ([System.IO.Path]::GetFullPath($source) -ne [System.IO.Path]::GetFullPath($destination)) {
            Copy-Item -LiteralPath $source -Destination $destination -Force
        }
    }
}

$wsh = New-Object -ComObject WScript.Shell
$startShortcut = $wsh.CreateShortcut((Join-Path $desktop "Codex Auto LongText ON.lnk"))
$startShortcut.TargetPath = Join-Path $target "START_Auto_LongText_FileClip.cmd"
$startShortcut.WorkingDirectory = $target
$startShortcut.Save()

$stopShortcut = $wsh.CreateShortcut((Join-Path $desktop "Codex Auto LongText OFF.lnk"))
$stopShortcut.TargetPath = Join-Path $target "STOP_Auto_LongText_FileClip.cmd"
$stopShortcut.WorkingDirectory = $target
$stopShortcut.Save()

$statusShortcut = $wsh.CreateShortcut((Join-Path $desktop "Codex Auto LongText STATUS.lnk"))
$statusShortcut.TargetPath = Join-Path $target "STATUS_Auto_LongText_FileClip.cmd"
$statusShortcut.WorkingDirectory = $target
$statusShortcut.Save()

$startupShortcutPath = Join-Path $startup "Codex Auto LongText ON.lnk"
$hiddenStartVbsPath = Join-Path $target "START_Auto_LongText_FileClip_Hidden.vbs"

$hiddenStartContent = @"
Option Explicit

Dim shell
Dim command

Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File " & Chr(34) & "$target\install-auto-longtext-fileclip.ps1" & Chr(34) & " -Start -MinChars $MinChars -TargetMode " & Chr(34) & "$TargetMode" & Chr(34)
shell.Run command, 0, False
"@
$hiddenStartContent | Set-Content -LiteralPath $hiddenStartVbsPath -Encoding ASCII

$watchdogPath = Join-Path $target "watch-auto-longtext-fileclip.ps1"
$watchdogVbsPath = Join-Path $target "Run-AutoLongTextWatchdog-Hidden.vbs"

$watchdogContent = @"
Option Explicit

Dim shell
Dim command

Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File " & Chr(34) & "$target\watch-auto-longtext-fileclip.ps1" & Chr(34) & " -MinChars $MinChars -TargetMode " & Chr(34) & "$TargetMode" & Chr(34)
shell.Run command, 0, False
"@
$watchdogContent | Set-Content -LiteralPath $watchdogVbsPath -Encoding ASCII

if ($Stop) {
    & schtasks.exe /Delete /TN $watchdogTaskName /F 2>$null | Out-Null
    Remove-Item -LiteralPath $startupShortcutPath -Force -ErrorAction SilentlyContinue
} elseif (Test-Path -LiteralPath $watchdogPath) {
    $startupShortcut = $wsh.CreateShortcut($startupShortcutPath)
    $startupShortcut.TargetPath = $hiddenStartVbsPath
    $startupShortcut.WorkingDirectory = $target
    $startupShortcut.WindowStyle = 7
    $startupShortcut.Save()

    $taskCommand = "wscript.exe `"$watchdogVbsPath`""
    try {
        & schtasks.exe /Create /TN $watchdogTaskName /SC MINUTE /MO 1 /TR $taskCommand /F | Out-Null
    } catch {
        Write-Warning "Failed to create watchdog scheduled task: $($_.Exception.Message)"
    }
}

$needle = "\auto-longtext-fileclip.ps1"
$watchNeedle = "\watch-auto-longtext-fileclip.ps1"
if ($Stop -or $Start) {
    $self = $PID
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.ProcessId -ne $self -and
            $_.Name -match '^powershell(\.exe)?$' -and
            ($_.CommandLine -like ('*' + $needle + '*') -or ($Stop -and $_.CommandLine -like ('*' + $watchNeedle + '*')))
        } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

if ($Start) {
    Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-STA",
        "-File", (Join-Path $target "auto-longtext-fileclip.ps1"),
        "-MinChars", "$MinChars",
        "-TargetMode", $TargetMode
    )
}

[pscustomobject]@{
    status = if ($Start) { "STARTED" } elseif ($Stop) { "STOPPED" } else { "INSTALLED" }
    target = $target
    minChars = $MinChars
    targetMode = $TargetMode
    startShortcut = Join-Path $desktop "Codex Auto LongText ON.lnk"
    stopShortcut = Join-Path $desktop "Codex Auto LongText OFF.lnk"
    statusShortcut = Join-Path $desktop "Codex Auto LongText STATUS.lnk"
    startupShortcut = $startupShortcutPath
    watchdogTask = $watchdogTaskName
} | ConvertTo-Json -Depth 4

exit 0
