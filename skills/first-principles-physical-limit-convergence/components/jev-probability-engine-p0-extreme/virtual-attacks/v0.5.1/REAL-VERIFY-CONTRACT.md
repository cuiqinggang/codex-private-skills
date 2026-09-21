# JEV Probability Engine P0 v0.5.1 — Frozen Reality Verify Contract

Executor authority only. No design, patching, alternative search or parameter changes.

## Frozen candidate

`JPE-P0-S2-SEMANTIC-PROJECTION-V4`

## Baseline

```text
REAL_P0_VERSION=v0.4.0
REAL_P0_MS=560.9819
BENCHMARK=PE-P0-GENERAL-01
MODEL=typesafe/jev-1.13
```

## Exact run

- current user PowerShell process owns `OPENROUTER_API_KEY`;
- 1 auth/schema probe;
- 3 warmups;
- 30 measured;
- 2 HTTP requests per benchmark run;
- expected HTTP requests = 67;
- no retry;
- no topology/model/prompt/criteria/verifier/timing/proxy/system change.

## PASS

All required:

```text
MEASURED_RUNS=30
PASS_RUNS=30
FAIL_RUNS=0
COMMERCIAL_GATE_SERIES=PASS
REQUEST_COUNT_MATCH=PASS
MIN_MS < 560.9819
```

PASS -> return result to GPT for append-only v0.5.1 certification.

Anything else -> KEEP v0.4.0 / 560.9819 ms, record Reality Delta, STOP.
