[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [Parameter(Mandatory = $true)]
    [string]$Task,

    [Parameter(Mandatory = $true)]
    [string]$VideoPath,

    [string]$TaskId,
    [string]$OutputRoot,
    [string]$CodexCommand = "codex",
    [string]$FfmpegCommand = "ffmpeg",
    [string]$FfprobeCommand = "ffprobe",
    [int]$CodexTimeoutSec = 1200,
    [int]$FfmpegTimeoutSec = 300,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:OutDir = $null

function Redact-SecretText {
    param([AllowNull()][string]$Text)
    if ($null -eq $Text) { return "" }
    $redacted = $Text -replace '([0-9]{8,12}:[A-Za-z0-9_-]{20,})', '<REDACTED_TELEGRAM_TOKEN>'
    $redacted = $redacted -replace '(sk-[A-Za-z0-9_-]{10,})', '<REDACTED_API_KEY>'
    return $redacted
}

function Write-TaskFailure {
    param(
        [string]$Code,
        [string]$Message
    )
    $safeMessage = Redact-SecretText $Message
    if ($script:OutDir -and (Test-Path -LiteralPath $script:OutDir)) {
        $resultPath = Join-Path $script:OutDir "result.txt"
        @(
            $Code
            $safeMessage
        ) | Set-Content -LiteralPath $resultPath -Encoding UTF8
    }
    throw "$Code $safeMessage"
}

function Resolve-ExistingPath {
    param(
        [string]$Path,
        [string]$Code
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-TaskFailure -Code $Code -Message "Missing path: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).ProviderPath
}

function New-SafeTaskId {
    param([string]$Prefix)
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $short = [guid]::NewGuid().ToString("N").Substring(0, 8)
    return "$Prefix-$stamp-$short"
}

function Normalize-TaskId {
    param([string]$Value, [string]$Prefix)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        $Value = New-SafeTaskId -Prefix $Prefix
    }
    $safe = $Value -replace '[^A-Za-z0-9_.-]', '-'
    if ([string]::IsNullOrWhiteSpace($safe)) {
        Write-TaskFailure -Code "STOP_TASK_ID_INVALID" -Message "TaskId is empty after sanitizing."
    }
    return $safe
}

function ConvertTo-ProcessArguments {
    param([string[]]$Arguments)
    $quoted = foreach ($arg in $Arguments) {
        $value = [string]$arg
        if ($value.Length -eq 0) {
            '""'
        } elseif ($value -notmatch '[\s"]') {
            $value
        } else {
            '"' + ($value -replace '"', '\"') + '"'
        }
    }
    return ($quoted -join " ")
}

function Invoke-ExternalProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [int]$TimeoutSec
    )

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $FilePath
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.Arguments = ConvertTo-ProcessArguments -Arguments $Arguments

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $psi
    try {
        [void]$process.Start()
    } catch {
        return [pscustomobject]@{
            TimedOut = $false
            ExitCode = -1
            StdOut = ""
            StdErr = $_.Exception.Message
        }
    }

    $completed = $process.WaitForExit($TimeoutSec * 1000)
    if (-not $completed) {
        try { $process.Kill() } catch {}
        return [pscustomobject]@{
            TimedOut = $true
            ExitCode = -1
            StdOut = Redact-SecretText $process.StandardOutput.ReadToEnd()
            StdErr = "Timed out after $TimeoutSec seconds."
        }
    }

    return [pscustomobject]@{
        TimedOut = $false
        ExitCode = $process.ExitCode
        StdOut = Redact-SecretText $process.StandardOutput.ReadToEnd()
        StdErr = Redact-SecretText $process.StandardError.ReadToEnd()
    }
}

function Get-VideoDurationSeconds {
    param(
        [string]$Path,
        [string]$FfprobeCommand,
        [string]$WorkingDirectory
    )
    $args = @(
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        $Path
    )
    $run = Invoke-ExternalProcess -FilePath $FfprobeCommand -Arguments $args -WorkingDirectory $WorkingDirectory -TimeoutSec 30
    if ($run.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($run.StdOut)) {
        return $null
    }
    $text = $run.StdOut.Trim()
    $culture = [System.Globalization.CultureInfo]::InvariantCulture
    $duration = 0.0
    if ([double]::TryParse($text, [System.Globalization.NumberStyles]::Float, $culture, [ref]$duration)) {
        return $duration
    }
    return $null
}

function Clear-GeneratedFrames {
    param(
        [string]$FramesDir,
        [string]$FramesRoot
    )
    $resolvedRoot = (Resolve-Path -LiteralPath $FramesRoot).ProviderPath.TrimEnd('\')
    $resolvedDir = (Resolve-Path -LiteralPath $FramesDir).ProviderPath.TrimEnd('\')
    if (-not $resolvedDir.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        Write-TaskFailure -Code "STOP_FRAME_PATH_UNSAFE" -Message "FramesDir is outside frames root: $FramesDir"
    }
    Get-ChildItem -LiteralPath $FramesDir -Filter "frame_*.jpg" -File -ErrorAction SilentlyContinue |
        Remove-Item -Force
}

$repo = Resolve-ExistingPath -Path $RepoPath -Code "STOP_REPO_MISSING"
$gitPath = Join-Path $repo ".git"
if (-not (Test-Path -LiteralPath $gitPath)) {
    Write-TaskFailure -Code "STOP_REPO_GIT_MISSING" -Message "RepoPath must contain .git: $repo"
}

if ([string]::IsNullOrWhiteSpace($Task)) {
    Write-TaskFailure -Code "STOP_TASK_EMPTY" -Message "Task cannot be empty."
}

$video = Resolve-ExistingPath -Path $VideoPath -Code "STOP_VIDEO_MISSING"
$allowedVideoExtensions = @(".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v")
$videoExt = [System.IO.Path]::GetExtension($video).ToLowerInvariant()
if ($allowedVideoExtensions -notcontains $videoExt) {
    Write-TaskFailure -Code "STOP_VIDEO_TYPE_UNSUPPORTED" -Message "Unsupported video extension '$videoExt' for $video"
}

$safeTaskId = Normalize-TaskId -Value $TaskId -Prefix "TGVID"
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $repo "output"
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$script:OutDir = Join-Path $OutputRoot "CODEX-TELEGRAM-VISION-$safeTaskId"
New-Item -ItemType Directory -Force -Path $script:OutDir | Out-Null

$taskPath = Join-Path $script:OutDir "task.txt"
$resultPath = Join-Path $script:OutDir "result.txt"
$manifestPath = Join-Path $script:OutDir "media-manifest.json"
$commandPath = Join-Path $script:OutDir "codex-command.json"
$ffmpegLogPath = Join-Path $script:OutDir "ffmpeg.log"

$Task | Set-Content -LiteralPath $taskPath -Encoding UTF8

$framesRoot = Join-Path $repo "input\telegram-media\frames"
New-Item -ItemType Directory -Force -Path $framesRoot | Out-Null
$framesDir = Join-Path $framesRoot $safeTaskId
New-Item -ItemType Directory -Force -Path $framesDir | Out-Null
Clear-GeneratedFrames -FramesDir $framesDir -FramesRoot $framesRoot

$duration = Get-VideoDurationSeconds -Path $video -FfprobeCommand $FfprobeCommand -WorkingDirectory $repo
$fpsValue = "1"
if ($null -ne $duration -and $duration -gt 20.0) {
    $fps = [Math]::Max(0.001, 20.0 / $duration)
    $fpsValue = $fps.ToString("0.######", [System.Globalization.CultureInfo]::InvariantCulture)
}

$framePattern = Join-Path $framesDir "frame_%04d.jpg"
$ffmpegArgs = @(
    "-y",
    "-i", $video,
    "-vf", "fps=$fpsValue",
    "-q:v", "2",
    $framePattern
)
$ffmpegRun = Invoke-ExternalProcess -FilePath $FfmpegCommand -Arguments $ffmpegArgs -WorkingDirectory $repo -TimeoutSec $FfmpegTimeoutSec
@(
    "FFMPEG_EXIT_CODE=$($ffmpegRun.ExitCode)"
    "FFMPEG_TIMED_OUT=$($ffmpegRun.TimedOut)"
    "FPS=$fpsValue"
    "DURATION=$duration"
    ""
    "STDOUT:"
    $ffmpegRun.StdOut
    ""
    "STDERR:"
    $ffmpegRun.StdErr
) | Set-Content -LiteralPath $ffmpegLogPath -Encoding UTF8

if ($ffmpegRun.TimedOut) {
    Write-TaskFailure -Code "STOP_FFMPEG_TIMEOUT" -Message "ffmpeg timed out after $FfmpegTimeoutSec seconds. Log: $ffmpegLogPath"
}
if ($ffmpegRun.ExitCode -ne 0) {
    Write-TaskFailure -Code "STOP_FFMPEG_FAILED" -Message "ffmpeg exited with $($ffmpegRun.ExitCode). Log: $ffmpegLogPath"
}

$frames = @(Get-ChildItem -LiteralPath $framesDir -Filter "frame_*.jpg" -File | Sort-Object Name)
if ($frames.Count -gt 20) {
    $frames | Select-Object -Skip 20 | Remove-Item -Force
    $frames = @(Get-ChildItem -LiteralPath $framesDir -Filter "frame_*.jpg" -File | Sort-Object Name)
}
if ($frames.Count -eq 0) {
    Write-TaskFailure -Code "STOP_NO_FRAMES" -Message "ffmpeg produced no frame_*.jpg files in $framesDir"
}

$videoItem = Get-Item -LiteralPath $video
$frameMedia = foreach ($frame in $frames) {
    [pscustomobject]@{
        type = "frame"
        path = $frame.FullName
        name = $frame.Name
        extension = $frame.Extension.ToLowerInvariant()
        length = $frame.Length
        sha256 = (Get-FileHash -LiteralPath $frame.FullName -Algorithm SHA256).Hash
    }
}

$manifest = [pscustomobject]@{
    taskId = $safeTaskId
    kind = "video"
    repoPath = $repo
    outputDir = $script:OutDir
    createdAt = (Get-Date).ToString("o")
    dryRun = [bool]$DryRun
    video = [pscustomobject]@{
        path = $videoItem.FullName
        name = $videoItem.Name
        extension = $videoItem.Extension.ToLowerInvariant()
        length = $videoItem.Length
        sha256 = (Get-FileHash -LiteralPath $videoItem.FullName -Algorithm SHA256).Hash
        durationSeconds = $duration
    }
    framesDir = $framesDir
    frames = @($frameMedia)
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$codexArgs = New-Object System.Collections.Generic.List[string]
foreach ($frame in $frames) {
    [void]$codexArgs.Add("--image")
    [void]$codexArgs.Add($frame.FullName)
}
[void]$codexArgs.Add($Task)

[pscustomobject]@{
    command = $CodexCommand
    args = @($codexArgs)
    workingDirectory = $repo
    timeoutSec = $CodexTimeoutSec
    dryRun = [bool]$DryRun
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $commandPath -Encoding UTF8

if ($DryRun) {
    @(
        "DRY_RUN_NO_CODEX_INVOCATION"
        "taskId=$safeTaskId"
        "video=$video"
        "frameCount=$($frames.Count)"
        "framesDir=$framesDir"
        "outputDir=$script:OutDir"
    ) | Set-Content -LiteralPath $resultPath -Encoding UTF8
    [pscustomobject]@{
        status = "DRY_RUN_NO_CODEX_INVOCATION"
        taskId = $safeTaskId
        outputDir = $script:OutDir
        resultPath = $resultPath
        framesDir = $framesDir
        frameCount = $frames.Count
    } | ConvertTo-Json -Compress
    return
}

$run = Invoke-ExternalProcess -FilePath $CodexCommand -Arguments @($codexArgs) -WorkingDirectory $repo -TimeoutSec $CodexTimeoutSec
$resultLines = @(
    "CODEX_EXIT_CODE=$($run.ExitCode)"
    "CODEX_TIMED_OUT=$($run.TimedOut)"
    ""
    "STDOUT:"
    $run.StdOut
    ""
    "STDERR:"
    $run.StdErr
)
$resultLines | Set-Content -LiteralPath $resultPath -Encoding UTF8

if ($run.TimedOut) {
    Write-TaskFailure -Code "STOP_CODEX_TIMEOUT" -Message "Codex timed out after $CodexTimeoutSec seconds. Result: $resultPath"
}
if ($run.ExitCode -ne 0) {
    Write-TaskFailure -Code "STOP_CODEX_FAILED" -Message "Codex exited with $($run.ExitCode). Result: $resultPath"
}

[pscustomobject]@{
    status = "CODEX_VIDEO_EXEC_PASS"
    taskId = $safeTaskId
    outputDir = $script:OutDir
    resultPath = $resultPath
    framesDir = $framesDir
    frameCount = $frames.Count
} | ConvertTo-Json -Compress
