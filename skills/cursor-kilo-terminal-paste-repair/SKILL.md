---
name: cursor-kilo-terminal-paste-repair
description: Use when paste stops working in the Cursor, Kilo Code, Claude Code, or VS Code integrated terminal on Windows, especially when clipboard works elsewhere but Ctrl+V does not paste into the terminal. Diagnoses clipboard formats, Kilo/Cursor process health, terminal focus, keybinding routing, and repairs terminal paste with evidence.
---

# Cursor/Kilo Terminal Paste Repair

## Purpose

Restore paste into Cursor/Kilo/Claude Code integrated terminals without confusing three different failure classes:

- system clipboard failure
- long-text attachment converter behavior
- Cursor/VS Code terminal keybinding and focus routing failure

The 2026-06-28 proven fix was: add explicit terminal-focused keybindings for `ctrl+v` and `shift+insert` to `Cursor\User\keybindings.json`.

## Known Root Cause Pattern

If paste works in other apps, the clipboard contains normal text, Kilo is running, and the integrated terminal is visible, the likely failure is not the clipboard. It is usually Cursor's keybinding/focus layer failing to route `Ctrl+V` to `workbench.action.terminal.paste` when terminal focus is active.

This can happen after extension updates, focus changes between Kilo Webview and the terminal, or missing user keybindings. Kilo itself may still be healthy.

## Fast Path

1. Check clipboard:

```powershell
Add-Type -AssemblyName System.Windows.Forms
[pscustomobject]@{
  ContainsText = [System.Windows.Forms.Clipboard]::ContainsText()
  TextLength = if ([System.Windows.Forms.Clipboard]::ContainsText()) { ([System.Windows.Forms.Clipboard]::GetText()).Length } else { 0 }
  ContainsFileDropList = [System.Windows.Forms.Clipboard]::ContainsFileDropList()
}
```

2. Check Cursor and Kilo are alive:

```powershell
Get-Process Cursor -ErrorAction SilentlyContinue | Where-Object MainWindowHandle -ne 0
Get-CimInstance Win32_Process | Where-Object { $_.Name -ieq "kilo.exe" -or $_.CommandLine -match "kilocode|kilo-code" }
```

3. Apply the minimal terminal paste keybinding repair:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\cursor-kilo-terminal-paste-repair\scripts\repair-cursor-terminal-paste.ps1"
```

4. Open the real Cursor/Kilo window and verify visually:

- terminal prompt visible
- a harmless probe text pastes into the terminal
- the probe is not executed
- the line is cleaned or cancelled afterward

## Repair

The repair ensures this exists in:

```text
%APPDATA%\Cursor\User\keybindings.json
```

```json
[
  {
    "key": "ctrl+v",
    "command": "workbench.action.terminal.paste",
    "when": "terminalFocus && terminalProcessSupported"
  },
  {
    "key": "shift+insert",
    "command": "workbench.action.terminal.paste",
    "when": "terminalFocus && terminalProcessSupported"
  }
]
```

If the file already has entries, merge without deleting unrelated user shortcuts. Always make a timestamped backup before editing.

## Acceptance Criteria

Report `TERMINAL_PASTE_REPAIR_PASS` only when all are true:

- clipboard contains normal text or the clipboard issue is separately identified
- Kilo/Cursor process is alive or the app failure is separately identified
- `keybindings.json` is valid JSON after edit
- real Cursor/Kilo window was opened or captured
- harmless paste probe reached the integrated terminal
- probe was not executed
- test line was cleaned or cancelled

If UI verification cannot be automated, report `PARTIAL_PASS_NEEDS_MANUAL_PASTE_TEST`.

## Files

- `scripts/repair-cursor-terminal-paste.ps1`: backup and merge terminal paste keybindings.
- `references/SOP.md`: full diagnostic and repair procedure.
- `references/FAILURE-MODES.md`: common false diagnoses and fixes.
- `references/AGENTS-PATCH-DRAFT.md`: optional global rule patch.
- `logs/recent-use-log.md`: append-only use history.
- `acceptance/index.html`: visual acceptance summary for this deployment.
