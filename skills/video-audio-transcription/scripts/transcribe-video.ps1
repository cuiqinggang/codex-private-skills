param(
  [Parameter(Mandatory=$true)]
  [string]$InputPath,

  [string]$OutputDir = "",
${REDACTED_SECRET}
  [ValidateSet("auto","gpu","cpu")]
  [string]$Engine = "auto",
  [string]$Language = "zh"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputPath)) {
  throw "Input not found: $InputPath"
}

if (-not (Test-Path -LiteralPath $ModelPath)) {
  throw "Model not found: $ModelPath"
}

$knownModelSha1 = @{
  "ggml-large-v3.bin" = "AD82BF6A9043CEED055076D0FD39F5F186FF8062"
}
$modelName = Split-Path -Leaf $ModelPath
$hash = (Get-FileHash -Algorithm SHA1 -LiteralPath $ModelPath).Hash
if (-not $knownModelSha1.ContainsKey($modelName)) {
  throw "Unknown model file for safety check: $modelName"
}
$expectedSha1 = $knownModelSha1[$modelName]
if ($hash -ne $expectedSha1) {
  throw "Model SHA1 mismatch for $modelName. Expected $expectedSha1, got $hash"
}

if (-not $OutputDir) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $OutputDir = Join-Path (Get-Location) "transcript-$stamp"
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$wavPath = Join-Path $OutputDir "audio_16k.wav"
$baseOut = Join-Path $OutputDir "transcript"

ffmpeg -y -i $InputPath -vn -ac 1 -ar 16000 -c:a pcm_s16le $wavPath

${REDACTED_SECRET}
${REDACTED_SECRET}

if ($Engine -eq "gpu" -or ($Engine -eq "auto" -and (Test-Path -LiteralPath $gpuExe))) {
  $exe = $gpuExe
  $engineName = "gpu"
} else {
  $exe = $cpuExe
  $engineName = "cpu"
}

if (-not (Test-Path -LiteralPath $exe)) {
  throw "whisper-cli not found for engine ${engineName}: $exe"
}

$started = Get-Date
& $exe -m $ModelPath -f $wavPath -l $Language -t 8 -osrt -otxt -oj -of $baseOut
$ended = Get-Date

$readableHtml = Join-Path $OutputDir "readable-transcript.html"
$readableExporter = Join-Path $PSScriptRoot "export-readable-transcript-html.ps1"
if (Test-Path -LiteralPath $readableExporter) {
  & $readableExporter -TranscriptPath "$baseOut.txt" -OutputPath $readableHtml -Title "Video Transcript" -Subtitle "large-v3 transcript, readable and copy-ready"
}

@{
  input = (Resolve-Path -LiteralPath $InputPath).Path
  output_dir = (Resolve-Path -LiteralPath $OutputDir).Path
  engine = $engineName
  model = (Resolve-Path -LiteralPath $ModelPath).Path
  model_sha1 = $hash
  started = $started.ToString("s")
  ended = $ended.ToString("s")
  elapsed_seconds = [math]::Round(($ended - $started).TotalSeconds, 2)
  txt = "$baseOut.txt"
  srt = "$baseOut.srt"
  json = "$baseOut.json"
  readable_html = $readableHtml
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $OutputDir "run-manifest.json") -Encoding UTF8

Write-Host "TRANSCRIPTION_DONE"
Write-Host "Output: $OutputDir"
