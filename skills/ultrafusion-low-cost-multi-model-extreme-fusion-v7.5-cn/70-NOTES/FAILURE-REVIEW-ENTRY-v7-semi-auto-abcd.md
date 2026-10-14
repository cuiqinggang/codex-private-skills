# Failure Review Entry: UltraFusion V7.0 Semi-Automatic ABCD

Date: 2026-07-05
Status: active failure-review entry point

Use this note when a V7.0 run fails, stalls, or produces low gain.

## Common Failure Modes

- Codex forgets to score the baseline before A layer.
- Codex outputs prose around the package and the user copies the wrong region.
- A layer answers converge too early and lack diversity.
- B layer becomes peer review instead of generating stronger answers.
- C layer merges mechanically without strategic judgment.
- D layer repeats C without final risk analysis.
- `Score_0`, `SCORE_FINAL`, or `Gain` is missing.
- `Gain < 2` is hidden instead of honestly marking `INVALID_CHAIN`.
- Missing external answers are fabricated by Codex.

## Review Questions

1. Was the baseline answer scored before the ABCD process?
2. Were all copy blocks clean and self-contained?
3. Did every layer contain V15 and the layer-specific task?
4. Were weak or missing external answers labeled honestly?
5. Did B produce new stronger answers rather than comments?
6. Did D produce final answer, score, and risk analysis?
7. Was the final gain at least 2.0?

## Repair Rule

If the failure is prompt-package contamination, regenerate only the affected layer package.

If the failure is weak external answers, down-weight or exclude the weak answer and continue only if at least two useful inputs remain.

If the failure is low gain, stop and record `INVALID_CHAIN`; do not add extra unplanned layers.

