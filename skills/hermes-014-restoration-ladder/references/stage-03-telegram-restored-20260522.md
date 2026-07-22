# Stage 03 Telegram Restored - 2026-05-22

Use this reference to replay the Telegram-only P3 restore from the P1/P2 stable
baseline.

## Stage Boundary

- Previous baseline: `references/p1p2-stable-baseline-20260522.md`
- New stage: Telegram live bridge restored through Windows native Hermes 0.14
- Not included: New API, Postgres, Redis, Watchdog, AutoRecover, login autostart
- Persistence level: live manual gateway process only
- Related Telegram skill note:
${REDACTED_SECRET}

Do not infer New API or reboot persistence from this stage.

## Root Cause

The P1/P2 minimal baseline intentionally disabled Telegram persistence in
${REDACTED_SECRET}

```text
#DISABLED_MINIMAL# TELEGRAM_BOT_TOKEN=<redacted>
#DISABLED_MINIMAL# TELEGRAM_ALLOWED_USERS=6164003953
#DISABLED_MINIMAL# TELEGRAM_HOME_CHANNEL=6164003953
#DISABLED_MINIMAL# TELEGRAM_PROXY=http://127.0.0.1:7890
```

Restoring Telegram required active non-commented keys with the same values. The
bot token must never be printed into chat, reports, or skill files.

## Final State

- Hermes 8642: healthy
- Direct Hermes chat marker: `HERMES_P3_TELEGRAM_FINAL_OK`
- Open WebUI 3000: healthy
- Telegram bridge: connected through Windows native Hermes gateway
- Telegram mode: long polling
- Telegram bot username: `u314156_openclaw_bot`
- Telegram home chat: `6164003953`
- Telegram proxy: `http://127.0.0.1:7890`
- Docker running: `open-webui-clean`
- `HermesGatewayWatchdog_Logon`: Disabled
- `HermesNewApiAutoRecover_Logon`: Disabled
- `HermesTelegramGateway_Autostart`: not found
- `HermesTelegramGateway_Watchdog`: not found
- `Hermes_Gateway`: not found
- Startup entry: absent

## Evidence

Run directory:

```text
${REDACTED_SECRET}
```

Files:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Final verification at `2026-05-22 19:19:36 +08:00`:

- `gateway_state.json`: `api_server=connected`, `telegram=connected`
- `http://127.0.0.1:8642/health`: HTTP 200
- `http://127.0.0.1:8642/v1/models`: HTTP 200
- Direct Hermes chat returned `HERMES_P3_TELEGRAM_FINAL_OK`
- `http://127.0.0.1:3000`: HTTP 200
- Telegram Bot API `getMe`: `ok=true`
- Telegram webhook: empty
- Outbound marker sent: `HERMES_P3_TG_OUTBOUND_20260522_191534`
- Inbound live proof from Telegram Desktop:
  - `2026-05-22 19:16:32`: inbound message from chat `6164003953`
  - `2026-05-22 19:16:38`: response ready and sent
  - `2026-05-22 19:17:05`: second inbound message from chat `6164003953`
  - `2026-05-22 19:17:09`: response ready and sent

## Replay Gates

### G01 - Baseline Health

Purpose: prove P1/P2 is healthy before adding Telegram.

${REDACTED_SECRET}

Command:

```powershell
${REDACTED_SECRET}
$State | Select-Object pid, active_agents, platforms
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Success criteria:

- `api_server` is `connected`.
- `/health` and `/v1/models` return HTTP 200.
- Open WebUI returns HTTP 200.
- Docker only needs `open-webui-clean` for this stage.

Failure criteria:

- 8642 or 3000 is not healthy.
- Port 8642 is not owned by the Windows native Hermes gateway.

Failure recovery: restore or compare against the P1/P2 backup before touching
Telegram.

Continue or stop: continue only if P1/P2 is healthy.

### G02 - Backup Before Telegram Writes

Purpose: preserve the live Hermes profile before changing Telegram state.

${REDACTED_SECRET}

Command:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
${REDACTED_SECRET}
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
Get-ChildItem -LiteralPath $Backup | Select-Object Name, Length, LastWriteTime
```

Success criteria: backup contains the available profile files.

Failure criteria: backup cannot be created.

Failure recovery: fix the backup path or permissions before edits.

Continue or stop: stop if backup fails.

### G03 - Restore Telegram Env Keys

Purpose: turn the saved P1/P2 disabled Telegram values into active keys without
printing the token.

Execution location: PowerShell

Command:

```powershell
${REDACTED_SECRET}
$Lines = Get-Content -LiteralPath $EnvPath
$Keys = @("TELEGRAM_BOT_TOKEN","TELEGRAM_ALLOWED_USERS","TELEGRAM_HOME_CHANNEL","TELEGRAM_PROXY")
$Map = @{}
foreach ($Line in $Lines) {
  foreach ($Key in $Keys) {
    if ($Line -like "#DISABLED_MINIMAL# $Key=*") {
      $Map[$Key] = $Line.Substring(("#DISABLED_MINIMAL# $Key=".Length))
    } elseif ($Line -like "$Key=*") {
      $Map[$Key] = $Line.Substring(("$Key=".Length))
    }
  }
}
foreach ($Key in $Keys) {
  if (-not $Map.ContainsKey($Key) -or [string]::IsNullOrWhiteSpace($Map[$Key])) {
    throw "Missing value source for $Key"
  }
}
$env:TG_TOKEN = $Map["TELEGRAM_BOT_TOKEN"]
$env:TG_ALLOWED = $Map["TELEGRAM_ALLOWED_USERS"]
$env:TG_HOME = $Map["TELEGRAM_HOME_CHANNEL"]
$env:TG_PROXY = $Map["TELEGRAM_PROXY"]
& "H:\Hermes_Windows_Native_014\venv\Scripts\python.exe" -c "import os; from hermes_cli.config import save_env_value; save_env_value('TELEGRAM_BOT_TOKEN', os.environ['TG_TOKEN']); save_env_value('TELEGRAM_ALLOWED_USERS', os.environ['TG_ALLOWED']); save_env_value('TELEGRAM_HOME_CHANNEL', os.environ['TG_HOME']); save_env_value('TELEGRAM_PROXY', os.environ['TG_PROXY'])"
Select-String -LiteralPath $EnvPath -Pattern "^TELEGRAM_|^#DISABLED_MINIMAL# TELEGRAM_" |
  ForEach-Object {
    $_.Line -replace "^(TELEGRAM_BOT_TOKEN=).+","$1<REDACTED>" -replace "^(#DISABLED_MINIMAL# TELEGRAM_BOT_TOKEN=).+","$1<REDACTED>"
  }
```

Success criteria:

- Active non-commented `TELEGRAM_*` keys exist.
- Token appears only as `<REDACTED>` in output.
- `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_HOME_CHANNEL` are `6164003953`.
- `TELEGRAM_PROXY` is `http://127.0.0.1:7890`.

Failure criteria:

- Any active value is missing.
- Token prints to terminal, chat, report, or skill file.

Failure recovery: restore `.env` from G02 backup and stop if the token source is
not local and trusted.

Continue or stop: continue only after redacted output is correct.

### G04 - Telegram Bot API Health

Purpose: prove the bot token and polling mode work before restarting Hermes.

Execution location: PowerShell

Command:

```powershell
${REDACTED_SECRET}
$Proxy = "http://127.0.0.1:7890"
$Me = Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/getMe" -Proxy $Proxy -TimeoutSec 30
$Webhook = Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/getWebhookInfo" -Proxy $Proxy -TimeoutSec 30
[pscustomobject]@{
  GetMeOk = $Me.ok
  Username = $Me.result.username
  WebhookOk = $Webhook.ok
  WebhookUrl = if ($Webhook.result.url) { "<NONEMPTY>" } else { "<EMPTY>" }
  PendingUpdateCount = $Webhook.result.pending_update_count
}
```

Success criteria:

- `GetMeOk=True`.
- `Username=u314156_openclaw_bot`.
- `WebhookUrl=<EMPTY>`.

Failure criteria:

- Unauthorized token.
- Non-empty webhook when polling is intended.
- Proxy/network timeout.

Failure recovery:

- Do not rotate the token without user confirmation.
- Do not clear a webhook without user confirmation.
- Verify local proxy on `127.0.0.1:7890` before changing config.

Continue or stop: continue only after Bot API health passes.

### G05 - Restart Manual Gateway

Purpose: reload Telegram config without enabling Watchdog, AutoRecover, Startup,
or scheduled tasks.

Execution location: PowerShell

Command:

```powershell
$Hermes = "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe"
& $Hermes gateway stop
Start-Sleep -Seconds 3
Start-Process -FilePath $Hermes -ArgumentList @("gateway","run","--replace") -WindowStyle Hidden -WorkingDirectory "H:\Hermes_Windows_Native_014"
Start-Sleep -Seconds 15
& $Hermes gateway status --deep
${REDACTED_SECRET}
  Select-Object pid, active_agents, platforms
${REDACTED_SECRET}
  Select-String -Pattern "Proxy detected|Connected to Telegram|Gateway running with 2 platform"
```

Success criteria:

- `gateway_state.json` shows `api_server=connected` and `telegram=connected`.
- Log shows `Proxy detected`.
- Log shows `Connected to Telegram (polling mode)`.
- Log shows `Gateway running with 2 platform(s)`.

Failure criteria:

- Gateway runs with only one platform.
- Telegram connection times out.
- 8642 does not listen after restart.

Failure recovery: inspect the failing layer first; do not start Watchdog or
AutoRecover as a shortcut.

Continue or stop: continue only after both platforms are connected.

### G06 - End-to-End Verification

Purpose: prove API, Open WebUI, outbound Telegram, inbound Telegram, and bot
reply all work.

Execution location: PowerShell and Telegram Desktop.

Command:

```powershell
$Health = Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
$Models = Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10
$Body = @{ model="hermes-agent"; messages=@(@{role="user";content="Return exactly HERMES_P3_TELEGRAM_FINAL_OK"}); stream=$false } | ConvertTo-Json -Depth 8
$Chat = Invoke-RestMethod -Uri "http://127.0.0.1:8642/v1/chat/completions" -Method Post -ContentType "application/json" -Body $Body -TimeoutSec 120
$Web = Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
${REDACTED_SECRET}
$Marker = "HERMES_P3_TG_OUTBOUND_$(Get-Date -Format yyyyMMdd_HHmmss)"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/sendMessage" -Method Post -Proxy "http://127.0.0.1:7890" -TimeoutSec 30 -Body @{ chat_id="6164003953"; text=$Marker } |
  Select-Object ok, result
${REDACTED_SECRET}
  Select-String -Pattern "inbound message|response ready|Sending response|Connected to Telegram" |
  Select-Object -Last 40
```

Success criteria:

- Health, models, and Open WebUI return HTTP 200.
- Direct chat returns `HERMES_P3_TELEGRAM_FINAL_OK`.
- Bot API send returns `ok=true`.
- User sends a Telegram Desktop message to the bot.
- Logs show `inbound message`, `response ready`, and `Sending response`.

Failure criteria:

- Bot can send but Hermes does not receive inbound messages.
- Hermes receives inbound but never prepares a response.
- Hermes prepares a response but Telegram does not deliver it.

Failure recovery:

- No inbound: check polling/webhook and allowlist.
- No response: check Hermes API/model layer.
- No delivery: check Telegram Bot API/proxy.

Continue or stop: stop after fresh end-to-end evidence is captured.

## Reuse Rule

When continuing from this stage:

1. Treat this as the known-good P3 Telegram live baseline.
2. Do not infer reboot persistence from this state.
3. Do not start New API, Watchdog, AutoRecover, or scheduled-task persistence unless the user explicitly asks for that next stage.
4. If Telegram fails again, use `hermes-telegram-persistent-bridge` first and read `references/p3-telegram-restored-20260522.md`.

## Rollback

Restore files from:

```text
${REDACTED_SECRET}
```

Then restart Hermes gateway and rerun:

```powershell
${REDACTED_SECRET}
```
