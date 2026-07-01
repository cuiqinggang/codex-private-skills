# AGENTS.md Patch Draft: Claude Code Cursor Predeploy

Add this rule to workspaces where Claude Code + Cursor upgrade work is likely:

```markdown
## Claude Code Cursor Predeploy Rule

When a task involves upgrading, repairing, routing, or deploying Claude Code inside Cursor, do not start from zero and do not delete/reinstall first.

First use:

`C:\Users\A\.codex\skills\claude-code-cursor-super-tool-predeploy`

Required order:

1. Collect existing Cursor + Claude Code stack information.
2. Classify current pieces as keep, adapt, replace, or fill.
3. Produce blocker report.
4. Remove only safe predeploy blockers with backups.
5. Enter formal long deployment only after reports and evidence exist.

Never print full API keys or tokens. Preserve Cursor, existing Claude Code skeleton, Codex, Hermes, Open WebUI, and DeepSeek/OpenRouter evidence unless the user explicitly asks to change them.
```
