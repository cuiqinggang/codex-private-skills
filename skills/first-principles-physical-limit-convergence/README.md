# 第一性原理物理极限收敛引擎 v1.9.0

英文名：**First-Principles Physical-Limit Convergence（第一性原理物理极限收敛）**

## 核心只有四步

```text
第1步：计算物理极限
第2步：计算本机现实最优区间
第3步：GPT完成虚拟99攻击迭代
第4步：生成并完整执行Codex实测命令包
```

这四步就是主流程，不再往里面增加新的执行层级。

## 最重要的纪律

```text
禁止自由探索（NO_FREE_EXPLORATION）= YES
虚拟循环只发生在GPT层 = YES
真实实测层反复回GPT重规划 = NO
完整命令包一次执行到底 = YES
```

GPT 在第3步已经把成熟方案、组合关系、收益、风险、停止点全部虚拟推演清楚；第4步 Codex 只负责按完整命令包执行。

正常的通过、失败、回滚结果不需要每一步重新返回 GPT。

## Codex可以有多大灵活性

一句话：

> **可以灵活决定怎么执行同一个已授权动作，不能灵活决定接下来做什么。**

允许：等价命令写法、脚本封装、路径修正、按既定规则恢复同一个任务。

禁止：换模型、换候选、换软件版本、改参数、改运行次数、改顺序、改阈值、增加性能剖析或新研究路线。

如果既定动作无法在这个边界内完成，就保存证据、停止、返回 GPT。

## 新发现的优化路线怎么办

如果主流程之后又发现一条需要新模型、新软件版本、新内核或新研究的路线，不插回当前主流程。

将它记录为：

```text
独立99路径（INDEPENDENT_99_PATH）
```

以后单独再走一次四步法。

这样既保留新机会，又不破坏主流程的简洁性。

## 两个核心时间数据

```text
T_PHY_TOTAL_REFERENCE（端到端物理极限参照）
= 物理终极参照

REAL_STATE_OPTIMUM_RANGE（本机现实最优区间）
= 当前本机现实目标
```

第3步虚拟99同时参考这两个数据。

## 当前唯一母技能身份

```text
技能ID = first-principles-physical-limit-convergence
版本 = 1.9.0
正式分支 = codex/first-principles-physical-limit-convergence-v1.9.0
```

历史 `absolute-time-fireworks-optimization` 只是祖先技能，不是当前母技能。

完整规则见 `SKILL.md`。
