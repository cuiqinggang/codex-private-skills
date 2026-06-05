# Stage 01 Open WebUI Panel

Use this reference after Stage 00 passes and the user asks to start the Hermes
desktop panel / page / Open WebUI layer.

This stage restores only:

```text
Open WebUI 3000
  -> Windows native Hermes 8642
  -> DeepSeek V4 Pro
```

It must not restore New API, Telegram, Watchdog, AutoRecover, Startup entries,
or scheduled-task reboot persistence.

## Gate G01 Start Panel

Purpose: start the Open WebUI panel using the existing Windows native Hermes
daily launcher.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$ErrorActionPreference='Stop'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1' -WaitAndOpen
```

Success criteria:

- The command exits 0.
- The newest `H:\Hermes_Windows_Native_014\reports\daily-start-*.log` contains
  `FINAL_PASS Windows native Hermes page is ready`.
- Browser opens `http://127.0.0.1:3000`.

Failure criteria:

- The launcher returns non-zero.
- The latest daily-start log contains `FAIL`.
- Docker cannot start Open WebUI.
- Port 3000 is not Open WebUI.

Failure recovery:

- Read the latest daily-start log first.
- Do not start New API, Telegram, Watchdog, or AutoRecover to compensate.

## Gate G02 Verify Panel State

Purpose: prove the panel layer works and nothing above Stage 01 was started.

Execution location: `C:\Users\A\Desktop\1`

Command:

```powershell
$owner = Get-NetTCPConnection -LocalPort 8642 -State Listen -ErrorAction Stop | Select-Object -First 1
$proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($owner.OwningProcess)"
"PORT_8642_OWNER=$($proc.CommandLine)"

$health=Invoke-WebRequest -Uri 'http://127.0.0.1:8642/health' -UseBasicParsing -TimeoutSec 10
'HEALTH_STATUS='+$health.StatusCode
$health.Content

$models=Invoke-WebRequest -Uri 'http://127.0.0.1:8642/v1/models' -UseBasicParsing -TimeoutSec 10
'MODELS_STATUS='+$models.StatusCode
$models.Content

$page=Invoke-WebRequest -Uri 'http://127.0.0.1:3000' -UseBasicParsing -TimeoutSec 20
'OPENWEBUI_STATUS='+$page.StatusCode
'OPENWEBUI_HAS_TEXT='+($page.Content -match 'Open WebUI')

docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

$self=$PID
Get-CimInstance Win32_Process |
  Where-Object {
    $_.ProcessId -ne $self -and
    $_.CommandLine -match 'Watchdog|watchdog|Telegram|telegram|NewAPI|AutoRecover|new-api-local|Hermes_NewAPI'
  } |
  Select ProcessId,Name,CommandLine | Format-List
```

Success criteria:

- `PORT_8642_OWNER` includes `H:\Hermes_Windows_Native_014`.
- `HEALTH_STATUS=200`.
- `MODELS_STATUS=200` and content includes `hermes-agent`.
- `OPENWEBUI_STATUS=200`.
- `OPENWEBUI_HAS_TEXT=True`.
- `docker ps` shows `open-webui-clean` only for this layer.
- No New API, Telegram, Watchdog, or AutoRecover process appears.

## 2026-05-22 Evidence

Command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1' -WaitAndOpen
```

Observed:

- Log: `H:\Hermes_Windows_Native_014\reports\daily-start-20260522-184336.log`
- `G01_PASS Windows native Hermes 8642 already healthy`
- `G02_PASS Docker API already ready`
- `G03_START docker start open-webui-clean`
- `PASS Open WebUI HTTP 3000`
- `G04_PASS opened http://127.0.0.1:3000`
- `FINAL_PASS Windows native Hermes page is ready`

Verification:

- `HEALTH_STATUS=200`
- `/health` returned `{"status": "ok", "platform": "hermes-agent"}`
- `MODELS_STATUS=200`
- `/v1/models` returned `hermes-agent`
- `OPENWEBUI_STATUS=200`
- `OPENWEBUI_HAS_TEXT=True`
- `docker ps` showed only `open-webui-clean` running.
- No New API, Telegram, Watchdog, or AutoRecover process was found.
