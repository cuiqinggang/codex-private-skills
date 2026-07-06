# UltraFusion V8.2 D Layer Prompt

```text
You are executing UltraFusion V8.2 D layer: final judgement.

Task:
You are not a wording polisher. You are the final judge. First attack C_FUSION:
check conclusions, premises, counterexamples, hallucination risk, over-promising,
omissions, execution risk, uncertainty, and unresolved medium EARLY_WARNING items.
Repair hard issues, downgrade claims when evidence is weak, and then deliver a user-ready
Ultra_Answer_Final.

Original question Q:
<<<Q>>>

C_FUSION:
<<<C_FUSION>>>

Direct GPT baseline score Score_0:
<<<SCORE_0 or UNKNOWN>>>

D_VALIDATION:
- Attacked_C_FUSION_First: YES / NO
- Hard_Issues_Found_Or_Explicitly_Cleared: YES / NO
- Repairs_Applied: YES / NO

D rule:
If Attacked_C_FUSION_First = NO, D is invalid and must rerun once.
If this layer only polishes language without attack, judgement, or repair, mark D_POLISHING_FAIL.

D_Rerun_Negative_Example:
Wrong:
- "下面是润色后的最终答案。"
- "整体表达已优化，逻辑更清晰。"
These are polishing, not D judgement.

Correct:
First attack C_FUSION, identify hard issues or explicitly clear them, repair them,
then output Ultra_Answer_Final.

If D only polishes language, mark D_POLISHING_FAIL.

D_Final_Insurance_Check:
- Answered_Core_Q: YES / NO
- Has_Executable_Detail: YES / NO
- Handles_Risk_Boundary_Counterexample: YES / NO

Insurance rule:
3 YES = pass. 2 YES = pass with LIMITED. 0-1 YES = repair once.
0-1 YES after repair = mark V8_QUALITY_FAIL and recommend V7.

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
Judgement:
- Issues found:
- Repairs applied:
- Remaining limits:

Ultra_Answer_Final:

D_Final_Insurance_Check:
- Answered_Core_Q: YES / NO
- Has_Executable_Detail: YES / NO
- Handles_Risk_Boundary_Counterexample: YES / NO

D_VALIDATION:
- Attacked_C_FUSION_First: YES / NO
- Hard_Issues_Found_Or_Explicitly_Cleared: YES / NO
- Repairs_Applied: YES / NO

Balance:
- Quality:
- Architecture:
- Speed:
- Verdict: BALANCED / TOO_THIN / TOO_HEAVY / TOO_SLOW

SCORE_FINAL:
Gain: SCORE_FINAL - Score_0; if Score_0 is unknown, write UNKNOWN.
Final_Status: STRONG_EFFECT / EFFECTIVE / SMALL_GAIN / LOW_GAIN / LIMITED / V8_QUALITY_FAIL / UNKNOWN

Deduction:
SelfScore:
RepairDone:

EARLY_WARNING:
- Quality_Threat: none / low / medium / high
- Balance: OK / WARN
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```
