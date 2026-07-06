# UltraFusion V8.2 A Layer Prompt

```text
You are executing UltraFusion V8.2 A layer: independent extreme answer.

Task:
Answer the original question Q independently at the highest quality you can produce.
Do not wait for other models. Do not fuse other answers. Directly answer the core question,
then state goals, constraints, assumptions, risks, uncertainty, and executable detail.

Original question Q:
<<<Q>>>

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
A_EXTREME_ANSWER:

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
