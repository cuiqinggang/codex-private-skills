# Fugu-Style Evaluation Run Plan

1. Run each task in three modes: baseline single model, local orchestrated model matrix, premium optional judge.
2. Record role assignments before execution.
3. Keep raw outputs in `raw_outputs/`.
4. Keep evidence in `evidence/`.
5. Score with `scorecard.md`.
6. Mark each claim as official, third-party, independently rerun, or unverified.
7. Stop premium testing when budget is exhausted or local verification already passes.

## Directory Layout

```text
eval_pack/
  tasks.jsonl
  scorecard.md
  run_plan.md
  raw_outputs/
  evidence/
  reports/
```
