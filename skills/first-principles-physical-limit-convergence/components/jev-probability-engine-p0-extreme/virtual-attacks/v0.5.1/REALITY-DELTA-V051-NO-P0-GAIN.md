# Reality Delta — v0.5.1 semantics-preserving projection did not beat v0.4.0

## Real result

```text
CANDIDATE=JPE-P0-S2-SEMANTIC-PROJECTION-V4
MEASURED_RUNS=30
PASS_RUNS=30
FAIL_RUNS=0
COMMERCIAL_GATE_SERIES=PASS
EXPECTED_HTTP_REQUESTS=67
ACTUAL_HTTP_REQUESTS=67
REQUEST_COUNT_MATCH=PASS

PREVIOUS_REAL_P0_VERSION=v0.4.0
PREVIOUS_T_P0_MS=560.9819

MIN_MS=956.2431
P50_MS=1699.9615
P95_MS=3809.9468
MAX_MS=4455.7899

BASELINE_BEATEN=NO
NEW_REAL_P0_ELIGIBLE=NO
STATUS=KEEP_V0.4.0
NEXT_ACTION=REALITY_DELTA_STOP
```

## Interpretation

The semantics-preserving candidate passed the full commercial gate, so the v0.5.0 semantic-drift failure was corrected.

However, the candidate did not beat the certified v0.4.0 real P0 of 560.9819 ms.

Therefore:

```text
SEMANTIC_EQUIVALENCE=REALITY_CONFIRMED
COMMERCIAL_GATE=PASS
PERFORMANCE_PROMOTION=FAIL
REAL_P0_VERSION=v0.4.0
REAL_P0_MS=560.9819
V0.5.1_REAL_P0_ELIGIBLE=NO
```

No latency number from this run may replace the v0.4.0 P0.

## Important comparison limitation

This run was not an interleaved same-session A/B comparison against v0.4.0. Provider/network conditions are stochastic and may have drifted since the v0.4.0 certification.

Accordingly, this result proves only:

1. v0.5.1 is semantically valid under the frozen benchmark;
2. v0.5.1 did not beat the historical certified v0.4.0 baseline in this reality run.

It does NOT isolate whether the slower wall time came from the projection transform itself versus changed provider/network latency.

## Gate decision

```text
REALITY_DELTA_RECORDED=YES
STOP=YES
RETURN_TO_STEP_2_IF_CONTINUING=YES
NO_AUTOMATIC_RETRY=YES
NO_DESIGN_CHANGE_IN_STEP_3=YES
```
