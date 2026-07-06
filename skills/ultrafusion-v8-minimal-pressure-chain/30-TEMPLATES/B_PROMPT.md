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

B_Rerun_Negative_Example:
Wrong:
- "A 稿整体不错，但还可以加强风险分析。"
- "A 的结构清楚，但细节不足。"
These are comments, not B_ENHANCED_ANSWER.

Correct:
Directly write a stronger standalone answer that can be delivered to the user.

If B output is mainly comments about A, mark B_DEGRADATION_FAIL.

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
- Balance: OK / WARN
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```
