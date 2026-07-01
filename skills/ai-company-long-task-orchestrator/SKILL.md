---
name: ai-company-long-task-orchestrator
description: Use this skill when the user asks Codex to run a long AI Company OS task, staged project task, Obsidian dashboard task, knowledge OS task, or 60-120 minute execution package. Do not use for small one-step edits, casual Q&A, or tasks without evidence requirements.
---

# AI Company Long Task Orchestrator

## Purpose

This skill turns a large user-approved task into a disciplined long-running Codex execution loop.

It is designed for:
- AI Company OS
- Obsidian Knowledge OS
- dashboard development
- staged long tasks
- GPT Gate Review workflows
- evidence-based acceptance loops

## Hard Rules

1. Do not ask the user to review every tiny step.
2. Execute in large stages.
3. Preserve user context.
4. Produce evidence, not vague claims.
5. Prefer 60-120 minute task packages when the task is large.
6. Never silently modify high-risk files.
7. Stop and ask before touching credentials, external accounts, real publishing channels, or destructive operations.

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
9. Produce GPT Gate Review package.
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
- What should GPT review?
