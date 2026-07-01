# 复刻执行手册

## 1. 复刻目标

目标不是“买一个 Fugu Ultra 账号就结束”，而是在 Codex/Kilo/SuperTool 里复刻这套调度方法：

```text
先判断任务 -> 再选择模型 -> 再分配角色 -> 再执行验证 -> 最后交付证据包
```

这比单纯把所有问题扔给一个贵模型更可控，也更适合用户已有的低成本极限回答技能包。

## 2. 最小可用架构

```text
Router
  -> Planner
  -> Executor
  -> Verifier
  -> Repairer
  -> Final Synthesizer
```

### Router

输入：

- 用户原始任务。
- 可用模型列表。
- 成本预算。
- 是否需要联网、文件、视觉、代码执行。

输出：

```json
{
  "difficulty": "simple|normal|hard|extreme",
  "risk": "low|medium|high",
  "route": "single|dual|multi|premium",
  "roles": ["planner", "executor", "verifier"],
  "evidence_required": ["tests", "citations", "files", "screenshots"],
  "budget_limit": "..."
}
```

### Planner

职责：

- 拆任务。
- 决定执行顺序。
- 指定停止条件。
- 写出可验收标准。

Planner 不直接做大量执行，避免把控制层和执行层混在一起。

### Executor

职责：

- 写代码、查资料、生成文件、运行命令。
- 记录证据。
- 遇到失败时报告阻塞，而不是编造完成。

### Verifier

职责：

- 根据验收标准检查。
- 不重做任务，只找问题。
- 给出 `PASS / FAIL / PARTIAL / BLOCKED`。

### Repairer

职责：

- 只接收失败项、证据和相关文件。
- 修复具体问题。
- 不重写已通过部分。

### Final Synthesizer

职责：

- 合并最终答案。
- 删除内部杂音。
- 输出用户能直接使用的结论、文件、命令包或 ZIP。

## 3. 路由策略

| 路由 | 条件 | 模型数量 | 说明 |
|---|---|---:|---|
| single | 简单、低风险、低价值 | 1 | 最省钱，最快 |
| dual | 有实现和验收 | 2 | 主执行 + 独立验证 |
| multi | 复杂、多领域、高失败成本 | 3-5 | 分工明确，必须有预算 |
| premium | 高难且值得花钱 | 1 个高端或 Fugu Ultra + 本地验证 | 用于最终裁判或压力测试 |

## 4. 用户当前模型矩阵复刻版

| 角色 | 首选 | 备用 | 备注 |
|---|---|---|---|
| Router/Planner | GLM-5.2 | Kimi Thinking | 强指令和约束优先 |
| Main Executor | DeepSeek V4 Pro | Kimi K2.7 Code | 代码和一般任务主力 |
| Cheap Worker | DeepSeek V4 Flash | Kimi 低价档 | 搜集、整理、批处理 |
| Long Context | Kimi K2.6/K2.7 | DeepSeek Pro | 长仓库、长文档 |
| Vision | Qwen3-VL-235B | Qwen3-VL Thinking | 图像、视频帧、UI |
| Gate/Verifier | GLM-5.2 | Kimi Thinking | 严格验收 |
| Premium Judge | Fugu Ultra | 当前最强闭源/路由器 | 只用于高价值任务 |

## 5. 标准 Prompt 模板

### Router Prompt

```text
你是任务路由器。只做分类和调度，不执行任务。

输入任务：
{task}

可用模型：
{models}

限制：
- 控制成本。
- 不使用未授权工具。
- 高风险任务必须有独立验证。
- 输出 JSON。

输出字段：
difficulty, risk, route, roles, model_assignment, evidence_required, budget_limit, stop_conditions.
```

### Planner Prompt

```text
你是 Planner。把任务拆成可执行步骤。
不要执行具体文件修改。
必须写出验收标准、证据要求、失败停止条件。

任务：
{task}

路由结果：
{route_json}
```

### Executor Prompt

```text
你是 Executor。按计划执行。
必须保留证据：命令输出、文件路径、测试结果、引用来源。
不要声称未验证的内容已完成。
遇到阻塞输出 BLOCKED，并说明下一步需要什么。

计划：
{plan}
```

### Verifier Prompt

```text
你是独立 Verifier。你的目标是找问题，不是帮 Executor 圆场。

检查：
1. 是否满足用户原始目标。
2. 是否有证据。
3. 是否有未运行测试却声称通过。
4. 是否成本或范围失控。
5. 是否遗漏交付物。

输出：
PASS / FAIL / PARTIAL / BLOCKED
findings
required_repairs
```

### Repair Prompt

```text
你是 Repairer。只修复 Verifier 指出的失败项。
不要重写已通过部分。
每个修复项必须附证据。

失败项：
{findings}
```

## 6. 执行闭环

```text
Router -> Planner -> Executor -> Verifier
                         ^        |
                         |        v
                      Repairer <- FAIL
```

最多循环建议：

| 任务等级 | 最大修复轮数 |
|---|---:|
| normal | 1 |
| hard | 2 |
| extreme | 3 |

超过最大修复轮数后，不要继续消耗成本，输出 `PARTIAL` 或 `BLOCKED`。

## 7. 长任务规则

长任务必须有：

- 开始时间。
- 目标文件夹。
- checkpoint 间隔。
- heartbeat 文件。
- 日志文件。
- final gate。
- 三位数字 ZIP 交付。

建议目录：

```text
run/
  00_intake.md
  01_route.json
  02_plan.md
  logs/
  evidence/
  checkpoints/
  final/
```

## 8. 低成本策略

1. 先用便宜模型做资料搜集和候选方案。
2. 用强控制模型做路线选择。
3. 用主执行模型完成主体工作。
4. 只在最后关键点调用高端模型。
5. 所有模型输出都压缩成结构化证据，不把完整长上下文反复传递。

## 9. 何时引入 Fugu Ultra

只在以下情况考虑：

- 任务价值明显高于模型成本。
- 本地模型已经给出两个以上冲突结论。
- 需要模拟“高端多模型调度器”作为对照。
- 要做高难 benchmark 或竞赛级代码审查。
- 用户明确要求测试 Fugu。

不要用于：

- 批量低价值任务。
- 简单翻译、改写、摘要。
- 已有本地模型足够完成的普通 Codex 任务。
