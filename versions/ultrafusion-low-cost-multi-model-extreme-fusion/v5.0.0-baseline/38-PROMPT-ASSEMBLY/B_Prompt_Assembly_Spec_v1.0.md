# B 层提示词拼装规范 v1.0

## 拼装公式

```
B_prompt =
  [V15_Guard_Prefix]
  + [V15_FULL]
  + [B_Layer_Template]
  + [用户原始问题 + 所有有效 A 层极限稿]
  + [输出格式约束]
```

## 拼装参数

| 参数 | 来源 | 必填 |
|------|------|------|
| V15_Guard_Prefix | 10-SPEC/V15_Guard_Prefix_v1.0.md | ✓ |
| V15_FULL | 10-SPEC/V15_FULL_v1.0.md | ✓ |
| B_Template | 30-TEMPLATES/ | ✓ |
| Input Materials | 上一层输出 | ✓ |
| User Question | 用户原始输入 | ✓ |
| Output Format | 按模板要求 | ✓ |


## 输出

B_<model>_Extreme.md

## 2026-06-28 B Layer Runtime Rule

B is one layer.

Temperature:

- Default: 0.60
- Range: 0.50-0.65

B prompt input must include:

- V15 guard and full V15;
- B layer template;
- original user question;
- all valid A-layer extreme drafts.

Each participating model reads all A drafts and directly generates its own `B_<model>_Extreme` draft.

Do not split B into sublayers or two-step variants unless the user explicitly requests a separate experiment.

Record max_tokens telemetry for B; do not hardcode final token limits yet.
