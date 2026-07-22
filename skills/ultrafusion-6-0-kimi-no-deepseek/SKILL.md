---
name: ultrafusion-6-0-kimi-no-deepseek
description: "Alias skill for UltraFusion 6.0 / 大模型变动: the v5.0 UltraFusion route upgraded from DeepSeek-core to Kimi-core. Use when the user says 6.0, 大模型变动, Kimi替代DeepSeek, 去DeepSeek, or 多智能体极限低成本回答6.0."
---

# UltraFusion 6.0 / 大模型变动

This is a memory-friendly alias for the canonical skill:

${REDACTED_SECRET}

## What 6.0 Means

6.0 means the model-route change that follows the old 5.0 baseline:

- Keep the original UltraFusion low-cost multi-model extreme-answer skill.
- Remove DeepSeek from the official core route.
- Promote Kimi to the official complex-task / deep-research / multi-agent review role.
- Keep GPT as the quality anchor.
- Keep GLM-5.2 / GLM Coding Plan as the coding, document, and long-running execution route.
- Leave DeepSeek only as backup, test, pure-reasoning, or reverse-review support.

## Required Behavior

When this alias is triggered, immediately load and follow the canonical
`ultrafusion-low-cost-multi-model-extreme-fusion` skill. Treat this alias as a
name and routing patch, not as a separate implementation.

If the user says any of these, use this alias:

- `6.0`
- `大模型变动`
- `多智能体极限低成本回答6.0`
- `Kimi替代DeepSeek`
- `去DeepSeek`
- `DeepSeek变Kimi`

## Official 6.0 Core Route

```text
GPT official site + Kimi official membership + GLM-5.2 / GLM Coding Plan
```

## Historical Mapping

- v5.0 baseline: GPT + DeepSeek-V4-Pro + MiniMax, with Qwen as observation/ablation.
- v6.0 alias: GPT + Kimi + GLM-5.2, with Qwen / DeepSeek / MiniMax as backups.
