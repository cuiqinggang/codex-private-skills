# Stage 04a 8642 Silent Healthcheck

Use this reference when the user wants Hermes 8642 to stay alive silently, while
explicitly not restoring New API, old Watchdog, AutoRecover, or desktop browser
autostart.

## Scope

This stage only provides:

```text
Task Scheduler every 1 minute
  -> wscript.exe hidden wrapper
  -> Check-Hermes8642.ps1
  -> GET http://127.0.0.1:8642/health
  -> start H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1 only if health fails
```

The script checks `/health` once and exits. It is not a long-running watchdog.

## Installed Files

```text
C:\Users\A\Hermes_AutoStart\healthcheck-8642\Check-Hermes8642.ps1
C:\Users\A\Hermes_AutoStart\healthcheck-8642\Run-Hermes8642HealthCheck.vbs
C:\Users\A\Hermes_AutoStart\healthcheck-8642\Register-Hermes8642SilentHealthCheck.ps1
C:\Users\A\Hermes_AutoStart\healthcheck-8642\Unregister-Hermes8642SilentHealthCheck.ps1
```

Runtime Hermes config was aligned so the requested launcher restores 8642:

```text
H:\Hermes_Windows_Native_014\runtime\.hermes\config.yaml
gateway.port=8642

H:\Hermes_Windows_Native_014\runtime\.hermes\.env
API_SERVER_PORT=8642
API_SERVER_HOST=127.0.0.1
```

Do not print `DEEPSEEK_API_KEY`.

## Scheduled Task

Task:

```text
Hermes8642SilentHealthCheck
```

Expected settings:

```text
State=Ready
Hidden=True
MultipleInstances=IgnoreNew
ExecutionTimeLimit=PT10M
Execute=wscript.exe
Arguments=C:\Users\A\Hermes_AutoStart\healthcheck-8642\Run-Hermes8642HealthCheck.vbs
Schedule=every 1 minute
```

The wrapper uses `WScript.Shell.Run command, 0, True`, so PowerShell runs hidden
and does not flash a console window.

## Logs

```text
C:\Users\A\.hermes\logs\hermes-8642-healthcheck.log
C:\Users\A\.hermes\logs\hermes-8642-healthcheck-status.json
```

Backup:

```text
H:\Hermes_Backups\HERMES-014-8642-SILENT-HEALTHCHECK-20260522
```

Final report:

```text
C:\Users\A\Desktop\1\output\HERMES-014-8642-SILENT-HEALTHCHECK-FLEX-20260522\FINAL_8642_SILENT_HEALTHCHECK_REPORT.md
```

## Passing Evidence

2026-05-22 validation passed:

- Normal health: `/health=200`, `/v1/models=200`, chat returned
  `HERMES_8642_SILENT_HEALTHCHECK_OK`, one 8642 listener.
- Silent task config: `Hidden=True`, `Execute=wscript.exe`,
  `MultipleInstances=IgnoreNew`, `LastTaskResult=0`.
- Recovery attempt 1: killed listener PID 19596 at 20:00:49; task logged
  `WARN 8642 health failed; starting Hermes launcher` at 20:01:05 and
  `PASS 8642 recovered after launcher start` at 20:01:24; chat returned
  `HERMES_8642_RECOVERY_1_OK`.
- Recovery attempt 2: killed listener PID 6400 at 20:02:00; task logged
  recovery at 20:02:03 and PASS at 20:02:16; chat returned
  `HERMES_8642_RECOVERY_2_OK`.
- Final state: one listener on `127.0.0.1:8642`, old
  `HermesGatewayWatchdog_Logon` and `HermesNewApiAutoRecover_Logon` disabled,
  no New API/Postgres/Redis Docker containers started.

2026-05-22 R2 reboot validation fixed the first cold-boot timing issue:

- R1 reboot recovered eventually but the first post-reboot validation window
  failed before 8642 became healthy.
- R2 changed the healthcheck to wait longer for cold startup, avoid duplicate
  launcher starts while a Hermes gateway process is already starting, and set
  the task execution limit to `PT10M`.
- R2 local kill test: killed 8642 listener at 20:50:37; task started recovery at
  20:51:03; 8642 recovered at 20:51:17; chat returned
  `HERMES_8642_R2_LOCAL_RECOVERY_OK`; `LISTEN_COUNT=1`.
- R2 real reboot: `LAST_BOOT=2026-05-22 20:53:39 +08:00`; post-reboot
  validation started at 20:55:46; `HEALTH_RECOVERED=True`; `/health=200`;
  `/v1/models=200`; chat returned `HERMES_8642_REBOOT_OK`; `LISTEN_COUNT=1`;
  `FORBIDDEN_PROCESS_COUNT=0`; `FORBIDDEN_DOCKER_COUNT=0`.
- Follow-up live check at 21:17 showed the task still `Ready`,
  `LastTaskResult=0`, `/health=200`, `/v1/models=200`, chat returned
  `HERMES_8642_R2_REBOOT_FINAL_OK`, and no New API/Postgres/Redis/old
  Watchdog/AutoRecover process was running.

## Rollback

To remove only this new 8642 healthcheck task:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\A\Hermes_AutoStart\healthcheck-8642\Unregister-Hermes8642SilentHealthCheck.ps1'
```

This does not delete scripts, logs, Hermes, Open WebUI, New API, Telegram, or old
disabled tasks.

## Boundaries

- Do not start New API, Postgres, or Redis.
- Do not use old `HermesGatewayWatchdog.ps1`.
- Do not use old `Hermes_NewAPI_AutoRecover.ps1`.
- Do not modify Telegram token.
- Do not modify Open WebUI config.
- Do not add desktop browser/Open WebUI autostart here; that is Stage 04b.
- Reboot validation is passed for the 8642 lifeline as of R2. Do not generalize
  that result to desktop/Open WebUI autostart, New API, Telegram, Watchdog, or
  AutoRecover.
