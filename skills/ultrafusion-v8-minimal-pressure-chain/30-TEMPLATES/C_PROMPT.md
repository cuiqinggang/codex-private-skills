# UltraFusion V8.2 C Layer Prompt

```text
You are executing UltraFusion V8.2 C layer: pressure fusion.

Task:
Read the original question Q and all valid B answers. Fuse them into one unified, clear,
dense, conflict-aware candidate final answer. Do not mechanically stitch. Do not produce
a low-matching summary. You must handle conflicts, mark weak evidence, compress duplication,
separate fact/inference/recommendation where needed, and leave judgement points for D.

Original question Q:
<<<Q>>>

B layer answers:
<<<B_ANSWERS>>>

C_VALIDATION:
- Conflict_Handled: YES / NO
- Weak_Evidence_Marked: YES / NO
- Duplication_Compressed: YES / NO
- D_Judgement_Points_Listed: YES / NO

C rule:
If any field is NO, C is invalid and must rerun once. If it still fails, mark C_STITCHING_FAIL.

Score_Consistency_Gate:
- Write concrete Deduction first.
- Write SelfScore second.
- Write RepairDone third.
- If Deduction is empty, generic, or has no concrete penalty point while SelfScore >= 8.5,
  lower the score or rewrite the scoring block.
- Keep only one final scoring block in the visible output.

Output:
C_FUSION:

FusionNotes:
- Conflict handling:
- Weak evidence marked:
- Duplication compressed:
- D judgement points:

C_VALIDATION:
- Conflict_Handled: YES / NO
- Weak_Evidence_Marked: YES / NO
- Duplication_Compressed: YES / NO
- D_Judgement_Points_Listed: YES / NO

Balance:
- Quality:
- Architecture:
- Speed:

Deduction:
SelfScore:
RepairDone:

EARLY_WARNING:
- Quality_Threat: none / low / medium / high
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```
