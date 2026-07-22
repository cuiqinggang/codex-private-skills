# UltraFusion 模型阵容 vNext-2026-07-01-night

## vNext 正式核心三智能体

| Slot | Model / Route | Status | Role | A | B | C | D |
|------|---------------|--------|------|---|---|---|---|
| M0 | GPT 官网版 / official subscription automation | **CORE** | 总控、最终融合、最高质量判断、最终表达、最终验收 | ✓ | ✓ | ✓ | ✓ |
| M1 | Kimi 官网会员版 / Agent Swarm / Deep Research | **CORE** | 复杂任务位、多智能体分群、多角色审查、大规模资料探索、复杂方案分支推演 | ✓ | ✓ | ✓ | ✓ |
| M2 | GLM-5.2 / GLM Coding Plan via Kilo or Claude Code | **CORE** | Coding Agent、技能包制作、PPT/文档结构化、长程任务执行、工程化落地 | ✓ | ✓ | ✓ | ✓ |

## vNext 备用模型池

| Model | Status | Role | Activation |
|-------|--------|------|------------|
| Qwen / 通义千问 | **BACKUP** | 低成本综合联网、文档、多模态、普通分析备用 | Kimi 测试增益不足时可替代 Kimi 进入核心 |
| DeepSeek | **BACKUP** | 免费测试、纯推理、低成本反向审稿 | 不再作为正式核心；只在测试或备用流程中启用 |
| MiniMax | **BACKUP** | 音视频、创意、多模态备用 | 不进入核心回答链 |

## DeepSeek 降级说明

DeepSeek 不再作为正式核心。原因是快速模式能联网但深度不足，
专家/深度思考模式推理强但不能联网。极限任务必须拆成“快速联网
搜索 + 专家深思”两道流程，正式长期使用太麻烦。

## GLM-5.2 接入路线

主路线：

```text
Kilo / Claude Code -> GLM Coding Plan -> GLM-5.2
```

Codex 不优先直连 GLM-5.2。只有找到公开成熟成功案例、完整教程和
可复制配置时才尝试。否则由 Kilo / Claude Code 执行，Codex 通过
复制粘贴、剪贴板、文件交接或坐标法取回结果。

---

## v5.0 历史基线


## Core-2 Bootstrap Mode（最小可运行模式）

| Slot | Model | Provider | Status | Role | A | B | C | D |
|------|-------|----------|--------|------|---|---|---|---|
| M0 | GPT-latest via official subscription automation | OpenAI Official Subscription | **ACTIVE** | 质量锚点 | ✓ | ✓ | ✓ | ✓ |
| M1 | DeepSeek-V4-Pro | DeepSeek Official API | **ACTIVE** | 主力推理 | ✓ | ✓ | ✓ | ✓ |

**说明：**
- 这是当前最小可运行模式，用于先验证 A/B/C/D 自动化链路。
- 不强制凑满 3 个或 4 个模型。
- 不得为了凑模型数量使用低质量模型。
- D_Final 必须标注"Core-2 双模型融合"。
- MiniMax-M2.7 接入后自动升级为 Core-3 Default Mode。

## 默认生产阵容 (Core-3)

| Slot | Model | Provider | Status | Role | A | B | C | D |
|------|-------|----------|--------|------|---|---|---|---|
| M0 | GPT-latest via GPT official subscription automation | OpenAI Official Subscription | **ACTIVE** | 质量锚点 | ✓ | ✓ | ✓ | ✓ |
| M1 | DeepSeek-V4-Pro | DeepSeek Official API | **ACTIVE** | 主力推理 | ✓ | ✓ | ✓ | ✓ |
| M2 | MiniMax-M2.7 | MiniMax Official API | **ACTIVE** | 多样性/交叉 | ✓ | ✓ | ✓ | ✓ |

## 观察位

| Slot | Model | Provider | Status | Role |
|------|-------|----------|--------|------|
| M3-Q | Qwen3.5-Flash | Qwen Official API | **OBSERVE** | 消融测试位 |

## 备用模型池

| Model | Provider | Priority | Conditions to activate |
|-------|----------|----------|----------------------|
| Kimi K2 | Moonshot API | HIGH | When DeepSeek unavailable |
| Gemini 2.5 Pro | Google AI | MEDIUM | Complex reasoning |
| GLM-4.5 | 智谱API | MEDIUM | Chinese-centric tasks |
| ERNIE 4.0 | 百度API | LOW | Legacy compatibility |
| Pangu 5.0 | 华为API | LOW | Enterprise tasks |

## Qwen 激活条件

Qwen3.5-Flash stays in OBSERVE until:
1. Passes 6-question ablation test
2. Proves ≥2 independent unique contributions
3. Average D_Final score lift ≥1.5 points
4. No significant noise increase in C layer
