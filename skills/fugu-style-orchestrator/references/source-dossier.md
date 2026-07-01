# 来源档案与说法分级

## 1. 查证时间

本档案根据 2026-06-24 的公开网页检索整理。以后使用前应重新搜索价格、模型 ID、可用地区、benchmark 更新。

## 2. 高可信来源

| 来源 | 用途 | URL |
|---|---|---|
| Sakana Fugu official page | Fugu/Fugu Ultra 定位、benchmark 表、价格、FAQ | https://sakana.ai/fugu/ |
| Sakana Fugu release blog | 官方发布说明、方法介绍、用户案例 | https://sakana.ai/fugu-release/ |
| Sakana Fugu Technical Report | 技术报告、orchestrator 方法、benchmark 声明 | https://arxiv.org/abs/2606.21228 |
| Anthropic Fable/Mythos announcement | Fable/Mythos 定位、价格、官方能力说明 | https://www.anthropic.com/news/claude-fable-5-mythos-5 |
| Anthropic suspension statement | 美国政府要求暂停访问的官方声明 | https://www.anthropic.com/news/fable-mythos-access |
| Kimi API Platform | Kimi K2.6/K2.7 定位、价格、工具生态 | https://platform.kimi.ai/ |
| OpenRouter Sakana page | Fugu Ultra 是否在 OpenRouter 出现、模型 ID 和价格参考 | https://openrouter.ai/sakana |
| Requesty Fugu Ultra page | 第三方路由可用性、价格、上下文参考 | https://www.requesty.ai/models/sakana/fugu-ultra |

## 3. 中等可信来源

这些来源适合了解外部解读，但不能单独作为 benchmark 结论：

| 来源 | 作用 |
|---|---|
| DataCamp / NDTV / 36Kr / Times of India | 多为转述官方发布和表格 |
| Kingy AI 分析文 | 对“是否真的打败 Fable/Mythos”有较谨慎拆解 |
| Reddit / Hacker News | 适合看用户质疑和早期体验，不能当最终证据 |

## 4. 说法分级

| 说法 | 状态 | 说明 |
|---|---|---|
| Fugu 是多智能体调度系统，以单一 API 暴露 | 支持 | 官方和技术报告一致 |
| Fugu Ultra 价格为 $5 input / $30 output per 1M | 支持 | 官方与 Requesty/OpenRouter信息一致，但应复查 |
| Fable/Mythos 价格为 $10 input / $50 output per 1M | 支持 | Anthropic 官方发布 |
| 美国政府要求暂停 Fable/Mythos 外国国民访问 | 支持 | Anthropic 官方声明 |
| Fugu Ultra 在部分 benchmark 超过公开前沿模型 | 支持但主要为官方报告 | 需要独立复测 |
| Fugu Ultra 全面打败 Fable 5 | 未充分证明 | 部分 benchmark 可说强或接近 |
| Fugu Ultra 全面打败 Mythos 5 | 不支持 | 很多比较是 Mythos Preview，不是完整 Mythos 5 |
| Fugu Ultra 可替代所有高端模型 | 不支持 | 真实企业替代还缺独立案例和失败分析 |

## 5. 使用时的措辞规则

允许说：

```text
Fugu Ultra 在 Sakana 官方公布的一组工程、科学和推理 benchmark 上表现很强，
部分指标超过公开前沿模型，并被官方称为接近 Fable 5 / Mythos Preview。
```

谨慎说：

```text
Fugu Ultra 可能是 Fable/Mythos 受限后的高端替代候选。
```

不要直接说：

```text
Fugu Ultra 全面打败 Mythos 5。
Fugu Ultra 已被独立证明超过所有 Claude 五代模型。
```

## 6. 需要未来补证的项目

1. Fugu Ultra 在真实 Codex/Kilo 长任务中的独立复测。
2. 与 Kimi K2.7 Code、DeepSeek V4 Pro、GLM-5.2 的同题对照。
3. 价格是否随上下文、缓存、路由商加价变化。
4. 国内网络和支付可用性。
5. OpenRouter/Requesty/Sakana 官方 API 的稳定性。
6. Fugu 是否允许排除特定海外底层模型，Fugu Ultra 当前固定池的合规影响。
