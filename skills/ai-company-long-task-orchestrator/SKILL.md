---
name: ai-company-long-task-orchestrator
description: Specialist orchestrator for long AI Company OS, Obsidian Knowledge OS, and related operating-dashboard projects that need staged execution, independent review, and handoff. Use only for this AI-company vertical; route ordinary long tasks to the general or ECC orchestrator. Do not use for small edits, casual Q&A, or tasks without evidence requirements.
---

# AI Company Long Task Orchestrator

## Purpose

This skill turns a large user-approved task into a disciplined long-running Codex execution loop.

It is designed for:
- AI Company OS
- Obsidian Knowledge OS
- dashboard development
- staged long tasks
- Independent Reviewer Gate workflows
- evidence-based acceptance loops

## Hard Rules

1. Do not ask the user to review every tiny step.
2. Execute in large stages.
3. Preserve user context.
4. Produce evidence, not vague claims.
5. Prefer 60-120 minute task packages when the task is large.
6. Never silently modify high-risk files.
7. Stop and ask before touching credentials, external accounts, real publishing channels, or destructive operations.
8. For requests about GPT/Codex responsibility, independent review, or ChatGPT Work handoff, read `references/GPT-CODEX-ROLE-TRANSFER-PROTOCOL-20260710.md` before planning.
9. Never report “GPT reviewed it” without naming the actual reviewer and review mode.
10. When multi-agent review is requested and available, use a separate read-only-first reviewer; otherwise label the fallback honestly.

## Required Workflow

For every long task:

1. Restate task goal.
2. Freeze boundaries.
3. Scan relevant project files.
4. Build execution plan.
5. Create or verify Git checkpoint if repo exists.
6. Execute implementation.
7. Run self-check.
8. Produce evidence package.
9. Produce an Independent Reviewer Gate package that declares `REVIEW_MODE` and `REVIEWER`.
10. Record lessons learned.

## Required Output Files

When applicable, create:

- STAGE-REPORT.md
- ACCEPTANCE-CHECKLIST.md
- VISUAL-EVIDENCE.md
- FILE-MANIFEST.md
- NEXT-STAGE-SUGGESTION.md
- LESSONS-LEARNED.md

## Acceptance Standard

A stage is not complete unless Codex can answer:

- What changed?
- Where did it change?
- Why is it safe?
- What evidence proves it?
- What remains unfinished?
- What must the named reviewer audit, and under which `REVIEW_MODE`?

## GPT—Codex Role Gate

For triggers such as `完整项目处理`, `GPT和Codex分工`, `哪个负责审核`, `独立审核`, `如何交接`, `如何转换`, or `ChatGPT工作和Codex协作`, apply:

- `rules/RULE-PATCH-20260710-GPT-CODEX-ROLE-SEPARATION.md`
- `references/GPT-CODEX-ROLE-TRANSFER-PROTOCOL-20260710.md`
- `templates/GPT-CODEX-MASTER-PROMPT-20260710.md`

Final reports must state:

- `PRIMARY_CONTROLLER`
- `MODEL_ROLE`
- `REVIEW_MODE`
- `REVIEWER`
- `STATUS`
