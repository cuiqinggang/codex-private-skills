# Runtime Parameters

## Temperature Strategy

Temperature controls divergence vs convergence. It does not control whether a layer is extreme.

All layers remain V15 extreme layers.

## Default Temperature Ranges

| Layer | Temperature | Reason |
|---|---:|---|
| A independent extreme drafts | 0.65-0.75 | maximize independent diversity and avoid early convergence |
| B1 cross-absorption | 0.50-0.65 | absorb other drafts while preserving difference |
| B2 second extreme rewrite | 0.40-0.55 | strengthen and begin controlled convergence |
| C dense fusion | 0.25-0.40 | consolidate, remove duplication, select strongest points |
| D final stress test | 0.10-0.25 | stabilize, verify, reduce hallucination and over-creative claims |

If only A/B/C/D are used:

| Layer | Temperature |
|---|---:|
| A | 0.65-0.75 |
| B | 0.45-0.65 |
| C | 0.25-0.40 |
| D | 0.10-0.25 |

## Initial Single-Value Defaults

Use these when a platform requires one value per layer:

```text
A  = 0.70
B1 = 0.60
B2 = 0.50
C  = 0.35
D  = 0.20
```

For A/B/C/D only:

```text
A = 0.70
B = 0.55
C = 0.35
D = 0.20
```

## Reasoning

The strategy is:

```text
A/B extract diversity.
C/D extract correctness.
```

Earlier layers need more variation because different models should expose different paths. Later layers need stability because the final answer must be reliable.

## Max Tokens Strategy

Do not fix final max token values yet.

`max_tokens` means the maximum output length for one model call. It is not the input context length.

Why it matters:

- higher values can increase cost;
- higher values can increase latency;
- too-low values can truncate V15 extreme answers;
- too-high values can produce bloated and repetitive drafts.

Current rule:

```text
Treat max_tokens as a measured variable during tests.
```

For each run, record:

- layer;
- model;
- input size estimate;
- output length;
- whether output was truncated;
- whether output was verbose or too short;
- whether the answer quality was harmed by length limits;
- actual or estimated cost.

Do not set permanent max token defaults until real test data exists.

## Formal Parameter Logging

Every serious test should record:

```text
question_id
mode
layer
model
temperature
max_tokens_setting
output_length
latency
estimated_or_actual_cost
quality_score
failure_notes
```
