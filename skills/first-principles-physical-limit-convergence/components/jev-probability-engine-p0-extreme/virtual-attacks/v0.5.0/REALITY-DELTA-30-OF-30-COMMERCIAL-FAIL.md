# Reality Delta — v0.5.0 candidate rejected by 30/30 commercial-gate failure

## Real result

```text
CANDIDATE=JPE-P0-S2-PROJECTED-EARLY-RELEASE-V3
MEASURED_RUNS=30
PASS_RUNS=0
FAIL_RUNS=30
COMMERCIAL_GATE_SERIES=FAIL
EXPECTED_HTTP_REQUESTS=67
ACTUAL_HTTP_REQUESTS=67
REQUEST_COUNT_MATCH=PASS
BASELINE_BEATEN=NO
NEW_REAL_P0_ELIGIBLE=NO
STATUS=KEEP_V0.4.0
```

No valid latency distribution exists because zero measured runs passed the commercial gate. The observed wall times must not be interpreted as a candidate P0.

## GPT-side source comparison

The frozen v0.5.0 candidate did not preserve the v0.4.0 semantic contract.

v0.4.0 included, per item:
- request
- current_state
- evidence
- constraints
- allowed_actions
- dependency_ids

and used explicit Choice criteria describing EXECUTE/HOLD/ROUTE/REJECT semantics.

The rejected v0.5.0 candidate removed:
- current_state
- allowed_actions
- dependency_ids

from projected item state and replaced the explicit Choice criteria with simple `actions.<ACTION>` references. It also changed question wording, shard composition, release scheduling, and receipt persistence at the same time.

Therefore the previous statement `QUESTION_SEMANTICS_PRESERVED=YES` was invalid.

## Verdict

```text
VIRTUAL_99_V050=INVALIDATED_BY_REALITY
SOLUTION_FROZEN_V050=REJECTED
REAL_P0_VERSION=v0.4.0
REAL_P0_MS=560.9819
RETURN_TO_STEP_2=YES
```

The next candidate must preserve the full v0.4.0 semantic contract and change only one performance factor at a time.
