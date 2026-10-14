# D 层提示词拼装规范 v1.0

## 拼装公式

```
D_prompt =
  [V15_Guard_Prefix]
  + [V15_FULL]
  + [D_Layer_Template]
  + [用户原始问题 + C_Fusion_Extreme + 可选 A_Initial/早期答案]
  + [输出格式约束]
```

## 拼装参数

| 参数 | 来源 | 必填 |
|------|------|------|
| V15_Guard_Prefix | 10-SPEC/V15_Guard_Prefix_v1.0.md | ✓ |
| V15_FULL | 10-SPEC/V15_FULL_v1.0.md | ✓ |
| D_Template | 30-TEMPLATES/ | ✓ |
| Input Materials | 上一层输出 | ✓ |
| User Question | 用户原始输入 | ✓ |
| Output Format | 按模板要求 | ✓ |


### 重要声明
D_Final 是最终稳定极限稿，不是普通审核报告。
如果 D 层未注入 V15_FULL，则 D_Final 无效。
D 层最终输出中不得复贴 V15 原文，但 D 层输入 prompt 必须包含 V15。

## 输出

D_Final_Ultra_Answer_Final.md
