# C 层提示词拼装规范 v1.0

## 拼装公式

```
C_prompt =
  [V15_Guard_Prefix]
  + [V15_FULL]
  + [C_Layer_Template]
  + [用户原始问题 + 所有有效 B 层第二轮极限稿]
  + [输出格式约束]
```

## 拼装参数

| 参数 | 来源 | 必填 |
|------|------|------|
| V15_Guard_Prefix | 10-SPEC/V15_Guard_Prefix_v1.0.md | ✓ |
| V15_FULL | 10-SPEC/V15_FULL_v1.0.md | ✓ |
| C_Template | 30-TEMPLATES/ | ✓ |
| Input Materials | 上一层输出 | ✓ |
| User Question | 用户原始输入 | ✓ |
| Output Format | 按模板要求 | ✓ |


### 重要声明
C_Fusion 是融合极限稿，不是普通融合稿。
如果 C 层未注入 V15_FULL，则 C_Fusion 无效。

## 输出

C_Fusion_Extreme.md
