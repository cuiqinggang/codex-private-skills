---
name: ultrafusion-v8-minimal-pressure-chain
description: "Use when a task needs UltraFusion V8.2 Minimal Gate Patch, V8 minimal ABCD pressure chain, Before-A route gate, per-layer EARLY_WARNING, B/C/D anti-degradation validation, SelfScore/Deduction/RepairDone, Gain scoring, or a daily lightweight alternative to the heavier UltraFusion V7 benchmark flow. Trigger for complex/high-value/high-risk/multi-constraint questions where GPT_DIRECT may be too shallow, but full heavy benchmark overhead is not justified."
---

# UltraFusion V8.2 Minimal Gate Patch

## Core Positioning

UltraFusion V8.2 is the daily high-cost-performance production route:

```text
V7.0 = heavy benchmark / full audit route
V8.2 = V8.1 + Before-A route gate + per-layer EARLY_WARNING + B/C/D anti-degradation validation + D final insurance check.
```

V8.2 is not a new heavy version. It does not add a layer, does not restore the full heavy injection package, and does not restore long C/D benchmark templates.

Route first:

```text
GPT_DIRECT:
Simple, low-risk, stable, low-value, or user asks for a short direct answer.

UF_V8_ABCD_MIN:
Complex, high-value, high-risk, multi-objective, multi-constraint, needs risks,
counterexamples, acceptance criteria, or a single model is likely to answer shallowly.
```

If the user explicitly asks for full V7.0, benchmark, complete heavy injection, official C/D packages, or external-model copy-paste benchmarking, use `ultrafusion-low-cost-multi-model-extreme-fusion` instead.

## Before-A Route Gate

This is not a new layer. It is a lightweight route decision before A.

```text
Before_A_Route_Gate:
Enter UF_V8_ABCD_MIN if the question satisfies any 2 or more:
1. Needs multi-objective tradeoff.
2. Has more than 3 constraints.
3. A single direct model answer is likely to be shallow.
4. Wrong answer cost is high.
5. User explicitly asks for high quality, evaluation, architecture, plan, repair, or judgement.

Otherwise use GPT_DIRECT.
```

## Mandatory V8.2 Rule Card

For `UF_V8_ABCD_MIN`, preserve pressure and cut packaging:

1. A = independent extreme answer.
2. B = absorb and enhance; not a review of A.
3. C = pressure fusion; not a stitched summary.
4. D = final judgement; not polishing.
5. Every layer must output one final scoring block only.
6. Deduct against five defects: missing answer, shallow answer, fabricated claim, disorder, and bloated nonsense.
7. `SelfScore < 8.5` must self-repair or rewrite once before output.
8. `8.5 <= SelfScore < 9.0` may pass but must explain concrete deductions.
9. Do not fabricate missing model answers, data, citations, or current model state.
10. Browse/check primary sources when facts may have changed.
11. Finish with `Score_0`, `SCORE_FINAL`, and `Gain = SCORE_FINAL - Score_0`.
12. Admit low or unknown gain; do not inflate the chain verdict.

## Score Consistency Gate

Apply this in SKILL usage and in A/B/C/D templates:

```text
Score_Consistency_Gate:
1. Write Deduction first.
2. Write SelfScore second.
3. Write RepairDone third.
4. If Deduction is empty, generic, or has no concrete penalty point while SelfScore >= 8.5, lower the score or rewrite the scoring block.
5. Final visible output may keep only one scoring block.
6. Remove draft scoring blocks from final output.
```

## Per-Layer Early Warning

Every A/B/C/D layer must end with:

```text
EARLY_WARNING:
- Quality_Threat: none / low / medium / high
- Reason:
- Action: continue / repair_once / stop_and_return / upgrade_to_V7
```

Rules:

```text
Quality_Threat = high:
Repair the current layer at most once. If it remains high, stop the remaining layers,
return the current best result, and state whether V7 is recommended.

Quality_Threat = medium:
Continue to the next layer. D must judge this risk explicitly.

Quality_Threat = low/none:
Continue normally.
```

## B/C/D Anti-Degradation Gates

```text
B_VALIDATION:
- Has_B_ENHANCED_ANSWER: YES / NO
- Is_Standalone_Answer: YES / NO
- Is_Only_Review: YES / NO

B rule:
If Has_B_ENHANCED_ANSWER = NO, or Is_Standalone_Answer = NO, or Is_Only_Review = YES,
B is invalid and must rerun once. If it still fails, mark B_DEGRADATION_FAIL.
```

```text
C_VALIDATION:
- Conflict_Handled: YES / NO
- Weak_Evidence_Marked: YES / NO
- Duplication_Compressed: YES / NO
- D_Judgement_Points_Listed: YES / NO

C rule:
If any field is NO, C is invalid and must rerun once. If it still fails, mark C_STITCHING_FAIL.
```

```text
D_VALIDATION:
- Attacked_C_FUSION_First: YES / NO
- Hard_Issues_Found_Or_Explicitly_Cleared: YES / NO
- Repairs_Applied: YES / NO

D rule:
If Attacked_C_FUSION_First = NO, D is invalid and must rerun once.
If D only polishes language without attack, judgement, or repair, mark D_POLISHING_FAIL.
```

## D Final Insurance Check

After `Ultra_Answer_Final`, D must run:

```text
D_Final_Insurance_Check:
- Answered_Core_Q: YES / NO
- Has_Executable_Detail: YES / NO
- Handles_Risk_Boundary_Counterexample: YES / NO
```

Rules:

```text
3 YES: pass.
2 YES: pass with LIMITED.
0-1 YES: repair once.
0-1 YES after repair: mark V8_QUALITY_FAIL and recommend V7.
```

## Quality-Architecture-Speed Balance Gate

V8.2 optimizes three linked targets, not quality alone:

```text
Quality: the answer must not become shallow, brittle, or under-specified.
Architecture: the process must stay smaller than V7.0 and avoid route sprawl.
Speed: the answer may be slower than GPT_DIRECT, but must not feel like a heavy benchmark run.
```

Before adding any extra step, apply this test:

```text
Add only if it prevents a likely quality failure or raises expected answer quality.
Reject if it mainly adds ceremony, labels, audit text, or waiting time.
Prefer one sharper gate over one more layer.
```

V8.2 must report its own balance:

```text
Balance:
- Quality:
- Architecture:
- Speed:
- Verdict: BALANCED / TOO_THIN / TOO_HEAVY / TOO_SLOW
```

Balance rules:

```text
If Verdict = TOO_THIN, mark a quality warning even when Gain passes.
If Verdict = TOO_HEAVY, the patch is overbuilt and extra structure must be rolled back.
If Verdict = TOO_SLOW, reduce ceremonial fields first; do not remove B/C/D quality duties.
```

## Workflow

1. Run `Before_A_Route_Gate`: decide `GPT_DIRECT` or `UF_V8_ABCD_MIN`.
2. For GPT direct answers, answer normally and keep the response concise.
3. For V8 chain work, estimate or record `Score_0` for a direct GPT baseline.
4. Run A layer with one to three independent drafts. Prefer two drafts for cost/performance; one draft is allowed when tools/models are limited.
5. Run B layer to produce a stronger new answer from valid A drafts, then apply `B_VALIDATION`.
6. Run C layer to fuse valid B drafts into one candidate final answer, then apply `C_VALIDATION`.
7. Run D layer to attack, repair, deliver the final answer, then apply `D_VALIDATION` and `D_Final_Insurance_Check`.
8. Apply `Score_Consistency_Gate` and `Balance` before final delivery.
9. Record a run summary when the task is important enough to preserve.

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

## Hard Boundaries

Do not add extra layers, side routes, long rubric tables, full heavy injection blocks, long benchmark C/D templates, or repeated scoring blocks to V8.2.

If a repair would add more than one extra pass, either accept a limited result with clear warning or upgrade to V7.0.

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
Balance:
Score_0:
SCORE_FINAL:
Gain:
Route:
```

For layer copy blocks, final output must contain exactly one final scoring block:

```text
Deduction:
SelfScore:
RepairDone:
```

Internal repair notes may be used while thinking, but do not repeat multiple scoring blocks in the final layer output.

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

If a V8.2 run feels weak, log the failure in:

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
- Early warning remains high after one repair.
- Final insurance fails and V7 may be required.

## Gain Verdict

```text
Gain < 0.5: LOW_GAIN; chain likely not worth it.
0.5 <= Gain < 1.0: SMALL_GAIN; use for medium-value tasks only.
1.0 <= Gain < 2.0: EFFECTIVE; clear daily value.
Gain >= 2.0: STRONG_EFFECT; UltraFusion clearly helped.
UNKNOWN: insufficient baseline or scoring evidence.
```

V8.2 is allowed to produce smaller gains than V7.0 because its purpose is lower cost and lower friction. If the task needs maximum auditability, upgrade to V7.0 rather than stretching V8.2.

## Knowledge Reuse Hook

Before complex related work, run or mentally apply the reuse check:

```powershell
python C:\Users\A\.codex\skills\codex-video-to-usable-skill-loop\scripts\preflight_reuse_check.py "UltraFusion V8.2 minimal gate patch"
```

Next-run instruction: when a user asks for `UltraFusion V8`, `UltraFusion V8.2`, `minimal pressure chain`, `ABCD minimal`, `high-cost-performance production`, `SelfScore Deduction RepairDone`, `Gain acceptance`, `Before-A route gate`, or `EARLY_WARNING`, load this skill first and use V8.2 unless the user explicitly asks for V7.0 heavy benchmark.
