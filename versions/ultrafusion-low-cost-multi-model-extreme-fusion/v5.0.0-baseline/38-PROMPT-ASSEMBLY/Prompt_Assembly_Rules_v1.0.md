# UltraFusion 提示词拼装总规则 v1.0

## 核心原则

UltraFusion 的正式执行不是用户手工粘贴提示词。
**所有 prompt 必须由自动化执行器拼装。**

## 每层 prompt 都必须包含

1. **V15_Guard_Prefix** — 前置约束层
2. **V15_FULL** — 完整 V15 规范
3. **当前层专用模板** — A/B/C/D Template
4. **当前层输入材料** — 上一层输出
5. **用户原始问题** — 保持原样
6. **输出格式约束** — 按层要求

## 拼装顺序

```
Layer_prompt =
  [V15_Guard_Prefix]
  + [V15_FULL]
  + [Layer_Template]
  + [Input_Materials]
  + [User_Original_Question]
  + [Output_Format_Constraint]
```

## 严禁事项

- 严禁跳过 V15_Guard_Prefix
- 严禁替换/改写/摘要 V15_FULL（必须原文注入）
- 严禁让用户手工拼装
- 严禁在 V15 注入前组装 prompt

## 2026-06-28 Runtime Parameters Are Separate From V15

Temperature and `max_tokens` are runtime parameters. They must not be inserted by editing, shortening, or rewriting V15 source text.

Use:

`45-RUNTIME/ABCD_Temperature_And_Token_Strategy_v1.0.md`

Default temperature profile:

- A: 0.70
- B: 0.60
- C: 0.35
- D: 0.20

B is one layer. It reads all valid A extreme drafts and directly produces B-layer extreme drafts.

`max_tokens` is currently record-only: store configured value, actual output length, truncation status, verbosity, and V15 impact. Do not hardcode final values until full-flow tests provide evidence.
