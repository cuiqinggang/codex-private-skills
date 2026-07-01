# UltraFusion 变更日志

## vNext-2026-07-01-night (2026-07-02) — 模型路线重大调整

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

## v5.0.0 (2026-06-16) — Hermes 技能包正式版

### 新增
- 完整 HMES 技能包结构（SKILL.md）
- V15 拆分为 Guard_Prefix + FULL 独立文件
- Prompt Assembly 完整 6 文件（总规则 + V15 硬门 + A/B/C/D 拼装规范）
- V15 注入验收门（V15_Injection_Hard_Gate）
- Qwen 消融测试规则与工作流
- 扣分原则 + 模型贡献度评分
- GPT 官网套餐自动化接入规范
- 国内模型官方 API 适配器规范
- 服务化路线图
- 模型失败空过规则体系

### 废弃
- 手工粘贴 A/B/C/D 的旧流程（归档到 90-ARCHIVE）
- E 层（不再存在——D_Final 即最终报告）
- 旧版 RUNBOOK v1.1（归档）

### 核心变更
- C 层：从普通融合升级为 V15 驱动极限融合
- D 层：从审核升级为 V15 驱动最终稳定极限稿
- A/B/C/D 四层全部强制注入 V15
- GPT 默认通过官网套餐接入（不默认 API）
- Qwen 降为观察位，需通过消融测试
