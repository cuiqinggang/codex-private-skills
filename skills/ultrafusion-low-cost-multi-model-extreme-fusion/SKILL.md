---
name: ultrafusion-low-cost-multi-model-extreme-fusion
description: "Use when deciding whether an answer should stay GPT-only, escalate to UltraFusion 6.1B official-site multi-model review, or run UltraFusion V7.0 semi-automatic ABCD copy-paste orchestration. Current route: normal questions use GPT directly; high-value/extreme questions use GPT + DeepSeek + Qwen official sites or UF_V7_SEMI_AUTO_ABCD when the user wants Codex-generated question packages."
version: UltraFusion-7.0-semi-auto-abcd-2026-07-05
author: UltraFusion System (Hermes Agent packaging)
license: MIT
metadata:
  aliases:
    - UltraFusion 6.1B
    - UltraFusion V7.0
    - UF_V7_SEMI_AUTO_ABCD
    - 半自动ABCD
    - ABCD问题包
    - 复制粘贴多层推理
    - Score_0 vs Score_FINAL
    - 官网三模型
    - 两档路由
    - GPT直答
    - GPT DeepSeek 千问
    - 多智能体极限低成本回答6.1B
  hermes:
    tags: [multi-model, official-site, two-tier-routing, gpt, deepseek, qwen, v15, quality-control, low-cost, version-6-1b, version-7-0, semi-auto-abcd, copy-paste-question-packages]
    related_skills: [hermes-agent-skill-authoring]
---

# UltraFusion 低成本多模型极限融合技能包 6.1B

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

## UltraFusion V7.0 Semi-Automatic ABCD Route

UltraFusion V7.0 adds an explicit semi-automatic route label:

```text
UF_V7_SEMI_AUTO_ABCD
```

Use this route when the user says `UltraFusion V7.0`, `半自动ABCD`, `ABCD问题包`, `复制粘贴多层推理`, `外部模型回答`, `Score_0 vs Score_FINAL`, or asks Codex to generate question packages for external models.

V7.0 division of labor:

```text
Codex generates layer question packages.
Human copies and pastes only.
External models answer.
Codex fuses, converges, scores, and judges the gain.
```

The required layers are:

```text
0 baseline scoring -> A extreme generation -> B fusion enhancement -> C strategy integration -> D final convergence
```

Final scoring must include:

```text
Score_0:
SCORE_FINAL:
Gain = SCORE_FINAL - Score_0
Chain verdict: EFFECTIVE_CHAIN | INVALID_CHAIN
```

If `Gain < 2.0`, the V7 run is an `INVALID_CHAIN`. Do not hide low gain by adding extra unplanned layers.

## 🚫 Hard Rules (Read First)

### UltraFusion 6.1B Current Official Route

UltraFusion 不要求一开始必须四模型满配。

**当前正式有效版本是 UltraFusion 6.1B。**

当前固定两档路由：

```text
第一档：普通问题 -> GPT / ChatGPT 官网直接回答
第二档：高价值 / 极限答案问题 -> GPT 官网 + DeepSeek 官网 + 千问/Qwen 官网
```

当前固定模型入口：

```text
GPT / ChatGPT: https://chatgpt.com/
DeepSeek Chat: https://chat.deepseek.com/
千问/Qwen: https://www.qianwen.com/
Qwen backup: https://chat.qwen.ai/
```

普通问题不使用 DeepSeek、千问/Qwen、V15、A/B/C/D、多模型融合、复杂验收。判断标准是：GPT 本身已经能给出足够有价值的答案，再调用其他模型不会显著增加质量。

只有当额外模型、V15、多模型互审能够显著提高答案质量时，才进入 UltraFusion 流程。

旧路线 `GPT + Kimi + GLM` 是 deprecated / old route / not current official route，不作为 6.1B 测试标准。

### Official-Site Operation Rule

官网模型测试默认使用普通用户可见界面流程：

```text
截图 -> 可见坐标定位 -> 一个小动作 -> 再截图 -> 验证
```

不要优先使用一般用户不会用的调试接口、DOM、CDP、浏览器控制、网页内部控制或反检测/规避类方法。若用户正在使用电脑，不得使用会抢占真实鼠标、键盘或前台焦点的输入方式。需要输入到当前已登录 Chrome 标签页时，必须等用户给出空档或改用隔离环境。

允许的目标是稳定、低频、尊重官网规则地使用公开界面；不允许绕过网站限制、隐藏自动化或规避检测。

### Only A/B/C/D — No E Layer
UltraFusion has exactly four layers:
| Layer | Input | Output |
|-------|-------|--------|
| **A** | V15 + A template + question | A_<model>_Extreme.md (per model) |
| **B** | V15 + B template + question + all valid A drafts | B_<model>_Extreme.md (per model) |
| **C** | V15 + C template + question + all valid B drafts | C_Fusion_Extreme.md |
| **D** | V15 + D template + question + C_Fusion | D_Final_Ultra_Answer_Final.md |

**No E layer exists.** D_Final is the final report. Creating an E layer is forbidden.

### B 层是极限融合，不是写审稿意见（B Layer = Extreme Fusion, Not Review）

B 层是对所有有效的 A 稿做**极限融合**（把多个 A 稿的信息交叉对比、取长补短、产出更强的独立答案），不是对 A 稿写审稿意见。

如果 B 层输出变成了"评论 A 稿哪里写得不好"而不是自己产出更强的答案，B 层就失败了。

### 简化路线标签（Reduced Route Labels）

不是完整四层的运行，必须在输出中标明用了哪种简化路线：

| 标签（Label） | 含义 | 说明 |
|-------------|------|------|
| `D-Lite`（D轻量版） | 跳过 B 层 | A 层输出直接送 C 融合，节省一次模型调用 |
| `restricted`（受限融合） | 模型数不足 | 可用模型不够 Core-3 时使用 |
| `bootstrap`（自举模式） | 临时测试路线 | 仅用于受限条件下验证链路；6.1B 正式路线以 GPT + DeepSeek + 千问/Qwen 为准 |
| `simplified`（简化版） | 省成本 | 按 Auto_Simplification_Workflow 规则简化 |
| `A_ONLY_CORE2_FUSION_TEST` | 只跑 A 层两模型测试 | 临时测试路线，仅用于验证截图/坐标/API 链路 |

**诚实标注规则（Label Honesty）：**

简化路线绝对不能自称"完整四层融合（full UltraFusion）"或"完整 ABCD（full ABCD）"。跑了 A 层测试就必须标 A_ONLY_CORE2_FUSION_TEST，跑了 D-Lite 就必须标 D-Lite。路线标签必须诚实。

### 加速优先保架构（Speed Optimization）

加速时优先用以下手段，不能为了加速砍掉四层结构但仍然自称完整融合：

- 层内并行（同一层多模型同时调用，不等上一个结束）
- 路由优化
- 等待策略调整（超时/重试）
- 自举模式（bootstrap）

**禁止**：为了加速砍掉 B/C/D 层但仍然自称"完整四层融合"或"完整 ABCD"。

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

For UltraFusion V7.0 full ABCD runs, the canonical V15 source is:

```text
10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
```

Do not replace it with a short summary, compact explanation, placeholder, or rewritten version. If the assembled package contains `<<<V15_FULL>>>` or only describes V15 instead of pasting the full canonical text, the layer is invalid.

If any layer's assembled prompt is missing V15_FULL:
```
UF_PROMPT_ASSEMBLY_FAIL: V15_FULL_MISSING
```
That layer's output is invalid and must not enter the next layer.

If the wrong or compressed V15 source is used:
```
UF_PROMPT_ASSEMBLY_FAIL: V15_CANONICAL_SOURCE_NOT_USED
```

## UltraFusion 6.1B Official Model Route

The official core route is now:

```text
Normal questions: GPT official site only
High-value / extreme questions: GPT official site + DeepSeek official site + Qwen official site
```

The route is official-site / official-client first. APIs are automation,
batch-processing, or fallback paths, not the primary extreme-answer route.

Core roles:

| Slot | Model / Route | Role |
|------|---------------|------|
| M0 | GPT official site | default direct-answer entry, initial frame, final fusion, final acceptance |
| M1 | DeepSeek Chat official site | low-cost deep analysis, adversarial review, reasoning depth |
| M2 | Qwen / Tongyi official site | third perspective, Chinese-source supplement, search/synthesis diversity |

Fallback roles:

| Model | Role |
|-------|------|
| Kimi | deprecated from current official 6.1B route; optional benchmark only |
| GLM-5.2 | not in the main answer chain; engineering/coding execution candidate |
| MiniMax | audio/video, creative, multimodal backup; not in the core answer chain |

## Legacy Default Model Roster (v5.0 baseline)

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
| `40-WORKFLOWS/` | Full ABCD workflow, D-Lite, ablation, V7 semi-auto copy-paste workflow |
| `45-RUNTIME/` | State schema, naming, cost tracking, V7 semi-auto run state |
| `50-TESTS/` | Test questions with full pipeline outputs |
| `60-KB/` | Knowledge base of Ultra_Answer_Final results |
| `90-ARCHIVE/` | Legacy manual runbooks, old prompt versions |

## Common Pitfalls

1. **Forgetting V15 injection on C/D layers.** C and D are extreme fusion steps, not simple merges. They need V15 as much as A and B do.
2. **Creating an E layer.** D_Final IS the final output. No E layer allowed.
3. **Unlabeled manual copy-paste workflow.** The old manual RUNBOOK is archived. Manual copy-paste is allowed only when explicitly labeled `UF_V7_SEMI_AUTO_ABCD` and uses clean Codex-generated question packages.
4. **Using old Qwen ablation rules against 6.1B.** In UltraFusion 6.1B, Qwen / 千问 is part of the current official high-value route. Do not demote it by applying older ablation-only rules.
5. **Fabricating missing model answers.** If a model didn't respond, don't make one up.
6. **Skipping stranger recheck at D layer.** Every D_Final must include counter-example testing.
7. **Treating B layer as review comments.** B is extreme fusion over A drafts, not peer-review. If B output looks like "A's answer could be improved here..." instead of producing a stronger independent answer, B layer failed.
8. **Labeling reduced routes as full ABCD.** A_ONLY_CORE2_FUSION_TEST / D-Lite / bootstrap / restricted / simplified must be labeled honestly. Never call them "full UltraFusion" or "full ABCD".
9. **Cutting layers for speed while claiming full fusion.** If you need speed, use layer-internal parallelism, better routing, or bootstrap mode. Do not remove B/C/D and still claim full ABCD.
10. **Using stale frontier-model claims.** Fable 5 / Mythos 5 and similar claims about model availability, capability, or export-control status must be re-checked against primary sources before reuse. See `65-RULE-PATCHES/`.
