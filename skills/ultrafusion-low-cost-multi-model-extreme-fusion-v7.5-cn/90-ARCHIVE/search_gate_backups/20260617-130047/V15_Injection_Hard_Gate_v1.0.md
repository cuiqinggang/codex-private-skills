# V15 注入验收门 v1.0

## 验收要求

每一次正式运行，都必须保存 assembled prompt 或 prompt manifest。

## 逐层检查

```
A_prompt_assembled: V15_PRESENT = ✓/✗
B_prompt_assembled: V15_PRESENT = ✓/✗
C_prompt_assembled: V15_PRESENT = ✓/✗
D_prompt_assembled: V15_PRESENT = ✓/✗
```

## 记录内容

每个 assembled prompt 必须记录：
- V15_SHA256：V15 原文的哈希
- V15_GUARD_PRESENT：是否为 true
- LAYER_TEMPLATE_PRESENT：是否为 true
- INPUT_ARTIFACTS_PRESENT：是否为 true
- PROMPT_ASSEMBLY_STATUS：PASS/FAIL

## 失败处理

如果任一层缺失 V15：
```
UF_PROMPT_ASSEMBLY_FAIL: V15_FULL_MISSING
```
该层输出不得进入下一层。
必须重新拼装，补入 V15，重新执行该层。

## 验收清单

- [ ] A 层 V15 已注入
- [ ] B 层 V15 已注入
- [ ] C 层 V15 已注入
- [ ] D 层 V15 已注入
- [ ] 所有 SHA256 已记录
- [ ] 所有 PROMPT_ASSEMBLY_STATUS = PASS
- [ ] 无 UF_PROMPT_ASSEMBLY_FAIL


## V15 版本信息（Gate Review 修复后）

| 文件 | SHA256 (前16位) | 大小 |
|------|----------------|------|
| V15_Guard_Prefix_v1.0.md | d89de551c375c1d5 | 2361 B |
| V15_FULL_v1.0.md | 42f23cde89dee3fa | 10917 B |
| V15_FULL_WITH_GUARD_v1.0.md | bb836ac959885190 | 13292 B |

V15_FULL_IS_COMPLETE: **true**
V15_FULL 来源: 从 V15_FULL_WITH_GUARD_v1.0.md (332行) 提取第39行起完整原文，未改写。
