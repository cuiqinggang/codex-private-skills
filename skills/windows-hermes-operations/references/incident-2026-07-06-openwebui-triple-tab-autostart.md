# 2026-07-06 Open WebUI Triple Tab Autostart

Use this when Windows login or manual Hermes startup opens three Open WebUI
tabs/pages in Chrome.

## User-Visible Symptom

- The user's screenshot showed three Chrome tabs titled Open WebUI / "open WebUI".
- The user described it as three login/open browser flows running in parallel.

## Cause

Multiple login/autostart entries could open `http://127.0.0.1:3000`:

1. Current C-drive primary Startup entry:
   `Hermes_OpenWebUI_AutoStart_Hidden.vbs`
${REDACTED_SECRET}
2. Old Stage 04b Startup entry:
   `HermesOpenWebUIAutoOpen.vbs`
${REDACTED_SECRET}
   -> `start-hermes-openwebui.ps1 -WaitAndOpen`.
3. `Hermes_NewAPI_AutoRecover.ps1` could call
   `START-HERMES-WEBUI.cmd`, which runs `start-hermes-openwebui.ps1` without
   `-NoOpen`, so a recovery path could also open a browser page.

The primary autostart script's mutex was not enough because the old Stage 04b
wrapper and the NewAPI recovery script used different locks and entrypoints.

## Accepted Repair

Keep exactly one browser opener:

```text
${REDACTED_SECRET}
```

Disable the old Stage 04b browser opener:

```text
${REDACTED_SECRET}
```

Keep NewAPI/Telegram recovery ability, but prevent it from opening a browser:

```text
${REDACTED_SECRET}
$HermesLauncher = Join-Path $HermesRoot "launcher\start-hermes-openwebui.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $HermesLauncher -StartBackendOnly -NoOpen
```

Do not remove the gateway or Telegram persistence entries merely to fix browser
duplication.

## Verification Checklist

- `HermesOpenWebUIAutoOpen.vbs` is absent from the active Startup folder.
- Active Startup browser opener is only `Hermes_OpenWebUI_AutoStart_Hidden.vbs`.
- `Hermes_NewAPI_AutoRecover.ps1` parses successfully.
- `Hermes_NewAPI_AutoRecover.ps1` no longer references `START-HERMES-WEBUI.cmd`
  as its Hermes launcher.
- If present, stale scheduled task `Hermes_OpenWebUI_AutoStart` may still point
  to `H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd`; if the H
  path is missing and disabling the task is denied, record it as an admin-only
  cleanup item rather than treating it as the active browser opener.

## Trigger Keywords

- "Open WebUI opened three tabs"
- "Hermes login opens three"
- "three Open WebUI pages"
- "browser opens three times"
- "login autostart parallel three"

