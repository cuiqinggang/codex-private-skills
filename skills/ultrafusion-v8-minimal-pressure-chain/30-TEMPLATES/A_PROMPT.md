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
- Write concrete Deduction first.
- Write SelfScore second.
- Write RepairDone third.
- If Deduction is empty, generic, or has no concrete penalty point while SelfScore >= 8.5,
  lower the score or rewrite the scoring block.
- Keep only one final scoring block in the visible output.

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
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```
