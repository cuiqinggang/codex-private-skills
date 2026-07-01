# Stage 04b Open WebUI Auto-Open

Use this reference when the user wants the Windows native Hermes desktop panel /
Open WebUI to open automatically after Windows login, after Stage 04a has already
made 8642 durable.

## Scope

For Hermes 0.15.2 and newer, also read
`references/incident-2026-06-02-stage04b-0152-autoopen-repair.md`. The Stage
04b scripts must send `Authorization: Bearer <API_SERVER_KEY>` for local 8642
`/v1/models` and chat checks, and the gateway Startup fallback should be hidden
with `Hermes_Gateway_Hidden.vbs` rather than a visible `Hermes_Gateway.cmd`
console.

This stage only provides:

```text
Current user Startup folder
  -> HermesOpenWebUIAutoOpen.vbs hidden wrapper
  -> Open-HermesOpenWebUI.ps1
  -> wait for Stage 04a 8642 lifeline health/models/single-listener
  -> reuse H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1 -WaitAndOpen
  -> Docker Desktop / open-webui-clean / browser http://127.0.0.1:3000
```

Do not start or configure New API, Postgres, Redis, old Watchdog, or
AutoRecover from this stage. Do not modify Telegram token or Open WebUI config.
Telegram may already be connected through the Hermes gateway, but Stage 04b does
not control it.

## Installed Files

```text
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Open-HermesOpenWebUI.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Run-HermesOpenWebUIAutoOpen.vbs
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Install-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Rollback-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Verify-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\PostReboot-Verify-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Run-PostReboot-Verify-HermesOpenWebUIAutoOpen.vbs
```

Startup entry:

```text
C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\HermesOpenWebUIAutoOpen.vbs
```

The VBS wrapper uses `WScript.Shell.Run command, 0, False`, so PowerShell runs
hidden. The intended visible side effect is the browser opening
`http://127.0.0.1:3000`.

## Logs

```text
C:\Users\A\.hermes\logs\hermes-openwebui-autoopen.log
C:\Users\A\.hermes\logs\hermes-openwebui-autoopen-status.json
H:\Hermes_Windows_Native_014\reports\daily-start-*.log
```

Backup:

```text
H:\Hermes_Backups\HERMES-014-STAGE04B-OPENWEBUI-AUTOOPEN-20260522
```

Detailed build and reproduction runbook:

```text
references/stage-04b-openwebui-autoopen-build-runbook-20260522.md
```

## Passing Evidence

2026-05-22 local validation passed:

- Startup entry exists: `HermesOpenWebUIAutoOpen.vbs`.
- Wrapper script has no New API, Telegram, Watchdog, AutoRecover, Postgres, or
  Redis references.
- 8642 listener count is 1.
- `/health=200`, `/v1/models=200`, chat returned `HERMES_STAGE04B_LOCAL_OK`.
- Open WebUI 3000 returned HTTP 200.
- Docker only showed `open-webui-clean`, healthy on port 3000.
- No New API/Postgres/Redis Docker containers were running.
- No NewAPI/old Watchdog/AutoRecover processes were running.
- The mature launcher wrote `FINAL_PASS Windows native Hermes page is ready`.
- Stage 04b status file wrote `FINAL_PASS`.

Observed Telegram state during the same local check:

- `gateway_state.json` showed `api_server=connected` and `telegram=connected`.
- A real Telegram inbound message at 21:36 produced `response ready` and
  `Sending response`.
- This is evidence that Telegram currently works through the Hermes gateway. It
  is not evidence that Stage 04b controls Telegram.

2026-05-22 reboot validation passed:

- Real reboot boot time: `2026-05-22 21:55:53`.
- Stage 04a lifeline recovered 8642 after boot: healthcheck logged recovery at
  `22:03:26`.
- Stage 04b waited for 8642, then reused the mature Open WebUI launcher.
- Mature launcher log:
  `H:\Hermes_Windows_Native_014\reports\daily-start-20260522-220326.log`.
- Launcher wrote `FINAL_PASS Windows native Hermes page is ready`.
- Stage 04b status wrote `FINAL_PASS` at `22:05:16`.
- One-shot post-reboot verifier wrote `G_STAGE04B_REBOOT_VERIFY_PASS`.
- Live recheck after reboot: one 8642 listener; `/health=200`,
  `/v1/models=200`, chat returned `HERMES_STAGE04B_REBOOT_LIVE_OK`, and
  Open WebUI 3000 returned HTTP 200.
- Docker only showed `open-webui-clean` on port 3000; no New API, Postgres, or
  Redis containers were running.
- No NewAPI, old Watchdog, or AutoRecover process was running.

Telegram observation after the same reboot:

- `gateway_state.json` showed `api_server=connected` and `telegram=connected`.
- Telegram initially timed out while the machine/proxy/network were still
  warming up, then auto-reconnected at `22:12:49` in polling mode.
- A real Telegram inbound message at `22:17:38` produced `response ready` and
  `Sending response` at `22:17:43`.
- The old `Hermes_Gateway.cmd` Startup entry is intentionally absent in this
  architecture; 8642 is now restored by the Stage 04a scheduled healthcheck.

## Rollback

To remove only the Stage 04b auto-open startup entry:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Rollback-HermesOpenWebUIAutoOpen.ps1'
```

This does not delete scripts, logs, Hermes, Open WebUI, Telegram, New API, or
the Stage 04a 8642 healthcheck.

## Boundaries

- Stage 04a keeps 8642 alive; Stage 04b only opens the desktop/Open WebUI layer.
- Do not use old `HermesGatewayWatchdog.ps1`.
- Do not use old `Hermes_NewAPI_AutoRecover.ps1`.
- Do not start New API, Postgres, or Redis.
- Do not modify Telegram token.
- Do not modify Open WebUI config.
- Reboot validation is passed for Stage 04b as of 2026-05-22. Do not generalize
  that result to New API, old Watchdog, or AutoRecover.
