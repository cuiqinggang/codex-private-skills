# Failure Review 2026-06-23: B-Layer Misread and Claude Fact Freshness Risk

## Incident

An UltraFusion speed analysis initially misunderstood B layer as "cross-review comments" rather than the UltraFusion B-layer extreme fusion step.

## Correct Understanding

In UltraFusion full ABCD:
- A layer is an extreme V15 drafting gate and produces per-model extreme drafts.
- B layer is an extreme V15 fusion gate: it sends the question and all valid A drafts back through each participating model, producing B_<model>_Extreme fusion drafts.
- C layer is an extreme V15 dense fusion/validation gate over valid B drafts.
- D layer is an extreme V15 stranger recheck and final stabilization gate.

Short rule: A/B/C/D are all extreme. Do not imply that only A is extreme while B/C/D are ordinary fusion/review/finalization.

B layer is therefore one of the core places where multi-model error orthogonality and contribution extraction happen. It must not be casually removed from full ABCD.

## Root Cause

The earlier analysis optimized from an abstract "review/fusion" mental model instead of reading the actual v5.0 workflow files first.

## Prevention Rule

Before discussing UltraFusion acceleration, read the active workflow files and distinguish:
- full ABCD architecture;
- D-Lite or simplified route;
- Core-2 bootstrap;
- execution-level speed optimizations.

## Accepted Acceleration Lanes

1. Route simple tasks to D-Lite.
2. Keep full ABCD for complex/high-risk/ambiguous tasks.
3. Use Core-2 Bootstrap while automation stabilizes.
4. Run all eligible A-layer model calls in parallel and all eligible B-layer model calls in parallel.
5. Parallelize browser/API bridge send, wait, collect, and validation steps where safe.
6. Improve browser/API bridge speed after measuring real completion behavior.
7. Reuse Search_Fact_Pool across layers.

## Disallowed Shortcut

Do not present "merge B into A" or "merge B into C" as an optimization for full ABCD. If tested, label it as experimental simplified mode and compare quality before promotion.

Do not execute A/B model calls one-by-one unless forced by a real provider, browser, account, or debug constraint. Serial execution wastes the main speed advantage of multi-provider orchestration.

## Allowed Temporary A-Only Test

The user explicitly allows a temporary intermediate route:

`A_ONLY_CORE2_FUSION_TEST`

Meaning:
- Run only A layer.
- Use GPT Pro browser subscription and free DeepSeek browser access.
- Use screenshot/coordinate bridge to send and collect long browser answers.
- Run GPT and DeepSeek A-layer extreme prompts, preferably in parallel.
- Fuse the two A-layer extreme answers into one provisional high-quality answer.
- Label it as an intermediate test, not full ABCD, not B/C/D, not D_Final, and not final UltraFusion acceptance.

This route is useful for low-cost bridge testing and fast quality probing. It does not replace full ABCD.

Current default from user: if a real task needs to call an UltraFusion-style execution before the full system is ready, use `A_ONLY_CORE2_FUSION_TEST` first. Do not execute the full ABCD pipeline by default until the user explicitly says it is ready or explicitly requests full ABCD.

## Claude Fable/Mythos Fact Freshness

The user also corrected a model-comparison premise around Claude Fable 5 / Mythos 5. This was checked against official Anthropic sources on 2026-06-23.

Future use must re-check official sources because model availability, export controls, and benchmark standings can change quickly.

Primary sources:
- https://www.anthropic.com/news/claude-fable-5-mythos-5
- https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
- https://www.anthropic.com/claude/fable
- https://www.anthropic.com/news/fable-mythos-access
