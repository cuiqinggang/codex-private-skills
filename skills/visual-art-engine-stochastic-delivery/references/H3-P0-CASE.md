# H3-P0 Case — Verified Stochastic Video Delivery

## Problem

MiniMax H3 / Star7 / 1-step achieved very low steady-state time but some seeds produced near-white/flat videos under fixed QC.

## What failed

- fixed-seed 10/10 quality certification;
- treating all quality failures as Star7 instability;
- same-seed reference fallback as universal rescue;
- ACT32 FP32 activation-boundary repair;
- searching for one single numerical divergence.

## Diagnostic result

```text
ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION
FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE
```

One seed (`920108`) failed both Star7 and original UNETLoader at the same 1-step contract, proving that some failures belong to the stochastic low-step sample region rather than one precision implementation.

## Winning system

```text
Star7 1-step
-> QC
-> PASS: accept
-> FAIL: reject + draw new OS-random seed
-> repeat same Star7 1-step path
```

## Final certification

```text
formal tasks=20
formal attempts=22
first-attempt pass=90%
mean attempts=1.10
T_TFVR mean=6.804s
T_TFVR P50=6.076s
T_TFVR P95=11.974s
T_TFVR max=12.862s
accepted QC=20/20
invalid output delivered=0
```

## Transferable lesson

For stochastic visual generation, quality stability can be a **delivery-system property** rather than a **single-attempt property**. When seed is not user semantics, a fast proposal + strict verifier + reseed loop can dominate globally slower “safe” paths.

Do not apply this automatically to exact-seed reproducibility, benchmark A/B, reference-driven deterministic comparisons, or exact edits.