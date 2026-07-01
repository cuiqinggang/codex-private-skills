# Rule Patch: Claude Code Cursor Predeploy

## Trigger

Apply this rule when a task mentions:

- Claude Code in Cursor
- Cursor as Claude Code entry
- Claude Code super tool
- CCR / Claude Code Router
- DeepSeek or OpenRouter Claude Code route
- existing Claude Code skeleton
- blocker elimination before deployment
- "do not start from zero"

## Rule

Before modifying the Claude Code + Cursor environment, Codex must:

1. Treat the existing setup as a partially working skeleton.
2. Run read-only information collection first.
3. Classify current components as keep, adapt, replace, or fill.
4. Generate a blocker report before attempting fixes.
5. Back up config before any write.
6. Hide secrets in every report.
7. Preserve Cursor as the default entry unless the user explicitly changes the architecture.
8. Preserve Codex, Hermes, Open WebUI, DeepSeek backup routes, and existing reports unless the task explicitly targets them.

## Stop Conditions

Stop and ask for user approval if:

- A destructive reinstall seems necessary.
- A secret value would need to be displayed.
- The task requires closing or interrupting other running AI tools.
- A change would modify unrelated Codex, Hermes, Open WebUI, or default GPT configuration.

## Acceptance

This rule is active only if the task report includes:

- Information collection status
- Blocker analysis status
- Predeploy elimination status
- Backup path or explicit no-write statement
- Final status code
