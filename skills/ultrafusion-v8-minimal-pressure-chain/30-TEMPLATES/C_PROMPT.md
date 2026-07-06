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

C_Content_Density_Gate:
FusionNotes must not be placeholder text.

- 冲突处理:
  Must include at least 1 concrete conflict point, or explicitly state "未发现具体冲突" with reason.

- 弱证据标记:
  Must include at least 1 weak / uncertain evidence point, or explicitly state "未发现弱证据" with reason.

- 重复压缩:
  Must identify what repeated content was compressed, using source label, paragraph topic, or keywords.

- D 层重点审判点:
  Must list at least 2 concrete judgement points for D.

If any field is generic, empty, or only says "已处理 / 已标记 / 已压缩" without concrete content:
mark C_STITCHING_FAIL and rerun C once.

Score_Consistency_Gate:
- Must write Deduction before SelfScore and RepairDone.
- If Deduction is empty (0 concrete items):
  SelfScore MUST be <= 7.0.
- If Deduction has only 1 concrete penalty item:
  SelfScore MUST be <= 8.0.
- If Deduction has 2+ concrete penalty items:
  SelfScore MAY be 8.5+.
- If Deduction is generic, such as "needs improvement" or "could be better"
  without concrete issue, affected section, or repair action, treat it as 0 concrete items.
- Final output must contain exactly one scoring block: Deduction / SelfScore / RepairDone.

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

C_Content_Density_Gate:
- Conflict_Field_Dense: YES / NO
- Weak_Evidence_Field_Dense: YES / NO
- Duplication_Compression_Clear: YES / NO
- D_Judgement_Points_Concrete_2Plus: YES / NO

Balance:
- Quality:
- Architecture:
- Speed:

Deduction:
SelfScore:
RepairDone:

EARLY_WARNING:
- Quality_Threat: none / low / medium / high
- Balance: OK / WARN
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```
