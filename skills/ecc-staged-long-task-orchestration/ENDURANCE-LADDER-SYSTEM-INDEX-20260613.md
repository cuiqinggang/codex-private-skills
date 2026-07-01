# Endurance Ladder System Index - 2026-06-13

## Purpose

This file records that `ecc-staged-long-task-orchestration` is a cumulative
long-task orchestration package, not a one-off 8 hour experiment.

The current ladder has accumulated practice from:

```text
10 minute / 30 minute / 90 minute / 2 hour / 8 hour
```

The orchestration package is:

```text
H:\AI\skills\ecc-staged-long-task-orchestration
```

The endurance source-of-truth remains:

```text
H:\AI\skills\ecc-endurance-ladder-unified
```

This package records staged GPT-Codex execution, evidence gates, recovery rules,
and lessons from real long-running runs. It must not replace the unified
endurance source package.

## Ladder Stages

| Stage | Role | Main lesson |
| --- | --- | --- |
| 10 minute | smoke / route check | confirm task shape and evidence path before expanding runtime |
| 30 minute | first sustained loop | checkpoint discipline starts to matter |
| 90 minute | medium endurance | partial progress is not final acceptance |
| 2 hour | L4 Run Guard Manager | real functional objective is required before longer validation |
| 8 hour | L5/T8H official run | time gate, runtime driver, recovery, checkpoint honesty, verification, repair, and final acceptance must all hold |

## 8 Hour Classification

The 2026-06-13 official run is accepted as:

```text
CLAUDE_STYLE_12_LAYER_T8H_REAL_ENDURANCE_RUN_PASS
T8H_OFFICIAL_RECOVERY_MODE_PASS
```

It must not be described as:

```text
T8H_CLEAN_CONTINUOUS_PASS
```

Reason:

- elapsed exceeded 480 minutes;
- final verifier passed;
- checkpoint_count was 9;
- final-acceptance.json had `final_pass=true` and `open_blockers=[]`;
- the run included early PARTIAL recovery, waiting tool timeout, and late recovery checkpoints;
- Layer 5 used `LOGICAL_CONTEXT_ISOLATION_ONLY`, not real subagent execution.

## Durable Rule Files

Future 4H/8H/longer runs must read:

- `FAILURE-HISTORY-20260613-T8H-RECOVERY-MODE.md`
- `T8H-CONTINUOUS-RUNTIME-AND-RECOVERY-RULE.md`
- `LAYER5-SUBAGENT-EVIDENCE-MODE-RULE.md`
- `T8H-EVIDENCE-ALIAS-AND-FINAL-ACCEPTANCE-ADDENDUM-RULE.md`

## One Sentence Rule

```text
Long endurance programming is not just minimum_elapsed_minutes; it requires
source-of-truth recovery, P1/P2/P3/P4, Run Guard, continuous runtime driver,
explicit Layer 5 evidence mode, honest recovery checkpoints, Verification Plane,
Repair Loop, Final Acceptance, and non-path-only evidence return.
```
