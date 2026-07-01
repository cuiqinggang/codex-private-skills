---
name: codex-git-safety-checkpoint
description: Use this skill before any major code, document, dashboard, skill, or project modification. It creates a safe Git checkpoint when the current folder is a Git repository. Do not use when no files will be changed.
---

# Codex Git Safety Checkpoint

## Purpose

Before large modifications, create a reversible state.

## Trigger Conditions

Use this skill before:
- large refactors
- dashboard redesign
- skill installation
- batch document edits
- automation script changes
- dependency changes
- destructive cleanup
- any change that may be hard to undo

## Procedure

1. Detect whether current directory is a Git repository:
   - git rev-parse --is-inside-work-tree

2. If it is a Git repository:
   - git status --short
   - git add -A
   - git commit -m "checkpoint: before major Codex modification"
   - If commit fails because there is nothing to commit, record that state.

3. If it is not a Git repository:
   - Do not initialize Git automatically unless user explicitly requested it.
   - Create a timestamped file manifest instead.

4. After implementation:
   - git status --short
   - summarize changed files
   - do not auto-push

## Hard Rules

- Never push to remote without explicit user instruction.
- Never delete Git history.
- Never force reset unless explicitly instructed.
- Never store secrets in commits.
- If secrets are detected, stop and report.

## Standard User Prompt

When the user says:
"开始修改前，帮我用 Git 提交当前版本，备注‘修改前备份’。"

Then execute:

git add -A
git commit -m "修改前备份"
