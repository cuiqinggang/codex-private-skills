# Runtime Gate Hard Standard

## Purpose

Prevent any task declared as 2H, 4H, 8H, long-task, endurance, runtime, or continuous runtime from reaching PASS before the real minimum runtime and checkpoint requirements are met.

This file closes the loophole where a task says "2H" but finishes in a few minutes and still reports PASS.

## Task Type Detection

Enable `RUNTIME_GATE` when the task name, TASK_ID, command package, run config, final acceptance, or task body contains any of:

```text
2H
4H
8H
two-hour
four-hour
eight-hour
long-task
endurance
runtime
runtime-enforced
continuous runtime
长任务
两小时
四小时
八小时
耐力运行
```

## Minimum Runtime

```text
30min => minimum_runtime_minutes = 30
2H => minimum_runtime_minutes = 120
4H => minimum_runtime_minutes = 240
8H => minimum_runtime_minutes = 480
```

If `elapsed_minutes < minimum_runtime_minutes`, final status must be `FAIL` or `PARTIAL`. `PASS` and `ACCEPTED` are forbidden.

## Checkpoint Rules

2H tasks require at least 8 checkpoints. Recommended timeline:

```text
0 / 15 / 30 / 45 / 60 / 75 / 90 / 105 / 120 final
```

4H tasks require at least 16 checkpoints.

8H tasks require at least 32 checkpoints.

Every checkpoint must include:

```text
timestamp
elapsed_minutes
phase_name
files_read
files_written
samples_processed
accepted_count
rejected_count
needs_human_count
current_risks
next_action
```

## Required Runtime Evidence

Every runtime-enforced task must output:

```text
outputs/runtime-evidence.json
```

It must include:

```json
{
  "task_id": "",
  "declared_runtime_minutes": 120,
  "minimum_runtime_minutes": 120,
  "started_at": "",
  "ended_at": "",
  "elapsed_minutes": 0,
  "checkpoint_count": 0,
  "checkpoint_interval_minutes": 15,
  "runtime_gate_passed": false,
  "formal_files_modified": [],
  "final_status_allowed": false
}
```

## PASS Conditions

`FINAL_STATUS = PASS` is allowed only when all are true:

1. `elapsed_minutes >= minimum_runtime_minutes`
2. checkpoint count is sufficient
3. `runtime_gate_passed = true`
4. `runtime-evidence.json` exists
5. `checkpoint-timeline.html` exists
6. final checkpoint exists
7. elapsed time is not forged
8. formal skill modifications match task authorization
9. verifier returns PASS

## Forced FAIL Conditions

If any condition is true, `PASS` is forbidden:

1. `elapsed_minutes < minimum_runtime_minutes`
2. checkpoint count is too low
3. `runtime-evidence.json` is missing
4. only a final checkpoint exists, with no intermediate process
5. task declares 2H but finishes in under 10 minutes
6. `started_at` or `ended_at` is missing
7. verifier does not check runtime gate

## Patch Install Task vs Runtime-Enforced Task

### Patch install task

Rule installation, documentation patching, and verifier updates may finish in minutes.

Allowed status:

```text
PATCH_INSTALL_PASS
```

Forbidden status:

```text
2H_RUNTIME_PASS
```

### Runtime-enforced task

2H sample optimization, 4H governance, 8H endurance run, and any task with runtime keywords must truly run until the target time or be marked BLOCKED/PARTIAL/FAIL.

It cannot PASS early.

## Status Codes

```text
RUNTIME_GATE_PASS
RUNTIME_GATE_FAIL
RUNTIME_GATE_FAIL_ELAPSED_TOO_SHORT
RUNTIME_GATE_FAIL_CHECKPOINTS_TOO_FEW
RUNTIME_GATE_FAIL_EVIDENCE_MISSING
RUNTIME_GATE_FAIL_FINAL_CHECKPOINT_MISSING
PATCH_INSTALL_PASS
2H_RUNTIME_PASS_FORBIDDEN
```

