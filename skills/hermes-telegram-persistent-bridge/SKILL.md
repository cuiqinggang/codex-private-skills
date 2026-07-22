---
name: hermes-telegram-persistent-bridge
description: Use when Telegram or browser access to Windows native Hermes stops answering, gets stuck, or needs persistence after reboot/login.
---

# Hermes Telegram Persistent Bridge

## Purpose

Repair the Windows native Hermes bridge without reviving the old WSL/OpenClaw
path. The durable integration point is:

```text
${REDACTED_SECRET}
```

## Hard Boundaries

- C drive is the hot runtime path for Hermes on this machine:
${REDACTED_SECRET}
  `H:\Hermes...` as backup/reference/disaster-recovery paths unless the user
  explicitly asks for backup maintenance.
- Do not change Windows proxy, FlClash proxy/node/rules, Telegram proxy, or the
  known-good `TELEGRAM_PROXY=http://127.0.0.1:7890`.
- Do not print bot tokens, `API_SERVER_KEY`, provider keys, or raw `.env`.
- Do not delete Telegram Desktop state unless the Desktop app itself is stuck
  loading or logged out.
- Ask before rotating tokens, changing firewall/security settings, deleting old
  WSL/OpenClaw files, or running unknown internet scripts.

## First Diagnostic

Always start here:

```powershell
${REDACTED_SECRET}
```

Treat PASS as a starting point, not final proof. `/health`, `/v1/models`, and
gateway state can pass while real answers are still stuck.

## Quick Triage

| Symptom | First reference |
| --- | --- |
| Upgrade Windows native Hermes to 0.17 while preserving Telegram/browser fixes | `references/incident-2026-06-20-hermes-017-windows-upgrade.md` |
| Telegram bridge stopped after Hermes upgrade | `references/incident-2026-06-01-hermes-0152-upgrade-repair.md` |
| Telegram Desktop stuck on loading/connecting/login UI | `references/incident-2026-06-16-telegram-desktop-stuck-loading.md` |
| Browser/Open WebUI/API Server slow, blank, or stalled | `references/incident-2026-06-17-api-server-streaming-config-cleanup.md` |
| Browser answers but first visible token is very slow while Telegram is fast | `references/incident-2026-06-18-api-server-light-chat-speed.md` |
| Phone Telegram sends but Hermes does not reply | `references/incident-2026-06-17-telegram-session-stuck-queued.md` |
| Phone Telegram shows `Working -- 3 min`, typing starts/stops, or answers are very delayed after drive/path cleanup | `references/incident-2026-07-05-c-hotpath-telegram-working-stall.md` |
| Default is OpenRouter/GLM5 but Telegram complex tasks hit DeepSeek 401 | `references/incident-2026-06-17-glm5-router-provider-mismatch.md` |
| Need GLM-5.2 default plus explicit DeepSeek official V4 Pro cost-saving switch and Qwen3-VL 235B availability | `references/incident-2026-06-23-glm52-deepseek-v4pro-qwen235-switch.md` |
| Hermes 0.17 path was rebuilt after drive-letter/path cleanup, or 8642 healthcheck reports old launcher missing | `references/incident-2026-06-30-327-hermes017-autostart-healthcheck.md` |
| Telegram/API says provider is rate-limiting OpenRouter GLM-5-Turbo | `references/incident-2026-06-17-openrouter-glm5-turbo-429-switch-glm52.md` |
| Telegram Pro route shows `base_url=http://127.0.0.1:3001/v1` or HTTP 502 | `references/incident-2026-05-25-router-3001-502.md` |
| Need full Windows native 0.14 runbook | `references/windows-native-014-telegram-runbook.md` |
| Need current known-good baseline | `references/telegram-bridge-current-state-20260607.md` |

## Safe Recovery Ladder

1. Run the diagnostic script above.
2. Check the 8642 lifeline:
   ```powershell
   Get-ScheduledTaskInfo -TaskName Hermes8642SilentHealthCheck
   ```
3. Check the real listener, not only `hermes gateway status`:
   ```powershell
   Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8642 -State Listen
   ```
   Then inspect the listener process command line. A normal hot-path listener
   must not be a stale `H:\Hermes...` or `K:\Hermes...` gateway.
4. Inspect recent `gateway.log` and `agent.log` for the real failure boundary:
   inbound message, `response ready`, API errors, queued follow-ups, or stuck
   tool loops.
5. If editing config, back up first. Keep
   `display.platforms.api_server.streaming=true`, avoid duplicate YAML blocks,
   and keep ordinary `api_server` toolsets narrow enough that short questions do
   not pay full browser/vision/web tool context unless those tools are required.
6. Restart only when needed. Prefer normal stop/start; if status misreports but
   a real listener exists, use the listener PID as source of truth.
7. Verify with real acceptance tests, not green lights alone.

## Acceptance Tests

Recovery is not complete until the relevant tests pass:

- Diagnostic script returns PASS.
- One real listener exists on `127.0.0.1:8642`.
- `gateway_state.json` shows `api_server` and `telegram` connected.
- Real `/v1/chat/completions` returns content.
- Streaming first chunk is quick enough to avoid browser white-screen waiting.
- For Telegram incidents, a fresh inbound phone/Desktop Telegram message has a
${REDACTED_SECRET}
- Open WebUI `http://127.0.0.1:3000` is checked only when browser UX is in scope.

## Local Constants

| Item | Value |
| --- | --- |
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
| API server | `http://127.0.0.1:8642` |
| Open WebUI | `http://127.0.0.1:3000` |
| Telegram home chat | `6164003953` |
| Local Telegram proxy | `http://127.0.0.1:7890` |
${REDACTED_SECRET}

${REDACTED_SECRET}
inside this skill.
