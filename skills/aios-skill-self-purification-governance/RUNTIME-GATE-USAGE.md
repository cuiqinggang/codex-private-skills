# Runtime Gate Usage

Runtime-enforced governance must use:

```text
H:\AI\skills\ecc-staged-long-task-orchestration\scripts\verify-runtime-gate.mjs
```

## Minimum Runtime

- 30min task: `minimum_runtime_minutes = 30`
- 2H task: `minimum_runtime_minutes = 120`
- 4H task: `minimum_runtime_minutes = 240`
- 8H task: `minimum_runtime_minutes = 480`

If elapsed time is below the minimum, the run must FAIL or be PARTIAL. It cannot PASS.

## Required Evidence

Runtime-enforced runs must produce:

- `outputs/runtime-evidence.json`
- `outputs/checkpoint-timeline.html`
- checkpoint files at the configured interval
- final checkpoint

## Patch Install vs Runtime Run

Patch install tasks may complete in minutes, but can only claim `PATCH_INSTALL_PASS`.

Runtime tasks must not claim PASS until the runtime verifier passes.

