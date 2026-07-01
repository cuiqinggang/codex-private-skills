# Incident 2026-06-02 - Stage 04b Auto-Open Repair For Hermes 0.15.2

Use this note when the Windows login auto-open flow starts Hermes but never
opens the browser, or the console shows repeated:

```text
API server rejected invalid API key ... method='GET' path='/v1/models'
```

## Root Cause

Hermes 0.15.2 requires `API_SERVER_KEY` for `/v1/models` and chat requests.
The Stage 04b scripts from 2026-05-22 still used unauthenticated local checks:

```powershell
Invoke-WebRequest http://127.0.0.1:8642/v1/models
```

After the 0.15.2 upgrade, `/health` returned OK but `/v1/models` failed, so
`Open-HermesOpenWebUI.ps1` waited until timeout with:

```text
health=True models=False listeners=1
FINAL_FAIL HERMES_8642_LIFELINE_NOT_READY_AFTER_900s
```

A second issue appeared after switching Telegram persistence to a Startup
folder fallback: `Hermes_Gateway.cmd` launched in a visible cmd window. The
original Stage 04b user experience should be hidden startup plus browser open,
not a foreground gateway console.

## Repair

Patch the Stage 04b and post-reboot verification scripts to read
`API_SERVER_KEY` from `C:\Users\A\.hermes\.env` and send it only to local 8642
requests as:

```powershell
@{ Authorization = "Bearer $key" }
```

Patched files:

```text
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Open-HermesOpenWebUI.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Verify-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\openwebui-autoopen\PostReboot-Verify-HermesOpenWebUIAutoOpen.ps1
C:\Users\A\Hermes_AutoStart\healthcheck-8642\PostReboot-Verify-Hermes8642.ps1
```

Also sync the same `API_SERVER_KEY` into:

```text
H:\Hermes_Windows_Native_014\runtime\.hermes\.env
```

This lets the Stage 04a runtime launcher survive the 0.15.2 auth requirement.
Do not print the key.

Patch `H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1` so it
recognizes 8642 owners launched via hidden `python.exe -m hermes_cli.main
gateway run --replace`. The direct 8642 owner may not contain
`H:\Hermes_Windows_Native_014` in its command line; inspect parent process
lineage before treating it as an unknown port conflict.

## Hidden Startup Entry

To avoid a visible cmd window at login, keep the gateway command script as the
target script but install a hidden VBS wrapper in Startup:

```text
C:\Users\A\.hermes\gateway-service\Hermes_Gateway.cmd
C:\Users\A\.hermes\gateway-service\Hermes_Gateway_Hidden.vbs
C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway_Hidden.vbs
```

Move the visible Startup `Hermes_Gateway.cmd` out of the Startup folder into
the repair backup instead of deleting it.

Keep the Stage 04b browser opener:

```text
C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\HermesOpenWebUIAutoOpen.vbs
```

## Verification

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Open-HermesOpenWebUI.ps1" -WaitForHermesSeconds 120
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_AutoStart\openwebui-autoopen\Verify-HermesOpenWebUIAutoOpen.ps1" -Marker "HERMES_STAGE04B_0152_OK"
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\windows-hermes-operations\scripts\check_windows_hermes_health.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

Expected evidence:

```text
FINAL_PASS Stage 04b opened http://127.0.0.1:3000
G_STAGE04B_VERIFY_PASS
WINDOWS_HERMES_HEALTHCHECK_PASS
check-hermes-telegram.ps1 Result: PASS
```

If Xiaolongxia containers are running, do not count `xiaolongxia-new-api`,
`xiaolongxia-postgres`, or `xiaolongxia-redis` as Stage 04b violations. They
are isolated on the Xiaolongxia stack and are not Hermes/Open WebUI New API.

## Successful Evidence From 2026-06-02

- `Open-HermesOpenWebUI.ps1 -WaitForHermesSeconds 120`: exit 0.
- `hermes-openwebui-autoopen-status.json`: `result=FINAL_PASS`, detail
  `Opened http://127.0.0.1:3000`.
- Latest daily launcher log:
  `H:\Hermes_Windows_Native_014\reports\daily-start-20260602-183658.log`.
- Daily launcher log contains `FINAL_PASS Windows native Hermes page is ready`.
- Stage 04b verifier returned `G_STAGE04B_VERIFY_PASS`.
- Startup folder contains `HermesOpenWebUIAutoOpen.vbs` and
  `Hermes_Gateway_Hidden.vbs`, not visible `Hermes_Gateway.cmd`.
