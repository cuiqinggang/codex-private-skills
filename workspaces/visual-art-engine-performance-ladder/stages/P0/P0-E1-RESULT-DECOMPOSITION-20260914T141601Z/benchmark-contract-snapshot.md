# P0 Benchmark Contract — P0-CONTROL-V1

Status: `FROZEN`
Stage: `P0 ComfyUI Control`
ComfyUI state: `API_READY`

## Fixed task

Measure the minimum stable software overhead of the existing ComfyUI control path:

`REQUEST -> QUEUE -> EXECUTE -> SAVE -> RESULT`

The task starts immediately before HTTP `POST /prompt` and ends only after the matching prompt history reports completion and the newly produced PNG has been fetched and fully validated.

## Frozen workload

- API: existing ComfyUI HTTP API and execution events.
- Graph: built-in `LoadImage -> SaveImage`.
- Input: packaged deterministic `assets/p0/black-256.png`.
- Output: one newly generated valid PNG.
- Resolution: exactly 256 x 256.
- Node classes: `LoadImage`, `SaveImage`.
- Workflow authority: `contracts/p0-workflow.json`.
- Filename prefix may contain a unique run ID solely to prove the output is new; it does not change the workload.

No custom node may be installed. If the frozen node classes are unavailable, record `P0_BLOCKED_NODE_UNAVAILABLE`; do not silently replace the graph. A contract change requires an explicit versioned reopen.

## Timing

Future formal protocol:

- `WARMUP_RUNS=3`
- `MEASURED_RUNS=20`
- `T_REQUEST = QUEUE_ACK - REQUEST_START`
- `T_QUEUE = EXECUTION_START - QUEUE_ACK`
- `T_EXECUTE = SAVE_DONE - EXECUTION_START`
- `T_RESULT = RESULT_READY - SAVE_DONE`
- `T_END_TO_END = RESULT_READY - REQUEST_START`
- CURRENT = median of the 20 measured `T_END_TO_END` values.
- Report `MIN`, `P50`, `P95`, `MAX`.

ComfyUI process cold startup is excluded. Cold and hot conditions must never be mixed.

## Result validity gate

A run is valid only when all are true:

- prompt/history reports completion without execution error;
- output is new for the matching prompt/run ID;
- bytes are a valid PNG signature and chunk stream;
- dimensions are exactly 256 x 256;
- PNG image data fully zlib-decodes and scanline size is complete;
- SHA-256 is recorded;
- raw API/WebSocket events and timestamps are persisted.

A file merely existing is not success. Any task/workflow/node/input/output/resolution change is `TIME=INVALID_RESULT`.

## Forbidden workload

No diffusion, checkpoint inference, Text Encoder inference, VAE inference, LoRA, ControlNet, IPAdapter, AI image, AI video, H3, evaluator, `full_engine_acceptance`, full unittest, release certification, Skill Creator, Knowledge Brain, CodeGraph full-repository scan, or recertification of already-PASS capabilities.

## v1.0.0 execution state

`P0_BENCHMARK_EXECUTED=NO`. This contract is frozen and tooling is ready, but CURRENT is pending.
