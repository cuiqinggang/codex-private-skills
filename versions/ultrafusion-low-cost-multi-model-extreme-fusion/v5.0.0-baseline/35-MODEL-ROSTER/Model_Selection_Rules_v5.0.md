# 模型选择规则 v5.0

## Core-3 固定规则

Core-3 是 UltraFusion 的固定生产阵容：
- GPT, DeepSeek, MiniMax 在每一轮都参与
- 不存在"选哪个、不选哪个"——三个都跑
- 仅当某模型不可用时触发替补逻辑

## 替补触发条件

当主力模型出现以下状态时触发替补：
- ERROR：接口返回错误
- RATE_LIMITED：限流
- AUTH_FAILED：鉴权失败
- EMPTY：连续2次返回空

## 替补优先级

1. Kimi K2 → 首位替补
2. Gemini 2.5 Pro → 复杂推理替补
3. GLM-4.5 → 中文任务替补
4. 若前3均不可用 → D_Final 标注"受限融合"

## 自动禁用规则

以下情况自动禁用某模型本轮：
- 连续3次返回 EMPTY
- 连续2次返回 REFUSED
- AUTH_FAILED（立即禁用）
- 输出安全过滤（立即禁用）
