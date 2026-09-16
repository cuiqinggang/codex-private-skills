# STEP 1 — PHYSICAL LIMIT REPORT

## TASK CONTRACT
```text
TASK_ID=
TASK_COMPLETED=
START_BOUNDARY=
END_BOUNDARY=
CORRECTNESS=
QUALITY_THRESHOLD=
STABILITY_THRESHOLD=
SAFETY=
```

## PHYSICAL DAG
| Block | Required? | Dependency | Parallel/Overlap | Resource | Evidence |
|---|---|---|---|---|---|

## T_PHY
```text
T_PHY_LOW=
T_PHY_HIGH=
CONFIDENCE=
```

## T_MACHINE_STAR
```text
T_MACHINE_STAR_LOW=
T_MACHINE_STAR_HIGH=
CONFIDENCE=
```

## ASSUMPTION LEDGER
| ID | Assumption | Low | Base | High | Confidence | Sensitivity | Source |
|---|---|---:|---:|---:|---|---|---|

## DE-ARMOR CANDIDATES
| Candidate | Why not physically required | Remove before V1? | Risk |
|---|---|---|---|

## ATTACK ORDER
| Rank | Block/mechanism | Expected reducible time | Confidence | Dependency |
|---:|---|---:|---|---|

## MULTI-AGENT DECISION
```text
AGENT_MODE=
N_STAR=
GPU_EXCLUSIVE=
PARALLEL_SUBTASKS=
SERIAL_SUBTASKS=
```

## VERDICT
```text
T_PHY_DEFINED=
T_MACHINE_STAR_DEFINED=
TARGET_REVISION_RULE_FROZEN=
READY_FOR_V1_DESIGN=
```
