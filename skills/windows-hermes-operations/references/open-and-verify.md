# Open and Verify Windows Native Hermes

Use these gates when the user asks to open Windows native Hermes / Windows版爱马仕.

## G01 Open

Purpose: Start the existing Windows native Hermes 0.14 launcher and Open WebUI.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
cmd.exe /c "H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd"
```

Success criteria:

- Command exits with code 0.
- Latest `H:\Hermes_Windows_Native_014\reports\daily-start-*.log` contains `FINAL_PASS Windows native Hermes page is ready`.
- Browser opens `http://127.0.0.1:3000`.

Failure criteria:

- Non-zero exit code.
- Latest daily-start log contains a `FAIL` line.
- 8642 is not owned by Windows native Hermes.

Failure recovery:

- Read the latest daily-start log first.
- Verify 8642 owner and `/v1/models`.
- Do not do broad recursive path discovery.

Continue or stop:

- Continue to G02 on success.
- Stop and inspect the failing layer on failure.

## G02 Verify Backend and Page

Purpose: Prove the new Windows native Hermes backend and Open WebUI are usable.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$owner = Get-NetTCPConnection -LocalPort 8642 -State Listen -ErrorAction Stop | Select-Object -First 1
$proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($owner.OwningProcess)"
"PORT_8642_OWNER=$($proc.CommandLine)"
(Invoke-WebRequest -Uri "http://127.0.0.1:8642/health" -UseBasicParsing -TimeoutSec 10).Content
(Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/models" -UseBasicParsing -TimeoutSec 10).Content
$page = Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 20
"OPENWEBUI_CODE=$([int]$page.StatusCode)"
```

Success criteria:

- `PORT_8642_OWNER` includes `H:\Hermes_Windows_Native_014`.
- `/health` includes `"platform": "hermes-agent"`.
- `/v1/models` includes `"id": "hermes-agent"`.
- `OPENWEBUI_CODE=200`.

Failure criteria:

- 8642 owner is `wslrelay.exe` or anything outside `H:\Hermes_Windows_Native_014`.
- `/v1/models` does not include `hermes-agent`.
- 3000 does not return HTTP 200.

Failure recovery:

- Read `references/cleanup-20260520.md` only if WSL or old OpenClaw appears in current evidence.
- Otherwise inspect latest `H:\Hermes_Windows_Native_014\reports\daily-start-*.log`.

Continue or stop:

- Stop after G02 and report exact evidence.

## Timing

After the old WSL cleanup on 2026-05-20, normal opens should no longer spend time cleaning a stale WSL 8642 owner. The launcher may still include its built-in 90 second staged wait when it starts backend components.
