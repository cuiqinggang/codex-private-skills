---
name: agent-browser
description: Use when this Windows Codex studio needs browser automation route selection or a safe review of agent-browser style tooling. Prefer the installed Browser plugin, Playwright skills, and screenshot-recognition workflows for local targets; use this skill to adapt legacy browser automation without relying on old OpenClaw, WSL, CDP, or Chrome-profile assumptions.
---

# Agent Browser Windows Studio

Use this skill when browser work needs route selection: in-app Browser plugin, Playwright, screenshot-recognition, Chrome with user profile, or a candidate agent-browser CLI.

## Route Priority

1. Local app or localhost UI: use the Browser plugin or Playwright.
2. Visual layout or unreliable DOM: use screenshot-recognition browser workflow.
3. Logged-in/profile-dependent site: use Chrome only when the task requires the user's session.
4. ChatGPT web planning: use the workspace-approved screenshot bridge route only.
5. agent-browser CLI: candidate only; review before installing or running.

## Windows Studio Rules

- Use Windows paths and PowerShell.
- Do not use legacy WSL, `/mnt`, `/home`, OpenClaw browser profile, old debug ports, or stale CDP assumptions.
- Do not move the real Windows mouse or keyboard unless the active task explicitly allows it or a workspace rule narrowly pre-authorizes that bridge.
- Stop for login, captcha, payment, account/security prompts, privacy-sensitive forms, or high-impact account actions.

## Workflow

1. Identify target URL/app, login needs, and whether visual verification matters.
2. Pick the lowest-risk available route from the priority list.
3. For local UI work, capture a screenshot or browser observation before and after meaningful actions.
4. For any proposed agent-browser CLI use, first inspect install source, command scope, output location, and rollback.
5. Report the selected route and PASS/FAIL evidence.

## Verification

- PASS: route chosen, action observed, and post-action state rechecked.
- FAIL: no visible target, tool requires unsafe install, or page enters account/security/payment gate.

