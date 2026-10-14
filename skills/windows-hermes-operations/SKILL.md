---
name: windows-hermes-operations
description: Use when the user asks to open, restart, verify, troubleshoot, recover, or clean up the Windows native Hermes / 爱马仕 system (including historical 0.14 and current installations), especially requests mentioning Windows版爱马仕, Hermes 0.14, Open WebUI on 3000, Hermes gateway on 8642, stale WSL Hermes, old OpenClaw gateway, or historical cleanup/deletion records.
---

# Windows Hermes Operations

## 当前启动故障入口（2026-10-14 实证，优先于下方历史记录）

处理开机启动、8642、Docker、Open WebUI 3000故障时，先读 [Docker启动恢复经验](references/docker-startup-recovery-20261014.md)。
现用启动器已迁到C盘，运行版本实测0.21.5；先核对现状，不按旧H盘路径或hermes-agent模型名盲目重装/回退。
未认证401先走现有认证；8642正常但3000异常先查Docker层。使用精确、有限恢复，不把历史WSL抢占当作本次原因。
本文下方0.14/H盘/旧计划任务等为历史操作记录，只有当前现场确认仍适用才执行。重启验收仍未完成，不能以本次热启动PASS替代。

## Safety Boundary

Protect the Windows native Hermes 0.14 system:

- Do not delete or modify `H:\Hermes_Windows_Native_014` unless the user explicitly asks for a targeted edit there.
- Do not delete or modify `C:\Users\A\.hermes` unless the user explicitly asks for a targeted edit there.
- Do not delete Docker/Open WebUI containers unless the user explicitly asks.
- Treat old WSL Hermes/OpenClaw cleanup as historical unless verification shows a new live conflict.

## Fast Open Path

If the user is rebuilding the system from a minimal clean state, or asks to
restore the original Hermes stack one layer at a time, use
`hermes-014-restoration-ladder` first. That skill separates the DeepSeek-only
base, Open WebUI panel, New API, Telegram, and reboot-persistence stages.

For a normal "open Windows Hermes" request, do not rediscover paths. Use:

```powershell
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

Then verify:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
```

Expected evidence:

- Latest `H:\Hermes_Windows_Native_014\reports\daily-start-*.log` contains `FINAL_PASS Windows native Hermes page is ready`.
- `127.0.0.1:8642` is owned by a command under `H:\Hermes_Windows_Native_014`.
- `/health` returns `platform=hermes-agent`.
- `/v1/models` returns `hermes-agent`.
- `http://127.0.0.1:3000` returns HTTP 200.

For exact gated commands and timing, read `references/open-and-verify.md`.

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
`docker compose up -d` from `C:\Users\A\new-api-local`, start
`open-webui-clean`, then verify Hermes chat, Open WebUI API chat, New API relay
logs, and Telegram bridge state.

For automatic reboot/login recovery, preserve the installed task
`HermesNewApiAutoRecover_Logon` and script
`C:\Users\A\.hermes\gateway-service\Hermes_NewAPI_AutoRecover.ps1`.
It handles Docker, New API, Open WebUI, Hermes, and Telegram health checks.

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

- `C:\Users\A\Hermes_AutoStart` was deleted during old WSL/OpenClaw cleanup.
  On 2026-05-22 a minimal compatibility shim was recreated there only because
  the existing `HermesGatewayWatchdog_Logon` scheduled task still pointed to
  that path and could not be edited without elevated permissions. The shim
  delegates to `C:\Users\A\.hermes\gateway-service\Hermes_NewAPI_AutoRecover.ps1`;
  it does not revive the old WSL/OpenClaw gateway.
- Old WSL paths such as `/home/u123456/.hermes`, `/home/u123456/.local/bin/hermes`, and `/home/u123456/.openclaw` were deleted.
- Old WSL systemd services for `hermes-worker-01..04.service` and `openclaw-gateway.service` were removed.
- Windows Task Scheduler entries `HermesTelegramGateway_Autostart` and `HermesTelegramGateway_Watchdog` could not be unregistered without administrator permission, but are inert because their wrapper path no longer exists.

If the user asks to fully remove those two visible scheduled task entries, run the removal only from an elevated/admin PowerShell session or ask the user to provide admin execution.
