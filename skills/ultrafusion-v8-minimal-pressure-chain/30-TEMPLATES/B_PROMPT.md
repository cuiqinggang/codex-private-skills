# UltraFusion V8.2 B Layer Prompt

```text
You are executing UltraFusion V8.2 B layer: absorb and enhance.

Task:
Read the original question Q and all valid A answers. Absorb strengths, repair omissions,
handle conflicts, and produce a stronger standalone answer. B is not a review layer.
Do not only comment on A1/A2/A3. The output must be a usable new answer.

Original question Q:
<<<Q>>>

A layer answers:
<<<A_ANSWERS>>>

B_VALIDATION:
- Has_B_ENHANCED_ANSWER: YES / NO
- Is_Standalone_Answer: YES / NO
- Is_Only_Review: YES / NO

B rule:
If Has_B_ENHANCED_ANSWER = NO, or Is_Standalone_Answer = NO, or Is_Only_Review = YES,
B is invalid and must rerun once. If it still fails, mark B_DEGRADATION_FAIL.

Score_Consistency_Gate:
- Write concrete Deduction first.
- Write SelfScore second.
- Write RepairDone third.
- If Deduction is empty, generic, or has no concrete penalty point while SelfScore >= 8.5,
  lower the score or rewrite the scoring block.
- Keep only one final scoring block in the visible output.

Output:
B_ENHANCED_ANSWER:

ComparedWithA:
- Added:
- Repaired:
- Improved:

B_VALIDATION:
- Has_B_ENHANCED_ANSWER: YES / NO
- Is_Standalone_Answer: YES / NO
- Is_Only_Review: YES / NO

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
