param(
  [string]$HermesRoot = "K:\Hermes_Windows_Native_014",
  [string]$HermesHome = "C:\Users\A\.hermes",
  [string]$ApiBase = "http://127.0.0.1:8642",
  [string]$WebUi = "http://127.0.0.1:3000",
  [string]$ProxyHost = "127.0.0.1",
  [int]$ProxyPort = 7890,
  [switch]$RequireWebUi
)

$ErrorActionPreference = "Continue"
$failures = New-Object System.Collections.Generic.List[string]

function Add-Check {
  param([string]$Name, [bool]$Ok, [string]$Detail)
  $status = if ($Ok) { "PASS" } else { "FAIL" }
  "{0,-34} {1} {2}" -f $Name, $status, $Detail
  if (-not $Ok) { $script:failures.Add($Name) | Out-Null }
}

function Test-Url {
  param([string]$Name, [string]$Url)
  try {
    $requestArgs = @{
      Uri = $Url
      UseBasicParsing = $true
      TimeoutSec = 10
    }
    if ($script:ApiServerHeaders.Count -gt 0 -and $Url -like "$ApiBase*") {
      $requestArgs.Headers = $script:ApiServerHeaders
    }
    $response = Invoke-WebRequest @requestArgs
    Add-Check $Name ($response.StatusCode -eq 200) ("HTTP " + [int]$response.StatusCode + " len=" + $response.Content.Length)
  } catch {
    Add-Check $Name $false $_.Exception.Message
  }
}

function Test-OptionalUrl {
  param([string]$Name, [string]$Url)
  try {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 10
    "{0,-34} {1} {2}" -f $Name, "PASS", ("HTTP " + [int]$response.StatusCode + " len=" + $response.Content.Length)
  } catch {
    "{0,-34} {1} {2}" -f $Name, "SKIP", ($_.Exception.Message + " (optional next-stage; does not block Hermes 8642 or Telegram mainline)")
  }
}

$HermesExe = Join-Path $HermesRoot "venv\Scripts\hermes.exe"
$EnvPath = Join-Path $HermesHome ".env"
$StatePath = Join-Path $HermesHome "gateway_state.json"
$LogPath = Join-Path $HermesHome "logs\gateway.log"
$StartupCmdPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd"
$StartupHiddenVbsPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway_Hidden.vbs"
$TaskScriptPath = Join-Path $HermesHome "gateway-service\Hermes_Gateway.cmd"
$env:HERMES_HOME = $HermesHome
$env:HOME = Split-Path -Parent $HermesHome
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

"Hermes Telegram diagnostic"
"Timestamp: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
""

Add-Check "Hermes CLI exists" (Test-Path -LiteralPath $HermesExe) $HermesExe
Add-Check "Hermes profile exists" (Test-Path -LiteralPath $HermesHome) $HermesHome
Add-Check "Telegram env file exists" (Test-Path -LiteralPath $EnvPath) $EnvPath

if (Test-Path -LiteralPath $EnvPath) {
  $envLines = Get-Content -LiteralPath $EnvPath
  $telegramLines = $envLines | Where-Object { $_ -match "^TELEGRAM_" }
  $redacted = $telegramLines | ForEach-Object { $_ -replace "^(TELEGRAM_BOT_TOKEN=).+","`$1<REDACTED>" }
  "Telegram env keys:"
  if ($redacted) { $redacted } else { "  <none>" }
  Add-Check "TELEGRAM_BOT_TOKEN" (($telegramLines | Where-Object { $_ -match "^TELEGRAM_BOT_TOKEN=.+" }).Count -gt 0) "present expected"
  Add-Check "TELEGRAM_ALLOWED_USERS" (($telegramLines | Where-Object { $_ -eq "TELEGRAM_ALLOWED_USERS=6164003953" }).Count -gt 0) "expected 6164003953"
  Add-Check "TELEGRAM_HOME_CHANNEL" (($telegramLines | Where-Object { $_ -eq "TELEGRAM_HOME_CHANNEL=6164003953" }).Count -gt 0) "expected 6164003953"
  Add-Check "TELEGRAM_PROXY" (($telegramLines | Where-Object { $_ -eq "TELEGRAM_PROXY=http://127.0.0.1:7890" }).Count -gt 0) "expected http://127.0.0.1:7890"
}

""
"Gateway status:"
if (Test-Path -LiteralPath $HermesExe) {
  try {
    & $HermesExe gateway status --deep
    Add-Check "gateway status command" ($LASTEXITCODE -eq 0) ("exit=" + $LASTEXITCODE)
  } catch {
    Add-Check "gateway status command" $false $_.Exception.Message
  }
}

""
Add-Check "gateway_state.json exists" (Test-Path -LiteralPath $StatePath) $StatePath
if (Test-Path -LiteralPath $StatePath) {
  try {
    $state = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    $apiState = $state.platforms.api_server.state
    $telegramState = $state.platforms.telegram.state
    Add-Check "state api_server connected" ($apiState -eq "connected") ("state=" + $apiState)
    Add-Check "state telegram connected" ($telegramState -eq "connected") ("state=" + $telegramState)
    Add-Check "state pid present" ([bool]$state.pid) ("pid=" + $state.pid)
  } catch {
    Add-Check "gateway_state parse" $false $_.Exception.Message
  }
}

""
try {
  $proxy = Get-NetTCPConnection -LocalAddress $ProxyHost -LocalPort $ProxyPort -State Listen -ErrorAction Stop | Select-Object -First 1
  Add-Check "local proxy listener" $true ($ProxyHost + ":" + $ProxyPort + " pid=" + $proxy.OwningProcess)
} catch {
  Add-Check "local proxy listener" $false ($ProxyHost + ":" + $ProxyPort + " not listening")
}

""
Test-Url "Hermes health endpoint" ($ApiBase + "/health")
Test-Url "Hermes models endpoint" ($ApiBase + "/v1/models")
if ($RequireWebUi) {
  Test-Url "Open WebUI" $WebUi
} else {
  Test-OptionalUrl "Open WebUI" $WebUi
}

""
Add-Check "gateway task script" (Test-Path -LiteralPath $TaskScriptPath) $TaskScriptPath
$startupEntryOk = (Test-Path -LiteralPath $StartupCmdPath) -or (Test-Path -LiteralPath $StartupHiddenVbsPath)
$startupEntryDetail = if (Test-Path -LiteralPath $StartupHiddenVbsPath) { $StartupHiddenVbsPath } else { $StartupCmdPath }
Add-Check "startup entry" $startupEntryOk $startupEntryDetail

""
if (Test-Path -LiteralPath $LogPath) {
  "Recent Telegram log evidence:"
  Get-Content -LiteralPath $LogPath -Tail 160 |
    Select-String -Pattern "telegram|Connected to Telegram|Proxy detected|inbound message|response ready|Sending response|connect timed out|Primary api.telegram.org" |
    Select-Object -Last 30 |
    ForEach-Object {
      $_.Line -replace "([0-9]{8,12}:[A-Za-z0-9_-]{20,})","<REDACTED_BOT_TOKEN>"
    }
} else {
  Add-Check "gateway log exists" $false $LogPath
}

""
if ($failures.Count -gt 0) {
  "Result: FAIL"
  "Failed checks: " + ($failures -join ", ")
  exit 1
}

"Result: PASS"
exit 0
