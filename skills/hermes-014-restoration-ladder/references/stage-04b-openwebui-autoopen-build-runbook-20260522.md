# Stage 04b Open WebUI Auto-Open Build Runbook

Use this reference to reproduce, verify, or repair the Stage 04b login
auto-open layer for Windows native Hermes 0.14.

This is part of the same restoration ladder as Stage 04a. Stage 04a keeps
`http://127.0.0.1:8642/health` alive. Stage 04b waits for that lifeline, starts
Docker/Open WebUI if needed, and opens `http://127.0.0.1:3000` after login.

## Objective

Make Windows login open the Hermes desktop panel / Open WebUI automatically,
without changing the already matured 8642 lifeline.

Target result:

```text
Windows login
  -> Startup folder VBS hidden wrapper
  -> Open-HermesOpenWebUI.ps1
  -> wait until 8642 health/models are ready and only one listener exists
  -> call mature launcher:
       H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1 -WaitAndOpen
  -> Docker Desktop starts if needed
  -> open-webui-clean starts if needed
  -> browser opens http://127.0.0.1:3000
```

## Boundaries

Do not use this stage to:

- start New API, Postgres, or Redis
- restore old Watchdog or AutoRecover
- change Telegram token or Telegram config
- change Open WebUI config
- replace the Stage 04a 8642 scheduled healthcheck

Telegram can become available after Hermes gateway starts, because the gateway
also owns the Telegram bridge. Stage 04b does not control Telegram; it only
opens the desktop/Open WebUI layer.

## Mature Path Reused

The mature existing Open WebUI path was reused instead of writing a new opener:

```text
H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1
```

Important existing behavior in that script:

- `-WaitAndOpen` runs the wait/open stage directly.
- `Ensure-Hermes` verifies 8642 health and models.
- `Ensure-Docker` starts Docker Desktop if the Docker API is not ready.
- `Ensure-OpenWebUI` starts `open-webui-clean` or `open-webui`.
- `Open-Page` opens `http://127.0.0.1:3000`.
- Success is logged as `FINAL_PASS Windows native Hermes page is ready`.

The wrapper exists only to make this mature path run automatically and quietly
after login, after Stage 04a has brought 8642 up.

## Installed Files

Primary Stage 04b files:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Startup entry:

```text
${REDACTED_SECRET}
```

Log and status files:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
H:\Hermes_Windows_Native_014\reports\daily-start-*.log
```

Backups:

```text
H:\Hermes_Backups\HERMES-014-STAGE04B-OPENWEBUI-AUTOOPEN-20260522
H:\CodexSkills\hermes-014-restoration-ladder
```

## Gate G01: Confirm Stage 04a Is Mature

Purpose: Stage 04b depends on Stage 04a; do not build browser auto-open until
8642 recovery is already stable.

Execution location:

```text
${REDACTED_SECRET}
```

Command:

```powershell
$ErrorActionPreference='Stop'; Get-ScheduledTask -TaskName 'Hermes8642SilentHealthCheck' | Select TaskName,State; Get-ScheduledTaskInfo -TaskName 'Hermes8642SilentHealthCheck' | Select LastRunTime,LastTaskResult,NextRunTime; (Invoke-WebRequest -Uri 'http://127.0.0.1:8642/health' -UseBasicParsing -TimeoutSec 10).StatusCode; (Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/models' -UseBasicParsing -TimeoutSec 10).Content
```

Success criteria:

- Task `Hermes8642SilentHealthCheck` exists and is `Ready`.
- Last task result is `0`.
- `/health` returns 200.
- `/v1/models` contains `hermes-agent`.

Failure recovery:

- Stop Stage 04b work.
- Repair Stage 04a from `stage-04-8642-silent-healthcheck-20260522.md`.

## Gate G02: Locate the Mature Open WebUI Route

Purpose: Reuse the old working launcher instead of creating a new Docker/browser
startup path.

Command:

```powershell
$ErrorActionPreference='Stop'; Test-Path 'H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1'; Test-Path 'H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd'; Select-String -LiteralPath 'H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1' -Pattern 'WaitAndOpen|Ensure-Docker|Ensure-OpenWebUI|FINAL_PASS Windows native Hermes page is ready'
```

Success criteria:

- Both files exist.
- The script contains `-WaitAndOpen` behavior and `FINAL_PASS` logging.

Failure recovery:

- Stop.
- Restore from H drive backup before writing any Startup entry.

## Gate G03: Install the Hidden Login Trigger

Purpose: Add only the Open WebUI auto-open trigger.

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

- Output includes `G_INSTALL_PASS_STAGE04B_STARTUP_VBS_READY`.
- Startup folder contains `HermesOpenWebUIAutoOpen.vbs`.

Failure recovery:

- Do not create scheduled tasks as a workaround unless explicitly requested.
- Inspect file paths and permissions.

## Gate G04: Local Manual Run

Purpose: Prove the wrapper works before reboot.

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

${REDACTED_SECRET}
  `result=FINAL_PASS`.
- Latest `daily-start-*.log` has
  `FINAL_PASS Windows native Hermes page is ready`.
- Browser opens `http://127.0.0.1:3000`.

Observed implementation note:

- The first wrapper version waited on the child PowerShell process too long.
- The fix was to treat `3000 OK + mature daily-start FINAL_PASS` as success,
  then write Stage 04b `FINAL_PASS`.

## Gate G05: Local Verification

Purpose: Verify full local state after the manual run.

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

- Output includes `G_STAGE04B_VERIFY_PASS`.
- Startup entry exists.
- 8642 has exactly one listener.
- `/health`, `/v1/models`, and chat pass.
- Open WebUI 3000 returns HTTP 200.
- Docker only runs `open-webui-clean` for this stage.
- No New API/Postgres/Redis/old Watchdog/AutoRecover is running.

## Gate G06: Backup and Skill Sync

Purpose: Preserve scripts, logs, reports, and skill reference on H drive.

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

- H backup directory exists.
- Local skill and H skill hashes match for `SKILL.md` and Stage 04b references.

## Gate G07: Reboot Verification Setup

Purpose: Create a one-shot post-reboot verifier before reboot.

Command:

```powershell
${REDACTED_SECRET}
```

Success criteria:

- Startup contains `HermesStage04bPostRebootVerify.vbs`.

Failure recovery:

- Do not reboot until the one-shot verifier is installed.

## Gate G08: Reboot and Verify

Purpose: Prove real reboot persistence.

Reboot command:

```powershell
shutdown.exe /r /t 5 /c "Stage04b Open WebUI auto-open reboot validation"
```

Post-reboot evidence file:

```text
${REDACTED_SECRET}
```

Success criteria:

- Report contains `G_STAGE04B_REBOOT_VERIFY_PASS`.
- `hermes-openwebui-autoopen-status.json` contains `FINAL_PASS`.
- Latest `daily-start-*.log` contains
  `FINAL_PASS Windows native Hermes page is ready`.
- Live recheck shows `/health=200`, `/v1/models=200`, chat marker returned,
  Open WebUI 3000 HTTP 200, one 8642 listener.
- No New API/Postgres/Redis/old Watchdog/AutoRecover is running.

Observed 2026-05-22 reboot result:

```text
BOOT_TIME=2026-05-22 21:55:53
Stage 04a recovered 8642 at 22:03:26
Stage 04b FINAL_PASS at 22:05:16
G_STAGE04B_REBOOT_VERIFY_PASS
```

## Gate G09: Telegram Relationship Check

Purpose: Explain and verify the relationship between Hermes auto-start and
Telegram availability.

Command:

```powershell
${REDACTED_SECRET}
```

Expected interpretation:

- `state api_server connected` should pass.
- `state telegram connected` should pass.
- A failure for the old
${REDACTED_SECRET}
  is expected in the Stage 04a/04b architecture, because Hermes is now restored
  by the scheduled 8642 lifeline instead of the old gateway Startup entry.

Optional outbound test without printing the token:

```powershell
${REDACTED_SECRET}
```

Observed 2026-05-22 result:

```text
Telegram timed out during boot/network warm-up.
Telegram auto-reconnected at 22:12:49 in polling mode.
Real inbound Telegram message at 22:17:38 produced response ready and Sending response at 22:17:43.
Outbound Bot API test returned TELEGRAM_SEND_OK=True.
```

Conclusion:

- When Hermes gateway is healthy and Telegram config/proxy are valid, Telegram
  can become usable automatically after the gateway starts.
- Open WebUI does not start Telegram; both are downstream of the Hermes gateway.

## Rollback

Remove only Stage 04b auto-open:

```powershell
${REDACTED_SECRET}
```

This removes the Startup VBS entry only. It does not delete scripts, logs,
Hermes, Open WebUI, Telegram, New API, or the Stage 04a 8642 healthcheck.

## Search Keywords

Use these when trying to find this work later:

```text
Stage 04b
Open WebUI auto-open
HermesOpenWebUIAutoOpen.vbs
Open-HermesOpenWebUI.ps1
start-hermes-openwebui.ps1 -WaitAndOpen
HERMES-014-STAGE04B-OPENWEBUI-AUTOOPEN-20260522
G_STAGE04B_REBOOT_VERIFY_PASS
H:\Hermes_Backups\HERMES-014-STAGE04B-OPENWEBUI-AUTOOPEN-20260522
H:\CodexSkills\hermes-014-restoration-ladder
```
