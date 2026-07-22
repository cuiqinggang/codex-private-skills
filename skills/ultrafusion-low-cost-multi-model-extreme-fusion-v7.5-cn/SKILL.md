---
name: ultrafusion-low-cost-multi-model-extreme-fusion-v7.5-cn
description: "当用户要求 UltraFusion V7.5 中文审校版、V7.0 半自动 ABCD 中文等价复刻、中文审校 V15/Score_0/SCORE_FINAL/Gain/失败复盘，或需要用户可逐条审校的 UltraFusion V7.0 中文说明时使用。本技能包保留 V7.0 低成本多模型极限融合与 UF_V7_SEMI_AUTO_ABCD 流程，不替代 V8.0/V8.2。"
version: UltraFusion-7.5-cn-review-abcd-2026-07-06
author: UltraFusion System / Codex 中文审校封装
license: MIT
metadata:
  aliases:
    - UltraFusion V7.5
    - V7.5 中文审校版
    - 中文等价复刻
    - V7.0 中文化
    - UF_V7_5_CN_REVIEW
    - UF_V7_SEMI_AUTO_ABCD
    - 半自动ABCD中文审校
    - Score_0 vs SCORE_FINAL
    - Gain 验收
  status: REVIEW_READY_CN
${REDACTED_SECRET}
  source_version: UltraFusion-7.0-semi-auto-abcd-2026-07-05
---

# UltraFusion V7.5 中文审校版技能包

## 1. 技能包名称

本技能包名称为 **UltraFusion V7.5 中文审校版**。

英文稳定标识：

```text
UltraFusion-7.5-cn-review-abcd-2026-07-06
```

内部路线标签保留：

```text
UF_V7_SEMI_AUTO_ABCD
```

中文解释：这是 V7.0 半自动 ABCD 路线的中文审校版，不是 V8 风格重构。

## 2. V7.5 中文审校版定位

V7.5 的目标是 **中文等价复刻**，不是升级、重构或简化。

它完整保留 V7.0 的核心机制：

- ABCD 半自动复制粘贴流程；
- 低成本多模型极限融合思想；
- V15 全量注入门禁；
- `Score_0`、`SCORE_FINAL`、`Gain` 评分链；
- `Gain < 2.0 -> INVALID_CHAIN` 的诚实失败判定；
- 失败复盘、运行记录和复制边界。

V7.5 只改变说明层：把用户需要阅读、审校、理解的说明性内容改成中文，并为必须保留的英文协议字段补中文解释。

## 3. 适用场景

使用本技能包的场景：

- 用户明确说 `UltraFusion V7.5`、`V7.5 中文审校版`、`V7.0 中文化`、`中文等价复刻`；
- 用户要逐条审校 V7.0 的 ABCD、V15、Gain、失败复盘；
- 用户要让非英文读者看懂 UltraFusion V7.0 的核心文件；
- 用户要对比原始中文思想与 V7.0 英文说明之间是否有偏差；
- 用户要生成可复制到 GPT / DeepSeek / Qwen 的半自动 ABCD 问题包，并保留中文解释。

## 4. 不适用场景

不要在以下场景使用本技能包：

- 简单问答，普通 GPT 直答已经足够；
- 用户要求 V8.0 / V8.2 极简压力链；
- 用户要求删除 V15、缩短为提示词摘要、或弱化门禁；
- 用户只是想快速得到一个无审计链路的答案；
- 外部模型不可用且用户不愿执行复制粘贴时。

## 5. 触发词

触发词包括：

```text
UltraFusion V7.5
V7.5 中文审校版
V7.0 中文化
中文等价复刻
半自动ABCD中文审校
UF_V7_5_CN_REVIEW
UF_V7_SEMI_AUTO_ABCD
ABCD问题包
复制粘贴多层推理
Score_0 vs SCORE_FINAL
Gain 验收
```

## 6. 普通问题低成本直答规则

普通问题默认不进入 ABCD。

如果 GPT / ChatGPT 直接回答已经足够清楚、可靠、低风险，就直接回答，不调用 DeepSeek / Qwen，不装配 V15，不跑 A/B/C/D。

中文解释：UltraFusion 是质量升级链路，不是所有问题都要套复杂流程。复杂流程必须带来真实收益，否则属于成本浪费。

## 7. 高价值问题 ABCD 升级规则

当问题满足以下任一条件时，可以升级到 V7.5 / V7.0 半自动 ABCD：

- 答错代价高；
- 单模型容易漏角度；
- 需要多视角事实校验；
- 需要审计过程；
- 用户明确要求极限答案；
- 用户要求生成外部模型复制粘贴问题包。

升级前必须先生成普通答案并给出：

```text
Score_0:
```

中文解释：`Score_0` 是普通答案初始评分，用来判断 ABCD 是否真的提升了质量。

## 8. GPT / DeepSeek / Qwen 半自动复制粘贴流程

V7.5 保留 V7.0 的分工：

```text
Codex 生成每一层问题包。
用户只负责复制和粘贴。
外部模型负责回答。
Codex 负责融合、收敛、评分和判断 Gain。
```

推荐外部模型：

- GPT / ChatGPT：质量锚点；
- DeepSeek：低成本深推理与反向检查；
- Qwen / 千问：中文材料、第三视角与综合补盲。

用户不需要自己设计提示词、比较稿件或做融合判断。

## 9. Score_0、SCORE_FINAL、Gain 解释

必须保留公式：

```text
Gain = SCORE_FINAL - Score_0
```

字段解释：

- `Score_0`：普通直答答案的初始质量分。
- `SCORE_FINAL`：D 层最终答案的质量分。
- `Gain`：ABCD 链路相对普通答案的增益。

判断规则：

```text
Gain < 2.0 -> INVALID_CHAIN
Gain >= 2.0 -> EFFECTIVE_CHAIN
```

中文解释：如果复杂链路没有至少提升 2 分，就不能因为流程复杂而假装成功。

## 10. V15 全量注入要求

每一层装配问题包时都必须包含完整 V15 正文：

```text
10-SPEC/V15_FULL_WITH_GUARD_v1.0.md
```

禁止用以下内容替代：

- V15 摘要；
- “遵守 V15”一句话；
- `<<<V15_FULL>>>` 占位符；
- 重新压缩或改写的 V15。

失败状态码：

```text
UF_PROMPT_ASSEMBLY_FAIL: V15_FULL_MISSING
```

中文解释：提示词装配失败，原因是没有完整注入 V15 正文。

## 11. A/B/C/D 各层职责

A 层：独立极限生成，不融合。

- 目标是发散、补盲点、找不同角度；
- 不允许模型互相抄；
- 不允许提前合并；
- 推荐 `temperature = 0.70`，建议范围 `0.65 - 0.75`。

B 层：融合增强，不是评论。

- 必须吸收 A 层强点；
- 必须生成新的完整独立答案；
- 如果只评论 A1/A2/A3，判定失败；
- 失败状态码：`B_DEGRADATION_FAIL`，中文解释：B 层退化为评论层，没有生成增强答案。

C 层：官方高密度融合，不是普通总结。

- 必须使用 `30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md`；
- 必须保留复检陌生稿规则、四维稠密融合、证据硬规则和逆向一致性检查；
- 推荐 `temperature = 0.35`，建议范围 `0.25 - 0.40`。

D 层：最终答案优先，再做终验。

- 必须先输出 `FINAL_ANSWER`；
- 再输出 `SCORE_FINAL`、风险检查、Gain 和链路判断；
- 禁止只输出评测报告；
- 推荐 `temperature = 0.20`，建议范围 `0.10 - 0.25`。

## 12. 用户操作边界

用户只需要：

- 复制 `[COPY_START]` 到 `[COPY_END]` 之间的完整问题包；
- 粘贴到对应外部模型；
- 把外部模型返回结果贴回 Codex；
- 审校中文说明是否符合原始想法。

用户不需要：

- 自己写 A/B/C/D 提示词；
- 自己判断哪个模型稿进入下一层；
- 自己计算 Gain；
- 自己修复 V15 装配问题。

## 13. Codex 操作边界

Codex 必须：

- 生成干净、完整、可复制的问题包；
- 保证每层注入完整 V15；
- 保证 C 层使用官方 C prompt；
- 保证 D 层 `FINAL_ANSWER FIRST`；
- 记录 `Score_0`、`SCORE_FINAL`、`Gain`；
- 诚实标记 `EFFECTIVE_CHAIN` 或 `INVALID_CHAIN`；
- 不伪造外部模型答案。

## 14. 失败模式

核心失败模式和中文解释：

- `V15_FULL_MISSING`：V15 全量正文缺失。
- `C_LAYER_SIMPLIFIED_PROMPT_USED`：C 层使用了简化提示词。
- `D_HARD_COMMAND_TRIGGERED_REFUSAL`：D 层命令过硬，触发外部模型拒答。
- `D_META_EVALUATION_WITHOUT_FINAL_ANSWER`：D 层只评估流程，没有先回答原问题。
- `D_LAYER_V15_FULL_MISSING`：D 层缺少完整 V15。
- `FINAL_ANSWER_TOO_THIN`：最终答案过薄，缺少可执行深度。
- `B_DEGRADATION_FAIL`：B 层退化为评论。
- `COPY_PASTE_BOUNDARY_ERROR`：复制边界错误。
- `EXTERNAL_MODEL_REFUSAL`：外部模型拒答。
- `TOKEN_TRUNCATION_RISK`：上下文过长导致截断风险。

## 15. 中文审校注意事项

审校时看三件事：

1. 逻辑是否和 V7.0 一致；
2. 英文机器字段是否保留且有中文解释；
3. 中文说明是否让用户能判断“这条规则限制什么、保护什么、避免什么失败”。

不要把专业字段强行翻译成中文路径或字段名。

## 16. 与 V7.0 的关系

V7.5 是 V7.0 的中文审校版。

它从以下源包复制而来：

```text
${REDACTED_SECRET}
```

V7.5 不覆盖 V7.0，不改变 V7.0 的机制，只增加中文说明和审校入口。

## 17. 与 V8.0 / V8.2 的区别

V8.0 / V8.2 是极简压力链路线，目标是日常高性价比生产。

V7.5 仍然保留 V7.0 的重型半自动 ABCD、完整 V15、外部模型复制粘贴和完整审计链路。

因此：

- V7.5 不替代 V8；
- V8 不反向改写 V7.5；
- 两者服务不同使用场景。

## 当前状态

```text
REVIEW_READY_CN
```

中文解释：V7.5 中文审校版已经可供用户阅读、对比和修改，但还不是外部模型实战终验封板版。