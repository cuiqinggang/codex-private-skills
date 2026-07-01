# SOP 2026-06-23: UltraFusion Architecture and Speed Correction

## Purpose

Prevent future UltraFusion answers from trading away the core A/B/C/D design because of a mistaken B-layer interpretation.

## Steps

1. Identify the requested route:
   - current default live route: A_ONLY_CORE2_FUSION_TEST until the user confirms full ABCD is ready;
   - simple or speed-first: D-Lite or existing simplification workflow;
   - normal high-quality: full ABCD;
   - limited model access: Core-2 bootstrap or restricted fusion;
   - temporary browser/capture test: A_ONLY_CORE2_FUSION_TEST with GPT + DeepSeek A-layer extreme drafts only;
   - experimental: clearly label as experimental.

2. Verify layer meanings before proposing changes:
   - A: extreme drafting; each model creates a V15 extreme draft;
   - B: extreme fusion; each participating model fuses all valid A drafts into a B-layer extreme result;
   - C: extreme dense fusion/validation over valid B drafts;
   - D: extreme stranger recheck and final stabilized answer.

3. Say the all-extreme rule out loud in summaries: A/B/C/D are all extreme V15 gates. Do not describe only A as extreme while making B/C/D sound like ordinary processing.

4. Keep full ABCD intact unless the user explicitly chooses a simplified route.

5. Prefer acceleration by execution:
   - run eligible A-layer model calls in parallel;
   - run eligible B-layer model calls in parallel after A outputs are collected;
   - parallelize browser windows, provider calls, waiting, collection, and validation where safe;
   - automate provider/browser bridges;
   - use fixed wait windows only after observed completion timings are reliable;
   - use API calls for suitable lower-risk support steps;
   - reuse Search_Fact_Pool instead of repeating searches;
   - select D-Lite through router for genuinely light tasks.

6. For the temporary A-only Core-2 test:
   - use GPT Pro browser and DeepSeek browser if those are the available low-cost channels;
   - run GPT and DeepSeek A-layer prompts in parallel when possible;
   - collect long answers with the step-by-step screenshot/coordinate method;
   - fuse the two A-layer extreme answers into a provisional answer;
   - mark the result as a test artifact, not D_Final and not final UltraFusion.

7. Do not run full ABCD by default while the full pipeline is not ready. Full ABCD requires explicit user request or later user confirmation that the full pipeline is ready.

8. For frontier-model comparison:
   - browse current official sources;
   - state the exact check date;
   - separate verified facts from inference;
   - avoid preserving hype or rankings as permanent facts.

9. Final answer must explicitly name the route used or recommended:
   - Full ABCD;
   - D-Lite;
   - Core-2 Bootstrap;
   - A_ONLY_CORE2_FUSION_TEST;
   - Restricted Fusion;
   - Experimental Simplification.

## Do Not

- Do not call a D-Lite run "full ABCD."
- Do not call only A "extreme"; all full A/B/C/D layers are extreme V15 gates.
- Do not remove B layer because it seems slow.
- Do not run multi-model A/B calls serially unless forced by provider/browser/account/debug constraints.
- Do not present an A-only GPT+DeepSeek fusion test as full UltraFusion or D_Final.
- Do not start full ABCD just because a task says UltraFusion while the current default route is A_ONLY_CORE2_FUSION_TEST.
- Do not treat current model availability as static.
- Do not write external model claims into reusable rules unless they were verified.
