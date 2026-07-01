# Validation Test Plan

## Goal

Prove that Best Answer AI creates a visibly better final answer than ordinary direct AI use, while keeping cost under control.

## Test Set

Start with 20-50 English questions.

Categories:

```text
business decision
product comparison
technical architecture
learning plan
personal strategy
research synthesis
writing/positioning decision
```

Avoid high-risk medical/legal/financial advice as primary launch examples unless strong disclaimers and source checking are added.

## Compare Three Modes

For each question, compare:

```text
1. Single direct AI answer
2. Quick/D-Lite answer
3. Full Best Answer A/B/C/D
```

## Score Dimensions

Use 1-10 scoring:

| Dimension | Question |
|---|---|
| usefulness | Would this help the user act better? |
| completeness | Does it cover important angles? |
| correctness | Are claims plausible and checked? |
| risk detection | Does it find traps and counterarguments? |
| clarity | Is the final answer easy to use? |
| density | Is it rich without useless bloat? |
| willingness to pay | Would a user pay for this answer? |

## Cost/Time Log

For every run, record:

```text
question_id
mode
models used
temperatures
max_tokens settings
latency
actual_or_estimated_tokens
actual_or_estimated_cost
failure/retry notes
final quality score
```

## Pass Criteria

The product is worth moving to web MVP if:

- Full Best Answer is clearly better than direct single AI on high-value questions;
- Quick mode is useful enough for free users;
- Full mode cost can be priced safely;
- outputs are stable enough to show strangers;
- at least some real or likely users say they would pay for serious questions.

## Early Test Procedure

1. Pick one question.
2. Run single direct AI answer.
3. Run Quick/D-Lite.
4. Run Full A/B/C/D.
5. Score all three.
6. Record cost and time.
7. Note whether Full was worth the extra cost.
8. Repeat until patterns are visible.

## Evidence Preservation

For each serious test, keep:

- original question;
- all major outputs;
- scoring table;
- cost/time notes;
- final conclusion;
- improvement notes for prompts or routing.

Do not rely only on memory.
