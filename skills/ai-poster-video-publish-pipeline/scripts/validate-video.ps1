param(
    [Parameter(Mandatory = $true)]
    [string]$VideoPath,

    [string]$ReportDir,
    [ValidateSet('full', 'short', 'any')]
    [string]$ExpectedMode = 'any'
)

$ErrorActionPreference = 'Stop'

function Convert-Rate {
    param([string]$Rate)
    if ($Rate -match '^(\d+)/(\d+)$') {
        $num = [double]$Matches[1]
        $den = [double]$Matches[2]
        if ($den -ne 0) {
            return $num / $den
        }
    }
    return [double]$Rate
}

function To-Invariant {
    param([double]$Value)
    return $Value.ToString('0.###', [System.Globalization.CultureInfo]::InvariantCulture)
}

function Invoke-FfmpegLogged {
    param(
        [string[]]$Arguments,
        [string]$LogPath
    )
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = & ffmpeg @Arguments 2>&1
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $oldPreference
    }
    $output | Set-Content -LiteralPath $LogPath -Encoding UTF8
    return $code
}

if (-not (Test-Path -LiteralPath $VideoPath)) {
    throw "Video not found: $VideoPath"
}
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
    throw "ffprobe is required for validate-video.ps1"
}
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    throw "ffmpeg is required for validate-video.ps1"
}

$videoFull = (Resolve-Path -LiteralPath $VideoPath).Path
if (-not $ReportDir -or $ReportDir.Trim().Length -eq 0) {
    $ReportDir = Join-Path (Split-Path -Parent $videoFull) 'reports'
}
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$probeText = & ffprobe -v error -print_format json -show_streams -show_format $videoFull
if ($LASTEXITCODE -ne 0) {
    throw "ffprobe failed for $videoFull"
}
$probe = ($probeText | Out-String) | ConvertFrom-Json
$videoStream = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
if (-not $videoStream) {
    throw "No video stream found: $videoFull"
}

$duration = [double]$probe.format.duration
$fps = Convert-Rate ([string]$videoStream.avg_frame_rate)
$checks = @()
$checks += [pscustomobject]@{ name = 'width_1080'; pass = ([int]$videoStream.width -eq 1080); actual = [int]$videoStream.width }
$checks += [pscustomobject]@{ name = 'height_1920'; pass = ([int]$videoStream.height -eq 1920); actual = [int]$videoStream.height }
$checks += [pscustomobject]@{ name = 'codec_h264'; pass = ([string]$videoStream.codec_name -eq 'h264'); actual = [string]$videoStream.codec_name }
$checks += [pscustomobject]@{ name = 'fps_30'; pass = ([Math]::Abs($fps - 30.0) -lt 0.05); actual = $fps }
if ($ExpectedMode -eq 'full') {
    $checks += [pscustomobject]@{ name = 'duration_full_40_to_55_seconds'; pass = ($duration -ge 40.0 -and $duration -le 55.0); actual = $duration }
}
elseif ($ExpectedMode -eq 'short') {
    $checks += [pscustomobject]@{ name = 'duration_short_25_to_35_seconds'; pass = ($duration -ge 25.0 -and $duration -le 35.0); actual = $duration }
}
else {
    $checks += [pscustomobject]@{ name = 'duration_reasonable_25_to_55_seconds'; pass = ($duration -ge 25.0 -and $duration -le 55.0); actual = $duration }
}

$framePaths = @()
$times = @(0.5, ($duration * 0.25), ($duration * 0.5), ($duration * 0.75), ([Math]::Max(0.5, $duration - 0.5)))
for ($i = 0; $i -lt $times.Count; $i++) {
    $timeText = To-Invariant ([double]$times[$i])
    $framePath = Join-Path $ReportDir ("frames{0:D2}.jpg" -f ($i + 1))
    $frameCode = Invoke-FfmpegLogged -Arguments @('-y', '-ss', $timeText, '-i', $videoFull, '-frames:v', '1', '-q:v', '2', $framePath) -LogPath (Join-Path $ReportDir ("frames{0:D2}.log" -f ($i + 1)))
    if ($frameCode -ne 0 -or -not (Test-Path -LiteralPath $framePath)) {
        throw "ffmpeg frame extraction failed at $timeText seconds"
    }
    $framePaths += $framePath
}

$interval = [Math]::Max(1.0, $duration / 5.0)
$intervalText = To-Invariant $interval
$contactSheet = Join-Path $ReportDir 'contact-sheet.jpg'
$vf = "fps=1/$intervalText,scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2,tile=5x1"
$sheetCode = Invoke-FfmpegLogged -Arguments @('-y', '-i', $videoFull, '-vf', $vf, '-frames:v', '1', '-q:v', '2', $contactSheet) -LogPath (Join-Path $ReportDir 'contact-sheet.log')
if ($sheetCode -ne 0 -or -not (Test-Path -LiteralPath $contactSheet)) {
    throw "ffmpeg contact sheet generation failed"
}

$allPass = -not ($checks | Where-Object { -not $_.pass })
$result = [pscustomobject]@{
    status = if ($allPass) { 'PASS' } else { 'FAIL' }
    video = $videoFull
    expected_mode = $ExpectedMode
    width = [int]$videoStream.width
    height = [int]$videoStream.height
    codec = [string]$videoStream.codec_name
    fps = $fps
    duration_seconds = $duration
    checks = $checks
    frames = $framePaths
    contact_sheet = $contactSheet
    manual_visual_checks_required = @(
        '检查开头、中间、结尾',
        '检查免费/3000元/联系方式或抖音无联系方式',
        '检查不裁切、不拉伸、不抖动',
        '检查文字不发虚'
    )
}

$reportPath = Join-Path $ReportDir 'video-validation.json'
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding UTF8
if ($allPass) {
    Write-Output "PASS video validation: $reportPath"
}
else {
    Write-Output "FAIL video validation: $reportPath"
    exit 1
}



