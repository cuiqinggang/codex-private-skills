# TIMING_LEDGER — HIPE P0 v0.1.0

## Known engine-build / maturation time

```text
TASK_TIME_ID=HIPE-P0-20260923T1958+0800

R1_CODEX_MS=843289.570
R2_CODEX_MS=883533.559

GPT_R3_INSTRUMENTED_START=2026-09-23T23:56:58+08:00
GPT_R3_VIRTUAL_FREEZE_T1=2026-09-24T00:13:49+08:00
GPT_R3_INSTRUMENTED_WALL_MS=1011000.000

KNOWN_ENGINE_BUILD_LOWER_BOUND_MS=2737823.129
KNOWN_ENGINE_BUILD_LOWER_BOUND=00:45:37.823

HISTORICAL_GPT_PRE_INSTRUMENTATION_TIME=UNKNOWN
TRUE_ENGINE_BUILD_MATURATION_TIME=UNKNOWN_GT_LOWER_BOUND

RUNTIME_T_VALID=NOT_YET_MEASURED
```

Rules:
- R1/R2/GPT-R3 are one-time engine-build/maturation costs, not production runtime.
- The duplicate UI "Worked for" values are not added again.
- Historical GPT active time that was never precisely instrumented is not fabricated.
- Production runtime T_VALID begins only when the frozen v0.1.0 Reality runner is executed.
- The R3 T1 above is the point at which all substantive frozen artifacts had been committed and re-read; this ledger write is measurement bookkeeping after T1.
