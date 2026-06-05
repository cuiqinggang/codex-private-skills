param(
  [string]$ProjectRoot = "C:\Users\A\xiaolongxia-free-api-local",
  [string]$OutputRoot = "C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524",
  [string]$SecretFile = "",
  [ValidateSet("quick", "full")]
  [string]$Mode = "full"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if (-not $SecretFile) {
  $SecretFile = Join-Path $ProjectRoot "secrets\deepseek_api_key.txt"
}

if (-not (Test-Path -LiteralPath $SecretFile)) {
  throw "DeepSeek secret file is missing: $SecretFile"
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

$env:XIAOLONGXIA_PROJECT_ROOT = $ProjectRoot
$env:XIAOLONGXIA_DEEPSEEK_SECRET_FILE = $SecretFile
$env:XIAOLONGXIA_DEEPSEEK_OUTPUT_ROOT = $OutputRoot
$env:XIAOLONGXIA_DEEPSEEK_SELFTEST_MODE = $Mode

try {
  & node (Join-Path $PSScriptRoot "xiaolongxia-deepseek-v4-flash-direct-selftest.js")
  if ($LASTEXITCODE -ne 0) {
    throw "DeepSeek direct selftest failed with exit code $LASTEXITCODE"
  }
}
finally {
  Remove-Item Env:\XIAOLONGXIA_PROJECT_ROOT -ErrorAction SilentlyContinue
  Remove-Item Env:\XIAOLONGXIA_DEEPSEEK_SECRET_FILE -ErrorAction SilentlyContinue
  Remove-Item Env:\XIAOLONGXIA_DEEPSEEK_OUTPUT_ROOT -ErrorAction SilentlyContinue
  Remove-Item Env:\XIAOLONGXIA_DEEPSEEK_SELFTEST_MODE -ErrorAction SilentlyContinue
  Remove-Item Env:\DEEPSEEK_API_KEY -ErrorAction SilentlyContinue
}
