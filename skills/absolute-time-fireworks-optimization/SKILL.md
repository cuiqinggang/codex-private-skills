---
name: absolute-time-fireworks-optimization
description: Minimize real end-to-end time after defining what task completion means, using the First-Principles Four-Column Method, structure-emergent planning, de-armoring, and keep-or-rollback convergence. Use for engineering, workflow, learning, research, design, decision, or personal tasks where time is the primary metric after an acceptable completion condition is fixed.
metadata:
  version: "2.0.0"
  short-description: 第一性原理四列法通用99收敛引擎
---

# 第一性原理四列法通用99收敛引擎

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END
HARD_BOUNDARY = TASK_COMPLETED == TRUE
```

先定义什么叫任务完成。在任务仍然完成的前提下，只优化真实端到端时间。原流程、节点、阶段、检查、验证层、日志、监控、质量包装、兼容设计和管理制度首先都只是 `CURRENT（当前现实）`，不是 `PHYSICAL NECESSITY（物理必需）`。

本技能继续使用唯一 skill ID `absolute-time-fireworks-optimization`，并依赖 `mature-replication-four-column` 的第一性原理四列法 V4.0；不创建上位、下位或平行技能。

## 四列

1. `CURRENT（当前真实状态）`：现在真实是什么，不给现实辩护。
2. `EXTERNAL FRONTIER（外部成熟前沿）`：现实世界已验证的成熟方案，帮助避免盲人摸象，但不是终极边界。
3. `FIRST-PRINCIPLES PHYSICAL LIMIT（第一性原理物理极限）`：暂时拿掉历史习惯与人为限制，只问完成任务最少必须发生什么，推导 `T_PHY` 或区间。
4. `ITERATIVE CONVERGENCE（迭代收敛）`：找最大时间损失，判断是否必需，删除/合并/旁路/后移/并行/替换/简化，实测后 KEEP（保留）或 ROLLBACK（回滚），再以 NEW CURRENT 重做四列。

## 结构由分析产生

不得预设阶段、节点或 `SYSTEM-99` 独立层。

- 简单任务可以整体收敛，不创建节点。
- 大型任务若可整体连续优化，可以删除、合并、并行或重组历史阶段。
- 只有真实因果依赖使后续工作无法提前开始时，才自然产生依赖节点；每个节点完成后，后续分析基于已经改变的新整体。
- `PLAN-99` 只表示：执行前先用同一套四列法优化执行方案本身。它没有预设结构。

## 去重甲

`De-Armoring（去重甲）` 是第四列的最高优先级执行机制之一：不断追问“这个东西不存在，任务还能完成吗？”找不到物理或因果必要性时，先把它列为 `ARMOR CANDIDATE（重甲候选）`，再通过删除或重组后的真实运行裁决。

watchdog、monitor、polling、重复执行、重复转换、等待链、检查站、历史兼容层、管理动作和人为节点都不自动获得存在资格。需要时尽量移到关键路径外或 `RESULT_READY（结果就绪）` 后。

## 99

99 是当前现实条件下的收敛等级，不是 `T_CURRENT/T_PHY=99%`，也不是数学绝对极限。任务真实完成、明显大型非必要块已清除、没有新的现实高收益路径且继续投入的边际收益显著下降时，可以 `99=YES / FREEZE=YES`。

## 分布式智能执行闭环

这不是新的方法层级，而是让同一方法自动连续运行的执行基础设施：

- `REASONING BRAIN（推理大脑）= ChatGPT_Web`：读取真实状态，完成四列分析、物理因果判断与 KEEP / ROLLBACK / NEXT / 99 裁决。
- `EXECUTOR（执行器）= Codex`：把单个明确决策变成本机动作，运行最小真实验证并收集原始证据。
- `SHARED FACT SOURCE（共同事实源）= cuiqinggang/codex-private-skills`：保存可供双方重新读取的真实状态。
- `DEDICATED BROWSER BRIDGE（专用浏览器桥梁）= playwright-native-ai-browser`：需要网页通信时恢复推理会话并传递任务与裁决。

高价值决策点必须返回推理大脑；禁止一次生成几十步后让执行器长时间盲跑。桥梁只引用成熟能力，不复制第二套 Skill；具体入口与故障路由见 [EXECUTION BRIDGE（执行桥梁）](references/EXECUTION-BRIDGE.md)。

## 最小读取

正常任务只读本文件和 [FAST PATH（成熟最短路径）](references/FAST-PATH.md)。

- 需要案例时：读 [CASE INDEX（案例索引）](references/CASE-INDEX.md)，P0 为 CASE-001。
- 发生异常时：只读 [FAILURE INDEX（失败经验索引）](references/FAILURE-INDEX.md) 中匹配触发条件的条目。
- 需要网页推理闭环时：读 [EXECUTION BRIDGE（执行桥梁）](references/EXECUTION-BRIDGE.md)。
- 复盘或审计时：再进入完整历史与证据。

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

最近使用见 [USAGE LOG（使用日志）](USAGE-LOG.md)，验收见 [ACCEPTANCE（验收页）](ACCEPTANCE.html)。
