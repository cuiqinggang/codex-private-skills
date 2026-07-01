# RULE PATCH 2026-06-23: UltraFusion B-Layer Integrity and Freshness Gate

## Trigger

Apply this rule whenever a task mentions:
- UltraFusion
- A/B/C/D fusion
- B layer / B层
- D-Lite
- multi-model fusion speed
- parallel UltraFusion execution
- 层内并行 / 并行运行
- Fable 5 / Mythos 5 / Claude frontier comparison

## Rule

1. For UltraFusion full mode, do not describe B layer as only "reviewing other answers." B layer is a model-level extreme fusion pass over all valid A drafts.
2. Always state that all four full ABCD layers are extreme V15 layers: A extreme drafting, B extreme fusion, C extreme dense validation/fusion, D extreme stranger recheck/final stabilization.
3. Do not propose deleting, merging, or downgrading B layer in full ABCD mode unless the user explicitly asks for an experimental simplified route and the output is labeled non-full.
4. Route simple tasks to D-Lite or other existing simplification workflows instead of weakening full ABCD.
5. Execute UltraFusion with layer-internal parallelism: launch/await/collect all eligible A-layer model calls in parallel, then all eligible B-layer model calls in parallel. C and D remain sequential because they depend on prior layer outputs.
6. Do not run model calls one-by-one unless a provider limitation, account limitation, browser limitation, or explicit debug mode requires it; if serial execution is used, record the reason.
7. A temporary `A_ONLY_CORE2_FUSION_TEST` route is allowed for intermediate testing: run only GPT + DeepSeek A-layer extreme answers, fuse those two A drafts into a provisional answer, and label it clearly as non-full and non-final.
8. The A-only test route may use GPT Pro browser access plus free DeepSeek browser access through screenshot/coordinate capture, but it must not be called B/C/D, full ABCD, D_Final, or final UltraFusion acceptance.
9. Current default: if an actual UltraFusion-style task execution is needed, use `A_ONLY_CORE2_FUSION_TEST` first. Do not run full ABCD unless the user explicitly says the full pipeline is ready or explicitly requests full ABCD for that task.
10. When discussing current frontier models, availability, bans, export controls, rankings, or benchmark status, verify current sources first.
11. If source verification is missing, mark model-comparison claims as unverified and do not write them into long-term rules as facts.

## Preflight Action

Run the reuse check with a task string containing "UltraFusion B layer speed freshness" and read the official UltraFusion workflow files before advising on acceleration or architecture.

## Failure Review Entry

If an answer incorrectly says "B layer is just peer review" or recommends cutting B from full ABCD for speed, log it under:

`C:\Users\A\.codex\skills\ultrafusion-low-cost-multi-model-extreme-fusion\70-NOTES\FAILURE-REVIEW-20260623-b-layer-misread-and-claude-fact-risk.md`

## Acceptance Criteria

- B layer is described as fusion over all A drafts.
- A/B/C/D are all described as extreme V15 layers, not only A.
- Full ABCD remains structurally intact.
- A and B model calls are parallelized where available.
- Any serial fallback is explicitly justified.
- Any A-only GPT+DeepSeek test is labeled `A_ONLY_CORE2_FUSION_TEST` and not represented as full ABCD.
- Full ABCD is not executed by default while the user says it is not ready.
- Simplified routes are labeled as D-Lite, bootstrap, restricted, or experimental.
- Current model claims cite fresh sources or are marked uncertain.
