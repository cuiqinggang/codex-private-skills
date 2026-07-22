# Reboot Chain Verification

Use this reference when checking whether the local chain reconnected after
Windows reboot/login, or when the user asks to verify New API, Hermes,
Open WebUI, and Telegram together.

## Scope

This verifies the live chain without changing configuration:

```text
Telegram polling
  -> Windows native Hermes gateway 8642
  -> New API local gateway 3001/v1
  -> upstream model channel

Open WebUI 3000
  -> http://host.docker.internal:8642/v1
  -> Windows native Hermes gateway 8642
```

Do not print `.env`, API keys, Telegram bot tokens, New API tokens, Open WebUI
JWTs, or upstream provider secrets.

## G01 Reboot And Auto-Recovery Evidence

Purpose: prove whether this is a fresh reboot/login test and whether the
auto-recovery wrapper completed.

${REDACTED_SECRET}

Command:

```powershell
$os = Get-CimInstance Win32_OperatingSystem
"NOW=$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))"
"LAST_BOOT=$($os.LastBootUpTime.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
"UPTIME_MINUTES=$([math]::Round(((Get-Date)-$os.LastBootUpTime).TotalMinutes,1))"

${REDACTED_SECRET}
$alive = Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
  Where-Object { $_.CommandLine -like "*$scriptPath*" -and $_.ProcessId -ne $PID }
if ($alive) { $alive | Select-Object ProcessId,CreationDate,CommandLine | Format-List } else { 'NO_AUTORECOVER_PROCESS' }

${REDACTED_SECRET}
"LOG=$log"
if (Test-Path -LiteralPath $log) {
  Get-Item -LiteralPath $log | Select-Object LastWriteTime,Length,FullName | Format-List
  Select-String -LiteralPath $log -Pattern 'auto-recovery start|SUMMARY|FINAL_PASS|FINAL_FAIL|Another HermesNewApiAutoRecover|Telegram smoke PASS' |
    Select-Object -Last 40 |
    ForEach-Object { "{0}:{1}" -f $_.LineNumber,$_.Line }
} else {
  'LOG_MISSING'
}

Get-ScheduledTask -TaskName 'HermesNewApiAutoRecover_Logon','HermesGatewayWatchdog_Logon' -ErrorAction SilentlyContinue |
  ForEach-Object {
    $info = Get-ScheduledTaskInfo -TaskName $_.TaskName
    [PSCustomObject]@{
      TaskName=$_.TaskName
      State=$_.State
      LastRunTime=$info.LastRunTime
      LastTaskResult=$info.LastTaskResult
      Action=(($_.Actions | ForEach-Object { ($_.Execute + ' ' + $_.Arguments).Trim() }) -join ' || ')
    }
  } | Format-List
```

Success criteria:

- `LAST_BOOT` is after the user's reboot if this is a reboot test.
- No stale `Hermes_NewAPI_AutoRecover.ps1` process remains after recovery.
- The current-day autorecovery log contains a fresh `SUMMARY ...` and
  `FINAL_PASS Hermes New API Telegram auto-recovery complete`.
- If the scheduled task is `Disabled`, do not treat Task Scheduler as the
  active recovery path; verify the Startup-folder fallback separately.

Known 2026-05-22 evidence:

- A post-login instance once hung after invoking the Hermes launcher and held
  the mutex, causing later runs to print `Another HermesNewApiAutoRecover
  instance is already running`.
- After stopping only that stuck wrapper process, the default autorecovery
  check completed with `FINAL_PASS`.
- `HermesNewApiAutoRecover_Logon` was observed as `Disabled`; the effective
  path was the Startup-folder fallback.

## G02 Runtime Ports And HTTP Health

Purpose: prove New API, Hermes, Open WebUI, and proxy listeners are up.

${REDACTED_SECRET}

Command:

```powershell
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'

$rows = foreach ($port in @(3001,8642,3000,7890)) {
  $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($conn) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
    [PSCustomObject]@{Port=$port;Pid=$conn.OwningProcess;Process=$proc.Name;CommandLine=$proc.CommandLine}
  } else {
    [PSCustomObject]@{Port=$port;Pid='';Process='';CommandLine='NOT_LISTENING'}
  }
}
$rows | Format-List

$checks = @(
  @{Name='New API UI'; Uri='http://127.0.0.1:3001'; Accept=@(200); Contains=''},
  @{Name='New API models no-token'; Uri='http://127.0.0.1:3001/v1/models'; Accept=@(401); Contains=''},
  @{Name='Hermes health'; Uri='http://127.0.0.1:8642/health'; Accept=@(200); Contains='hermes-agent'},
  @{Name='Hermes models'; Uri='http://127.0.0.1:8642/v1/models'; Accept=@(200); Contains='hermes-agent'},
  @{Name='Open WebUI'; Uri='http://127.0.0.1:3000'; Accept=@(200); Contains=''}
)
foreach ($c in $checks) {
  try {
    $resp = Invoke-WebRequest -Uri $c.Uri -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
    $status = [int]$resp.StatusCode
    $content = [string]$resp.Content
    $containsOk = if ($c.Contains) { $content -like "*$($c.Contains)*" } else { $true }
    [PSCustomObject]@{Name=$c.Name; Status=$status; Expected=($c.Accept -join '/'); Contains=$c.Contains; Pass=(($c.Accept -contains $status) -and $containsOk); Length=$content.Length; Error=''}
  } catch {
    $status = $null
    if ($_.Exception.Response) { try { $status = [int]$_.Exception.Response.StatusCode } catch {} }
    [PSCustomObject]@{Name=$c.Name; Status=$status; Expected=($c.Accept -join '/'); Contains=$c.Contains; Pass=($null -ne $status -and ($c.Accept -contains $status)); Length=0; Error=$_.Exception.Message}
  }
} | Format-Table -AutoSize
```

Success criteria:

- `new-api`, `new-api-postgres`, `new-api-redis`, and `open-webui-clean` are
  running and healthy.
- `new-api` maps only `127.0.0.1:3001->3000/tcp`.
- PostgreSQL and Redis expose no host ports.
- Hermes `8642` is owned by a Windows native Hermes process under
  `H:\Hermes_Windows_Native_014`.
- New API UI returns `200`; New API `/v1/models` returns expected `401`
  without a token; Hermes `/health` and `/v1/models` return `200`; Open WebUI
  returns `200`.

## G03 Telegram Polling And Bot API

Purpose: prove Telegram is configured, polling, and reachable through the local
proxy without exposing the bot token.

${REDACTED_SECRET}

Command:

```powershell
${REDACTED_SECRET}

${REDACTED_SECRET}
$tokenLine = Select-String -LiteralPath $envPath -Pattern '^TELEGRAM_BOT_TOKEN=' -ErrorAction Stop | Select-Object -First 1
$token = $tokenLine.Line -replace '^TELEGRAM_BOT_TOKEN=', ''
$proxy = 'http://127.0.0.1:7890'

$me = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getMe" -Proxy $proxy -TimeoutSec 30
[PSCustomObject]@{Check='getMe'; Ok=$me.ok; Username=$me.result.username; Id=$me.result.id; IsBot=$me.result.is_bot} | Format-List

$wh = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getWebhookInfo" -Proxy $proxy -TimeoutSec 30
[PSCustomObject]@{Check='getWebhookInfo'; Ok=$wh.ok; UrlEmpty=([string]::IsNullOrEmpty($wh.result.url)); PendingUpdateCount=$wh.result.pending_update_count; LastErrorDate=$wh.result.last_error_date; LastErrorMessage=$wh.result.last_error_message} | Format-List
```

Success criteria:

- Telegram diagnostic prints `Result: PASS`.
- `gateway_state.json` has `api_server=connected` and `telegram=connected`.
- `getMe.ok=True` and bot username is `u314156_openclaw_bot`.
- `getWebhookInfo.url` is empty for polling mode.

## G04 Automated Recovery Smoke

Purpose: prove the recovery script can complete its own gates in the current
state and optionally send a single Telegram outbound smoke message.

${REDACTED_SECRET}

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

- Exit code is `0`.
- Output contains `Telegram smoke PASS message_id=...`.
- Output contains `SUMMARY docker=True new_api=True open_webui=True hermes=True basic=True telegram=True`.
- Output contains `FINAL_PASS Hermes New API Telegram auto-recovery complete`.
- After completion, no `Hermes_NewAPI_AutoRecover.ps1` process remains.

Use `-TelegramSmoke` only for manual validation. The automatic login run should
not send Telegram messages.

## G05 Direct Hermes To New API Model Probe

Purpose: prove the chain is not merely listening; Hermes can call New API and
receive a model response.

${REDACTED_SECRET}

Command:

```powershell
$marker = 'HERMES_E2E_OK_' + (Get-Date -Format 'HHmmss')
$body = @{
  model = 'hermes-agent'
  messages = @(@{ role = 'user'; content = "Please answer only: $marker" })
  stream = $false
} | ConvertTo-Json -Depth 8

$resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/chat/completions' `
  -Method Post -ContentType 'application/json' -Body $body `
  -UseBasicParsing -TimeoutSec 240

$json = $resp.Content | ConvertFrom-Json
$content = [string]$json.choices[0].message.content
[PSCustomObject]@{
  Status=[int]$resp.StatusCode
  ContentLength=$content.Length
  ContainsMarker=($content -like "*$marker*")
  Preview=($content.Substring(0,[Math]::Min(160,$content.Length)))
} | Format-List
```

Success criteria:

- HTTP status is `200`.
- Response content contains the marker.
${REDACTED_SECRET}
- `docker logs new-api` shows a recent `/v1/chat/completions` `200` relay and
  `record consume log`.

Known 2026-05-22 evidence:

- Marker `HERMES_E2E_OK_1804` returned with HTTP `200`, content length `18`.
- New API recorded `/v1/chat/completions` `200`.
- Hermes `agent.log` recorded `Turn ended ... response_len=18`.

## G06 Open WebUI Optional API Probe

Use this only when the user specifically needs Open WebUI API proof or when
browser chat still appears broken after G02-G05 pass. Follow
`references/hermes-openwebui-chain.md` G06 and keep the short-lived JWT only in
the PowerShell process. Do not print the JWT.

## Interpreting Results

Fully connected current-state proof requires G02, G03, G04, and G05 to pass.

Fresh reboot proof additionally requires G01 to show `LAST_BOOT` after the
user's reboot and a fresh current-day `FINAL_PASS` from the auto-recovery log.

Do not claim reboot persistence from a same-session retest. Say explicitly when
the system has not been rebooted since the last test.

Known risk to preserve until fixed: `HermesNewApiAutoRecover_Logon` may be
`Disabled`; the Startup-folder fallback can still work, but Task Scheduler is
not providing the recovery path in that state.
