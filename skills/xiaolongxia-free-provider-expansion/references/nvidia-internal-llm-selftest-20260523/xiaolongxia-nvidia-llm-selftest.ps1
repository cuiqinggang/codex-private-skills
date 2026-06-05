param(
  [ValidateSet('primary', 'fallback', 'auto')]
  [string]$ModelMode = 'auto',
  [switch]$SimulatePrimaryFailure,
  [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
  [string]$OutputRoot = 'C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-INTERNAL-LLM-SELFTEST-20260523',
  [string]$SecretFile = '',
  [string]$PrimaryModel = 'meta/llama-3.1-8b-instruct',
  [string]$FallbackModel = 'meta/llama-3.1-70b-instruct',
  [int]$TimeoutSec = 60
)

$ErrorActionPreference = 'Stop'

if (-not $SecretFile) {
  $SecretFile = Join-Path $ProjectRoot 'secrets\nvidia_api_key.txt'
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

$env:PROJECT_ROOT = $ProjectRoot
$env:OUTPUT_ROOT = $OutputRoot
$env:NVIDIA_SECRET_FILE = $SecretFile
$env:MODEL_MODE = $ModelMode
$env:SIMULATE_PRIMARY_FAILURE = if ($SimulatePrimaryFailure) { 'true' } else { 'false' }
$env:PRIMARY_MODEL = $PrimaryModel
$env:FALLBACK_MODEL = $FallbackModel
$env:TIMEOUT_SEC = [string]$TimeoutSec

try {
  & node (Join-Path $PSScriptRoot 'xiaolongxia-nvidia-llm-selftest.js')
  if ($LASTEXITCODE -ne 0) { throw "internal llm selftest failed with exit code $LASTEXITCODE" }
} finally {
  Remove-Item Env:\NVIDIA_API_KEY -ErrorAction SilentlyContinue
}
