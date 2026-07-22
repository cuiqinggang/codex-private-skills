# Stage Gate Script Verification Template

## purpose

Add stage-by-stage verification for every declared gate and hard rule.

## inputs

- gate list
- validation gates
- pass criteria
- evidence chain

## forbidden scope

- gate PASS without artifact
- model self-claim as verification
- final report text replacing script output

## gates

1. define stage gate source-of-truth
2. add verify-stage-gates
3. patch validation gates
4. patch pass criteria
5. add smoke trap
6. run verification

## required evidence

- gate-list
- per-gate verification artifacts
- stage-verification-summary
- verify-stage-gates output

## script verification

Run verify-stage-gate-rules or target package equivalent.

## final status codes

- ECC_STAGE_GATE_SCRIPT_VERIFICATION_PATCH_PASS

## failure status codes

- ECC_STAGE_GATE_SCRIPT_VERIFICATION_STOP
