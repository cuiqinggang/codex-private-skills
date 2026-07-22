# 2026-06-08 Hermes Open WebUI Autostart Conflict Hardening

Use this when Windows login/reboot does not automatically bring Hermes into the
browser, when multiple autostart entries may conflict, or when the user asks to
make the Hermes/Open WebUI/Telegram startup flow durable.

## Accepted Goal

The desired login chain is:

```text
Windows login
-> Hermes 8642
-> Docker Desktop background engine
-> open-webui-clean
-> Open WebUI 3000
-> existing Google Chrome profile opens http://127.0.0.1:3000
-> Telegram remains connected through Hermes 8642
```

Docker Desktop account login is not required. Do not treat the Docker login UI
as a blocker. The background engine and Open WebUI container are what matter.

## Symptoms Observed

On 2026-06-08 the system was mostly healthy, but autostart had conflict risk:

- `Hermes_OpenWebUI_AutoStart` existed and returned `Last Result: 0`.
- Recent autostart logs showed multiple runs around login/manual recovery:
  `10:15`, `10:36`, and `10:40`.
- The task had `DisallowStartIfOnBatteries=True` and
  `StopIfGoingOnBatteries=True`.
- `Set-ScheduledTask` returned `Access is denied`, so task power settings could
  not be changed from the current non-elevated session.
- Multiple simultaneous launches initially wrote to the same second-based log
  file, mixing `FINAL_SKIP` and `FINAL_PASS`.

## Fix Applied

Primary script:

```text
H:\Hermes_Windows_Native_014\launcher\auto-start-hermes-openwebui.ps1
```

Changes:

1. Added a named mutex:

```text
Global\HermesOpenWebUIAutoStart
```

If another instance is already running, the second instance logs:

```text
FINAL_SKIP another Hermes Open WebUI autostart instance is already running
```

and exits successfully. This prevents scheduled task, Startup VBS, and manual
runs from cleaning Docker or opening browsers at the same time.

2. Changed log naming from seconds-only to millisecond plus PID:

```text
autostart-YYYYMMDD-HHMMSS-fff-PID.log
```

This prevents two instances launched in the same second from mixing logs.

3. Added explicit browser open logic:

```text
Open-OpenWebUIBrowser
```

It opens:

```text
C:\Program Files\Google\Chrome\Application\chrome.exe http://127.0.0.1:3000
```

This uses the user's existing Chrome user profile instead of launching an
isolated temporary browser.

4. Added Startup-folder fallback:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

The VBS runs:

```text
H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd
```

hidden at login. Keep the scheduled task too; the mutex makes dual launch safe.

## Verification Evidence

Direct autostart run:

```text
PASS Hermes /health 200
PASS Hermes /v1/models has hermes-agent
PASS docker ps stable first pass
INFO container status: open-webui-clean|Up ... (healthy)
PASS open-webui-clean running
PASS Open WebUI 3000 HTTP 200
OPEN existing Google Chrome profile to http://127.0.0.1:3000
PASS browser opened http://127.0.0.1:3000
FINAL_PASS Windows native Hermes Open WebUI autostart ready
```

Concurrent launch test:

```text
autostart-20260608-111138-991-3660.log -> FINAL_PASS
autostart-20260608-111139-009-20160.log -> FINAL_SKIP
```

Telegram strict diagnostic with browser panel required:

```text
Hermes health endpoint PASS
Hermes models endpoint PASS
Open WebUI PASS HTTP 200
state api_server connected PASS
state telegram connected PASS
Result: PASS
```

Docker/Open WebUI direct proof:

```text
docker desktop status -> Status running
open-webui-clean|Up ... (healthy)|0.0.0.0:3000->8080/tcp
curl http://127.0.0.1:3000 -> HTTP_CODE=200
```

## Important Rules For Future Repairs

- Do not delete `open-webui-clean`, Docker volumes, Open WebUI database, or
  Hermes config to fix autostart.
- Do not use a temporary Chromium/Playwright browser to claim browser login
  success. Use the user's already logged-in Google Chrome profile.
- Do not make Docker account login part of the acceptance criteria.
- If Task Scheduler settings cannot be changed because of access denied, keep
  the task and add a Startup-folder fallback that calls the same locked script.
- If two autostart mechanisms exist, the script-level mutex is the safety
  boundary.

## Rollback

Backups created:

```text
${REDACTED_SECRET}
```

Rollback script:

```text
copy auto-start-hermes-openwebui.ps1.bak H:\Hermes_Windows_Native_014\launcher\auto-start-hermes-openwebui.ps1
```

Rollback Startup fallback:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

