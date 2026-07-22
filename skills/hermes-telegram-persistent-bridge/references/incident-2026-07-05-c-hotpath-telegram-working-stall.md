# 2026-07-05 C Hot Path And Telegram Working Stall

## Value Judgment

HIGH_VALUE.

This incident captured a Hermes Telegram failure where the phone chat displayed
`Working -- 3 min`, typing appeared and stopped, and a trivial `你好` message was
very delayed or failed to receive a final answer. The root cause was not the
phone client. The local Hermes runtime had multiple mixed C/H/K launch paths and
multiple gateway instances, and the normal API route also carried a heavy agent
prompt for short questions.

## Trigger Phrases

Use this note when:

- The user says Telegram shows `Working -- 3 min`, "正在输入", or "连接中" but no
  final answer appears.
- A trivial Telegram message such as `你好` takes minutes.
- Diagnostics show PASS, but the real Telegram UX is slow or stuck.
- `gateway.log` shows inbound Telegram text and send/network timeout, or old
  path conflicts such as C, H, and K Hermes roots in process command lines.
- After drive-letter cleanup, startup, Open WebUI auto-start, or healthcheck
  scripts may still point to `H:\Hermes...` or `K:\Hermes...`.

## Hard Rule

C drive is the hot runtime path:

```text
${REDACTED_SECRET}
```

Do not use `K:\AI`, `K:\Hermes...`, or `H:\Hermes...` as the normal Hermes
runtime path. Those roots are backup/reference/disaster-recovery material unless
the user explicitly asks for backup maintenance.

## Root Causes Found

1. Mixed launch roots:
   - gateway service VBS and healthcheck scripts were not consistently aligned;
   - OpenWebUI scheduled task still pointed at `H:\Hermes_Windows_Native_014`;
   - old C/H/K gateway processes could coexist, causing Telegram polling
     conflicts and fake "task running" states.
2. False green checks:
   - `hermes gateway status`, `/health`, and `gateway_state.json` can look good
     while a stale listener or wrong-root task is still involved.
3. Heavy API route for short prompts:
   - before repair, a trivial `只回答：OK` request took 38.43s and carried about
     11.7k input tokens;
   - after narrowing `platform_toolsets.api_server`, the warmed request took
     4.29s.

## Repair Ladder

1. Run the standard diagnostic, but treat PASS only as a starting point:
   ```powershell
${REDACTED_SECRET}
   ```
2. Check real gateway/listener processes:
   ```powershell
   Get-CimInstance Win32_Process |
     Where-Object { $_.CommandLine -match 'Hermes_Windows_Native_014|Hermes_AutoStart|\.hermes\\gateway-service' } |
     Select-Object ProcessId,Name,CommandLine

   Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8642 -State Listen |
     ForEach-Object {
       $p=Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)"
       [pscustomobject]@{PID=$_.OwningProcess; Name=$p.Name; CommandLine=$p.CommandLine}
     }
   ```
3. Clean only Hermes gateway/healthcheck duplicates, then restart one C-drive
   gateway. Do not change proxy, tokens, firewall, or Telegram login state.
4. Align these hot-path files to C drive:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
   - OpenWebUI auto-open scripts under
${REDACTED_SECRET}
5. Scan editable hot-path scripts for stale launch roots:
   ```powershell
   Select-String -Path `
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
     -Pattern 'H:\\Hermes_Windows_Native_014|K:\\Hermes_Windows_Native_014'
   ```
6. If short API answers are still slow, inspect `agent.log` for input token
   count and API latency. Keep `reasoning_effort: none`, keep API streaming on,
   and narrow ordinary `platform_toolsets.api_server` before making code-level
   light-chat changes.

## Acceptance Evidence From 2026-07-05

- Standard diagnostic returned PASS using C-drive CLI:
${REDACTED_SECRET}
- Gateway state showed `api_server` and `telegram` connected.
- Real 8642 listener existed.
- Editable hot-path script scan returned no active `H:\Hermes...` or
  `K:\Hermes...` matches.
- `/v1/chat/completions` short-answer test improved:
  - before repair: 38.43s;
  - after API toolset narrowing, cold-ish test: 18.41s;
  - warmed test: 4.29s.
- Knowledge Brain health check and hot sync returned PASS.

## Known Residual

The scheduled task `Hermes_OpenWebUI_AutoStart` still pointed to:

```text
H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd
```

Attempts to change or disable it with `Set-ScheduledTask` and `schtasks.exe`
returned `Access is denied` / run-as password requirements. Do not silently hack
Task Scheduler internals. If this task must be fixed, use an elevated Windows
Task Scheduler session or recreate the task with the correct C-drive action.

## Next-Run Reuse Instruction

For future "Telegram shows Working/typing but no final answer" reports, do not
stop at PASS diagnostics. First check for mixed C/H/K Hermes roots and duplicate
gateway processes, then test a short `/v1/chat/completions` request and compare
latency. Treat C drive as the only ordinary hot runtime path.
