---
name: ultrafusion-v8-minimal-pressure-chain
description: "Use when a task needs UltraFusion V8.0, 极简压力链, 高性价比答案, ABCD minimal pressure chain, SelfScore/Deduction/RepairDone, Gain scoring, or a daily alternative to the heavier UltraFusion V7 benchmark flow. Trigger for complex/high-value/high-risk/multi-constraint questions where GPT_DIRECT may be too shallow, but full V7/V15 benchmark overhead is not justified."
---

# UltraFusion V8 Minimal Pressure Chain

## Core Positioning

Use V8.0 as the daily high-value production route:

```text
V7.0 = heavy benchmark / full audit route
V8.0 = daily high-cost-performance production route
```

Do not run UltraFusion for ceremony. Route first:

```text
GPT_DIRECT:
Simple, low-risk, stable, low-value, or user asks for a short direct answer.

UF_V8_ABCD_MIN:
Complex, high-value, high-risk, multi-objective, multi-constraint, needs risks,
counterexamples, acceptance criteria, or a single model is likely to answer shallowly.
```

If the user explicitly asks for full V7.0, benchmark, complete V15 injection, official C/D packages, or external-model copy-paste benchmarking, use `ultrafusion-low-cost-multi-model-extreme-fusion` instead.

## Mandatory V8 Rule Card

For `UF_V8_ABCD_MIN`, preserve pressure and cut packaging:

1. A = independent extreme answer.
2. B = absorb and enhance; not a review of A.
3. C = pressure fusion; not a stitched summary.
4. D = final judgement; not polishing.
5. Every layer must output `SelfScore`, `Deduction`, and `RepairDone`.
6. Deduct against five defects: `漏答 / 浅 / 假 / 乱 / 脆`.
7. `SelfScore < 8.5` must self-repair or rewrite once before output.
8. `8.5 <= SelfScore < 9.0` may pass but must explain deductions.
9. Do not fabricate missing model answers, data, citations, or current model state.
10. Browse/check primary sources when facts may have changed.
11. Finish with `Score_0`, `SCORE_FINAL`, and `Gain = SCORE_FINAL - Score_0`.
12. Admit low or unknown gain; do not inflate the chain verdict.

## Workflow

1. Decide route: `GPT_DIRECT` or `UF_V8_ABCD_MIN`.
2. For GPT direct answers, answer normally and keep the response concise.
3. For V8 chain work, estimate or record `Score_0` for a direct GPT baseline.
4. Run A layer with one to three independent drafts. Prefer two drafts for cost/performance; one draft is allowed when tools/models are limited.
5. Run B layer to produce a stronger new answer from valid A drafts.
6. Run C layer to fuse valid B drafts into one candidate final answer.
7. Run D layer to attack, repair, and deliver the final answer.
8. Record a run summary when the task is important enough to preserve.

Default low-cost model pattern:

```text
A: 1-3 independent drafts, ideally GPT + one other available model.
B: one stronger synthesis draft.
C: one fusion pass.
D: one final judgement pass.
```

When only one model is available, still keep layer pressure and mark:

```text
Limited_Model_Diversity: true
```

## Layer Templates

Use these copy blocks when the user needs manual execution, external models, or preserved run artifacts:

- `30-TEMPLATES/A_PROMPT.md`
- `30-TEMPLATES/B_PROMPT.md`
- `30-TEMPLATES/C_PROMPT.md`
- `30-TEMPLATES/D_PROMPT.md`
- `30-TEMPLATES/RUN_SUMMARY_TEMPLATE.md`

Do not paste all templates into normal chat unless the user asks for copy blocks. For ordinary Codex work, apply the protocol internally and return the final answer plus a compact audit.

## Output Policy

For most user-facing answers, keep the visible output practical:

```text
Final answer
Compact judgement
Score_0:
SCORE_FINAL:
Gain:
Route:
```

For preserved runs, save:

```text
Q.md
A_results.md
B_results.md
C_fusion.md
D_final.md
RUN_SUMMARY.md
```

Suggested run log location:

```text
40-RUNS/RECENT_USE_LOG.md
```

## Failure Review Entry

If a V8 run feels weak, log the failure in:

```text
references/FAILURE_REVIEW_ENTRY.md
```

Use the failure review when:

- B becomes comments instead of a new answer.
- C becomes paste-together summary.
- D only polishes language.
- SelfScore is high but deduction is empty.
- Gain is below `0.5` on a task that should have benefited.
- A model answer is missing and the chain accidentally invents it.

## Gain Verdict

```text
Gain < 0.5: LOW_GAIN; chain likely not worth it.
0.5 <= Gain < 1.0: SMALL_GAIN; use for medium-value tasks only.
1.0 <= Gain < 2.0: EFFECTIVE; clear daily value.
Gain >= 2.0: STRONG_EFFECT; UltraFusion clearly helped.
UNKNOWN: insufficient baseline or scoring evidence.
```

V8.0 is allowed to produce smaller gains than V7.0 because its purpose is lower cost and lower friction. If the task needs maximum auditability, upgrade to V7.0 rather than stretching V8.0.

## Knowledge Reuse Hook

Before complex related work, run or mentally apply the reuse check:

```powershell
python C:\Users\A\.codex\skills\codex-video-to-usable-skill-loop\scripts\preflight_reuse_check.py "UltraFusion V8 极简压力链"
```

Next-run instruction: when a user asks for `UltraFusion V8`, `极简压力链`, `ABCD 极简`, `高性价比生产版`, `SelfScore Deduction RepairDone`, or `Gain 验收`, load this skill first and use V8.0 unless the user explicitly asks for V7.0 heavy benchmark.
