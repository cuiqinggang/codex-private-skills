# <GATE_ID> <GATE_NAME>

Current gated score must appear before any historical blocked attempt records.

Gate ID: <GATE_ID>
Gate name: <GATE_NAME>
Target URL: <https://example.com>

## Evidence

Target desktop screenshot: evidence/screenshots/stage-gates/<GATE_ID>_target_desktop.png
Generated desktop screenshot: evidence/screenshots/stage-gates/<GATE_ID>_generated_desktop.png
Target mobile screenshot: evidence/screenshots/stage-gates/<GATE_ID>_target_mobile.png
Generated mobile screenshot: evidence/screenshots/stage-gates/<GATE_ID>_generated_mobile.png
Comparison board: evidence/screenshots/stage-gates/<GATE_ID>_comparison.png

User-visible proof:
- Comparison board shown in chat: YES/NO
- Percentages shown in chat: YES/NO
- Gate script output shown in chat: YES/NO
- Pass/block decision shown before next gate: YES/NO

## Score

Desktop similarity: <0-100>%
Mobile similarity: <0-100>%
Overall similarity: <0-100>%
Formula: round(Desktop * 0.6 + Mobile * 0.4) = <0-100>%

## Deductions

- Layout geometry:
- Typography hierarchy:
- Color / lighting / background:
- Key component shape:
- Mobile order / responsive behavior:

## Decision

Proceed allowed: NO

Reason:
- Replace this with the concrete reason this gate can or cannot proceed.

Next action:
- If blocked, stay in this same gate and repair before moving on.

## Blocked Attempt Records

Use this section only after the current score above. Do not write historical failed scores with the exact labels `Desktop similarity`, `Mobile similarity`, or `Overall similarity`; use `Desktop attempt score`, `Mobile attempt score`, and `Overall attempt score`.

- Attempt:
- Desktop attempt score:
- Mobile attempt score:
- Overall attempt score:
- Script result:
- Why blocked:
- Repair performed inside the same gate:
