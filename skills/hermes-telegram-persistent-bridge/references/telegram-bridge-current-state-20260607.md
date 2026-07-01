# 2026-06-07 Telegram Bridge Current State

Use this note when checking Telegram after Windows native Hermes 0.14 recovery.

## Accepted State

Telegram bridge was verified connected during the G39 Windows Native Hermes
8642 mainline acceptance.

Evidence pattern:

```json
{
  "platforms": {
    "api_server": { "state": "connected" },
    "telegram": { "state": "connected" }
  }
}
```

The accepted process owner for 8642 was Windows native Hermes:

```text
python.exe ... hermes_cli.main gateway run --replace
```

The accepted endpoints were:

- `http://127.0.0.1:8642/health` HTTP 200, `platform=hermes-agent`.
- `http://127.0.0.1:8642/v1/models` HTTP 200, contains `hermes-agent`.

2026-06-07 evening follow-up: Telegram remained PASS while Open WebUI 3000 was
down because Docker Desktop was stuck in `starting`. After Docker/Open WebUI
recovery, the stricter browser-panel diagnostic also passed with
`-RequireWebUi`. Keep treating Telegram as attached to Hermes 8642; only require
Open WebUI when the user is explicitly testing the browser panel route.

## Layer Rule

Telegram bridge attaches to the Windows native Hermes 8642 gateway. It does not
require Open WebUI 3000 to be available.

Do not fail Telegram just because Docker Desktop, WSL2, `open-webui-clean`, or
Open WebUI `3000` is down.

Open WebUI 3000 is useful for the browser shell, but Telegram should be checked
against:

- `gateway_state.json`
- Hermes `/health`
- Hermes `/v1/models`
- gateway logs
- a real inbound/outbound Telegram message when needed

## Diagnostic Rule

The diagnostic script should keep Open WebUI as optional by default. Only make
Open WebUI required when the user is specifically testing the browser panel
route.

Correct default behavior:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

Browser-panel-required behavior:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1" -RequireWebUi
```

## Safety

Never print:

- Telegram bot token
- `API_SERVER_KEY`
- Open WebUI API keys
- passwords, tokens, or secrets from `.env` or config databases

Do not rotate the Telegram bot token unless the user explicitly asks for token
rotation.
