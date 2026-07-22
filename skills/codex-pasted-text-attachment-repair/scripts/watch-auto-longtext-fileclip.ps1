param(
    [int]$MinChars = 2000,
    [int]$PollMilliseconds = 200,
    [string]$TargetMode = "Codex",
    [string]$KiloWorkspaceDirectory = "$env:USERPROFILE\Desktop\ClaudeCode_Outputs\kilo-validation"
)

$ErrorActionPreference = "Stop"

$target = Join-Path $env:USERPROFILE ".codex\manual-paste-attachments"
$script = Join-Path $target "auto-longtext-fileclip.ps1"
$logPath = Join-Path $target "auto-longtext-fileclip.log"

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') WATCHDOG $Message"
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}

New-Item -ItemType Directory -Force -Path $target | Out-Null

if (-not (Test-Path -LiteralPath $script)) {
    Write-Log "MISSING script=$script"
    exit 2
}

$needle = "\auto-longtext-fileclip.ps1"
$self = $PID
$running = @(
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.ProcessId -ne $self -and
            $_.Name -match '^powershell(\.exe)?$' -and
            $_.CommandLine -like ('*' + $needle + '*')
        }
)

if ($running.Count -gt 0) {
    exit 0
}

Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-STA",
    "-File", $script,
    "-MinChars", "$MinChars",
    "-PollMilliseconds", "$PollMilliseconds",
    "-TargetMode", $TargetMode,
    "-KiloWorkspaceDirectory", $KiloWorkspaceDirectory
)

Write-Log "RESTARTED TargetMode=$TargetMode KiloWorkspaceDirectory=$KiloWorkspaceDirectory script=$script"
