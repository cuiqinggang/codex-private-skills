# UltraFusion 模型阵容 v5.0


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
