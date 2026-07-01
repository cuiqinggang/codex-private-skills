$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $Root "feishu-bridge.pid"
if (-not (Test-Path -LiteralPath $PidFile)) {
  "NO_PID_FILE"
  exit 0
}
$pidText = (Get-Content -LiteralPath $PidFile -Raw).Trim()
if (-not $pidText) {
  "EMPTY_PID_FILE"
  exit 0
}
$proc = Get-Process -Id ([int]$pidText) -ErrorAction SilentlyContinue
if ($null -eq $proc) {
  "NOT_RUNNING pid=$pidText"
  exit 0
}
Stop-Process -Id $proc.Id
"STOPPED pid=$pidText"
