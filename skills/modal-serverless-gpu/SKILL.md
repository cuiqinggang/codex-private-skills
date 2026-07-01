---
name: modal-serverless-gpu
description: Use when this Windows Codex studio needs Modal serverless GPU planning, deployment review, or safe Python cloud ML execution design. Use for cost-aware dry-run planning, app structure review, and Windows PowerShell command adaptation; stop before authentication, secret creation, deployment, public endpoints, or paid execution.
---

# Modal Serverless GPU Windows Studio

Use this skill when considering Modal for GPU/serverless Python workloads.

## Boundaries

- Do not run authentication, secret, deployment, scheduled job, or paid GPU commands without explicit task scope.
- Do not upload private data or keys.
- Prefer local reproducibility first.
- Use Windows PowerShell command forms.

## Workflow

1. Identify workload: function, model, GPU need, inputs, outputs, runtime, and cost tolerance.
2. Check if local execution or existing APIs are enough.
3. Draft a minimal Modal app structure and dependency list.
4. Separate local unit tests from cloud execution.
5. Plan secrets by name only; never expose secret values.
6. Stop before `modal deploy`, scheduled jobs, public endpoints, or paid runs unless explicitly requested.

## Verification

- PASS: local test plan, dependency list, cost boundary, and safe cloud execution plan exist.
- FAIL: secret ambiguity, uncontrolled deployment, or no local sanity check.

