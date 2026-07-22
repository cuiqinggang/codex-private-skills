$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Script = Join-Path $Root "feishu_hermes_bridge.py"
$Log = Join-Path $Root "feishu-bridge.log"
$PidFile = Join-Path $Root "feishu-bridge.pid"
${REDACTED_SECRET}

if (-not (Test-Path -LiteralPath $Python)) {
${REDACTED_SECRET}
  if (Test-Path -LiteralPath $ProvenPython) {
    $Python = $ProvenPython
  } else {
    $BasePython = "H:\Hermes_Windows_Native_014\venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $BasePython)) {
      $BasePython = "python"
    }
    & $BasePython -m venv (Join-Path $Root ".venv")
    & $Python -m pip install --disable-pip-version-check lark-oapi requests
  }
}
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -like "*feishu_hermes_bridge.py*" } |
  ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force
  }
if (-not $env:FEISHU_APP_ID -or -not $env:FEISHU_APP_SECRET) {
  if (-not (Test-Path -LiteralPath $SecretFile)) {
    throw "Missing FEISHU_APP_ID/FEISHU_APP_SECRET and secret file: $SecretFile"
  }
}
$env:FEISHU_CONNECTION_MODE = "websocket"
$proc = Start-Process -FilePath $Python -ArgumentList @($Script, "--secret-file", $SecretFile, "--log", $Log) -WorkingDirectory $Root -PassThru -WindowStyle Hidden
$proc.Id | Set-Content -LiteralPath $PidFile -Encoding ascii
"STARTED pid=$($proc.Id) log=$Log"
