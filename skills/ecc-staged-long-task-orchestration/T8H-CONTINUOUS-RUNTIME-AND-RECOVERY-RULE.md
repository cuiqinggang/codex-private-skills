# T8H Continuous Runtime And Recovery Rule

## Hard Rule

For T8H official execution:

```text
minimum_elapsed_minutes >= 480
CONTINUOUS_RUNTIME_UNTIL_T8H_OR_BLOCKED = true
```

Both are required. A time gate is not a runtime driver.

## Invalid Stop States Before T+8h

Before elapsed >= 480, these are not valid final states:

```text
PARTIAL_STARTED
STARTED
CHECKPOINT_CREATED
WAITING_FOR_NEXT_HOUR
VERIFIER_EXPECTED_FAIL
PATH_ONLY_RETURN
```

Allowed before T+8h:

- runtime status logs;
- checkpoint logs after real elapsed thresholds;
- recovery notes;
- expected verifier FAIL evidence.

## Recovery Rules

If Codex, shell waiting, or the desktop runtime is interrupted:

1. Do not refresh `00-start-timestamp.json`.
2. Do not create a new official workspace unless the run is explicitly rejected.
3. Do not rerun Run Guard to reset the start.
4. Recompute elapsed from the original start timestamp.
5. Record recovery in a recovery log.
6. Create only checkpoints whose elapsed threshold has already passed.
7. Use actual recovery timestamp for late checkpoints.
8. Do not forge an hour-boundary timestamp.

## Checkpoint Classes

```text
ON_TIME_CHECKPOINT
LATE_RECOVERY_CHECKPOINT
FORGED_CHECKPOINT
```

Acceptance:

```text
ON_TIME_CHECKPOINT = accepted
LATE_RECOVERY_CHECKPOINT = accepted only if disclosed and verified
FORGED_CHECKPOINT = fatal fail
```

## Required Status Codes

```text
T8H_CONTINUOUS_RUNTIME_DRIVER_REQUIRED
T8H_OFFICIAL_RUN_STARTED_BUT_RUNTIME_DRIVER_STOPPED_EARLY
T8H_CONTINUOUS_RUNTIME_DRIVER_PATCH_APPLIED
T8H_RECOVERY_MODE_PASS
T8H_CLEAN_CONTINUOUS_PASS
T8H_LATE_RECOVERY_CHECKPOINT_ACCEPTED
T8H_FORGED_CHECKPOINT_TIMESTAMP_REJECTED
TIME_GATE_IS_NOT_RUNTIME_DRIVER
```

## Final Naming

If honest recovery or late checkpoint occurred, classify the final pass as:

```text
T8H_OFFICIAL_RECOVERY_MODE_PASS
```

Do not call it:

```text
T8H_CLEAN_CONTINUOUS_PASS
```
