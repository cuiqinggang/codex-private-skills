# Failure Review: D Layer Produced Meta-Evaluation Without Final Answer

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`
Status: fixed

## What Happened

The external model accepted the safer D-layer rubric framing, but it produced only a benchmark / system evaluation report. It did not produce the actual `Ultra_Answer_Final` that answers the original user question.

The output judged the UltraFusion V7.0 system as `Prototype-Ready`, calculated `SCORE_FINAL` and `Gain`, and listed risks, but it did not deliver the required final answer covering the original question's requested system flow, roles, templates, scoring, cost/time control, risks, 30-day plan, and Go/No-Go criteria.

## Root Cause

The D-layer request over-emphasized "evaluation report" and placed scoring/rubric language before the real deliverable. This encouraged the model to treat D layer as a meta-evaluation of the UltraFusion system rather than final-answer generation for the original question.

## Corrective Action

All D-layer copy packages must use `FINAL_ANSWER FIRST` structure:

1. `Ultra_Answer_Final` must be the first output section.
2. The first output section must answer the original question directly.
3. Scoring, Gain, counterexamples, and benchmark verdict must appear only after the final answer as an audit appendix.
4. The package must explicitly forbid outputs that only evaluate the system or only discuss `Prototype-Ready`.

## Required First Signal

```text
【D层执行命令：FINAL_ANSWER FIRST】
```

## Required Output Order

```text
# 1. Ultra_Answer_Final
# 2. D层验收附录
```

## Future Prevention

Before sending a D-layer package to an external model, validate:

- contains `FINAL_ANSWER FIRST`
- contains `# 1. Ultra_Answer_Final`
- says the first section must answer the original question Q
- forbids "only benchmark evaluation without Ultra_Answer_Final"
- places scoring/Gain/risk after the final answer
