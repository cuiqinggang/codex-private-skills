# v0.5.0-candidate Reality Verify Contract

Codex/Reasonix/本地执行器只执行；不得设计、搜索、修改或选择替代路线。

## Frozen input
- Candidate: `JPE-P0-S2-PROJECTED-EARLY-RELEASE-V3`
- Source: `candidate-reality-challenge-v3.cs`
- Baseline: `v0.4.0 / 560.9819 ms`
- Benchmark: `PE-P0-GENERAL-01`
- Model: `typesafe/jev-1.13`

## Exact run
- PowerShell 7+
- current process `OPENROUTER_API_KEY` only
- 1 auth/schema probe
- 3 warmups
- 30 measured
- 2 HTTP requests per benchmark run
- expected total HTTP requests = 67
- no retry
- no model/topology/prompt/threshold/verifier/timer/proxy/system-setting change

## PASS
All are required:
```text
PASS_RUNS=30
FAIL_RUNS=0
COMMERCIAL_GATE_SERIES=PASS
REQUEST_COUNT_MATCH=PASS
MIN_MS < 560.9819
```

If PASS:
- report `NEW_REAL_P0_ELIGIBLE=YES`;
- do not redesign;
- return result to GPT for append-only v0.5.0 certification writeback.

If not PASS:
- keep `v0.4.0 / 560.9819 ms`;
- record Reality Delta;
- STOP;
- do not repair/retry with a changed design.

## Security
API key must never be printed, persisted, committed, or copied into result artifacts.
