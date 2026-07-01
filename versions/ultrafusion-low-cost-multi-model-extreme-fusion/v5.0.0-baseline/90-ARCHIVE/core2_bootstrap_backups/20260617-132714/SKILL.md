---
name: ultrafusion-low-cost-multi-model-extreme-fusion
description: Use when the answer quality of a single model is not enough — ultra-reliable, low-cost multi-model extreme fusion for high-risk / complex / ambiguous questions. Fully automated A-B-C-D pipeline with mandatory V15 injection. No manual copy-paste.
version: 5.0.0
author: UltraFusion System (Hermes Agent packaging)
license: MIT
metadata:
  hermes:
    tags: [multi-model, extreme-fusion, v15, abcd-pipeline, quality-control, low-cost, automated]
    related_skills: [hermes-agent-skill-authoring]
---

# UltraFusion 低成本多模型极限融合技能包 v5.0

## Overview

UltraFusion is an **automated multi-model extreme fusion system** — not a prompt collection, not a manual answer-stitching tool.

It orchestrates 3+ models through a 4-layer A→B→C→D pipeline, injecting V15 extreme quality standards at every layer, and produces a single **D_Final / Ultra_Answer_Final** report that is fact-checked, contradiction-tested, and deduction-scored.

**Why UltraFusion instead of one strong model:**
- Cross-model fact triangulation catches hallucinations
- Multi-perspective reasoning finds counter-examples
- Deduction scoring surfaces quality, not length
- V15 hard gates prevent low-quality answers from leaking through

## When to Use

**Use UltraFusion when:**
- Answer quality of a single model is not enough
- High-risk questions (medical, legal, financial, safety)
- Complex multi-causal reasoning
- Ambiguous questions with multiple valid interpretations
- Decisions where being wrong is expensive
- You need a verifiable, auditable answer trail

**Don't use for:**
- Simple factual lookup ("what is the capital of France")
- Trivial yes/no questions
- Tasks where speed matters more than correctness
- Single-model already provides sufficient quality

## 🚫 Hard Rules (Read First)

### No Manual Copy-Paste
UltraFusion is **fully automated**. The user must never manually open multiple model web pages, copy A/B/C/D drafts, or stitch answers together. All execution is handled by:
- Hermes Agent automated orchestration
- Codex CLI automated orchestration
- Provider Adapter automated API calls
- GPT official subscription browser automation
- Future local Runner / Web service

The legacy manual RUNBOOK is archived for reference only (`90-ARCHIVE/`).

### Only A/B/C/D — No E Layer
UltraFusion has exactly four layers:
| Layer | Input | Output |
|-------|-------|--------|
| **A** | V15 + A template + question | A_<model>_Extreme.md (per model) |
| **B** | V15 + B template + question + all valid A drafts | B_<model>_Extreme.md (per model) |
| **C** | V15 + C template + question + all valid B drafts | C_Fusion_Extreme.md |
| **D** | V15 + D template + question + C_Fusion | D_Final_Ultra_Answer_Final.md |

**No E layer exists.** D_Final is the final report. Creating an E layer is forbidden.



### Search Gate (V15+G v1.1)

Search Gate 是 V15+G 的轻量增强层，用于防止"高分幻觉"。

V15 本身擅长优化答案质量，但如果模型不知道某个实体、版本、当前状态或政策是否存在，V15 可能把错误前提打磨成高质量假答案。

**规则：**
- 不知道的先搜，会变的先搜，静态知识不搜
- 搜索结果进入 Search_Fact_Pool，供 A/B/C/D 共用
- 搜索预算：简单 1 次 / 中等 3 次 / 深度 5 次
- 搜不到或矛盾必须在 D_Final 中标注

### All Four Layers Must Inject V15
This is UltraFusion's core rule. Every layer's assembled prompt must contain:
1. V15_Guard_Prefix
2. V15_FULL specification
3. Layer-specific template
4. Input materials for that layer
5. User's original question

If any layer's assembled prompt is missing V15_FULL:
```
UF_PROMPT_ASSEMBLY_FAIL: V15_FULL_MISSING
```
That layer's output is invalid and must not enter the next layer.

## Default Model Roster (Core-3)

| Slot | Model | Role |
|------|-------|------|
| M0 | **GPT** (official subscription) | Quality anchor — must participate A→D |
| M1 | **DeepSeek-V4-Pro** | Primary reasoning engine |
| M2 | **MiniMax-M2.7** | Diversity & cross-check |
| M3-Q | **Qwen3.5-Flash** | Ablation test slot — NOT in default fusion |

Qwen3.5-Flash does NOT enter C_Fusion by default. It runs as an observation/ablation slot. Promotion to default Core-4 requires passing a 6-question ablation test proving independent contribution.

## GPT Access Rule

GPT is UltraFusion's **fixed quality anchor** and participates in all four layers.

GPT connects via user's existing **GPT official subscription + Hermes browser automation**, not OpenAI API by default. This means GPT usage does not count against API token costs.

If GPT automation is unavailable → `GPT_STATUS = UNAVAILABLE` → D_Final must flag "GPT quality anchor missing".

## C/D Layers Are Extreme Fusion

C_Fusion is NOT a simple merge — it is a **V15-driven extreme fusion** draft.
D_Final is NOT a review pass — it is the **V15-driven final stabilized extreme report**.

Both C and D layers execute the full V15 quality control process internally, then output only the result.

## D_Final Fixed Structure

D_Final / Ultra_Answer_Final is both the final answer AND the audit report:

```
# UltraFusion D_Final / Ultra_Answer_Final

## 0. Run Summary
## 1. Final Answer (the user-facing deliverable)
## 2. Key Facts & Evidence Levels
## 3. Counter-Examples & Alternative Theories
## 4. Reasoning Chain Closure Check
## 5. Model Contributions & Deductions
## 6. V15 Four-Dimension Scoring
## 7. Residual Uncertainty
## 8. Next Steps
```

## Model Failure & Skip Rules

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | Complete | Enter pipeline |
| PARTIAL | Useable, downgraded | Enter with weight reduction |
| EMPTY | No valid answer | Skip |
| REFUSED | Declined to answer | Skip, log reason |
| LOW_QUALITY | Shallow/敷衍 | Do NOT enter C_Fusion |
| ERROR / RATE_LIMITED / AUTH_FAILED | Unavailable | Substitute or skip |

**Hard rules:**
- Never fabricate missing model answers
- Do not force low-quality answers into C_Fusion
- If < 2 models PASS → D_Final must flag "Insufficient multi-model / constrained fusion"
- If GPT missing → D_Final must flag "GPT quality anchor missing"

## Deduction Principles

FinalScore = V15_BaseScore − DeductionPoints + UniqueContributionBonus

Key deductions:
- Critical fact error: −15 to −40
- Fabricated data/citations: −20 to −50
- Hallucinated references: −30 to −60
- Weak evidence as strong conclusion: −10 to −25
- Did not answer core question: −15 to −40
- High-risk (medical/legal) strong claim without warning: −30 to −70

Hard failures (immediate FAIL):
- Fabricated missing model answers
- Fabricated references/data/standards
- High-risk dangerous recommendations
- Key fact errors not corrected
- C or D layer missing V15 injection
- D layer skipped stranger recheck

## Quick Start

```
# Hermes: load this skill, provide a question
"Use ultrafusion-low-cost-multi-model-extreme-fusion to answer: <your question>"

# Codex: load from .codex/skills/
codex exec --skill ultrafusion-low-cost-multi-model-extreme-fusion
```

## File Map

| Directory | Content |
|-----------|---------|
| `10-SPEC/` | V15 specification, guard prefix, fusion spec |
| `20-RUNBOOK/` | Automated execution runbooks |
| `30-TEMPLATES/` | A/B/C/D layer prompt templates |
| `35-MODEL-ROSTER/` | Model lineup, selection, failure rules |
| `36-PROVIDER-ADAPTERS/` | Per-provider API automation specs |
| `37-SCORING/` | V15 scoring, deduction rules |
| `38-PROMPT-ASSEMBLY/` | Prompt assembly specs + V15 injection gate |
| `40-WORKFLOWS/` | Full ABCD workflow, D-Lite, ablation |
| `45-RUNTIME/` | State schema, naming, cost tracking |
| `50-TESTS/` | Test questions with full pipeline outputs |
| `60-KB/` | Knowledge base of Ultra_Answer_Final results |
| `90-ARCHIVE/` | Legacy manual runbooks, old prompt versions |

## Common Pitfalls

1. **Forgetting V15 injection on C/D layers.** C and D are extreme fusion steps, not simple merges. They need V15 as much as A and B do.
2. **Creating an E layer.** D_Final IS the final output. No E layer allowed.
3. **Manual copy-paste workflow.** The old manual RUNBOOK is archived. All execution must be automated.
4. **Forcing Qwen into fusion without ablation proof.** Qwen stays in observation slot until tested.
5. **Fabricating missing model answers.** If a model didn't respond, don't make one up.
6. **Skipping stranger recheck at D layer.** Every D_Final must include counter-example testing.
