# UltraFusion V7.0 Semi-Automatic ABCD Copy-Paste Workflow

Date: 2026-07-05
Status: active optional route
Route label: `UF_V7_SEMI_AUTO_ABCD`

## Purpose

UltraFusion V7.0 is a semi-automatic multi-layer reasoning route for high-value answers where Codex acts as the orchestration engine and the human only copies question packages into external models and pastes model outputs back into Codex.

Core division of labor:

- Codex generates layer question packages.
- The human copies and pastes only.
- External models answer the packages.
- Codex fuses, converges, scores, and decides whether the chain improved the answer enough.

This route exists because official-site automation can be unavailable, inconvenient, or too invasive for a live desktop session. V7.0 preserves the UltraFusion A/B/C/D structure while making the human operation deliberately simple.

## When To Use

Use `UF_V7_SEMI_AUTO_ABCD` when:

- the user says `UltraFusion V7.0`, `半自动ABCD`, `复制粘贴多层推理`, `ABCD问题包`, `外部模型回答后融合`, or similar;
- the question is high-value enough that a single direct answer may be insufficient;
- browser automation is not desired, unavailable, or would disturb the user's active session;
- the user wants Codex to generate clean copy-paste packages for GPT, DeepSeek, Qwen, Kimi, GLM, or another external model.

Do not use it for simple factual questions, routine coding edits, or cases where direct GPT-quality output is already enough.

## Layer 0: Baseline Scoring

Input:

- original question `Q`;
- ordinary model answer from GPT, DeepSeek, Qwen, or another single model.

Codex output:

- `Score_0` from 0 to 10;
- baseline answer quality analysis;
- decision: whether the problem deserves the full ABCD process.

Escalation rule:

- If `Score_0 >= 8.5` and the remaining risk is low, Codex may recommend stopping.
- If the answer has factual risk, strategic risk, important omissions, or the user explicitly asks for UltraFusion, enter A layer.

## A Layer: Extreme Generation

Input:

- `Q`;
- full V15 requirements;
- `A_PROMPT`;
- optional Search_Fact_Pool when the question depends on current facts.

Codex generates one A-layer question package for external models.

Human operation:

1. Copy the A-layer package.
2. Paste it into external models.
3. Collect `A1`, `A2`, and `A3`.
4. Paste the A answers back into Codex.

Codex gate:

- At least two usable A answers are preferred.
- Empty, refused, shallow, fabricated, or off-question answers are marked and either down-weighted or excluded.

## B Layer: Fusion Enhancement

Input:

- valid `A1/A2/A3`;
- full V15 requirements;
- `B_PROMPT`.

Codex generates one B-layer question package.

Human operation:

1. Copy the B-layer package.
2. Paste it into external models.
3. Collect `B1`, `B2`, and `B3`.
4. Paste the B answers back into Codex.

Hard rule:

- B is fusion enhancement, not review comments.
- A valid B answer must produce a stronger independent answer that absorbs the best of A and fixes A's weaknesses.

## C Layer: Strategy Integration

Input:

- valid `B1/B2/B3`;
- full V15 requirements;
- `C_PROMPT`.

Codex generates the C-layer question package.

Human operation:

1. Copy the C-layer package.
2. Paste it into the selected strongest external model, usually GPT unless the user chooses another model.
3. Collect `C_FINAL`.
4. Paste it back into Codex.

Expected output:

- one strategy answer;
- explicit tradeoffs;
- clear assumptions;
- unresolved uncertainty.

## D Layer: Final Convergence

Input:

- `C_FINAL`;
- full V15 requirements;
- `D_PROMPT`.

Codex generates the D-layer question package.

Human operation:

1. Copy the D-layer package.
2. Paste it into the selected final external model.
3. Collect final answer material.
4. Paste it back into Codex.

Codex finalizes:

- `FINAL_ANSWER`;
- `SCORE_FINAL` from 0 to 10;
- risk analysis;
- `Score_0 vs SCORE_FINAL`;
- `Gain = SCORE_FINAL - Score_0`.

Invalid-link rule:

- If `Gain < 2.0`, mark the run as `INVALID_CHAIN`.
- If `Gain >= 2.0`, mark the run as `EFFECTIVE_CHAIN`.

## Required Codex Output At Each Human Handoff

Every layer package must be copy-paste clean:

```text
[ULTRAFUSION_V7_LAYER=<A|B|C|D>]
[QUESTION_ID=<short id>]
[COPY_START]
...package body...
[COPY_END]
```

Do not mix analysis outside the copy block into the package body. Human operation must stay copy/paste only.

## Acceptance Checklist

- Baseline score exists before A layer.
- V15 is present in every layer package.
- A/B/C/D are all represented unless Codex explicitly labels a reduced route.
- B layer is not mistaken for peer review.
- D layer includes risk analysis and scoring.
- Final comparison includes `Score_0`, `SCORE_FINAL`, and `Gain`.
- `Gain < 2` is honestly marked as `INVALID_CHAIN`.
- Missing or weak external answers are never fabricated.

