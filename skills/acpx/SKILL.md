---
name: acpx
description: Use when this Windows Codex studio needs to assess, adapt, or lightly verify ACP/acpx command-line agent orchestration. Use for planning safe local Windows trials, comparing against existing Codex/Superpowers routes, or extracting ideas from legacy OpenClaw ACP skills without importing old paths, credentials, or runtime assumptions.
---

# ACPX Windows Studio

Use this skill to evaluate ACP/acpx style agent orchestration for the current Windows studio. It is not permission to install a new agent framework or wire it into production by default.

## Windows Studio Rules

${REDACTED_SECRET}
- Use PowerShell examples and Windows paths only.
- Prefer existing Codex skills, Superpowers-style gates, and local browser/screenshot workflows before adding ACP/acpx.
- Do not reuse legacy OpenClaw, WSL, `/mnt`, `/home`, old Chrome profile, or old gateway paths without rewriting them for this Windows machine.
- Stop before installs, global PATH changes, account login, secrets, payment setup, background services, or production routing changes.

## Workflow

1. Define the orchestration goal: planning, parallel review, tool routing, browser action, or long-running execution.
2. Check whether an existing local skill already solves it.
3. If ACP/acpx still matters, inspect only official docs or local preserved notes first; do not run unknown bootstrap commands.
4. Create a Windows dry-run plan with exact PowerShell commands, expected output, rollback, and stop gates.
5. Run only read-only or project-local checks automatically.
6. After any trial, record PASS/FAIL evidence and whether ACP/acpx should remain a candidate, be adapted, or be rejected.

## Verification

- PASS: the task has a Windows-safe plan or a local dry-run result with no secret/account/system changes.
- FAIL: the route requires unreviewed install scripts, old OpenClaw paths, broad background services, or unclear credential handling.

