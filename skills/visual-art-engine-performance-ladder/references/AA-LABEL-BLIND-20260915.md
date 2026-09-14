# P0 Label-Blind Authoritative A/A — 2026-09-15

## Status

This batch is complete. It provides runtime causal confirmation that the previously identified arm-label leakage was a real benchmark contaminant, but it does **not** certify Measurement Protocol V2 as fully PASS because the order-effect equivalence gate remains inconclusive.

- `AA_VALID_RUNS=160`
- `AA_CALIBRATION=INCONCLUSIVE`
- `CANDIDATE_LOCK=ON`
- `LABEL_BLIND_FIX_CAUSALLY_CONFIRMED=YES`
- `PORT_8188_RESPONDING=YES (HTTP 200)`

No E4/E5/E7 candidate and no Track B optimization was started.

## Frozen harness identity

- `RUNNER_SHA=c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54`
- `HARNESS_MANIFEST_SHA=81974d60e1aa54bac03e0d5c27556d87b4ff4e52e742d9e36156998de4b807bf`
- superseded label-blind runner: `8f5c3a592ba18a0570b5213996bdbb4f9618f178d0bd80af16f0c56e912d4062`

Label-blind offline gates before execution:

- `STATISTICAL_SELFTEST=PASS`
- `NORMALIZED_A_B_WORKFLOW_EQUAL=YES`
- `WORKFLOW_LABEL_LEAK=0`
- `TIMED_PATH_LABEL_LEAK=0`
- `HTTP_LABEL_LEAK=0`
- `A_NORMALIZED_WORKFLOW_SHA=94094bf2da0fda3ffba7e69d2e8c63356bb27b0efbb1f1223ece2bc9dafff2aa`
- `B_NORMALIZED_WORKFLOW_SHA=94094bf2da0fda3ffba7e69d2e8c63356bb27b0efbb1f1223ece2bc9dafff2aa`

## Old contaminated A/A

The previous authoritative A/A produced a false label-associated positive result:

- `OLD_AA_EFFECT_MS=3.24545`
- `OLD_AA_95CI=[0.579475,5.953475]`

Its CI was entirely positive and the effect exceeded the old A/A noise floor. Later source/path audit found that `measured-A/B` entered workflow/output identity and timed evidence paths.

## New label-blind A/A

The frozen label-blind harness completed `160/160` valid attempts.

Formal result:

- `AA_FORMAL_EFFECT_MS=2.8688`
- `AA_FORMAL_95CI=[-0.847625,6.585225]`
- `AA_NOISE_FLOOR_MS=3.7609`

The descriptive overall A/B median delta observed during the run was approximately `-0.64975 ms`; the formal estimator above remains the authoritative decision statistic.

Interpretation:

1. The formal CI now crosses zero.
2. The formal effect is below the batch noise floor.
3. The prior label-associated, CI-entirely-positive false optimization signal disappeared under the label-blind harness.

Therefore the label-leak repair is causally confirmed at runtime.

## Remaining gate: order effect

- `ORDER_EFFECT_MS=6.619075`
- `ORDER_EFFECT_95CI=[-3.081325,22.327025]`
- equivalence interval used by the frozen rules: `±3.05 ms`

The order-effect CI is not wholly contained in the equivalence interval. Therefore the correct result is:

`AA_CALIBRATION=INCONCLUSIVE`

—not PASS and not FAIL.

The candidate lock remains on. The next work must address or obtain sufficient independent evidence for the order-effect equivalence gate without changing alpha, CI, MDE, decision rules, workload semantics, workflow, or the frozen harness merely to obtain PASS.

## Runtime/path lesson

The first attempt to run the repaired A/A exposed a Windows path-length problem when creating deep evidence subdirectories under the already long Stage root. The same frozen A/A was rerun using a shorter evidence root (`aa-lb-v3`) without changing workflow semantics, statistical rules, order seed, batch identity, or timed path structure. The shortened evidence path allowed evidence creation and WebSocket connection to proceed.

Permanent lesson: benchmark evidence roots on Windows must be short enough that per-run subdirectories and filenames remain below practical path limits. Path-length readiness belongs in preflight; changing the evidence root for path safety must not change arm-specific timed behavior.

## Evidence location

Local Stage evidence root:

`workspaces/visual-art-engine-performance-ladder/stages/P0/P0-MEASUREMENT-PROTOCOL-V2-20260914T160020Z/aa-lb-v3/`

Primary result file:

`aa-lb-v3/paired-results.json`

Raw Stage evidence should be synced separately; this reference intentionally records the decision result and durable lessons without duplicating the complete raw run corpus into the skill package.

## Decision

- label-blind root-cause fix: **confirmed**
- statistical/null rules: **unchanged**
- Measurement Protocol V2 final certification: **not yet PASS**
- candidate performance work: **still locked**
- next gate: **order-effect equivalence / additional independent A/A evidence under the same frozen rules**
