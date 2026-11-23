# UltraFusion A/B/C/D Temperature and Token Strategy v1.1

Date: 2026-06-28
Status: active runtime parameter rule

## Scope

This file defines runtime parameters only. It does not modify `V15_FULL`, `V15_Guard_Prefix`, or any V15 source text.

## Core Principle

A/B/C/D are all V15 extreme stages. There are no ordinary drafts in the full flow.

Temperature controls divergence and convergence. It never lowers the V15 quality bar.

Key sentence:

`Temperature descends from A to D: A/B maximize independent divergence; C/D maximize correctness and stability.`

## Stage Policy

| Stage | Role | Temperature range | Single-value default |
|---|---|---:|---:|
| A | independent extreme drafts with wide divergence across ideas, structures, and reasoning paths | 0.65-0.75 | 0.70 |
| B | absorb all A extreme drafts and generate per-model B extreme drafts | 0.50-0.65 | 0.60 |
| C | dense extreme fusion | 0.25-0.40 | 0.35 |
| D | final extreme review and answer | 0.10-0.25 | 0.20 |

## B Layer Rule

B is one layer. Do not split it into sublayers or two-step variants.

Each participating model reads all valid A-layer extreme drafts, absorbs strengths, identifies gaps, and directly generates its own `B_<model>_Extreme` draft.

Requirements:
- keep B as a single top-level layer;
- preserve useful diversity from A;
- do not output a mere summary;
- do not turn B into peer-review comments;
- do not add extra B sub-stages unless the user explicitly requests a separate experiment.

## A Layer Divergence Rule

A is a wide-divergence layer, not a narrow-difference layer.

Each model should independently explore:
- different reasoning paths;
- different answer structures;
- different assumptions and framing;
- different judgment routes;
- different high-value blind spots.

A should avoid early convergence, imitation, or premature fusion.

## max_tokens Policy

Do not set final fixed max_tokens values yet.

For early full-flow tests, record:
- actual output length per stage and model;
- whether the response was truncated;
- whether the output was overly verbose;
- whether length limits harmed V15 execution;
- whether A/B spent too many tokens without useful contribution;
- whether C/D required more room for fusion or final review.

After several real runs, calibrate stage-specific max_tokens from observed outputs.

Initial principle:
- A/B should not be blindly enlarged.
- C/D may need wider budgets because they carry fusion and final review.

## Current Default Route

As of 2026-06-28, the default for actual UltraFusion-style testing is full ABCD workflow testing with this parameter strategy.

The previous `A_ONLY_CORE2_FUSION_TEST` route is paused as the default and should be used only if the user explicitly asks to return to that temporary test route.
