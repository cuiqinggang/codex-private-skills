# UltraFusion Changelog

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
