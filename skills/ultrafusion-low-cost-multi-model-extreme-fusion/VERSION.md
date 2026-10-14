# UltraFusion Version

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
