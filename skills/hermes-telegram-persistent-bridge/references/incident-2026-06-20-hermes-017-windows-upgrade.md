# 2026-06-20 Windows Native Hermes 0.17 Upgrade

## Trigger

Use this when the Windows native Hermes install should be upgraded from
`hermes-agent 0.16.0` to `0.17.0` while preserving Telegram, Open WebUI, the
8642 API server, local proxy behavior, and the browser light-chat speed fix.

## Boundaries

- Do not change Windows proxy, FlClash proxy/node/rules, Telegram proxy, or
  `TELEGRAM_PROXY=http://127.0.0.1:7890`.
- Do not print `.env`, bot tokens, `API_SERVER_KEY`, or provider keys.
- Do not install optional new tools just because 0.17 logs a warning. In this
  upgrade, `raft CLI not found` appeared as a warning but did not affect
  Telegram, 8642, or Open WebUI.

## Preflight

Confirm current and latest package:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe --version
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip index versions hermes-agent
```

Observed before upgrade:

```text
INSTALLED: 0.16.0
LATEST:    0.17.0
```

## Backup

${REDACTED_SECRET}

${REDACTED_SECRET}
${REDACTED_SECRET}
- `H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1`
- `H:\Hermes_Windows_Native_014\venv\Lib\site-packages\gateway\platforms\api_server.py`
- `pip freeze`
- `hermes --version`

Do not print secrets from `.env`.

## Upgrade

Stop only the current 8642 Hermes listener, then upgrade inside the existing
Hermes virtual environment:

```powershell
$listeners = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8642 -State Listen -ErrorAction SilentlyContinue
$listeners | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force }
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip install --upgrade hermes-agent==0.17.0
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip check
```

Observed result:

```text
Successfully installed hermes-agent-0.17.0 ...
No broken requirements found.
Hermes Agent v0.17.0 (2026.6.19)
```

## Restore Local Patches

The package upgrade overwrites `gateway\platforms\api_server.py`. Reapply only
the minimal browser light-chat patch to the new 0.17 file; do not copy the old
0.16 file wholesale.

Required behavior:

- ordinary streaming `/v1/chat/completions` without `X-Hermes-Session-Id` uses
  light direct chat;
- direct light chat defaults to `z-ai/glm-5.2`;
- OpenRouter must receive `extra_body={"reasoning": {"enabled": False}}`;
- if the first light stream returns no visible content, retry once;
- explicit session continuation and automation routes still use the full Hermes
  Agent.

Also verify the launcher still exports `API_SERVER_KEY` into the child Gateway
process before `Start-Process`.

## Start And Verify

Start backend through the existing launcher:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1 `
  -NoOpen -StartBackendOnly
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File `
${REDACTED_SECRET}
```

Required PASS evidence:

- `Hermes Agent v0.17.0`
- `gateway_state.json` shows `api_server` and `telegram` connected
- local proxy listener remains `127.0.0.1:7890`
- `/health` returns 200
- `/v1/models` returns 200 and includes `hermes-agent`
- Open WebUI `http://127.0.0.1:3000` returns 200
- `Hermes8642SilentHealthCheck` next run has `LastTaskResult=0`

## Acceptance Evidence From This Upgrade

Final diagnostics:

```text
Hermes Agent v0.17.0 (2026.6.19)
check-hermes-telegram.ps1 Result: PASS
Open WebUI HTTP 200
Hermes8642SilentHealthCheck LastTaskResult=0 after next scheduled run
```

Browser `/v1/chat/completions` light-chat tests after reapplying the patch:

```text
6/6 completed
0 empty responses
max first visible token: 9.179s
average first visible token: 3.920s
max total response time: 9.314s
```

One short prompt had an API-side first-token spike, then later requests recovered.
Treat this as provider jitter unless repeated failures occur. Escalate only if
there are consecutive first-token delays over 8-10 seconds, empty responses, or
mid-stream stops.
