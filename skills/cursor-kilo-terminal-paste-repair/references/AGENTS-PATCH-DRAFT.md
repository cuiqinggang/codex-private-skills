# AGENTS.md Patch Draft

## Cursor/Kilo Terminal Paste Repair Rule

When paste stops working in Cursor, Kilo Code, Claude Code, or a VS Code integrated terminal, first distinguish:

- system clipboard health
- long-text attachment conversion
- terminal focus/keybinding routing

If clipboard works elsewhere and Kilo/Cursor are alive, inspect and repair `%APPDATA%\Cursor\User\keybindings.json` before reinstalling or restarting tools. Ensure terminal-focused `Ctrl+V` and `Shift+Insert` route to `workbench.action.terminal.paste`, then verify in the real UI with a harmless non-executed paste probe.

Preferred skill:

```text
${REDACTED_SECRET}
```
