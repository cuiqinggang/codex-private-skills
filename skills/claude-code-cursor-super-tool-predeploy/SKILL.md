---
name: claude-code-cursor-super-tool-predeploy
description: Use when preparing, auditing, repairing, or upgrading the existing Cursor + Claude Code stack into a mature low-cost multi-model super-tool, especially before CCR/OpenRouter/DeepSeek routing, skills/hooks/subagents migration, blocker elimination, or long deployment. Trigger on "Claude Code Cursor", "Cursor 内 Claude Code", "Claude Code 超级工具", "CCR 部署前", "卡点消除", "现有架子升级", or "不要从零重装 Claude Code".
---

# Claude Code Cursor Super-Tool Predeploy

## Purpose

Use this skill before any serious attempt to upgrade the user's existing Cursor + Claude Code setup.

The starting assumption is:

- Cursor already exists and remains the main work entry.
- Claude Code already has a partial working skeleton inside or alongside Cursor.
- The goal is not a blind reinstall.
- The goal is information collection, blocker analysis, blocker elimination, then a controlled one-pass maturity upgrade.

## Hard Rules

- Do not start by deleting or reinstalling Claude Code.
- Do not overwrite `.claude`, `.claude-code-router`, PowerShell profile, shortcuts, or provider environment variables without backups.
- Do not print full API keys or auth tokens. Presence checks are allowed; at most show a short prefix when necessary.
- Treat `Cursor + Git Bash + Claude Code + CCR` as the preferred target shape unless the user changes the goal.
- Separate four decisions before touching config: keep, adapt, replace, fill.
- Information collection comes before blocker removal.
- Blocker removal comes before long deployment.
- Long deployment must have reports, evidence, rollback notes, and final acceptance.

## Required Workflow

1. Read `references/material-summary-20260618.md`.
2. Run or manually follow `scripts/collect-current-stack.ps1` for read-only diagnostics.
3. Write the information report:
${REDACTED_SECRET}
4. Write the blocker report:
${REDACTED_SECRET}
5. Write the predeploy elimination report:
${REDACTED_SECRET}
6. Only then enter formal long deployment:
   `CLAUDE_CODE_CURSOR_SUPER_TOOL_ONE_PASS_LONG_DEPLOYMENT_V1`

## Gate Names

- `CLAUDE_CODE_CURSOR_EXISTING_STACK_INFO_COLLECTION_V1`
- `CLAUDE_CODE_CURSOR_SUPER_TOOL_BLOCKER_ANALYSIS_V1`
- `CLAUDE_CODE_CURSOR_PRE_DEPLOY_BLOCKER_ELIMINATION_V1`
- `CLAUDE_CODE_CURSOR_SUPER_TOOL_ONE_PASS_LONG_DEPLOYMENT_V1`

## What To Collect

- Cursor status, terminal type, Git Bash/WSL availability, paste/input stability, and whether Cursor should remain the main entry.
- Claude Code version, path, launch status, login status, `claude -p` text output, tool execution, file read/write behavior, and raw `<tool_call>` leakage.
- Provider variables for Anthropic-compatible endpoints, model names, and key presence without secret exposure.
- Legacy proxy leftovers, especially `ccswitch_proxy.py`, port `15721`, PowerShell profile startup hooks, and stale shortcuts.
- Existing output folder, file-input helper, `.claude` directory, CCR config, model candidates, Codex/Hermes/GPT collaboration routes.

## Blocker Classes

- Environment blockers
- Protocol/tool-use blockers
- Model blockers
- Ecosystem blockers
- User-experience blockers
- External collaboration blockers

## Related Skills

Use these as references, not replacements:

- `complete-claude-style-replica-flow`
- `codex-deepseek-v4pro-ccx-ccswitch-replay`
- `codex-lite-power-upgrade`
- `claude-code-deepseek-v4pro-windows` in the H-drive merged skill archive

## Final Status Codes

- `CLAUDE_CODE_CURSOR_PREDEPLOY_PASS`
- `CLAUDE_CODE_CURSOR_PREDEPLOY_REVIEW_READY`
- `CLAUDE_CODE_CURSOR_PREDEPLOY_PARTIAL`
- `CLAUDE_CODE_CURSOR_PREDEPLOY_BLOCKED`
