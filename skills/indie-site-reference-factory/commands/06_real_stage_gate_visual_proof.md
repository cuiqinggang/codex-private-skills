# 06 Real Stage-Gate Visual Proof

Use this command whenever the task is a real reference-site clone test or a skill-package validation test.

## Mandatory Rules

1. Choose a visually valuable reference site.
   - Do not validate the skill with an overly simple page.
   - A valid test target should include hero hierarchy, a distinct primary visual, mobile layout, and a meaningful first lower section.

2. Every visual gate must show a comparison image in the chat.
   - Target desktop.
   - Generated desktop.
   - Target mobile.
   - Generated mobile.
   - The comparison board path should be `evidence/screenshots/stage-gates/<GATE_ID>_comparison.png`.

3. Every visual gate must show the scoring logic in the chat.
   - Desktop similarity.
   - Mobile similarity.
   - Overall similarity.
   - Formula.
   - Deductions.
   - Script output.
   - Proceed allowed: YES/NO.

4. A gate below 95% blocks progress.
   - Stay inside the same gate.
   - Repair locally.
   - Re-screenshot.
   - Re-score.
   - Re-run `validate_stage_gate.ps1`.

5. Historical blocked attempts must remain visible.
   - Keep them as proof that the gate actually blocked weak work.
   - Put the current gated score before blocked attempt records.
   - Label old scores as `attempt score` so validators do not treat them as current scores.

6. Target pollution is not cloned.
   - Cookie banners, popups, login overlays, browser overlays, and capture artifacts must be documented in `G00_TARGET_CAPTURE`.
   - Exclude them from scoring.
   - Do not copy them into the generated independent site.

## Proven Example

2026-07-09 Framer test:

- G30 initially blocked at 87%, then passed at 96% after local repair.
- G50 initially blocked at 85%, then passed at 95% after local repair.
- Final progress gate: Desktop=95%, Mobile=95%, Overall=95%, `PROGRESS_GATE=CLONE_SIMILARITY_PASS`.

Reference case file:
`references/FRAMER_STAGE_GATE_REAL_TEST_20260709.md`
