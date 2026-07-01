# ChatGPT Web Trinity Bridge V2 Validation - 2026-06-11

## Status

```text
NOT_MATURE_YET
```

V2 has useful partial evidence, but it is not a mature production bridge yet.
The earlier `BATCH_PASS_WITH_WARNINGS` run proved that sequential source-to-
output mapping can work, but it does not satisfy the current acceptance bar.
Mature status requires repeated clean batch passes, no wrong-target paste, and
no saved loading-card screenshots.

## Fixes Since V1

```text
P0 fixed: page stability alone is no longer treated as success.
P0 fixed: send must be confirmed by composer/send-state change.
P0 fixed: a run can fail as ATTACHMENT_FAIL_SEND_NOT_CONFIRMED or
          ATTACHMENT_FAIL_NO_NEW_RESPONSE instead of false PASS.
P1 improved: default window title pattern includes ChatGPT, chatgpt.com,
             Image Repair, Request, and Response.
P1 improved: result saver can use --screenshot-file from the attachment run,
             avoiding multi-window live screenshot drift.
P2 improved: batch runner accepts send retry and send-confirm timeout controls.
P0 fixed in progress: middle-screen target locking rejects Codex windows and
                  removes auto-move/auto-resize fallback that could switch
                  to the wrong input surface.
```

## V2 Live Batch Evidence

Run:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_batch_runner_live_final\20260610-235445_sequential_batch
```

Inputs:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_batch\20260610-224007_batch_v2_offline_two_frame_test\inputs\01_frame_00_0.0s.jpg
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_batch\20260610-224007_batch_v2_offline_two_frame_test\inputs\02_frame_01_0.5s.jpg
```

Saved repaired outputs:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_batch_runner_live_final\20260610-235445_sequential_batch\01_frame_00_0.0s\result\20260611-000345_result_save_a6fb80\local_outputs\01_frame_00_0.0s_repaired.png
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_batch_runner_live_final\20260610-235445_sequential_batch\02_frame_01_0.5s\result\20260611-000754_result_save_d06da7\local_outputs\01_frame_01_0.5s_repaired.png
```

Audit:

```text
item 1: attachment_ok=False, save_ok=True
item 2: attachment_ok=True,  save_ok=True
AUDIT_STATUS=BATCH_PASS_WITH_WARNINGS
warnings=['attachment_nonzero_but_output_saved:1']
failures=[]
```

The first item timed out while waiting for the web response to finish, but the
final result screenshot existed and the saver successfully extracted the local
repaired image. In V2 production semantics this is a warning, not a batch
failure, because the required output file exists.

## Required Production Semantics

```text
BATCH_PASS requires all source images to have saved repaired outputs and no
warnings.
BATCH_PASS_WITH_WARNINGS is not mature acceptance evidence. It is only a debug
artifact unless the user explicitly accepts a one-off salvage result.
BATCH_FAIL means at least one source has no saved repaired output.
WRONG_TARGET_CONTAMINATION means the same prompt was pasted into Codex and
ChatGPT, or into two ChatGPT composers. It invalidates the run even if an image
file is later saved.
MATURE_PASS requires at least 2-3 repeated batch runs, each with 2-3 images,
and every run must be clean BATCH_PASS.
```

## Remaining Work For V2.1

```text
Download the original ChatGPT generated file where the web UI exposes it.
Extract multiple generated results when ChatGPT returns more than one.
Improve upload completion detection beyond conservative attachment waits.
Add a cleaner new-chat isolation route to reduce old-conversation pollution.
```
