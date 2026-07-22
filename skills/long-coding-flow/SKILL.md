---
name: long-coding-flow
description: Use when the user asks for long-running coding, several-hour programming, Cursor or Claude Code long tasks, DeepSeek V4Pro coding, DeepClaude, Ralph Loop, handoff-based execution, or making coding work repeatable, testable, recoverable, and low-cost.
---

# Long Coding Flow

## Positioning

This is a mature execution package for long coding work. It is not a prompt for one big model run. It turns large engineering work into gated, testable, restartable, low-cost stages that Cursor, Claude Code, Codex, Hermes, or DeepSeek V4Pro can hand off safely.

## Use First When

- The task may take more than one focused session.
- The user wants Cursor + Claude Code + DeepSeek V4Pro to code for hours.
- The task needs checkpoints, tests, logs, handoff, rollback, or recovery.
- A loop tool such as Ralph Loop, DeepClaude, Claude Code, Codex, or Hermes may execute multiple rounds.

## Core Rule

Do not let an agent “just keep coding”. Build a task package first, then run one bounded stage at a time.

## ECC 2.0 Cross-Harness Addendum

When a long coding task involves ECC 2.0, multiple harnesses, MCP/tool sprawl,
parallel worktrees, multi-agent execution, or `orch-*` style orchestration,
read `references/ECC-2.0-CROSS-HARNESS-ABSORPTION-20260706.md` before creating
`02-plan.md`.

Use it as a read-only rule addendum. Do not install ECC, copy external configs,
enable hooks, change MCP settings, or modify global Claude Code / Codex /
Cursor / Hermes settings unless the user explicitly asks for that separate
operation.

## Required Task Package

Create or read these files before execution:

| File | Purpose |
|---|---|
| `00-goal.md` | Goal, non-goal, success criteria, forbidden changes |
| `01-context.md` | Relevant files, rules, risks, mature references |
| `02-plan.md` | 30-90 minute stages with verification |
| `03-execution-log.md` | Commands, results, evidence |
| `04-verification.md` | Tests, failures, root cause, next hypothesis |
| `05-handoff.md` | Done, not done, blocked, next first step |
| `06-next-actions.md` | Low-risk next steps, approval-needed items, do-not-do list |
| `07-loop-control.md` | max rounds, timebox, stop signals, allowed dirs, forbidden commands |
| `08-rollback.md` | checkpoint, diff, backup, recovery |
| `09-decisions.md` | key tradeoffs and why they were chosen |

Use `templates/long-coding-next-sprint/` when starting from scratch.

For cross-harness or parallel-agent tasks, `01-context.md` and `05-handoff.md`
must also include a session snapshot, tool/MCP inventory, worktree lifecycle
summary, and operation type when applicable.

## Gated Flow

| Gate | Purpose | Continue When | Stop When |
|---|---|---|---|
| G01 Goal | goal and forbidden changes are explicit | success criteria are testable | goal is subjective or drifting |
| G02 Environment | cwd, branch, deps, current diff are known | rollback point exists | user changes may be overwritten |
| G03 Context | project rules and relevant files are read | enough context for this stage | missing critical rule |
| G04 Split | stages are 30-90 minutes | each stage has one deliverable | stage is too broad |
| G05 Verify | tests/checks are defined before edits | command or checklist exists | no meaningful verification |
| G06 Execute | only current stage is changed | within allowed files | scope expands |
| G07 Log | commands and evidence are recorded | log and verification updated | evidence missing |
| G08 Debug | failure layer is identified | smallest repair is clear | repeated guessing |
| G09 Handoff | next worker can resume from files | handoff is complete | next step depends on chat memory |
| G10 Sediment | success becomes skill/script/rule | verification passed | not validated |

## Execution Rules

- One stage at a time.
- Prefer existing tests and project rules before adding abstractions.
- Keep context narrow for low-cost models.
- Never feed full old chats back into the model; use task package + latest handoff + verification.
- If using DeepClaude or DeepSeek V4Pro, only use temporary process-level settings after approval.
- Record every command that changes files or verifies behavior.

## Stop And Ask

Stop before:

- API key, Cookie, token, paid API, account login, or captcha.
- Production config changes: Hermes, Codex global rules, Open WebUI, Cursor global settings.
- Long-lived background service or Windows scheduled task changes.
- Deleting files, large batch rewrites, unknown install scripts, or remote write permissions.
- Two repeated failures with unclear root cause.

## Verification

A long-coding task is not complete because code was written. It is complete only when:

- the stage success criteria pass,
- `03-execution-log.md` and `04-verification.md` are updated,
- `05-handoff.md` states the next recoverable step,
- risky or skipped checks are explicitly listed.
