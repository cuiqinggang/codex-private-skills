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


## Search Gate 检查 (v1.1)

每个 assembled prompt 必须额外检查 Search Gate 是否存在：

```
A_prompt_assembled: SEARCH_GATE_PRESENT = ✓/✗
B_prompt_assembled: SEARCH_GATE_PRESENT = ✓/✗
C_prompt_assembled: SEARCH_GATE_PRESENT = ✓/✗
D_prompt_assembled: SEARCH_GATE_PRESENT = ✓/✗
```

### Search Gate 缺失处理

如果 Search Gate 缺失：
```
UF_PROMPT_ASSEMBLY_WARNING: SEARCH_GATE_MISSING
```

Search Gate 缺失**不等于 V15_FULL 缺失**，不直接使该层无效。
但如果问题涉及当前状态、未知实体或高风险易变事实，而 Search Gate 缺失，
则该轮 D_Final 必须标注"搜索规则缺失，事实核查受限"。

## 验收清单

- [ ] A 层 V15 已注入
- [ ] B 层 V15 已注入
- [ ] C 层 V15 已注入
- [ ] D 层 V15 已注入
- [ ] 所有 SHA256 已记录
- [ ] 所有 PROMPT_ASSEMBLY_STATUS = PASS
- [ ] 无 UF_PROMPT_ASSEMBLY_FAIL
- [ ] Search Gate 已检查（不影响层有效性，仅影响标注）


## V15 版本信息（Gate Review 修复后）

| 文件 | SHA256 (前16位) | 大小 |
|------|----------------|------|
| V15_Guard_Prefix_v1.0.md | d89de551c375c1d5 | 2361 B |
| V15_FULL_v1.0.md | 42f23cde89dee3fa | 10917 B |
| V15_FULL_WITH_GUARD_v1.0.md | bb836ac959885190 | 13292 B |

V15_FULL_IS_COMPLETE: **true**

## V7.0 Canonical V15 Source Lock

UltraFusion V7.0 full ABCD packages must use the canonical full-text source:

```text
10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
```

Canonical SHA256:

```text
BB836AC959885190A1BEC81ECA77454F0CD183D08BB3814070A977C39147514E
```

The user-supplied recovery attachment from 2026-07-05 matches this file after trimming trailing whitespace. It is accepted as the current full V15 body unless a more complete version is later found and recorded.

Additional failure codes:

```text
UF_PROMPT_ASSEMBLY_FAIL: V15_CANONICAL_SOURCE_NOT_USED
UF_PROMPT_ASSEMBLY_FAIL: V15_PLACEHOLDER_NOT_REPLACED
UF_PROMPT_ASSEMBLY_FAIL: C_LAYER_OFFICIAL_PROMPT_MISSING
UF_PROMPT_ASSEMBLY_FAIL: C_LAYER_SIMPLIFIED_PROMPT_USED
UF_PROMPT_ASSEMBLY_FAIL: C_FUSION_OUTPUT_SCHEMA_MISSING
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_EXECUTION_COMMAND_MISSING
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_V15_FULL_MISSING
UF_PROMPT_ASSEMBLY_FAIL: D_LAYER_OFFICIAL_PROMPT_MISSING
```

Do not pass an A/B/C/D package if V15 is summarized, abbreviated, rewritten, or left as `<<<V15_FULL>>>`.
V15_FULL 来源: 从 V15_FULL_WITH_GUARD_v1.0.md (332行) 提取第39行起完整原文，未改写。

## V7.0 C Layer Official Prompt Gate

C-layer packages must load the official prompt source:

```text
30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md
```

Required signals:

- `复检陌生稿规则`
- `四维稠密融合`
- evidence / data hard rules
- reverse consistency checking
- `【最终答案：C_Fusion】`
- `【评审报告】`
- `【版本说明】`

If any signal is missing, the C layer package is invalid and must not enter D layer.

## V7.0 D Layer Execution Command Gate

D-layer packages must place the execution wrapper immediately after `[COPY_START]`:

```text
30-TEMPLATES/D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md
```

Required first-message signal:

```text
【D层执行命令：FINAL_ANSWER FIRST】
```

If a D package begins with broad protocol text and does not foreground final-answer-first output, the package is invalid because external models may produce only a benchmark/meta-evaluation report.

The wrapper must require output order:

```text
# 1. Ultra_Answer_Final
# 2. D层验收附录
```

Scoring and Gain must appear after, not before, the final answer.

The execution wrapper is necessary but not sufficient. A valid D-layer package must also include the full canonical V15 body and the official D prompt source:

```text
10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
30-TEMPLATES/40_D_Layer_Final_Extreme_Report_Template_v3.0.md
```

Required D package signals:

- `【D层执行命令：FINAL_ANSWER FIRST】`
- `V15+G 前置约束层`
- `Auto-V15`
- `V15 瀑布式`
- `本阶段（D 层）核心定位与约束`
- `Ultra_Answer_Final`
- original question Q
- `A_Initial / Score_0`
- `C_Fusion`

If the D package includes the wrapper but omits V15 or the official D prompt, invalidate and regenerate the entire D package. Do not send a wrapper-only D package to an external model.
