# UltraFusion Changelog

## UltraFusion V7.0 Semi-Automatic ABCD - 2026-07-05

- Added route label `UF_V7_SEMI_AUTO_ABCD`.
- Added semi-automatic copy-paste workflow where Codex generates question packages, the human copies and pastes, external models answer, and Codex performs fusion, convergence, scoring, and gain judgment.
- Added baseline and final gain scoring rule: `Gain = SCORE_FINAL - Score_0`; `Gain < 2.0` is `INVALID_CHAIN`.
- Added V7 question package template, run state schema, failure-review entry, and deployment report.
- Bound trigger phrases: `UltraFusion V7.0`, `半自动ABCD`, `ABCD问题包`, `复制粘贴多层推理`, `外部模型回答`, `Score_0 vs Score_FINAL`, `Gain < 2`.

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
