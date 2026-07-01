# 路由层模板 v1.0

## Prompt

```
你是一个任务路由器。

分析以下问题，输出：
1. 复杂度: SIMPLE / MEDIUM / COMPLEX / EXPERT
2. 风险等级: LOW / MEDIUM / HIGH
3. 推荐工作流: FULL / D-LITE
4. 推荐模型组合: Core-3 / Core-3+Kimi / D-Lite-GPT
5. 需要激活的替补: [NONE / Kimi / Gemini / GLM]

问题: {user_question}
```

## 2026-06-28 Router Runtime Rule

Current default for actual UltraFusion testing:

- Recommend `FULL_ABCD_TEST` unless the user explicitly asks for a reduced route.
- `A_ONLY_CORE2_FUSION_TEST` is paused as default.
- Runtime temperature profile: `ABCD_TEMP_v1`.
- max_tokens policy: `RECORD_ONLY_UNTIL_CALIBRATED`.
- B is one layer; do not split it into sublayers or two-step variants.

ABCD_TEMP_v1 defaults:

| Stage | Temperature |
|---|---:|
| A | 0.70 |
| B | 0.60 |
| C | 0.35 |
| D | 0.20 |

Router output should include:

1. recommended workflow: `FULL_ABCD_TEST`
2. temperature profile: `ABCD_TEMP_v1`
3. max_tokens policy: `RECORD_ONLY_UNTIL_CALIBRATED`
