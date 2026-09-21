# Codex Handoff — JEV Probability Engine P0 v0.5.0 candidate

This is an executor-only handoff.

Do not design, optimize, patch, select alternatives, or change any frozen file.

1. Confirm branch:
   `codex/jev-probability-engine-p0-v0.5.0-virtual99-freeze`
2. Read `manifest.json` and `REAL-VERIFY-CONTRACT.md`.
3. Do not edit anything.
4. If the current PowerShell process does not already contain `OPENROUTER_API_KEY`, STOP and report the block. Never print or persist the key.
5. From repository root execute exactly:
   `pwsh -NoProfile -File skills/first-principles-physical-limit-convergence/components/jev-probability-engine-p0-extreme/virtual-attacks/v0.5.0/run-frozen-v050-real-verify.ps1`
6. Return only the runner's final summary and result path.
7. Whether PASS or FAIL, STOP. Do not repair or rerun with a changed design.
