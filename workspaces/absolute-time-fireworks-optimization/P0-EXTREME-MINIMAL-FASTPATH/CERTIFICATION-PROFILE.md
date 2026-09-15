# P0 99 Certification Profile V1

- PROJECT: P0-EXTREME-MINIMAL-FASTPATH
- TASK: fixed LoadImage black-256 -> final PNG bytes
- T_START: immediately before POST /prompt
- T_END: matching prompt execution_success + PNG bytes + one full decode + 256x256 + decoded pixel identity
- CLOCK: time.perf_counter_ns
- TIMED_WRITES_ALLOWED: NO
- RUNTIME: ComfyUI 0.9.2 at 127.0.0.1:8188
- IMPLEMENTATION: P0CachedPNGWebsocket with strong-reference tensor cache
- WARMUP: 2
- A/A: 10 blocks, alternating ABBA/BAAB, 40 measured
- INDEPENDENT_UNIT: four-run block
- EFFECT: block mean(A) - block mean(B)
- CI: two-sided 95% t interval, df=9
- EQUIVALENCE_BOUND: [-2ms,+2ms]
- VALIDITY: matching prompt, execution_success, PNG bytes, PNG format, full decode, 256x256, decoded pixel identity
- LABEL_BLIND: arm label is added to returned metadata after RESULT_READY only
- EVIDENCE: one representative PNG and results JSON after all timed runs
- DECISION: AA PASS only if full 95% CI is inside equivalence bound and validity is 40/40
