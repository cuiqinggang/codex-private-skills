# Failure Modes

## False Clipboard Diagnosis

If paste works elsewhere and clipboard formats show `UnicodeText`, the clipboard is probably healthy. Continue to Cursor terminal focus/keybinding checks.

## Long Text Converter Confusion

The Codex long-text fallback can turn very long clipboard text into a file-drop attachment for Codex. It should ignore short text below its threshold. If `ContainsFileDropList` is false and text length is small, the converter is not the paste blocker.

## Kilo Service Confusion

Kilo can be running and listening while terminal paste still fails. Do not reinstall or restart Kilo until keyboard routing has been checked.

## Webview Focus Theft

Kilo's chat/input Webview and Cursor's integrated terminal share the same window. A click in the wrong area can route paste to the Kilo input or nowhere visible. Terminal-scoped keybindings plus clicking the bottom terminal prompt resolve the common case.

## Keybindings Present But Paste Still Feels Broken

Observed on 2026-06-30: `keybindings.json` already contained the proven `ctrl+v` and `shift+insert` terminal paste bindings, the clipboard contained normal text, and Cursor/Kilo was running. In this state, do not diagnose the old terminal shortcut bug as missing again.

Split the symptom by target:

- Bottom PowerShell/integrated terminal: click the prompt first, then use `Ctrl+V` or `Shift+Insert`. If this works, terminal paste is healthy.
- Kilo/Claude Code chat Webview input: long text may be blocked by the webview/input path or handled as an attachment/converter workflow. Terminal keybindings do not control this field.
- Very long pasted material: prefer saving as a `.txt` file and attaching/importing it, or use the relevant long-text attachment workflow if the target app is Codex Desktop.

If the user says "long or short both fail", verify with two harmless probes: one short probe into the terminal prompt and one short probe into the Kilo input field. The fix depends on which target fails.

## Probe Cleanup Trouble

PowerShell integrated terminals may not respond to `Ctrl+U` like Unix shells. Prefer not to execute probes. Use backspace, `Esc`, or `Ctrl+C` to cancel the current input line after verification.
