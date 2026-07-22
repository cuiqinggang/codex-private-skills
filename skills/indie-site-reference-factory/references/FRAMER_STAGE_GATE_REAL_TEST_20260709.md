# Framer Stage-Gate Real Test 2026-07-09

Purpose: preserve the first useful real proof that `indie-site-reference-factory` can act as a strict per-stage gate system instead of a loose final screenshot workflow.

Reference target: https://www.framer.com

Test workroot:
${REDACTED_SECRET}

## What Made This Test Useful

The reference site was visually valuable: dark immersive hero, luminous blue prompt box, chip row, editor/canvas UI, mobile hero, and rich lower project cards. A weak clone is easy to spot, so this target is suitable for testing whether the skill package really enforces quality.

The user explicitly rejected a too-simple earlier target because simple pages can look "close enough" without proving clone ability.

## Required Evidence Pattern

Every visual gate must publish, in the chat and in the progress package:

- A four-image comparison board: target desktop, generated desktop, target mobile, generated mobile.
- Desktop similarity percentage.
- Mobile similarity percentage.
- Overall similarity percentage.
- Deduction logic.
- Gate script result.
- Pass/block decision before moving to the next gate.

If the comparison image is not shown to the user, the gate is not complete.

## Real Gate Failures Caught

### G30_PRIMARY_VISUAL

Initial score:
- Desktop: 95%
- Mobile: 76%
- Overall: 87%
- Script result: `STATUS=GATE_BLOCKED`

Reason: desktop luminous prompt was close, but the mobile editor preview was structurally wrong. It showed an oversized black canvas instead of the target-like compact editor with left rail, center preview, right rail, and bottom tool strip.

Repair:
- Rebuilt the editor preview as a compact design-tool canvas.
- Added left page tree, right rail, bottom floating tools.
- Repositioned the mobile center preview.

Final score:
- Desktop: 96%
- Mobile: 95%
- Overall: 96%
- Script result: `STATUS=PASS`

### G50_FIRST_SECTION

Initial score:
- Desktop: 89%
- Mobile: 78%
- Overall: 85%
- Script result: `STATUS=GATE_BLOCKED`

Reason: the first lower mobile section used plain gradient cards and did not reproduce the target's rich project-card density. This was too weak to prove clone ability.

Repair:
- Rebuilt cards into three independent but visually equivalent editorial/project cards.
- Preserved target rhythm without copying target brands, exact images, or customer content.
- Excluded documented cookie-banner pollution from scoring.

Final score:
- Desktop: 95%
- Mobile: 96%
- Overall: 95%
- Script result: `STATUS=PASS`

## Final Result

Final progress gate output:

```text
RoundCompareCount=1
DesktopSimilarity=95%
MobileSimilarity=95%
OverallSimilarity=95%
PROGRESS_GATE=CLONE_SIMILARITY_PASS
```

## Rules Added From This Test

1. Do not choose an overly simple reference site for capability validation.
2. Do not proceed from any visual gate unless the comparison board is shown to the user.
3. Current gated scores must appear before historical blocked scores in the gate report, otherwise validators may read stale low scores.
4. Blocked attempts are valuable evidence and must remain in the report as blocked records.
5. Target pollution such as cookie banners must be documented in G00 and excluded from clone scoring; it must not be copied.
6. Lower-section richness matters. A good hero alone is not enough for clone acceptance.
7. Final pass requires both `validate_stage_gate.ps1 -Gate G90_FINAL` and `validate_progress_gate.ps1` to pass.
