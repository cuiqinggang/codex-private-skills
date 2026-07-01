# 测试与验收方案

## 1. 为什么必须有测试

Fugu 类系统最容易出现的问题是“看起来很聪明，但无法复现”。因此每次评估必须记录：

- 任务原文。
- 使用模型。
- 每个角色的输入输出。
- 成本估算。
- 运行时间。
- 证据。
- 评分。
- 失败原因。

没有这些记录，就不能把“感觉好”升级成“技能包规则”。

## 2. 测试集分层

### A. 轻量冒烟测试

目标：验证流程是否跑通。

| 编号 | 任务 | 评分重点 |
|---|---|---|
| S01 | 把一个复杂任务拆成执行计划 | 路由是否合理 |
| S02 | 给一段有 bug 的代码做审查 | 是否发现关键 bug |
| S03 | 根据网页资料整理对比表 | 是否引用来源 |
| S04 | 对一张 UI 截图生成坐标表 | 视觉是否准确 |
| S05 | 对一个错误答案做 verifier 检查 | 是否敢判 FAIL |

### B. Codex/Kilo 真实任务测试

目标：验证对用户工作流是否有用。

| 编号 | 任务 | 评分重点 |
|---|---|---|
| C01 | 生成可回滚命令包 | 是否有回滚和证据 |
| C02 | 长任务 2 小时计划与 checkpoint | 是否能持续推进 |
| C03 | 技能包整理和打包 | 文件结构是否可用 |
| C04 | 本地知识库路由方案 | 是否轻入口、重资料库 |
| C05 | 多模型低成本极限回答 | 是否控制成本且提高质量 |

### C. 高难对标测试

目标：模拟 Fugu 官方展示的强项。

| 类别 | 对应公开 benchmark 思路 | 本地复刻方式 |
|---|---|---|
| 软件工程 | SWE-Bench / SWE-Bench Pro | 真实 repo bug 修复 + 测试通过 |
| 终端任务 | TerminalBench | 命令行多步任务 + 证据日志 |
| 代码竞赛 | LiveCodeBench | 算法题 + 单元测试 |
| 科学推理 | GPQA-Diamond | 高难科学题 + 来源核查 |
| 综合难题 | HLE-like | 多学科题 + 引用与推理 |
| 图表视觉 | CharXiv Reasoning | 图表/截图问答 |
| 长上下文 | Long Context Reasoning | 长文档检索 + 事实定位 |

## 3. 评分 Rubric

每题 100 分：

| 维度 | 分值 | 标准 |
|---|---:|---|
| 正确性 | 30 | 结论、代码、数据是否正确 |
| 完整性 | 20 | 是否覆盖用户要求和边界 |
| 证据 | 15 | 是否有引用、测试、日志、截图、文件 |
| 执行质量 | 15 | 是否真正执行而不是空谈 |
| 验证修复 | 10 | 是否有独立验证和修复闭环 |
| 成本效率 | 10 | 是否用合适模型，避免浪费 |

判定：

| 分数 | 结果 |
|---:|---|
| 90-100 | PASS |
| 75-89 | ACCEPTED_WITH_LIMITS |
| 60-74 | PARTIAL |
| <60 | FAIL |

## 4. Gate Review 模板

```json
{
  "task_id": "C01",
  "route": "dual|multi|premium",
  "models_used": [],
  "evidence": [],
  "score": {
    "correctness": 0,
    "completeness": 0,
    "evidence": 0,
    "execution_quality": 0,
    "verification_repair": 0,
    "cost_efficiency": 0
  },
  "verdict": "PASS|ACCEPTED_WITH_LIMITS|PARTIAL|FAIL|BLOCKED",
  "required_repairs": [],
  "notes": ""
}
```

## 5. 对比实验设计

每个任务至少跑三种方案：

| 方案 | 说明 |
|---|---|
| Baseline | 单模型直接做 |
| Local-Orchestrated | 用户模型矩阵：GLM/DeepSeek/Kimi/Qwen |
| Premium-Orchestrated | 加入 Fugu Ultra 或其他高端裁判 |

记录：

- 质量分。
- 成本估算。
- 运行时间。
- 失败次数。
- 是否需要人工介入。
- 最终是否可交付。

## 6. 成本效率计算

建议用：

```text
value_score = quality_score / estimated_cost_usd
```

但不能只看这个。高风险任务要增加错误成本：

```text
effective_value = quality_score / (estimated_cost_usd + expected_failure_cost)
```

如果任务失败会造成重大返工，高价模型可能反而划算。

## 7. 最小验收标准

一个复刻的 Fugu 式流程要进入正式技能包，至少满足：

- 10 个轻量测试，PASS >= 8。
- 5 个 Codex/Kilo 真实任务，PASS 或 ACCEPTED_WITH_LIMITS >= 4。
- 成本不超过“全程高端模型”的 40%。
- 至少 2 个任务证明 verifier 抓到了 executor 漏洞。
- 所有输出能被打包复现。

## 8. 失败分类

| 类型 | 说明 | 修复方式 |
|---|---|---|
| ROUTE_ERROR | 选错模型或流程 | 调整路由规则 |
| EXECUTION_ERROR | 主执行失败 | 换 executor 或缩小任务 |
| VERIFIER_WEAK | 验证器没抓到错 | 强化 rubric 或换 verifier |
| COST_BLOWUP | 成本超限 | 减少 agent 数和轮数 |
| SYNTHESIS_LOSS | 合成时丢信息 | 要求引用子输出编号 |
| EVIDENCE_GAP | 没有证据 | 强制日志/测试/引用 |

## 9. 复测频率

- 新模型加入时：跑 S01-S05。
- 模型价格变化时：重算成本表。
- 技能包修改后：至少跑 3 个冒烟测试。
- 长任务失败后：把失败案例加入回归测试。
