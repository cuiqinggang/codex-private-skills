param(
  [string]$OutputDirectory = (Join-Path (Get-Location) "windows-hermes-healthcheck")
)

$ErrorActionPreference = "SilentlyContinue"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$HermesHome = "C:\Users\A\.hermes"
$EnvPath = Join-Path $HermesHome ".env"
$script:ApiServerHeaders = @{}
if (Test-Path -LiteralPath $EnvPath) {
  $apiServerKeyLine = Get-Content -LiteralPath $EnvPath |
    Where-Object { $_ -match "^API_SERVER_KEY=" } |
    Select-Object -First 1
  if ($apiServerKeyLine) {
    $apiServerKey = ($apiServerKeyLine -replace "^API_SERVER_KEY=", "").Trim().Trim('"').Trim("'")
    if ($apiServerKey) {
      $script:ApiServerHeaders = @{ Authorization = "Bearer $apiServerKey" }
    }
  }
}

function Get-PortOwner {
  param([int]$Port)
  $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $conn) {
    return [ordered]@{ port = $Port; listening = $false; pid = $null; process = $null; commandLine = $null }
  }
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
  return [ordered]@{
    port = $Port
    listening = $true
    pid = $conn.OwningProcess
    process = $proc.Name
    commandLine = $proc.CommandLine
  }
}

function Test-Http {
  param([string]$Uri, [int]$TimeoutSec = 8)
  try {
    $requestArgs = @{
      Uri = $Uri
      UseBasicParsing = $true
      TimeoutSec = $TimeoutSec
    }
    if ($script:ApiServerHeaders.Count -gt 0 -and $Uri -like "http://127.0.0.1:8642*") {
      $requestArgs.Headers = $script:ApiServerHeaders
    }
    $res = Invoke-WebRequest @requestArgs
    return [ordered]@{ uri = $Uri; ok = $true; status = [int]$res.StatusCode; bodyPreview = (($res.Content | Out-String).Substring(0, [Math]::Min(300, ($res.Content | Out-String).Length))) }
  } catch {
    return [ordered]@{ uri = $Uri; ok = $false; status = $null; error = $_.Exception.Message }
  }
}

$port8642 = Get-PortOwner -Port 8642
$port3000 = Get-PortOwner -Port 3000
$health = Test-Http -Uri "http://127.0.0.1:8642/health"
$models = Test-Http -Uri "http://127.0.0.1:8642/v1/models"
$webui = Test-Http -Uri "http://127.0.0.1:3000" -TimeoutSec 15

$ownerLooksNative = $false
if ($port8642.commandLine -and $port8642.commandLine -like "*H:\Hermes_Windows_Native_014*") {
  $ownerLooksNative = $true
}

$modelsContainHermes = $false
if ($models.bodyPreview -and $models.bodyPreview -like "*hermes-agent*") {
  $modelsContainHermes = $true
}

$mainlinePass = $port8642.listening -and $health.ok -and $models.ok -and $modelsContainHermes

$report = [ordered]@{
  created_at = (Get-Date).ToString("s")
  mainline = "Windows Native Hermes 8642"
  status = $(if ($mainlinePass) { "PASS" } else { "FAIL" })
  checks = [ordered]@{
    port8642 = $port8642
    ownerLooksNative = $ownerLooksNative
    health = $health
    models = $models
    modelsContainHermes = $modelsContainHermes
  }
  optional_next_stage = [ordered]@{
    port3000 = $port3000
    webui = $webui
  }
  note = "Read-only check. No service was started or stopped. No secret file was read. BIOS, WSL2, Docker, and Open WebUI 3000 do not block the Windows Native Hermes 8642 mainline. Open WebUI 3000 is preserved as an optional/next-stage route."
}

$jsonPath = Join-Path $OutputDirectory "windows-hermes-healthcheck.json"
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

if ($mainlinePass) {
  Write-Output "WINDOWS_HERMES_8642_MAINLINE_PASS"
  Write-Output "WINDOWS_HERMES_HEALTHCHECK_PASS"
} else {
  Write-Output "WINDOWS_HERMES_8642_MAINLINE_FAIL"
  Write-Output "WINDOWS_HERMES_HEALTHCHECK_FAIL"
}
Write-Output $jsonPath
