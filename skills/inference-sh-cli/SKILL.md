---
name: inference-sh-cli
description: Use when this Windows Codex studio needs to assess inference.sh or infsh style cloud AI app workflows, CLI usage, or deployment ideas. Use for official-source review, Windows dry-run planning, and credential-safe evaluation; stop before installs, authentication, paid cloud actions, or deployment.
---

# inference.sh CLI Windows Studio

Use this skill to evaluate inference.sh / infsh workflows safely from Windows.

## Boundaries

- Do not run `curl | shell`, unknown installers, global package installs, login commands, or deployment commands without explicit review.
- Do not paste or print API keys.
- Do not create paid resources or public endpoints automatically.
- Prefer official docs and local dry-runs.

## Workflow

1. Clarify goal: inspect, prototype, deploy, compare provider, or migrate an app.
2. Verify source trust: official docs, package registry, repository, license, and last-known commands.
3. Translate commands to Windows PowerShell.
4. Create a dry-run plan: working directory, env vars, expected files, network calls, rollback.
5. If execution is safe and local-only, run the smallest version/help/status command.
6. Stop before auth, secrets, deployment, cloud spend, or public exposure.

## Verification

- PASS: official-source command plan or safe local version/help output.
- FAIL: unknown installer, hidden credential flow, paid resource action, or unclear rollback.

