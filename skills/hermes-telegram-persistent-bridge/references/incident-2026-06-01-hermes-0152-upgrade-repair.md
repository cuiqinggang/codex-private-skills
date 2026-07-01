# Incident 2026-06-01 - Hermes 0.15.2 Telegram Bridge Recovery

This is the Telegram-side companion to the Windows Hermes 0.15.2 upgrade repair.
Use it when Telegram stopped after a Hermes upgrade, especially if the Hermes
CLI was repaired in place from 0.14.x to 0.15.2.

## Key Change In 0.15.2

`API_SERVER_KEY` is now required for the local API server. Telegram can connect
successfully while local health scripts still fail if they call `/v1/models`
without:

```powershell
@{ Authorization = "Bearer $ApiServerKey" }
```

Therefore Telegram diagnostics for this machine must read
`C:\Users\A\.hermes\.env`, redact all secrets, and use the bearer token only in
local HTTP request headers.

## Recovery Checklist

1. Confirm Hermes itself is healthy first. If the CLI fails with
   `ModuleNotFoundError: No module named 'hermes_cli.main'`, use
   `windows-hermes-operations/references/incident-2026-06-01-hermes-0152-upgrade-repair.md`.
2. Run the Telegram diagnostic:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

3. Confirm `.env` contains, without printing secrets:

```text
TELEGRAM_BOT_TOKEN=<present>
TELEGRAM_ALLOWED_USERS=6164003953
TELEGRAM_HOME_CHANNEL=6164003953
TELEGRAM_PROXY=http://127.0.0.1:7890
API_SERVER_KEY=<present>
```

4. Confirm long polling mode:

```powershell
# Read TELEGRAM_BOT_TOKEN and TELEGRAM_PROXY from .env; never print token.
Invoke-RestMethod -Uri "https://api.telegram.org/bot<TOKEN>/getWebhookInfo" -Proxy "http://127.0.0.1:7890"
```

Expected: `result.url` is empty.

5. Confirm bot reachability:

```powershell
Invoke-RestMethod -Uri "https://api.telegram.org/bot<TOKEN>/getMe" -Proxy "http://127.0.0.1:7890"
Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot<TOKEN>/sendMessage" -Proxy "http://127.0.0.1:7890" -Body @{ chat_id = "6164003953"; text = "Hermes repair check PASS <timestamp>" }
```

6. Confirm gateway runtime state:

```powershell
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" gateway status --deep
Get-Content -LiteralPath "C:\Users\A\.hermes\gateway_state.json" -Raw | ConvertFrom-Json
```

Expected:

```text
api_server connected
telegram connected
```

7. Confirm real inbound Telegram response by checking:

```text
Connected to Telegram (polling mode)
inbound message: platform=telegram
response ready: platform=telegram
Sending response
```

in `C:\Users\A\.hermes\logs\gateway.log`.

## Startup Fallback

If `hermes gateway install` is unavailable or not elevated, use the Startup
folder fallback:

```text
C:\Users\A\.hermes\gateway-service\Hermes_Gateway.cmd
C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd
```

Both files should set local proxy variables before starting Hermes:

```cmd
set "HTTPS_PROXY=http://127.0.0.1:7890"
set "HTTP_PROXY=http://127.0.0.1:7890"
set "ALL_PROXY=http://127.0.0.1:7890"
```

## Successful Evidence From 2026-06-01

- `gateway_state.json`: `api_server=connected`, `telegram=connected`.
- `check-hermes-telegram.ps1`: `Result: PASS`.
- Bot API `getMe`: username `u314156_openclaw_bot`.
- `getWebhookInfo`: webhook URL empty.
- Bot API `sendMessage`: sent to chat `6164003953`.
- Inbound Telegram message produced `response ready` and `Sending response`.
