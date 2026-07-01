# SOP 2026-06-23: Speed Without Structure Loss

## Goal

Make UltraFusion faster without weakening full ABCD quality controls.

## Route Selection

Use the smallest honest route:
- Current default live route: A_ONLY_CORE2_FUSION_TEST until the user confirms full ABCD is ready.
- D-Lite: simple factual, low-risk, speed-first tasks.
- A_ONLY_CORE2_FUSION_TEST: temporary middle test using only GPT + DeepSeek A-layer extreme drafts and a provisional fusion answer.
- Core-2 Bootstrap: automation validation or limited provider availability.
- Full ABCD: high-risk, complex, ambiguous, expensive-to-be-wrong tasks.
- Experimental Simplification: only when explicitly testing quality/cost tradeoffs.

## Full ABCD Integrity

Full ABCD means:
1. A prompts include V15 and create per-model extreme drafts.
2. B prompts include V15, original question, and all valid A drafts; B is extreme fusion.
3. C prompt includes V15, original question, and all valid B drafts; C is extreme dense fusion/validation.
4. D prompt includes V15, original question, and C_Fusion; D is extreme stranger recheck/final stabilization.

Do not summarize full ABCD as if only A is extreme. All four full layers are V15 extreme gates.

If B is skipped, the run is not full ABCD.

## Preferred Speed Optimizations

1. Run A layer in parallel across all eligible models.
2. Run B layer in parallel across all eligible models after all valid A drafts are collected.
3. Parallelize send, wait, collect, and validation operations where provider/browser/account constraints allow.
4. Reduce unnecessary browser polling after stable timing data exists.
5. Use provider adapters/API calls where automation and quality are already validated.
6. Keep GPT as quality anchor when available.
7. Reuse Search_Fact_Pool across A/B/C/D.
8. Use fixed model roster rules and guard fallback instead of ad hoc model changes.
9. Record route, skipped layers, unavailable models, serial fallbacks, and residual uncertainty in D_Final.

## A-Only Core-2 Fusion Test

This route is allowed only as an intermediate test:

1. Open GPT Pro browser and DeepSeek browser.
2. Send the A-layer extreme prompt to both models, preferably in parallel.
3. Collect long answers using the step-by-step screenshot/coordinate bridge.
4. Fuse the two A-layer extreme answers into a provisional answer.
5. Label the result `A_ONLY_CORE2_FUSION_TEST`.
6. Do not call the result D_Final or full UltraFusion.
7. Do not use it as final acceptance for the full ABCD pipeline.

Current default: use this route for actual calls until full ABCD is ready. Do not launch full ABCD by default.

## Quality Gate

Any proposed acceleration must answer:
- Which route is this?
- Are all executed full ABCD layers described and treated as extreme V15 gates?
- Is B layer still present if claiming full ABCD?
- Are A and B model calls parallelized where possible?
- If anything is serial, is the provider/browser/account/debug reason recorded?
- If using A-only GPT+DeepSeek, is it labeled as `A_ONLY_CORE2_FUSION_TEST`?
- Is V15 injected in every executed layer?
- Are missing/failed models fabricated? They must not be.
- Is current factual information verified if the question depends on current model/law/company status?
