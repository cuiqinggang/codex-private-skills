# P0 Four-Column Process Audit — 2026-09-14

## Scope

Stage: `P0 ComfyUI Control`
Contract: `P0-CONTROL-V1`
Graph: `LoadImage -> SaveImage`
Method: `mature-replication-four-column` V4.0
Working skill: `visual-art-engine-performance-ladder 1.0.1_LOCAL_PATCH`

This is an early-methodology audit. It is intentionally explicit and conservative. The full local evidence bundle has not yet been uploaded to the shared workspace, so raw-event and script-level verification remains pending.

---

## 1. CURRENT

Status: `MEASURED / SUMMARY_VALID / SHARED_RAW_AUDIT_PENDING`

Measured results reported by Codex:

- warmup: 3/3 valid
- measured: 20/20 valid
- failures: 0
- median end-to-end: 32.55975 ms
- min: 27.2659 ms
- p95: 58.1779 ms
- max: 58.4551 ms
- request median: 5.55075 ms
- queue median: 4.71925 ms
- execute median: 3.4891 ms
- result median: 16.99775 ms
- save timing: not independently isolated; included in execute
- output validation: pass
- unique prompt ids: 23/23
- unique output hashes: 23/23
- raw event records: 417
- event mapping warning: none
- queue idle after run: yes

Approximate share of total median:

- REQUEST: 17.05%
- QUEUE: 14.49%
- EXECUTE: 10.72%
- RESULT: 52.20%
- residual/event-boundary difference: ~5.54%

Observed median-to-min gap: 5.29385 ms (~16.26% of median).
Observed p95/median ratio: ~1.787.

Audit judgment:

`CURRENT` is strong enough to accept as the first measured baseline at summary level. Final evidence acceptance requires the shared raw bundle and benchmark script to be reviewed from GitHub.

---

## 2. EXTERNAL FRONTIER

Status: `ARCHITECTURE_FRONTIER_IDENTIFIED / NUMERIC_FRONTIER_UNKNOWN`

Official ComfyUI documentation confirms that the native minimal control path is based on:

- POST `/prompt` for validation and queue insertion
- `/ws` for real-time execution events
- `/history/{prompt_id}` for completed history/results
- `/queue` for queue state

Official sources:

- https://docs.comfy.org/development/comfyui-server/comms_routes
- https://docs.comfy.org/development/comfyui-server/comms_messages
- https://github.com/Comfy-Org/ComfyUI/blob/master/script_examples/websockets_api_example.py

Therefore the current direct-local native API architecture is already aligned with the official minimal path; there is no evidence yet that an extra proxy or alternate control plane is required for P0.

However, an apples-to-apples public benchmark for `LoadImage -> SaveImage`, 256x256, localhost, API-ready ComfyUI, measured as REQUEST->RESULT_READY has not yet been found. Therefore:

`T_EXTERNAL = UNKNOWN`

Do not invent a numeric external frontier.

Next external-research task should specifically search for comparable local-control latency, not image-generation benchmarks.

---

## 3. FIRST-PRINCIPLES PHYSICAL TIME

Status: `PROVISIONAL / NOT YET SIGNABLE`

Hard fact from the current run:

Because at least one valid execution completed in 27.2659 ms under the frozen contract,

`T_PHY <= 27.2659 ms`

for this task/environment definition.

This is only an upper bound on the physical minimum, not the final T_PHY estimate.

A useful lower bound/range cannot yet be signed because two key components remain unresolved:

1. `SAVE` is not independently isolated from EXECUTE.
2. `RESULT` is the largest median segment (~16.998 ms, ~52.2% of total), but its internal composition has not yet been audited from the benchmark script and raw event stream.

This matters because ComfyUI has a known lifecycle distinction between execution-completion signaling and persistence/history visibility. Public upstream discussion notes that `execution_success` can occur before final history persistence, so a client can observe a gap between execution completion and output/history visibility:

- https://github.com/Comfy-Org/ComfyUI/issues/11540
- https://github.com/Comfy-Org/ComfyUI/issues/15341

Therefore the next T_PHY step is not to optimize anything. It is to decompose `RESULT_READY` and confirm exactly what is being timed.

Required decomposition audit:

- request serialization + localhost HTTP round trip
- prompt validation + queue insertion
- queue dispatch/scheduling
- LoadImage decode/tensor conversion
- SaveImage tensor->PIL + PNG encode/write
- execution completion event
- history persistence / result visibility
- client detection/polling delay
- output validation/hashing, confirming whether they are inside or outside T_END_TO_END

Only after this decomposition should a numerical `T_PHY_RANGE` be approved.

---

## 4. ITERATIVE CONVERGENCE

Status: `LOCKED`

Reason:

- CURRENT: measured
- EXTERNAL numeric frontier: not yet established
- T_PHY/T_PHY_RANGE: not yet established

Therefore optimization is not authorized yet.

The likely first high-value area, based on CURRENT alone, is RESULT-path latency/jitter, not node execution. But this is a diagnostic hypothesis, not an optimization order.

The first allowed next action is evidence/audit work:

1. upload the complete P0 evidence bundle to the shared GitHub workspace;
2. audit `run-p0-control.py`, raw events, timing summary, and result-ready semantics;
3. establish numeric/qualified EXTERNAL FRONTIER;
4. derive and review P0 `T_PHY_RANGE`;
5. only then unlock ITERATIVE CONVERGENCE and choose the first single-variable experiment.

---

## Methodology audit

V4.0 is behaving correctly in this first real use:

- it prevented optimization before CURRENT existed;
- it now prevents optimization before external reality and T_PHY are understood;
- it exposes a real measurement ambiguity (RESULT/SAVE semantics) instead of prematurely calling 32.56 ms 'good' or 'bad';
- it preserves the frozen task and rejects workload-changing shortcuts.

Current methodology status:

`V4_FORWARD_USE_EVIDENCE = PARTIAL_PASS`

Reason: it has successfully governed P0 CURRENT acquisition, but the full four-column cycle has not yet completed.

Do not mark V4.0 forward-use evidence as fully complete until at least one stage reaches a reviewed `99 -> FREEZE` cycle.
