param(
${REDACTED_SECRET}
  [int]$Port = 8188
)

$ErrorActionPreference = "Stop"
$Comfy = Join-Path $TaskRoot "ComfyUI"
$Python = Join-Path $TaskRoot ".venv-comfyui\Scripts\python.exe"
$Logs = Join-Path $TaskRoot "logs"
New-Item -ItemType Directory -Force -Path $Logs | Out-Null

if (-not (Test-Path -LiteralPath $Python)) {
  throw "Python not found: $Python"
}
if (-not (Test-Path -LiteralPath (Join-Path $Comfy "main.py"))) {
  throw "ComfyUI main.py not found under: $Comfy"
}

$existing = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
  Where-Object { $_.State -eq "Listen" } |
  Select-Object -First 1

if ($existing) {
  [pscustomobject]@{
    status = "already-running"
    port = $Port
    pid = $existing.OwningProcess
    url = "http://127.0.0.1:$Port"
  } | ConvertTo-Json
  exit 0
}

$stdout = Join-Path $Logs "skill-start-comfyui.stdout.log"
$stderr = Join-Path $Logs "skill-start-comfyui.stderr.log"
$args = @("main.py", "--listen", "127.0.0.1", "--port", "$Port", "--disable-auto-launch", "--enable-manager")
$p = Start-Process -FilePath $Python -ArgumentList $args -WorkingDirectory $Comfy -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru

[pscustomobject]@{
  status = "started"
  pid = $p.Id
  port = $Port
  url = "http://127.0.0.1:$Port"
  stdout = $stdout
  stderr = $stderr
} | ConvertTo-Json
