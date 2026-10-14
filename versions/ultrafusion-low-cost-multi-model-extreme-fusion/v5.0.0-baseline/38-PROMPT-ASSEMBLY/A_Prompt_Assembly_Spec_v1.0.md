# A 层提示词拼装规范 v1.0

## 拼装公式

```
A_prompt =
  [V15_Guard_Prefix]
  + [V15_FULL]
  + [A_Layer_Template]
  + [用户原始问题]
  + [输出格式约束]
```

## 拼装参数

| 参数 | 来源 | 必填 |
|------|------|------|
| V15_Guard_Prefix | 10-SPEC/V15_Guard_Prefix_v1.0.md | ✓ |
| V15_FULL | 10-SPEC/V15_FULL_v1.0.md | ✓ |
| A_Template | 30-TEMPLATES/ | ✓ |
| Input Materials | 上一层输出 | ✓ |
| User Question | 用户原始输入 | ✓ |
| Output Format | 按模板要求 | ✓ |


## 输出

A_<model>_Extreme.md
