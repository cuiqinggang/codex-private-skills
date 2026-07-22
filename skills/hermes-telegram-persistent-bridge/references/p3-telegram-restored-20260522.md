# P3 Telegram Restored Baseline - 2026-05-22

This note records the post-P1/P2 restoration of the Telegram bridge for Windows native Hermes 0.14.

## Scope

- Starting point: `HERMES-014-P1P2-HEALTH-BACKUP-20260522`.
- Goal: reconnect Telegram from the stable Hermes 8642 plus Open WebUI 3000 baseline.
- Explicitly not restored: New API, Postgres, Redis, Watchdog, AutoRecover, login autostart.
- Secrets policy: Telegram bot token was never printed into chat, reports, or this skill.

## Current Result

- Hermes root: `H:\Hermes_Windows_Native_014`
${REDACTED_SECRET}
- Gateway command: `H:\Hermes_Windows_Native_014\venv\Scripts\hermes gateway run --replace`
- Gateway PID at final verification: `19596`
- API server: `connected`
- Telegram: `connected`
- Telegram mode: long polling
- Telegram bot username: `u314156_openclaw_bot`
- Telegram chat id: `6164003953`
- Telegram webhook: empty
- Telegram proxy: `http://127.0.0.1:7890`
- Open WebUI: HTTP 200 on `http://127.0.0.1:3000`
- Docker running containers: `open-webui-clean`
- Scheduled tasks:
  - `HermesGatewayWatchdog_Logon`: Disabled
  - `HermesNewApiAutoRecover_Logon`: Disabled
- Startup entry: not installed; this is intentional for the P3 non-persistence state.

## Config State

${REDACTED_SECRET}

```text
TELEGRAM_BOT_TOKEN=<redacted>
TELEGRAM_ALLOWED_USERS=6164003953
TELEGRAM_HOME_CHANNEL=6164003953
TELEGRAM_PROXY=http://127.0.0.1:7890
```

The file may also retain older `#DISABLED_MINIMAL# TELEGRAM_*` comments from the P1/P2 minimal baseline. The active non-commented keys are the source of truth for P3.

## Evidence

Run directory:

```text
${REDACTED_SECRET}
```

Write-before-change backup:

```text
${REDACTED_SECRET}
```

Final verification snapshot:

```text
${REDACTED_SECRET}
```

Fresh verification at `2026-05-22 19:19:36 +08:00`:

- `gateway_state.json`: `api_server=connected`, `telegram=connected`
- `http://127.0.0.1:8642/health`: HTTP 200
- `http://127.0.0.1:8642/v1/models`: HTTP 200
- Direct Hermes chat marker: `HERMES_P3_TELEGRAM_FINAL_OK`
- `http://127.0.0.1:3000`: HTTP 200
- Telegram `getMe`: `ok=true`, username `u314156_openclaw_bot`
- Telegram `getWebhookInfo`: webhook URL empty
- Outbound Bot API marker sent: `HERMES_P3_TG_OUTBOUND_20260522_191534`
- Inbound live Telegram evidence after restart:
  - `2026-05-22 19:16:32`: inbound message from chat `6164003953`
  - `2026-05-22 19:16:38`: response ready and sent to `6164003953`
  - `2026-05-22 19:17:05`: second inbound message from chat `6164003953`
  - `2026-05-22 19:17:09`: response ready and sent to `6164003953`

## Recovery Path Used

1. Ran the bundled diagnostic script:

```powershell
${REDACTED_SECRET}
```

2. Confirmed the failure layer was persistence/autostart, not Hermes API or Telegram runtime.
3. Confirmed `.env` had active Telegram keys and retained P1/P2 disabled comments.
4. Backed up live Hermes config and state before relying on the current file state.
5. Restarted the gateway manually and verified fresh Telegram polling connection.
6. Sent a Bot API smoke-test message and verified live inbound plus reply logs from Telegram Desktop.
7. Left Watchdog, AutoRecover, and Startup entry disabled/not installed.

## Next Stage Boundary

This is a P3 live Telegram baseline, not a P4 reboot-persistence baseline. If the next task is reboot/login persistence, start a new gated run and only then decide whether to install Startup entry or scheduled-task persistence.

## Rollback

Restore files from:

```text
${REDACTED_SECRET}
```

Then restart Hermes gateway and rerun the diagnostic script.
