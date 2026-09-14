# A/A Harness Root-Cause Audit — Arm Label Leakage

Status: `ROOT_CAUSE_CONFIRMED_IN_SOURCE / FIX_IMPLEMENTED / CAUSAL_RUNTIME_CONFIRMATION_BLOCKED`

## Frozen state

- Old authoritative batch: `authoritative-runs/AUTH-AA-STAT-FINAL-40B`
- Old runner SHA-256: `fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b`
- Old batch remains immutable evidence.
- `AA_CALIBRATION=FAIL`
- `CANDIDATE_LOCK=ON`
- No statistical threshold, alpha, CI, MDE, cluster unit, null rule, or KEEP rule was changed.

## Closed evidence chain

The old 160-run A/A produced a formal effect of `3.24545 ms` with 95% CI
`[0.579475, 5.953475] ms`.

Raw-event decomposition shows:

| Segment | A-minus-B block effect |
|---|---:|
| ComfyUI server `execution_start -> execution_success` | `0.00000 ms` |
| `QUEUE_ACK -> EXECUTION_START` | `+0.91815 ms` |
| `SAVE_DONE -> RESULT_READY` | `+1.89000 ms` |
| `executing(null) -> HISTORY_CONFIRMED` | `+0.152875 ms` |
| `HISTORY_CONFIRMED -> RESULT_READY` | `+1.18235 ms` |

The output PNG size is exactly 665 bytes for both arms. Median raw-event and
history sizes are also equal. The dominant effect is outside the real server
execution interval.

## Source-level contamination

The old runner passed the arm-bearing label into:

- ComfyUI `SaveImage.filename_prefix`;
- the output filename returned to and fetched through `/view`;
- the raw-event file path that is flushed during the timed interval;
- the evidence PNG path written before `RESULT_READY`;
- the history/equivalence evidence paths.

Examples were `measured-A-*` and `measured-B-*`. Therefore A1 and A2 used the
same algorithm but not a label-blind execution path. This violates the protocol
rule that A/A labels are metadata only.

`ROOT_CAUSE_CANDIDATE=AA_ARM_LABEL_LEAK_IN_WORKFLOW_AND_TIMED_FILE_PATHS`

`SERVER_EXECUTION_EFFECT_MS=0`

`CLIENT_CONTROL_PATH_EFFECT_DOMINANT=YES`

## Repair

The repaired runner preassigns fixed-shape opaque tokens by physical attempt
before invoking either arm. A/B remains only in post-run metadata.

- workflow and `filename_prefix`: opaque token only;
- raw/history/output/equivalence paths: opaque token only;
- `/view` query derives from the label-blind ComfyUI output;
- fine-grained marks are in-memory `monotonic_ns` values;
- runtime guards fail closed on workflow, HTTP, or timed-path label leakage;
- selftest normalizes the opaque token and requires byte-equivalent A/B workflow
  JSON.

New runner SHA-256:
`c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54`

Current full harness fingerprint:
`81974d60e1aa54bac03e0d5c27556d87b4ff4e52e742d9e36156998de4b807bf`

Deterministic manifest:
`../harness-manifest-label-blind.json`

Version chain:

- `8f5c3a592ba18a0570b5213996bdbb4f9618f178d0bd80af16f0c56e912d4062`
  = `SUPERSEDED_LABEL_BLIND_RUNNER`;
- `c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54`
  = `CURRENT_LABEL_BLIND_RUNNER`.

Selftest evidence:
`../statistical-selftest-label-blind.json`

Observed selftest gates:

- `A_NORMALIZED_WORKFLOW_SHA=B_NORMALIZED_WORKFLOW_SHA=94094bf2da0fda3ffba7e69d2e8c63356bb27b0efbb1f1223ece2bc9dafff2aa`
- `TIMED_PATH_LABEL_LEAK=0`
- `WORKFLOW_LABEL_LEAK=0`
- `HTTP_LABEL_LEAK=0`
- `STATISTICAL_SELFTEST=PASS`

## Remaining causal test

Runtime confirmation requires a fresh 40-block, 160-run authoritative A/A in
the same healthy ComfyUI environment. Two launch requests were not executed:
the second followed the user's explicit task-scoped approval, but the runtime
still applied an absolute rejection to creating a local process that listens on
`127.0.0.1:8188`. No bypass was attempted.

The new runner replayed the old 160-run blocks through the unchanged statistical
function and reproduced null rate, CI, and MDE values exactly. See
`statistical-replay.json`. This is statistical parity evidence only and is not
a fresh label-blind runtime A/A.

`FRESH_LABEL_BLIND_AA=BLOCKED_RUNTIME_PERMISSION`

Until that run completes:

- `ROOT_CAUSE=AA_ARM_LABEL_LEAK`
- `ROOT_CAUSE_FIX=IMPLEMENTED`
- `CURRENT_RUNNER_SHA=c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54`
- `HARNESS_MANIFEST_SHA=81974d60e1aa54bac03e0d5c27556d87b4ff4e52e742d9e36156998de4b807bf`
- `AUTHORITATIVE_AA=BLOCKED_RUNTIME_PERMISSION`
- `AA_CALIBRATION=FAIL`
- `CANDIDATE_LOCK=ON`
- `P0_99=NO`
- `P0_FREEZE=NO`
- `P1_UNLOCKED=NO`

The root cause is source-confirmed as contamination, while the claim that it
explains the full 3.24545 ms remains pending the new A/A collapse test.
