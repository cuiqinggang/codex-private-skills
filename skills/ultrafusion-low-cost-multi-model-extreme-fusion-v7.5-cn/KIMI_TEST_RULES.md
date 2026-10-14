# Kimi Test Rules

## Goal

验证 Kimi 是否在复杂极限任务中带来 `>= 8` 分的平均质量提升。

## Applicable Tasks

- 复杂方案设计
- 技能包设计
- 多角色审查
- 大规模资料探索
- 多路线并行推演
- 复杂商业/产品/技术判断

## Non-Applicable Tasks

- 简单问答
- 普通总结
- 普通翻译
- 普通资料整理

## Test Design

Run paired comparisons:

- A version: `GPT + GLM-5.2`
- Alternative A version: `GPT + Qwen + GLM-5.2`
- B version: `GPT + Kimi + GLM-5.2`

Use complex tasks only. Do not use simple tasks to decide Kimi's value.

## Scoring

- 正确性: 25
- 深度: 20
- 覆盖完整度: 20
- 关键遗漏发现: 15
- 多样性/新角度: 10
- 可执行性: 10

Total: 100

## Decision

- `>= 8` point average lift: Kimi fixed into extreme mode.
- `4-7` point average lift: enable Kimi for specific complex tasks.
- `< 4` point average lift: do not fix Kimi into the route; fall back to Qwen.
