---
name: lambda-labs-gpu-cloud
description: Use when this Windows Codex studio needs Lambda Labs GPU cloud planning, SSH workflow review, cost-aware ML instance operations, or migration of a local GPU workload to cloud. Use for planning and verification only unless the user explicitly asks to operate the account; stop before login, payment, key creation, instance creation, or spending.
---

# Lambda Labs GPU Cloud Windows Studio

Use this skill for safe planning around Lambda Labs GPU instances from a Windows workstation.

## Stop Gates

Stop before:

- account login, payment, billing, or quota actions
- SSH key creation or upload
- instance create/start/stop/delete
- public endpoint exposure
- secret/API key handling
- long-running paid training or inference

## Workflow

1. Define workload: model, VRAM, disk, runtime, expected duration, and budget.
2. Check whether local ComfyUI/Docker/WSL/native GPU can satisfy the task first.
3. If cloud is justified, draft a cost and lifecycle plan: create, connect, transfer, run, collect artifacts, shut down.
4. Translate commands to Windows PowerShell and OpenSSH.
5. Prefer small smoke tests and explicit shutdown verification.
6. Report residual cost risk.

## Verification

- PASS: workload plan includes budget, SSH method, artifact path, and shutdown check.
- FAIL: no cost boundary, unclear credentials, or uncontrolled instance lifecycle.

