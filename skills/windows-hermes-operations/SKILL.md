---
name: windows-hermes-operations
description: Use when the user asks to open, restart, verify, troubleshoot, recover, or clean up the Windows native Hermes / 鐖遍┈浠?0.14 system, especially requests mentioning Windows鐗堢埍椹粫, Hermes 0.14, Open WebUI on 3000, Hermes gateway on 8642, stale WSL Hermes, old OpenClaw gateway, or historical cleanup/deletion records.
---

# Windows Hermes Operations

## Accepted mainline and upgrade history

Read [accepted-mainline-and-upgrade-history.md](references/accepted-mainline-and-upgrade-history.md) for exact version history, autostart decisions, and model-selection repairs.

## Safety Boundary

Protect the Windows native Hermes 0.14 system:

- Do not delete or modify `H:\Hermes_Windows_Native_014` unless the user explicitly asks for a targeted edit there.
${REDACTED_SECRET}
- Do not delete Docker/Open WebUI containers unless the user explicitly asks.
- Treat old WSL Hermes/OpenClaw cleanup as historical unless verification shows a new live conflict.
- For the Windows Native Hermes 8642 mainline, do not treat BIOS firmware virtualization, WSL2, Docker Desktop, `open-webui-clean`, or Open WebUI `3000` as hard prerequisites.
- Open WebUI `3000` is still a needed next-stage web panel route; preserve it and diagnose it separately instead of using it to fail the 8642 mainline.

## Fast Open Path

If the user is rebuilding the system from a minimal clean state, or asks to
restore the original Hermes stack one layer at a time, use
`hermes-014-restoration-ladder` first. That skill separates the DeepSeek-only
base, Open WebUI panel, New API, Telegram, and reboot-persistence stages.

For a normal "open Windows Hermes" request, do not rediscover paths. The active launcher is C-drive only; H/K copies are backup or compatibility history. Use:

```powershell
${REDACTED_SECRET}
```

Then verify:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
${REDACTED_SECRET}
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10 -Headers @{ Authorization = "Bearer $key" }
Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
```

Expected evidence:

- Windows Native Hermes 8642 mainline PASS means 8642 listens, `/health` returns 200, and `/v1/models` returns 200 with `hermes-agent`.
${REDACTED_SECRET}
- `/health` returns `platform=hermes-agent`.
- `/v1/models` returns `hermes-agent`.
- `http://127.0.0.1:3000` returns HTTP 200 only for the Open WebUI next-stage/panel route. If 3000 is unavailable, record it as web panel not started; do not fail the Windows Native Hermes 8642 mainline.

For exact gated commands and timing, read `references/open-and-verify.md`.

For a read-only health snapshot that does not start or stop services, run:

```powershell
${REDACTED_SECRET}
```

Read `references\quick-healthcheck-20260528.md` when you need the historical
acceptance rule. Current 8642 mainline acceptance is: `/health` alone is not
enough; `/v1/models` must include `hermes-agent`, and the 8642 owner should be
checked when possible. BIOS, WSL2, Docker, and Open WebUI `3000` are optional
or next-stage checks and must not block the 8642 mainline result.

## Digital Assistant Does Not Answer After Restart

If New API on `3001` and Open WebUI on `3000` are healthy but Hermes `8642` is
`NOT_LISTENING`, use `new-api-local-deploy` and read
`references/hermes-openwebui-chain.md`. Its fast recovery pattern records the
2026-05-22 repair: start `START-HERMES-WEBUI.cmd`, verify the latest
`daily-start-*.log` has `FINAL_PASS`, then prove direct Hermes chat,
streaming chat, Open WebUI API chat, New API relay logs, and Telegram bridge
state before claiming recovery.

If Hermes `8642` is healthy but Docker API is unavailable and New API `3001`
or Open WebUI `3000` are `NOT_LISTENING`, this is a different failure layer.
Use `new-api-local-deploy` and read `references/hermes-openwebui-chain.md` for
the Docker/New API down recovery pattern: start Docker Desktop, run
${REDACTED_SECRET}
`open-webui-clean`, then verify Hermes chat, Open WebUI API chat, New API relay
logs, and Telegram bridge state.

For automatic reboot/login recovery, preserve the installed task
`HermesNewApiAutoRecover_Logon` and script
${REDACTED_SECRET}
In the current direct DeepSeek web setup, it handles Docker/Open WebUI, Hermes,
and Telegram health checks without requiring New API `3001`.

## If There Is a Problem

First identify the failing layer:

1. Check whether 8642 is owned by Windows native Hermes.
2. Check `/health` and `/v1/models`; `/health` alone is not sufficient.
3. Check whether Open WebUI on 3000 is available.
4. Check the latest `daily-start-*.log`.
5. Only if WSL appears in a current port owner or process check, read `references/cleanup-20260520.md` before taking cleanup action.

Do not repeat the old broad filesystem search for `hermes.exe`; it was slow and unnecessary. The mature entrypoint is the launcher above.

## Historical Cleanup Record

The old WSL Hermes and old OpenClaw gateway were removed on 2026-05-20 after user confirmation. Keep this as the rollback/troubleshooting record:

- `references/cleanup-20260520.md`

Important current state from that cleanup:

${REDACTED_SECRET}
  On 2026-05-22 a minimal compatibility shim was recreated there only because
  the existing `HermesGatewayWatchdog_Logon` scheduled task still pointed to
  that path and could not be edited without elevated permissions. The shim
${REDACTED_SECRET}
  it does not revive the old WSL/OpenClaw gateway.
- Old WSL paths such as `/home/u123456/.hermes`, `/home/u123456/.local/bin/hermes`, and `/home/u123456/.openclaw` were deleted.
- Old WSL systemd services for `hermes-worker-01..04.service` and `openclaw-gateway.service` were removed.
- Windows Task Scheduler entries `HermesTelegramGateway_Autostart` and `HermesTelegramGateway_Watchdog` could not be unregistered without administrator permission, but are inert because their wrapper path no longer exists.

If the user asks to fully remove those two visible scheduled task entries, run the removal only from an elevated/admin PowerShell session or ask the user to provide admin execution.

