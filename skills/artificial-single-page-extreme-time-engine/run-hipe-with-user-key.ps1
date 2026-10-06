param(
  [Parameter(Mandatory=$true)][string]$HipeRoot,
  [Parameter(Mandatory=$true)][string]$TaskPath,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$Python = "python"
)

$k = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "User")
if (-not $k) {
  throw "OPENROUTER_API_KEY is not set in Windows User environment."
}

$env:OPENROUTER_API_KEY = $k
try {
  & $Python -B (Join-Path $HipeRoot "runtime\production.py") --task $TaskPath --out $OutDir
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
}
