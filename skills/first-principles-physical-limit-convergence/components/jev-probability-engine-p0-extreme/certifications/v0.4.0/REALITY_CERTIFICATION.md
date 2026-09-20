# JEV Probability Engine P0 v0.4.0 — Reality Certification

## Certification

```text
SKILL=jev-probability-engine-p0
VERSION=v0.4.0
STATUS=REAL_P0_CERTIFIED

REAL_CERTIFIED=YES
REAL_P0_CERTIFIED=YES

BENCHMARK=PE-P0-GENERAL-01
MODEL=typesafe/jev-1.13
TOPOLOGY=s2
CANDIDATE_ID=JPE-P0-S2-PERSISTENT-TRANSPORT-V2

T_REAL_STAR_MS=560.9819
T_P0_MS=560.9819
P50_MS=648.87
P95_MS=988.8238
MAX_MS=1285.2925

MEASURED_RUNS=30
PASS_RUNS=30
FAIL_RUNS=0
COMMERCIAL_GATE_SERIES=PASS

EXPECTED_HTTP_REQUESTS=67
ACTUAL_HTTP_REQUESTS=67
REQUEST_COUNT_MATCH=PASS

BASELINE_BEATEN=YES
NEW_REAL_P0_ELIGIBLE=YES
```

## Preserved history and measured improvement

```text
PREVIOUS_REAL_P0_VERSION=v0.3.0
PREVIOUS_T_P0_MS=840.6046999999962

NEW_REAL_P0_VERSION=v0.4.0
NEW_T_P0_MS=560.9819

P0_TIME_REDUCTION_PERCENT=33.2644821044
P0_TIME_REDUCTION_PERCENT_APPROX=33.2645
P0_SPEEDUP=1.4984524456x
P0_SPEEDUP_APPROX=1.49845x
```

The previous v0.3.0 Reality Anchor, its original result, all V1/V2 history, and the 840.6046999999962 ms P0 record remain historical evidence. This certification is an append-only promotion and does not reinterpret old evidence as v0.4.0.

## Real execution structure

```text
REAL_JEV_DECISION_WAVES_PER_RUN=1
REAL_HTTP_REQUESTS_PER_RUN=2
REAL_HTTP_REQUEST_CONCURRENCY=2
REAL_LOCAL_EXECUTION_WAVES=2
```

Transport:

- `SocketsHttpHandler=1/process`
- `HttpClient=1/process`
- `System.Text.Json`
- `Task.WhenAll`
- connection pooling / keep-alive through the process-lifetime handler and client

## Unchanged timing boundary

T0 is immediately before the formal public input read. T1 is after `VerifyRealityAsync` has completed and the per-run manifest has been written.

The timer still includes formal input read, state construction, question construction, sharding, serialization, both HTTP requests, response parsing, local execution, dependency waits, persisted-receipt verification, and manifest write. No timing-boundary relaxation was used for v0.4.0.

## Immutable Reality Challenge V2 evidence

```text
C495E53182D91B310615FCA95FDB343980AE9533BC9C6BFEDDF32FB519D85691  REALITY_CHALLENGE_V2_RESULT.json
AAB27543F56B7995EF15FEBCBF6401FBE8366E72AE9DDD785CA72930125BA076  REALITY_CHALLENGE_V2_ACCEPTANCE.md
98EEC72B7060B9F7A21A5E0C97CBE98ABFAB587F321F5C17361FB123D801C3E8  candidate-reality-challenge-v2.cs
F7A6601128F21190F1515908929B93CDFC114A7120F0DA25F7272FDAB9316939  run-reality-challenge-v2.ps1
```

These copied files are byte-identical to the completed Reality Challenge V2 source files. No OpenRouter request or benchmark rerun was performed during certification writeback.
