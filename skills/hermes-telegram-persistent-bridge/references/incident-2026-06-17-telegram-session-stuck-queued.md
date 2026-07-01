# 2026-06-17 Telegram Session Stuck And Queued Messages

## Value Judgment

HIGH_VALUE.

This incident records a Hermes Telegram failure where the gateway, API server,
proxy, startup shortcut, and health checks all passed, but phone Telegram
messages stopped receiving replies. The root cause was not proxy or Telegram
login state; one long-running Telegram agent session was stuck in browser,
screenshot, and vision-analysis tooling, and later phone messages were being
flushed but queued behind that unfinished session.

## Trigger Phrases

Use this note when:

- The user says phone Telegram sends messages but Hermes does not answer.
- `check-hermes-telegram.ps1` passes but no reply appears on Telegram.
- `gateway.log` shows `[Telegram] Flushing text batch` after the user's latest
  messages, but no matching new `response ready`.
- `agent.log` shows a long-running task stuck in browser, screenshot,
  `vision_analyze`, or repeated tool loops.
- `hermes gateway status` says no gateway is running, but Windows shows a real
  listener on `127.0.0.1:8642`.

## Boundaries

- Do not change Windows proxy, FlClash proxy/node/rules, Telegram proxy, or the
  known good `TELEGRAM_PROXY=http://127.0.0.1:7890`.
- Do not print API keys, Telegram tokens, provider keys, or `.env` contents.
- Do not declare recovery from `/health` alone. Prove a real answer path.
- Do not delete Telegram Desktop state for this symptom unless the Desktop app
  itself is stuck loading or logged out.

## Repair Ladder

### Q01 - Run Standard Diagnostic

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

If it passes, continue. Passing diagnostics only prove the bridge is connected;
they do not prove the active Telegram conversation is not blocked.

### Q02 - Check 8642 Lifeline And Real Listener

```powershell
Get-ScheduledTaskInfo -TaskName Hermes8642SilentHealthCheck |
  Select-Object LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns

Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8642 -State Listen |
  ForEach-Object {
    $p=Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)"
    [pscustomobject]@{PID=$_.OwningProcess; CommandLine=$p.CommandLine}
  }
```

Expected listener command contains:

```text
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway run --replace
```

### Q03 - Locate The Missing Response Boundary

Inspect recent logs:

```powershell
Get-Content -LiteralPath "C:\Users\A\.hermes\logs\gateway.log" -Tail 260
Get-Content -LiteralPath "C:\Users\A\.hermes\logs\agent.log" -Tail 260
```

Failure pattern from this incident:

- Normal replies existed before 13:41.
- At 13:41 a Telegram task started.
- Later phone messages at 13:43, 13:44, 13:53, 13:55, 13:56, 13:58, and 14:01
  were flushed.
- The agent continued browser and vision work.
- No final `response ready` appeared before restart.

### Q04 - Clear Only The Stuck Gateway Session

First try the normal stop:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe gateway stop
```

If Hermes status misreports `No gateway running` but Q02 shows a real listener,
use the listener PID from Q02 as the source of truth and stop that process:

```powershell
Stop-Process -Id <LISTENER_PID> -Force
```

Then restart:

```powershell
Start-Process -FilePath "cmd.exe" `
  -ArgumentList "/c","H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd" `
  -WindowStyle Hidden
```

### Q05 - Verify Recovery

Run the standard diagnostic again. Required proof:

- `state api_server connected`: PASS.
- `state telegram connected`: PASS.
- `Hermes8642SilentHealthCheck`: `LastTaskResult=0`.
- A fresh inbound Telegram phone message appears in `gateway.log`.
- A matching new `response ready` appears after that inbound message.
- Real `/v1/chat/completions` returns content.
- Streaming first chunk returns quickly.

## 2026-06-17 Passing Evidence

- Stuck listener PID was `16236`.
- New listener after restart was PID `5956`.
- Telegram reconnected in polling mode at `2026-06-17 14:11:06`.
- Fresh phone Telegram inbound message arrived at `2026-06-17 14:11:11`.
- Matching `response ready` appeared at `2026-06-17 14:11:33`, about 21.7
  seconds later.
- Standard diagnostic returned PASS.
- 8642 real chat completion returned content.
- Streaming first chunk returned in about 0.11 seconds.

## Next-Run Reuse Instruction

For future "Telegram can send but Hermes does not answer" reports, start with
this note after the standard diagnostic. Treat "flushing without response
ready" as a blocked session, not as a proxy problem.
