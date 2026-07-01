param(
  [string]$Root = 'H:\AI\ComfyUI_Aaki_v3',
  [string]$SkillRoot = 'H:\AI\skills\comfyui-aaki-v3-video-baseline',
  [string]$Url = 'http://127.0.0.1:8188',
  [switch]$VerifyHash,
  [string]$OutFile = ''
)

$ErrorActionPreference = 'Stop'

function Test-HttpStatus {
  param([string]$Target)
  try {
    $result = & curl.exe --max-time 5 -s -o NUL -w "%{http_code}" $Target
    return [int]$result
  } catch {
    return 0
  }
}

$Comfy = Join-Path $Root 'ComfyUI'
$checks = [ordered]@{}

$paths = [ordered]@{
  InstallRoot = $Root
  ComfyRoot = $Comfy
  DiffusionModel = Join-Path $Comfy 'models\diffusion_models\wan2.2_ti2v_5B_fp16.safetensors'
  TextEncoder = Join-Path $Comfy 'models\text_encoders\umt5_xxl_fp8_e4m3fn_scaled.safetensors'
  Vae = Join-Path $Comfy 'models\vae\wan2.2_vae.safetensors'
  RawVideoOutput = Join-Path $Comfy 'output\video'
  VideoSelected = Join-Path $Comfy 'output\video_selected'
  RemotionInbox = Join-Path $Comfy 'output\remotion_inbox'
  Workflow = Join-Path $SkillRoot 'workflows\wan22_5b_lowrisk_ui_workflow.json'
  ApiPrompt = Join-Path $SkillRoot 'prompts\wan22_5b_lowrisk_api_prompt.json'
}

foreach ($key in $paths.Keys) {
  $path = $paths[$key]
  $checks[$key] = [ordered]@{
    path = $path
    exists = Test-Path -LiteralPath $path
    length = if (Test-Path -LiteralPath $path -PathType Leaf) { (Get-Item -LiteralPath $path).Length } else { $null }
  }
}

$checks.HttpRoot = [ordered]@{
  url = "$Url/"
  status = Test-HttpStatus "$Url/"
}

$checks.SystemStats = [ordered]@{
  url = "$Url/system_stats"
  status = Test-HttpStatus "$Url/system_stats"
}

$checks.Queue = [ordered]@{
  url = "$Url/queue"
  status = Test-HttpStatus "$Url/queue"
}

$checks.Gpu = [ordered]@{
  nvidia_smi = (& nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used,memory.free,compute_cap --format=csv,noheader,nounits)
}

if ($VerifyHash) {
  $checks.Hashes = [ordered]@{
    DiffusionModel = (Get-FileHash -LiteralPath $paths.DiffusionModel -Algorithm SHA256).Hash
    TextEncoder = (Get-FileHash -LiteralPath $paths.TextEncoder -Algorithm SHA256).Hash
    Vae = (Get-FileHash -LiteralPath $paths.Vae -Algorithm SHA256).Hash
  }
}

$failed = @()
foreach ($key in $paths.Keys) {
  if (-not $checks[$key].exists) { $failed += $key }
}
foreach ($key in @('HttpRoot','SystemStats')) {
  if ($checks[$key].status -ne 200) { $failed += $key }
}

$result = [ordered]@{
  created_at = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K')
  ok = ($failed.Count -eq 0)
  failed = $failed
  checks = $checks
  note = 'No prompt was queued and no video was generated.'
}

$json = $result | ConvertTo-Json -Depth 8
if ($OutFile) {
  $dir = Split-Path -Parent $OutFile
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $json | Set-Content -LiteralPath $OutFile -Encoding UTF8
}

$json
if ($failed.Count -gt 0) { exit 1 }

