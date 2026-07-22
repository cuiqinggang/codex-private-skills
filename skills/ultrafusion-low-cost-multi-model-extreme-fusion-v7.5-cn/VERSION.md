# UltraFusion Version

## 6.0 Alias / 大模型变动

- Short memory name: `6.0 大模型变动`
${REDACTED_SECRET}
- Meaning: preserve the v5.0 lineage, remove DeepSeek from the official core route, and promote Kimi into the official complex-task route.

## vNext-2026-07-01-night

- 主题：核心模型路线重大调整
- 核心变化：DeepSeek 降级，Kimi 升级，GLM-5.2 走 Kilo/Claude Code 成熟路线
- 正式核心：GPT + Kimi + GLM-5.2
- 备用：Qwen、DeepSeek、MiniMax
- 基线版本：v5.0.0
- 基线 Git tag：`ultrafusion-v5.0.0-baseline`

## Version Rule

This version supersedes the v5.0.0 model route while preserving the v5.0.0
baseline as a frozen snapshot. Future updates should create a new named version
snapshot and keep tests, decisions, and acceptance evidence with that snapshot.

## UltraFusion V7.0 Semi-Automatic ABCD - 2026-07-05

- Route label: `UF_V7_SEMI_AUTO_ABCD`
- Purpose: Codex generates A/B/C/D question packages; the human only copies and pastes; external models answer; Codex fuses, converges, scores, and records gain.
- Required layers: `0 baseline -> A extreme generation -> B fusion enhancement -> C strategy integration -> D final convergence`.
- Required comparison: `Score_0`, `SCORE_FINAL`, `Gain = SCORE_FINAL - Score_0`.
- Invalid-link rule: `Gain < 2.0` means `INVALID_CHAIN`.
- V15 canonical source: `10-SPEC/V15_FULL_WITH_GUARD_v1.0.md`
- V15 canonical SHA256: `BB836AC959885190A1BEC81ECA77454F0CD183D08BB3814070A977C39147514E`
- V15 package rule: full canonical text must be injected; summaries/placeholders/wrong V15 versions invalidate the layer.
- C layer official prompt source: `30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md`
- C layer official prompt SHA256: `8095B50C31E8FB31B506BC53278BC053C439743E17ACA40F37FACDBC99085BA2`
- C layer package rule: simplified C prompts are invalid; required signals include `复检陌生稿规则`, `四维稠密融合`, and `【最终答案：C_Fusion】`.
- D layer execution wrapper source: `30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md`
- D layer package rule: first visible instruction must be `FINAL_ANSWER FIRST`; `Ultra_Answer_Final` must answer the original question Q before any scoring/Gain/risk appendix.
- D layer V15 rule: `FINAL_ANSWER FIRST` is only the wrapper; every valid D package must still include full canonical V15 and the official D prompt in the same copy block.
- D layer completeness rule: a valid-order D result still fails if `Ultra_Answer_Final` is a thin summary. Required artifacts include copyable prompt templates, run schema, privacy SOP, failure attribution, and decision thresholds.
- Current benchmark status note: `70-NOTES/BENCHMARK-STATUS-20260706-v7-full-pipeline-final-gate-open.md`; final gate remains open until an external D answer passes the production-depth checklist.
- Main files:
  - `10-SPEC/V15_CANONICAL_SOURCE.md`
  - `30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md`
  - `30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md`
  - `40-WORKFLOWS/Semi_Automatic_ABCD_CopyPaste_Workflow_v7.0.md`
  - `30-TEMPLATES/V7_Semi_Auto_Question_Package_Template.md`
  - `37-SCORING/V7_Baseline_Gain_Scoring_Rule.md`
  - `45-RUNTIME/V7_Semi_Auto_Run_State_Schema.md`
  - `65-RULE-PATCHES/RULE-PATCH-20260705-ultrafusion-v7-semi-auto-abcd.md`
  - `70-NOTES/FAILURE-REVIEW-ENTRY-v7-semi-auto-abcd.md`
