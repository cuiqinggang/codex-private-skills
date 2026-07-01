# Long Coding Flow Integration

Use `long-coding-flow` for L3 and above.

Required task package files:

```text
00-goal.md
01-context.md
02-plan.md
03-execution-log.md
04-verification.md
05-handoff.md
06-next-actions.md
07-loop-control.md
08-rollback.md
09-decisions.md
```

## Stage Rules

- One bounded stage at a time.
- Prefer 30-90 minute stages.
- Define verification before edits.
- Record evidence after commands and changes.
- Update handoff before stopping.
- Stop after repeated unclear failures.

## Recovery Rule

Resume from `05-handoff.md`, latest `04-verification.md`, and current diff/evidence. Do not rely on old chat memory.
