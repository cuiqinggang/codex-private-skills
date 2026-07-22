# Runbook

## Purpose

Run AIOS skill self-purification as a semi-automatic governance workflow. The workflow finds duplicate, stale, risky, or unclear skill rules, but it does not merge changes into formal skills without review.

## Standard Flow

1. Pick the run mode: 30min, monthly 2H, or quarterly 4H.
2. Load `DO-NOT-AUTO-OPTIMIZE.md`.
3. Load `PATCH-BUFFER-STANDARD.md`.
4. If runtime-enforced, load `RUNTIME-GATE-USAGE.md`.
5. Select representative skills.
6. Copy samples into a shadow workspace.
7. Generate candidate patches only.
8. Split every candidate into accepted, rejected, or needs-human.
9. Produce evidence pages and runtime evidence.
10. Run the acceptance gate.

## Stop Conditions

- A run attempts to modify formal business skills.
- A run tries to auto-merge accepted candidates.
- A run deletes failure reviews, hard user rules, safety boundaries, or true PASS long-task acceptance flows.
- A runtime-enforced run lacks `runtime-evidence.json`.
- A runtime-enforced run finishes before the required elapsed time.

## V3 Validation Baseline

V3 proved this pattern with:

- elapsed minutes: 120.02
- checkpoint count: 9
- runtime gate: PASS
- formal skills modified: NO

