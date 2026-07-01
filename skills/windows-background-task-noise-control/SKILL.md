---
name: windows-background-task-noise-control
description: Diagnose and quiet Windows startup/background interruptions. Use when the user reports blue PowerShell/cmd windows, blank console windows, beeps, windows that pop up then disappear, boot-time blue screens/windows, scheduled tasks interrupting work, or asks to make Codex/AI/Hermes/Knowledge Brain/CodeGraph maintenance jobs run silently while preserving useful visible widgets such as the Codex quota panel.
---

# Windows Background Task Noise Control

## Purpose

Find the launcher causing visible PowerShell/cmd windows and make only that launcher silent. Preserve useful background jobs and intentionally visible UI widgets.

## Workflow

1. Capture evidence:
   - Note screenshot text, window title, approximate time, and whether it is a long-lived blank console or a short flash.
   - Read `references/popup-noise-sop.md` for boot/startup cases or repeated incidents.
2. Inspect sources:
   - Current processes: `powershell.exe`, `cmd.exe`, `conhost.exe`, `wscript.exe`, `cscript.exe`, with `CreationDate`, `ParentProcessId`, and `CommandLine`.
   - Startup folders: current user and ProgramData Startup.
   - Custom scheduled tasks: root `\` tasks and names containing `AI`, `Codex`, `Knowledge`, `CodeGraph`, `Hermes`, `sync`, `watchdog`, `LongText`, or `Quota`.
   - Use `scripts/audit-noisy-scheduled-tasks.ps1` for a quick combined audit.
3. Back up before changing:
   - Export scheduled task XML.
   - Copy `.cmd`, `.ps1`, `.vbs`, and `.lnk` launchers to a timestamped backup folder.
4. Quiet the launcher, not the feature:
   - For scheduled PowerShell actions, add `-WindowStyle Hidden`.
   - For Startup `.cmd` files that still flash, replace the Startup entry with a `.vbs` wrapper using `WScript.Shell.Run command, 0, False`.
   - For frequent scheduled tasks that still flash even with `-WindowStyle Hidden`, change the task action to a `.vbs` wrapper that runs PowerShell with window style `0`.
   - For `.cmd` files that must remain task targets, make their internal PowerShell launch use `start "" /min powershell.exe -WindowStyle Hidden ...`.
   - For visible widgets such as the Codex quota panel, keep the widget visible and hide only the launcher/watchdog console.
   - Preserve script paths, arguments, trigger frequency, and useful functionality.
5. Verify:
   - Re-read startup shortcuts/tasks.
   - Confirm useful widgets still work, especially Codex quota.
   - Check logs and run a short process watch for newly created console processes.
6. Report:
   - List changed launchers, backup location, remaining access-denied items, and whether each feature was preserved.

## Guardrails

- Never disable, delete, or unregister tasks unless the user explicitly asks.
- Do not bulk-edit Microsoft system tasks.
- If `Set-ScheduledTask` returns access denied, report it and quiet the target script if safe; do not force-recreate the task.
- Treat `CodexQuotaPanel.ps1` specially: the bottom-right Codex quota panel is intentionally visible. Keep the widget visible and auto-starting; hide only its PowerShell/cmd launcher.
- Treat Knowledge Brain and CodeGraph jobs as useful unless the user asks to disable them; prefer hidden execution and lower frequency.

## Useful Patterns

- PowerShell task action:
  `powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "script.ps1"`
- Hidden VBS wrapper:
  `CreateObject("WScript.Shell").Run "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""script.ps1""", 0, False`
- Per-minute watchdog task:
  use `wscript.exe "Run-...-Hidden.vbs"` as the scheduled-task action, then let the VBS start the real PowerShell script hidden.
