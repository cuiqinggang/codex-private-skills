# Recent Use Log

## 2026-06-28

- Trigger: user reported paste no longer worked in the Claude Code/Kilo terminal, while paste worked elsewhere.
- Diagnosis: clipboard contained normal text; no file-drop attachment; Kilo process was running; Cursor terminal was visible; `keybindings.json` did not exist.
- Fix: added terminal-focused `Ctrl+V` and `Shift+Insert` keybindings to `%APPDATA%\Cursor\User\keybindings.json`.
- Evidence: real Cursor/Kilo window captured; harmless probe text pasted into bottom PowerShell terminal and was not executed.
- Result: `TERMINAL_PASTE_REPAIR_PASS`.

## 2026-06-30

- Trigger: user reported the Claude Code/Kilo paste problem may have returned and referenced the previous Ctrl+V repair.
- Diagnosis: clipboard contained normal text; no file-drop list; Cursor and Kilo were running; `keybindings.json` already contained the two proven terminal paste bindings.
- Fix: re-ran `repair-cursor-terminal-paste.ps1` to normalize the keybindings file and create a fresh backup.
- New lesson: when bindings are present, split the issue into bottom integrated terminal paste versus Kilo/Claude Code Webview input paste. The old Ctrl+V terminal fix cannot repair a webview long-text input limit or focus issue.
- Result: `TERMINAL_PASTE_KEYBINDINGS_PRESENT`; UI probe still required for full `TERMINAL_PASTE_REPAIR_PASS`.
