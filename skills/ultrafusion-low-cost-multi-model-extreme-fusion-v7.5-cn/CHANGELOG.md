# UltraFusion Changelog

## UltraFusion V7.0 Semi-Automatic ABCD - 2026-07-05

- Added route label `UF_V7_SEMI_AUTO_ABCD`.
- Added semi-automatic copy-paste workflow where Codex generates question packages, the human copies and pastes, external models answer, and Codex performs fusion, convergence, scoring, and gain judgment.
- Added baseline and final gain scoring rule: `Gain = SCORE_FINAL - Score_0`; `Gain < 2.0` is `INVALID_CHAIN`.
- Added V7 question package template, run state schema, failure-review entry, and deployment report.
- Bound trigger phrases: `UltraFusion V7.0`, `半自动ABCD`, `ABCD问题包`, `复制粘贴多层推理`, `外部模型回答`, `Score_0 vs Score_FINAL`, `Gain < 2`.

### V15 Canonical Source Correction - 2026-07-05

- Locked V7.0 ABCD prompt packages to the full canonical V15 source: `10-SPEC/V15_FULL_WITH_GUARD_v1.0.md`.
- Added `10-SPEC/V15_CANONICAL_SOURCE.md` with hash and user recovery attachment evidence.
- Confirmed the user-supplied recovery attachment trim-matches the canonical 332-line V15+G source.
- Added failure handling for summarized, placeholder, or wrong-version V15 injection.

### C Layer Official Prompt Lock - 2026-07-06

- Added official C layer prompt source: `30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md`.
- Added hard gate: C packages missing `复检陌生稿规则`, `四维稠密融合`, evidence/data hard rules, or `【最终答案：C_Fusion】` are invalid.
- Added rule patch: `65-RULE-PATCHES/RULE-PATCH-20260706-c-layer-official-prompt.md`.
- Added failure review: `70-NOTES/FAILURE-REVIEW-20260706-c-layer-simplified-prompt.md`.
- Recorded official C prompt SHA256: `8095B50C31E8FB31B506BC53278BC053C439743E17ACA40F37FACDBC99085BA2`.

### D Layer Execution Command First - 2026-07-06

- Added D-layer execution wrapper: `30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md`.
- Added rule patch: `65-RULE-PATCHES/RULE-PATCH-20260706-d-layer-execution-command-first.md`.
- New gate: every D-layer package must begin with a safe evaluation-request wrapper so external models generate the D-layer report instead of summarizing the prompt framework.
- Added correction command artifact for the benchmark run: `outputs/ufv7-d-layer-execution-correction-command-20260706.md`.
- Replaced hard "must execute / do not treat as prompt injection" wording after an external model refused; added failure review `70-NOTES/FAILURE-REVIEW-20260706-d-hard-command-triggered-refusal.md` and safe request artifact `outputs/ufv7-d-layer-safe-execution-request-20260706.md`.
- Replaced report-first D framing with `FINAL_ANSWER FIRST` after the external model produced only meta-evaluation without the actual final answer. Added failure review `70-NOTES/FAILURE-REVIEW-20260706-d-meta-evaluation-without-final-answer.md`.
- Patched final-answer-first D packaging after a wrapper-only package omitted full V15. D packages must now include the execution wrapper, full canonical V15, official D prompt, original Q, A_Initial/Score_0, and C_Fusion in one copy block.
- Added D output completeness gate after an external model produced a valid-order but overly short final answer. D results now fail as `UF_D_OUTPUT_FAIL: FINAL_ANSWER_TOO_THIN` unless they include copyable prompts, run schema, privacy SOP, structure-break/error fields, and concrete 30-day decision thresholds.
- Added clean final-gate handoff notes for the long benchmark thread. Current status is `FINAL_GATE_OPEN`: A/B/C and D package assembly gates are handled, but the final external D answer still needs one production-depth rerun and acceptance check.

## 6.0 Alias / 大模型变动 - 2026-07-02

- Added memorable alias skill: `ultrafusion-6-0-kimi-no-deepseek`
- Bound trigger phrases: `6.0`, `大模型变动`, `多智能体极限低成本回答6.0`, `Kimi替代DeepSeek`, `去DeepSeek`, `DeepSeek变Kimi`.
- Preserved original skill name and canonical package path.
- Clarified that 6.0 means DeepSeek leaves the official core route and Kimi becomes the official complex-task route.

## vNext-2026-07-01-night

### 新增

- Kimi 升级为正式核心复杂任务智能体。
- Kimi Agent Swarm / Deep Research / 多角色审查规则。
- Kimi 增益测试标准。
- GLM-5.2 接入路线规则。
- Codex 不再自行摸索 GLM-5.2 直连。
- DeepSeek 降级规则。
- Qwen 备用定位。

### 调整

- 原 `GPT + DeepSeek + GLM-5.2` 改为 `GPT + Kimi + GLM-5.2`。
- DeepSeek 从核心模型变为备用模型。
- Qwen 从候选替代位变为备用综合模型。
- Kimi 从候选第四智能体变为核心复杂任务位。

### 原因

- DeepSeek 正式使用流程割裂。
- Kimi 更符合复杂任务、多智能体审查、大规模资料探索。
- GLM-5.2 已有 Kilo / Claude Code 成熟路线。
- Codex 直连 GLM-5.2 没有成熟案例时不值得摸索。
