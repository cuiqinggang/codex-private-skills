# Windows Native Hermes 0.14 Telegram Runbook

This runbook restores the durable Telegram bridge for Windows native Hermes 0.14 on this machine.

## Scope

- Use Windows native Hermes under `H:\Hermes_Windows_Native_014`.
${REDACTED_SECRET}
- Use Telegram long polling through Hermes gateway.
- Preserve user files and old WSL cleanup history.
- Do not print or store Telegram bot tokens in notes, plans, or chat.

## G01 - Baseline

Purpose: verify the current Hermes and Telegram state before writing anything.

${REDACTED_SECRET}

Command:

```powershell
$Hermes = "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe"
& $Hermes gateway status --deep
${REDACTED_SECRET}
  Select-Object pid, argv, active_agents, platforms
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
```

Success criteria:

- Gateway process exists.
- `/health` returns HTTP 200 with `platform=hermes-agent`.
- `/v1/models` returns `hermes-agent`.
- Open WebUI returns HTTP 200.

Failure criteria:

- Port 8642 is owned by a non-Hermes process.
- `gateway_state.json` is missing or has failed platforms.
- HTTP checks fail.

Failure recovery:

- Start from the normal Hermes launcher:

```powershell
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

Continue or stop: continue if API and WebUI are healthy; stop if 8642 is owned by an unknown process.

## G02 - Telegram API Health

Purpose: prove the Telegram bot token is valid and polling mode is available.

Execution location: PowerShell

Command:

```powershell
$Token = $env:TELEGRAM_BOT_TOKEN
if (-not $Token) {
${REDACTED_SECRET}
}
$Proxy = "http://127.0.0.1:7890"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/getMe" -Proxy $Proxy -TimeoutSec 20 |
  Select-Object ok, result
Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/getWebhookInfo" -Proxy $Proxy -TimeoutSec 20 |
  Select-Object ok, result
```

Success criteria:

- `getMe.ok` is true.
- Bot username is `u314156_openclaw_bot`.
- `getWebhookInfo.result.url` is empty for long polling.

Failure criteria:

- Unauthorized means token is wrong or revoked.
- A non-empty webhook URL can conflict with polling.
- Network timeout means local proxy or direct Telegram route is unavailable.

Failure recovery:

- If unauthorized, ask the user to rotate/provide a new token.
- If webhook is set and polling is intended, clear it with Telegram `deleteWebhook` only after user confirmation.
- If network timeout occurs, verify FlClash/Core or another local proxy on `127.0.0.1:7890`.

Continue or stop: continue only if token and network are healthy.

## G03 - Backup Before Writes

Purpose: preserve live Hermes config and state before edits.

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
Get-ChildItem -LiteralPath $Backup | Select-Object Name, Length
```

Success criteria: backup directory contains the available files.

Failure criteria: backup cannot be created or files cannot be read.

Failure recovery: fix permissions or choose a user-writable backup path.

Continue or stop: stop if backup cannot be created before config writes.

## G04 - Persist Telegram Configuration

Purpose: make the Telegram bridge survive Hermes restart and Windows login.

Execution location: PowerShell

Command:

```powershell
$env:TG_TOKEN = "<TOKEN_FROM_USER_OR_SECURE_SOURCE>"
$env:TG_CHAT_ID = "6164003953"
& "H:\Hermes_Windows_Native_014\venv\Scripts\python.exe" - <<'PY'
import os
from hermes_cli.config import save_env_value

token = os.environ["TG_TOKEN"]
chat_id = os.environ["TG_CHAT_ID"]
save_env_value("TELEGRAM_BOT_TOKEN", token)
save_env_value("TELEGRAM_ALLOWED_USERS", chat_id)
save_env_value("TELEGRAM_HOME_CHANNEL", chat_id)
save_env_value("TELEGRAM_PROXY", "http://127.0.0.1:7890")
PY
${REDACTED_SECRET}
  ForEach-Object { $_.Line -replace "^(TELEGRAM_BOT_TOKEN=).+","$1<REDACTED>" }
```

Success criteria:

- `.env` contains the four Telegram keys.
- Token is redacted in terminal output.
- `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_HOME_CHANNEL` are `6164003953`.
- `TELEGRAM_PROXY` is `http://127.0.0.1:7890`.

Failure criteria:

- Token is printed.
- PowerShell variables are not passed to Python.
- `.env` is not writable.

Failure recovery:

- Use `$env:TG_TOKEN`, not only local `$TG_TOKEN`, when calling Python.
- Restore `.env` from G03 backup if a bad write occurs.

Continue or stop: continue after verifying only intended keys changed.

## G05 - Restart Gateway

Purpose: force Hermes to load the persisted Telegram configuration.

Execution location: PowerShell

Command:

```powershell
$Hermes = "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe"
& $Hermes gateway stop
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
Start-Sleep -Seconds 10
${REDACTED_SECRET}
  Select-Object pid, platforms
${REDACTED_SECRET}
  Select-String -Pattern "telegram|Connected to Telegram|Proxy detected|response ready|Sending response"
```

Success criteria:

- `gateway_state.json` shows `api_server=connected` and `telegram=connected`.
- Logs include `Proxy detected` and `Connected to Telegram (polling mode)`.
- Open WebUI still returns HTTP 200.

Failure criteria:

- `telegram connect timed out after 30s`.
- `Primary api.telegram.org connection failed`.
- Gateway runs with only one platform.

Failure recovery:

- Verify proxy listener:

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 7890 -State Listen
Get-Process FlClash,FlClashCore -ErrorAction SilentlyContinue
```

- If proxy is up but first connection times out, wait for the reconnection watcher; this incident connected on retry.
- If direct network is healthy and proxy is down, remove `TELEGRAM_PROXY` only after testing direct `getMe`.

Continue or stop: continue only after Telegram is connected.

## G06 - Login Autostart

Purpose: avoid daily manual reconnection.

Execution location: PowerShell

Command:

```powershell
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" gateway install
```

Success criteria:

- Scheduled Task `Hermes_Gateway` is installed, or Hermes reports a login/startup entry.

Known failure:

${REDACTED_SECRET}
- Hermes 0.14 fallback code did not recognize this localized access-denied string.

Fallback command:

```powershell
& "H:\Hermes_Windows_Native_014\venv\Scripts\python.exe" - <<'PY'
from hermes_cli.gateway_windows import get_task_script_path, _install_startup_entry
path = _install_startup_entry(get_task_script_path())
print(path)
PY
${REDACTED_SECRET}
Start-Sleep -Seconds 10
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" gateway status --deep
```

Success criteria:

- `status --deep` reports `Windows login item installed`.
${REDACTED_SECRET}
- Manual run of the startup entry results in gateway running with Telegram connected.

Failure recovery:

- If true Scheduled Task is required, rerun from elevated/admin PowerShell.
- If Startup folder is blocked, ask before changing Windows security policy.

Continue or stop: continue after status reports login item installed and gateway running.

## G07 - End-to-End Telegram Test

Purpose: prove both outbound and inbound paths.

Execution location: PowerShell and Telegram Desktop.

Outbound command:

```powershell
${REDACTED_SECRET}
$Body = @{
  chat_id = "6164003953"
  text = "Hermes Telegram smoke test $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}
Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/sendMessage" -Method Post -Body $Body -Proxy "http://127.0.0.1:7890" -TimeoutSec 30 |
  Select-Object ok, result
```

Inbound test:

- Open `tg://resolve?domain=u314156_openclaw_bot`.
- Send a short message from the user's Telegram account.
- Watch gateway logs.

Verification command:

```powershell
${REDACTED_SECRET}
  Select-String -Pattern "inbound message|response ready|Sending response|Connected to Telegram"
```

Success criteria:

- Bot API `sendMessage` returns `ok=true`.
- Logs include `inbound message` for chat `6164003953`.
- Logs include `response ready` and `Sending response`.
- Telegram Desktop shows the bot reply.

Failure criteria:

- Bot can send but Hermes does not receive inbound messages.
- Hermes receives inbound but never logs `response ready`.
- Telegram reply is not delivered after `Sending response`.

Failure recovery:

- For no inbound: check allowlist and polling/webhook state.
- For no response: check Hermes model/API server layer.
- For no delivery: check Telegram API/proxy and bot token state.

Continue or stop: stop only after full end-to-end evidence is captured.

## External References

- Telegram Bot API: `https://core.telegram.org/bots/api`
- Hermes Telegram setup: `https://hermes-agent.ai/blog/hermes-agent-telegram-setup`
- Hermes Windows native guide: `https://hermes-agent.nousresearch.com/docs/user-guide/windows-native`
