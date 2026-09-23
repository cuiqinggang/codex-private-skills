# REAL-HANDOFF — HIPE P0 v0.1.0

This file is the only Reality handoff for v0.1.0.

## Fixed source
Run only the files in this directory from branch:
`codex/hybrid-intelligence-probability-engine-p0-v0.1.0-virtual-freeze-r3`

Read first:
`VIRTUAL-FREEZE-v0.1.0.md`

Execute:
`REAL-VERIFY-v0.1.0.ps1 -Runs 10`

## Reality permissions
Allowed:
- fetch/read frozen source;
- execute the frozen wrapper/runner;
- measure;
- return result/evidence.

Forbidden:
- modify any frozen file;
- change models, endpoints, prices, prompts, routing, thresholds, benchmark, run count, fallback, verifier, or timing boundary;
- discover a new route;
- repair failure;
- scan credential stores or print secrets.

If `OPENROUTER_API_KEY` is unavailable to the approved runtime, or any frozen gate fails:
```text
REALITY_DELTA=<exact observed delta>
ACTION=STOP
RETURN_TO_GPT=YES
```
No second attempt with a changed design.

If all frozen gates pass, return the runner's final metrics, result SHA256, and outer process timing, then STOP.
