# TIMING_LEDGER — HIPE P0

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
```

## v0.1.0 Reality attempt — runner not started

```text
ATTEMPT_LABEL=【混合智能概率引擎｜冻结方案现实验证｜3｜实】
OUTER_START_TIMESTAMP=2026-09-24T00:18:36.1794988+08:00
OUTER_END_TIMESTAMP=2026-09-24T00:21:45.5355827+08:00
OUTER_PROCESS_MS=189343.144

REAL_VALID=NOT_TESTED
REAL_RUNNER_STARTED=NO
RUNTIME_T_VALID=NOT_MEASURED
REALITY_DELTA=FROZEN_RUNNER_DENIED_BY_AUTO_REVIEW_CREDENTIAL_AND_PAID_NETWORK_ACTION
RESULT_SHA256=NOT_CREATED
```

This 189343.144 ms is Reality-attempt orchestration/review time. It is NOT a production T_VALID and is not used to claim engine runtime performance.

## v0.1.1 return-to-virtual maturation

```text
TRIGGER=V0.1.0_REALITY_DELTA
GPT_SIDE_PREVALIDATION=PASS
STRUCTURAL_SELFTEST=PASS
VIRTUAL_MATURITY=PASS
REALITY_CERTIFICATION=PENDING
RUNTIME_T_VALID=NOT_YET_MEASURED

GPT_R4_ACTIVE_TIME=NOT_PRECISELY_INSTRUMENTED
```

The current GPT-page maturation interval did not start with an exact stopwatch boundary, so no fabricated duration is added.

Rules:
- R1/R2/GPT-R3 and later return-to-virtual work are one-time engine-build/maturation costs, not production runtime.
- Reality attempts where the frozen runner never starts are recorded separately and never counted as T_VALID.
- Historical active time that was never precisely instrumented is not fabricated.
- Production runtime T_VALID begins only when the frozen Reality runner actually executes the benchmark.
