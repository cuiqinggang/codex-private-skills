---
name: hermes-feishu-bot-bridge
description: Use when connecting, verifying, repairing, or extending the Feishu/Lark group bot bridge for Windows native Hermes, especially tasks mentioning the Aimaishi Feishu bot, Feishu long connection, im.message.receive_v1, im:message.group_msg, HERMES_FEISHU_OK, or local Hermes replies from Feishu group @ messages.
---

# Hermes Feishu Bot Bridge

## Scope

Use this skill for the local Windows native Hermes to Feishu group bot channel. The proven path is a standalone Python bridge using Feishu official `lark-oapi` WebSocket long connection, not a public callback URL.

Keep these boundaries:

- Do not print App Secret or WebSocket `access_key` / `ticket`.
- Do not modify Hermes main config, Open WebUI, New API, or model pools unless the user explicitly asks and a backup is made.
- Port `3000` is Open WebUI; local Hermes API is `http://127.0.0.1:8642`.
- Use group test evidence before claiming pass.

## Known Good State

Current local working artifacts were first proven under:

```text
${REDACTED_SECRET}
```

The reusable skill scripts live under this skill's `scripts/` directory. They intentionally do not include secrets.

Required Feishu app state:

- Event subscription mode: long connection / WebSocket
- Event: `im.message.receive_v1`
- Permissions: `im:message`, `im:message:send_as_bot`, `im:chat:readonly`, `im:message.group_msg`
- Bot is in the target internal group

## First Checks

Use PowerShell from this workspace or any normal shell:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10
```

Expected:

- `/health` includes `platform=hermes-agent`
- `/v1/models` includes `hermes-agent`

Check bridge logs:

```powershell
${REDACTED_SECRET}
```

## Start Or Restart Bridge

The bridge reads credentials from environment variables first:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

If those are absent, it reads:

```text
${REDACTED_SECRET}
```

Start/restart:

```powershell
${REDACTED_SECRET}
```

Stop:

```powershell
${REDACTED_SECRET}
```

The start script kills existing `feishu_hermes_bridge.py` processes before starting one fresh bridge.

## Verification Gates

G01 WebSocket:

- Log contains `bridge_start connection_mode=websocket`
- Log contains `websocket_client_starting`
- Log contains `connected to wss://msg-frontier.feishu.cn/ws/v2?...access_key=***...ticket=***`

G02 fixed acceptance:

Send the fixed acceptance message in the Feishu test group. The exact Chinese text is defined by `DEFAULT_TRIGGER` in `scripts/feishu_hermes_bridge.py`; it ends with `HERMES_FEISHU_OK`.

Pass only when:

- Log contains `event_received`
- Log contains `reply_sent ... reply=HERMES_FEISHU_OK`
- Group shows `HERMES_FEISHU_OK`

G03 general question:

Send an ordinary group message that starts with an @ mention of the Aimaishi bot.

Pass only when:

- Log contains `event_received`
- Log contains `hermes_request`
- Log contains `reply_sent`
- Group shows a Hermes-generated reply

## Known Mention Formats

The bridge must treat these Feishu text forms as a bot mention:

- `@爱马仕机器人 ...`
- `<at ...>爱马仕机器人</at> ...`
- `@_user_1 ...` with `mentions` metadata naming `爱马仕机器人`
- leading placeholder only, such as `@_user_1 ...`

The placeholder form has been observed after inviting external people into the
test group and later removing them. If logs show `event_received ... text=@_user_1 ...`
followed by `event_skip reason=bot_not_mentioned`, update/restart the bridge
from this skill package and send a fresh message.

## Diagnostics

Run Feishu app and group diagnostics:

```powershell
$env:FEISHU_APP_ID="cli_..."
$env:FEISHU_APP_SECRET="<secret>"
${REDACTED_SECRET}
```

Run recent group message read diagnostic:

```powershell
$env:FEISHU_CHAT_ID="oc_..."
${REDACTED_SECRET}
```

If it returns `code=230027` and `need scope: im:message.group_msg`, add `im:message.group_msg`, republish the app, restart the bridge, then send a fresh message. Old messages are not replayed.

## Behavior Notes

- Non-@ group messages are ignored.
- Fixed acceptance trigger replies without calling Hermes.
- Ordinary bot @ messages are forwarded to Hermes `/v1/chat/completions`.
- The bridge deduplicates repeated Feishu deliveries by `message_id` for 10 minutes; sending the same text again as a new message still gets a new reply.
- If Hermes appears to see Chinese as question marks in ad hoc PowerShell tests, use Python or Unicode-escaped JSON. The bridge sends JSON with `ensure_ascii=True`.

## Detailed Runbook

Read `references/runbook-20260525.md` when repairing failures, changing behavior, or continuing the implementation.
