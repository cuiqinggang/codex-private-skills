param(
  [string]$OutputRoot = 'C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-TO-AUTOSTART-20260524\autostart-runs',
  [switch]$NoBrowser,
  [int]$TimeoutSec = 120
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$AutoStartRoot = 'C:\Users\A\Xiaolongxia_BootReplay_AutoStart'
$ProjectRoot = 'C:\Users\A\xiaolongxia-free-api-local'
$OpenClawCmd = 'C:\Users\A\AppData\Roaming\npm\openclaw.cmd'
$NewApiUrl = 'http://127.0.0.1:3011'
$NewApiApiBase = 'http://127.0.0.1:3011/v1'
$OpenClawUrl = 'http://127.0.0.1:18789/'
$XiaolongxiaTokenFile = Join-Path $ProjectRoot 'secrets\xiaolongxia_newapi_token.txt'
$SelftestScript = Join-Path $ProjectRoot 'scripts\xiaolongxia-nvidia-llm-selftest.ps1'
$LogDir = Join-Path $AutoStartRoot 'logs'

New-Item -ItemType Directory -Force -Path $OutputRoot, $LogDir | Out-Null
$RunId = Get-Date -Format 'yyyyMMdd-HHmmss'
$RunDir = Join-Path $OutputRoot $RunId
New-Item -ItemType Directory -Force -Path $RunDir | Out-Null
$LogPath = Join-Path $LogDir "boot-replay-$RunId.log"

function Write-Log {
  param([string]$Message)
  $line = "$(Get-Date -Format o) $Message"
  Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
  Write-Host $line
}

function Add-Check {
  param(
    [System.Collections.ArrayList]$Checks,
    [string]$Name,
    [bool]$Success,
    [object]$Detail = $null
  )
  [void]$Checks.Add([pscustomobject]@{
    name = $Name
    success = $Success
    detail = $Detail
    timestamp = (Get-Date).ToString('o')
  })
}

function Test-HttpOk {
  param([string]$Url, [int]$Timeout = 15)
  try {
    $r = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec $Timeout
    return [pscustomobject]@{ ok = ($r.StatusCode -ge 200 -and $r.StatusCode -lt 400); status = [int]$r.StatusCode; body = $r.Content; headers = $r.Headers }
  } catch {
    return [pscustomobject]@{ ok = $false; status = $null; error = $_.Exception.Message; body = '' }
  }
}

function Wait-Until {
  param([scriptblock]$Probe, [int]$Seconds, [string]$Name)
  $deadline = (Get-Date).AddSeconds($Seconds)
  $last = $null
  while ((Get-Date) -lt $deadline) {
    $last = & $Probe
    if ($last -and $last.ok) { return $last }
    Start-Sleep -Seconds 3
  }
  throw "Timed out waiting for $Name. Last result: $($last | ConvertTo-Json -Compress -Depth 5)"
}

function Get-ChromePath {
  $candidates = @(
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
    'chrome.exe'
  )
  foreach ($c in $candidates) {
    if (-not $c) { continue }
    if (Test-Path $c) { return $c }
    $cmd = Get-Command $c -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
  }
  return $null
}

$mutex = New-Object System.Threading.Mutex($false, 'Local\XiaolongxiaBootReplayAutostart')
$hasMutex = $false
$checks = New-Object System.Collections.ArrayList

try {
  $hasMutex = $mutex.WaitOne(0)
  if (-not $hasMutex) { throw 'Another Xiaolongxia boot replay run is already active.' }

  Write-Log 'BOOT_REPLAY_START'

  $oldTask = Get-ScheduledTask -TaskName 'Xiaolongxia_Autostart_Logon' -ErrorAction SilentlyContinue
  if ($oldTask -and $oldTask.State -ne 'Disabled') {
    throw 'Unsafe old Xiaolongxia_Autostart_Logon task is not disabled. Aborting.'
  }
  Add-Check $checks 'old_failed_autostart_disabled_or_missing' $true @{ state = if ($oldTask) { [string]$oldTask.State } else { 'missing' } }

  $newApiProbe = Test-HttpOk "$NewApiUrl/api/status"
  if (-not $newApiProbe.ok) {
    Write-Log 'New API not healthy, starting docker compose.'
    Push-Location $ProjectRoot
    try {
      & docker compose up -d | Out-File -LiteralPath (Join-Path $RunDir 'docker-compose-up.log') -Encoding UTF8
      if ($LASTEXITCODE -ne 0) { throw "docker compose up failed with exit code $LASTEXITCODE" }
    } finally {
      Pop-Location
    }
  }

  $newApiReady = Wait-Until -Name 'New API 3011' -Seconds $TimeoutSec -Probe { Test-HttpOk "$NewApiUrl/api/status" }
  Add-Check $checks 'newapi_3011_status' $true @{ url = "$NewApiUrl/api/status"; status = $newApiReady.status }

  $newApiHome = Test-HttpOk $NewApiUrl
  $title = [regex]::Match([string]$newApiHome.body, '<title>(.*?)</title>').Groups[1].Value
  if (-not $newApiHome.ok -or $title -ne 'New API') { throw "3011 identity check failed. Title=$title" }
  Add-Check $checks 'newapi_identity_not_xiaolongxia_ui' $true @{ url = $NewApiUrl; title = $title; marker = '3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI' }

  if (-not (Test-Path $XiaolongxiaTokenFile)) { throw 'Xiaolongxia New API token file missing.' }
  $token = (Get-Content -Raw -LiteralPath $XiaolongxiaTokenFile).Trim()
  if (-not $token) { throw 'Xiaolongxia New API token file is empty.' }
  $modelsResponse = Invoke-WebRequest -UseBasicParsing -Uri "$NewApiApiBase/models" -Headers @{ Authorization = "Bearer $token" } -TimeoutSec 30
  $modelsJson = $modelsResponse.Content | ConvertFrom-Json
  $modelCount = @($modelsJson.data).Count
  if ($modelsResponse.StatusCode -ne 200 -or $modelCount -lt 1) { throw 'Model pool /v1/models check failed.' }
  Add-Check $checks 'model_pool_models' $true @{ url = "$NewApiApiBase/models"; status = [int]$modelsResponse.StatusCode; model_count = $modelCount }

  if (-not (Test-Path $SelftestScript)) { throw 'Internal LLM selftest script missing.' }
  $selftestOut = Join-Path $RunDir 'internal-llm-selftest-auto'
  & $SelftestScript -ModelMode auto -OutputRoot $selftestOut -TimeoutSec 60 | Tee-Object -FilePath (Join-Path $RunDir 'internal-llm-selftest-auto.log') | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Internal LLM selftest failed with exit code $LASTEXITCODE" }
  Add-Check $checks 'internal_llm_auto_selftest' $true @{ output = $selftestOut }

  $tcp = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 18789 -State Listen -ErrorAction SilentlyContinue
  if (-not $tcp) {
    Write-Log 'OpenClaw gateway not listening, starting foreground gateway in hidden process.'
    $stdout = Join-Path $LogDir "openclaw-gateway-$RunId.stdout.log"
    $stderr = Join-Path $LogDir "openclaw-gateway-$RunId.stderr.log"
    Start-Process -FilePath $OpenClawCmd -ArgumentList @('gateway','run','--allow-unconfigured','--bind','loopback','--port','18789','--verbose') -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr | Out-Null
  }

  $gatewayHealth = Wait-Until -Name 'OpenClaw gateway health' -Seconds $TimeoutSec -Probe {
    try {
      $raw = & $OpenClawCmd gateway health --json --timeout 20000 2>$null
      $j = $raw | ConvertFrom-Json
      [pscustomobject]@{ ok = ($j.ok -eq $true); health = $j }
    } catch {
      [pscustomobject]@{ ok = $false; error = $_.Exception.Message }
    }
  }
  Add-Check $checks 'openclaw_gateway_health' $true @{ ok = $gatewayHealth.health.ok; default_agent = $gatewayHealth.health.defaultAgentId }

  $openclawHome = Test-HttpOk $OpenClawUrl
  $openclawTitle = [regex]::Match([string]$openclawHome.body, '<title>(.*?)</title>').Groups[1].Value
  if (-not $openclawHome.ok -or $openclawTitle -ne 'OpenClaw Control') { throw "18789 identity check failed. Title=$openclawTitle" }
  Add-Check $checks 'openclaw_18789_identity' $true @{ url = $OpenClawUrl; title = $openclawTitle }

  if (-not $NoBrowser) {
    $chrome = Get-ChromePath
    if (-not $chrome) { throw 'Google Chrome not found for browser open.' }
    Start-Process -FilePath $chrome -ArgumentList $OpenClawUrl
    Add-Check $checks 'browser_open_openclaw_control' $true @{ browser = $chrome; url = $OpenClawUrl; opened_3011 = $false; opened_hermes = $false }
  } else {
    Add-Check $checks 'browser_open_openclaw_control' $true @{ skipped = $true; reason = 'NoBrowser switch' }
  }

  $status = 'BOOT_REPLAY_AUTOSTART_RUN_PASS'
  $exitCode = 0
} catch {
  $status = 'BOOT_REPLAY_AUTOSTART_RUN_FAIL'
  $exitCode = 1
  Add-Check $checks 'fatal_error' $false @{ message = $_.Exception.Message }
  Write-Log "ERROR $($_.Exception.Message)"
} finally {
  $summary = [pscustomobject]@{
    status = $status
    generated_at = (Get-Date).ToString('o')
    run_id = $RunId
    newapi_url = $NewApiUrl
    api_base = $NewApiApiBase
    openclaw_url = $OpenClawUrl
    opened_3011_as_xiaolongxia_ui = $false
    opened_hermes = $false
    real_group_send = $false
    key_printed = $false
    checks = $checks
    log = $LogPath
  }
  $summary | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $RunDir 'boot-replay-summary.json') -Encoding UTF8
  $md = @(
    '# Xiaolongxia Boot Replay Autostart Run',
    '',
    ('Status: ' + $status),
    '',
    ('- New API: `' + $NewApiUrl + '`'),
    ('- API Base: `' + $NewApiApiBase + '`'),
    ('- OpenClaw browser: `' + $OpenClawUrl + '`'),
    '- 3011 marker: 3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI',
    '- Opened Hermes: false',
    '- Real group send: false',
    '- Key printed: false',
    '',
    '## Checks'
  )
  foreach ($c in $checks) {
    $md += "- $($c.name): $(if($c.success){'PASS'}else{'FAIL'})"
  }
  $md | Set-Content -LiteralPath (Join-Path $RunDir 'boot-replay-summary.md') -Encoding UTF8
  Write-Log $status
  if ($hasMutex) { [void]$mutex.ReleaseMutex() }
  $mutex.Dispose()
}

exit $exitCode
