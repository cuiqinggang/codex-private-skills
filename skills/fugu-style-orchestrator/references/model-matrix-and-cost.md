# 模型矩阵与成本判断

## 1. 基本原则

不要问“哪个模型最强”，而要问：

```text
这个任务的哪个步骤，应该由哪个模型以最低成本可靠完成？
```

Fugu 式系统的优势来自“组合”，不是来自“永远使用最贵模型”。

## 2. 当前建议矩阵

| 模型/系统 | 推荐角色 | 优势 | 风险 |
|---|---|---|---|
| DeepSeek V4 Pro | 主执行、代码、一般分析 | 性价比高，适合大量执行 | 复杂约束/Gate 不一定最稳 |
| DeepSeek V4 Flash | 轻任务、批处理 | 便宜快 | 不适合最终结论 |
| GLM-5.2 | 控制层、Gate、Repair | 指令遵循、长流程治理 | 成本高于便宜执行模型 |
| Kimi K2.7 Code | 代码、长上下文、Agent 编程 | 长上下文和工具生态强 | 输出可能偏长，仍需 Gate |
| Kimi K2.6 | 多模态、长上下文、Agent | 成本远低于 Fugu Ultra | 不是黑盒多模型调度器 |
| Qwen3-VL-235B | 视觉、截图、坐标、图表 | 视觉主力 | 不作为通用控制层 |
| Fugu | 低延迟调度器 | 单入口路由体验好 | 透明度有限 |
| Fugu Ultra | 高难外援、最终裁判、压力测试 | 多 agent 调度，benchmark 强 | 贵，慢，底层池固定 |

## 3. Fugu Ultra 与 Fable/Mythos 价格

公开信息显示：

| 模型 | 输入 / 1M token | 输出 / 1M token |
|---|---:|---:|
| Claude Fable 5 / Mythos 5 | $10 | $50 |
| Fugu Ultra | $5 | $30 |
| Fugu Ultra >272K context | $10 | $45 |

常见样例：

| 用量 | Fable/Mythos | Fugu Ultra | 结论 |
|---|---:|---:|---|
| 100K 输入 + 10K 输出 | $1.50 | $0.80 | Fugu Ultra 约便宜 47% |
| 1M 输入 + 100K 输出 | $15.00 | $8.00 | Fugu Ultra 约便宜 47% |
| 10M 输入 + 1M 输出 | $150.00 | $80.00 | Fugu Ultra 仍明显便宜 |

注意：这只是在高端模型之间比较。和 Kimi/DeepSeek 相比，Fugu Ultra 仍然很贵。

## 4. Fugu Ultra 与 Kimi 价格层级

Kimi K2.6/K2.7 公开价格大致在：

```text
输入约 $0.95 / 1M
输出约 $4.00 / 1M
```

因此，Fugu Ultra 相对 Kimi：

| 项目 | 倍数 |
|---|---:|
| 输入价 | 约 5.3 倍 |
| 输出价 | 约 7.5 倍 |

所以：

- 对 Fable/Mythos：Fugu Ultra 有性价比。
- 对 Kimi/DeepSeek：Fugu Ultra 是高端外援，不是日常主力。

## 5. 何时值得用高价模型

值得用：

- 一次错误会导致大量返工。
- 本地多模型结果冲突。
- 需要对外发布的重要结论。
- 高难代码审查，可能发现隐藏 bug。
- 论文复现、专利调查、复杂安全分析。

不值得用：

- 资料整理初稿。
- 大量重复格式转换。
- 简单代码修改。
- 已有明确测试可以验证的普通任务。

## 6. 推荐路由表

| 任务 | 默认路线 |
|---|---|
| 简单中文整理 | DeepSeek/Kimi 单模型 |
| 代码实现 | DeepSeek V4 Pro -> GLM Gate |
| 长代码库理解 | Kimi K2.7 Code -> GLM Gate |
| UI/截图/坐标 | Qwen3-VL -> GLM Gate |
| 高难代码审查 | DeepSeek/Kimi 双跑 -> GLM Gate -> 可选 Fugu Ultra |
| 论文复现 | Kimi/DeepSeek 执行 -> GLM 控制 -> 可选 Fugu Ultra 复核 |
| 多模型极限回答 | Cheap workers 并行 -> GLM 汇总 -> Fugu Ultra 只做最终对照 |

## 7. 成本保护规则

1. 任何 premium route 必须先估算成本。
2. Fugu Ultra 默认最多 1 次最终裁判，不参与每轮修复。
3. 如果本地 verifier 已经给出 PASS，不再调用高价模型。
4. 如果高价模型与本地结论冲突，必须用证据判定，不盲信高价模型。
5. 长上下文超过 272K 时，重新评估是否分块，因为 Fugu Ultra 价格会变化。
