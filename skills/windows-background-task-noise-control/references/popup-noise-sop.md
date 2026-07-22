# Popup And Boot Blue Window SOP

## Diagnose

- Compare visible-window time with process `CreationDate`.
- Long-lived blank blue window usually means a listener/UI helper was launched in a normal PowerShell console.
- Short flashes often come from Startup `.cmd` files, scheduled task actions, or nested `Start-Process powershell.exe` calls without hidden window style.
- `conhost.exe` is usually evidence of a console host; trace its parent process.

## Common Fixes

- Scheduled task launches PowerShell visibly: add `-WindowStyle Hidden`.
- Startup `.cmd` flashes: replace the Startup shortcut/entry with a hidden `.vbs` wrapper.
- Task action cannot be edited: modify the target `.cmd` to call hidden/minimized PowerShell.
- Nested launcher in a `.ps1` starts a watcher: add `-WindowStyle Hidden` to the child `Start-Process`.
- Per-minute scheduled PowerShell task still flashes despite `-WindowStyle Hidden`: switch the task action to `wscript.exe "Run-...-Hidden.vbs"`, and let that VBS call the PowerShell script with `WScript.Shell.Run command, 0, False`.
- GUI helper launched by console: keep the GUI visible, hide the console launcher.
- Visible widget watchdog restarts a GUI through PowerShell: keep the widget visible, but add hidden/minimized console handling to the watchdog restart command and verify the widget log still refreshes.
- Codex quota panel blue window: if `Windows PowerShell` and `Codex Quota` share the same `CodexQuotaPanel.ps1` PID, do not add `-WindowStyle Hidden` to the panel launcher. Hide only the host console from inside `CodexQuotaPanel.ps1` with `GetConsoleWindow` + `ShowWindow(..., 0)`, then run the quota-panel hardening check.
- Hermes gateway black window: if the gateway is a long-lived `cmd.exe -> python.exe -m hermes_cli.main gateway run --replace` chain, do not disable Hermes. Run it through `pythonw.exe` with a small wrapper that preserves stdout/stderr logs, then verify 8642 `/health` and `/v1/models`.

## Protected Useful Widgets

- Codex quota panel: keep the bottom-right quota widget visible and auto-starting. Only hide the launcher console.
- Knowledge Brain and CodeGraph: keep useful sync/indexing jobs unless the user asks to disable them; use hidden execution or lower frequency.

## Evidence To Save

- Process command line and parent PID.
- Startup shortcut target before/after.
- Scheduled task XML backup.
- Modified launcher files.
- Logs proving preserved features still run.
- Unresolved access-denied items.
