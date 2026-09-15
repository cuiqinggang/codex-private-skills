$ErrorActionPreference = "Stop"

$Root = "C:\AI\ComfyUI_Aaki_v3"
$Comfy = Join-Path $Root "ComfyUI"
$Python = Join-Path $Root "python\python.exe"
$DataRoot = "C:\AI\ComfyUI_Aaki_v3\data"
$OutputDir = Join-Path $DataRoot "output"
$InputDir = Join-Path $DataRoot "input"
$TempDir = Join-Path $DataRoot "temp"

New-Item -ItemType Directory -Force -Path $OutputDir, $InputDir, $TempDir | Out-Null

Set-Location $Root
& $Python -s "ComfyUI\main.py" `
  --windows-standalone-build `
  --port 8188 `
  --output-directory $OutputDir `
  --input-directory $InputDir `
  --temp-directory $TempDir
