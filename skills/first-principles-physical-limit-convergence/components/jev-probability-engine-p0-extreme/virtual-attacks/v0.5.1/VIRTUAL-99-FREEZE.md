# JEV Probability Engine P0 v0.5.1-candidate — Virtual-99 Freeze

## Status

```text
BASELINE=v0.4.0
BASELINE_T_P0_MS=560.9819
CANDIDATE=JPE-P0-S2-SEMANTIC-PROJECTION-V4
MATURE_SOLUTION_CLUSTER=PASS
SEMANTIC_EQUIVALENCE_GATE=PASS
STRUCTURAL_PAYLOAD_REDUCTION=PASS
VIRTUAL_99=PASS
SOLUTION_FROZEN=YES
REAL_VERIFY=NOT_YET
```

## Why v0.5.0 was rejected

The v0.5.0 candidate changed question semantics, removed item fields and changed several execution structures at once. Reality returned 0/30 PASS. That candidate is rejected and cannot be reused as a valid latency reference.

## v0.5.1 single-factor freeze

Start from the certified v0.4.0 C# candidate and preserve exactly:

- QChoice text and explicit EXECUTE/HOLD/ROUTE/REJECT criteria;
- NormalizeItem fields: request/current_state/evidence/constraints/allowed_actions/dependency_ids;
- BuildQuestions;
- round-robin two-shard question split;
- RequestDecisionAsync;
- response parsing and ChooseAction;
- Task.WhenAll global model join;
- two local execution waves;
- 24 receipt files;
- Reality verifier;
- T0/T1 boundary;
- model typesafe/jev-1.13;
- 1 JEV model barrier, 2 HTTP requests per run, no retry.

The only performance transformation is:

```text
FULL 24-ITEM STATE SENT TO BOTH SHARDS
        ↓
EACH SHARD RECEIVES ONLY ITEMS REFERENCED BY ITS UNCHANGED QUESTIONS
```

Each retained item is copied with the exact v0.4.0 NormalizeItem representation.

## Structural proof

Because the original round-robin question split is unchanged:

- each request still has the same 16 questions as v0.4.0;
- each projected state contains 16 referenced items;
- v0.4.0 copied 24 items into request A and 24 into request B = 48 item copies;
- v0.5.1 copies 16 + 16 = 32 item copies.

```text
ITEM_COPY_REDUCTION = 16 / 48 = 33.333333%
```

All removed serialized item objects have positive byte length. Therefore:

```text
REQUEST_A_BYTES_v051 < REQUEST_A_BYTES_v040
REQUEST_B_BYTES_v051 < REQUEST_B_BYTES_v040
TOTAL_BYTES_v051     < TOTAL_BYTES_v040
```

without changing questions, criteria, retained item fields, executor, verifier or timer.

## Virtual time statement

A precise millisecond value is deliberately not invented. The old 533 ms shadow target is revoked because it came from a candidate that failed semantic preservation.

The only valid Virtual-99 time claim is:

```text
T_VIRTUAL_CANDIDATE < 560.9819 ms is structurally plausible and worth one reality challenge,
but T_REAL can only be established by the frozen Step-3 run.
```

## Promotion gate

- one auth/schema probe;
- 3 warmups;
- 30 measured;
- 30/30 PASS;
- 67/67 total HTTP requests;
- COMMERCIAL_GATE_SERIES=PASS;
- MIN_MS < 560.9819.

If any gate fails: keep v0.4.0, record Reality Delta, STOP.
