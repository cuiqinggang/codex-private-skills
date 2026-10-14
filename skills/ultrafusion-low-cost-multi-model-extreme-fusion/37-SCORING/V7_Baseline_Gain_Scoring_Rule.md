# UltraFusion V7.0 Baseline Gain Scoring Rule

Date: 2026-07-05
Status: active

## Formula

```text
Gain = SCORE_FINAL - Score_0
```

Where:

- `Score_0` is the quality score of the ordinary baseline answer before A/B/C/D.
- `SCORE_FINAL` is the final quality score after D-layer convergence.

## Decision Rule

```text
If Gain < 2.0 -> INVALID_CHAIN
If Gain >= 2.0 -> EFFECTIVE_CHAIN
```

## Scoring Discipline

- Use a 0-10 scale.
- Do not inflate `SCORE_FINAL` just because the process was longer.
- Penalize factual errors, fabricated citations, missing caveats, weak reasoning, shallow fusion, and unsafe overconfidence.
- A long final answer with little real improvement can still be `INVALID_CHAIN`.
- If baseline was already excellent, Codex may recommend stopping before ABCD rather than forcing a low-gain run.

## Required Final Comparison

Every V7 run must end with:

```text
Score_0:
SCORE_FINAL:
Gain:
Chain verdict: EFFECTIVE_CHAIN | INVALID_CHAIN
Reason:
```

