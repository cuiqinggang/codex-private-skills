# 禁止自由探索门禁 — v1.9.0

英文：`NO-FREE-EXPLORATION-GATE（禁止自由探索门禁）`

## 核心

```text
禁止自由探索（NO_FREE_EXPLORATION）= YES
Codex角色（CODEX_ROLE）= 确定性执行器 / 验证器
```

Codex 不允许自行：

- 增加候选；
- 改候选顺序；
- 设计新实验；
- 追加运行；
- 开 profiler（性能剖析）、kernel trace（内核追踪）、参数搜索、版本搜索；
- 根据中间结果发明下一条优化路线。

## 执行可以灵活，方案不能灵活

允许 Codex 为了完成**同一个已经授权的动作**，采用等价执行方式，例如：

- PowerShell 写法换成等价 `.ps1`；
- 路径写法换成等价绝对路径；
- 在命令包规定范围内重试同一个动作；
- 创建临时日志、备份、报告；
- 会话中断后恢复同一个既定任务。

这些都属于：

```text
有限执行灵活性（BOUNDED_EXECUTION_FLEXIBILITY）
```

但以下属于改变方案，绝对禁止 Codex 自行决定：

- 换模型、候选、软件版本；
- 改参数、seed（种子）、运行次数、顺序；
- 改通过阈值、质量门禁、计时边界；
- 安装未授权依赖；
- 新增测试、性能剖析或研究路线。

一句话：

```text
可以灵活决定“怎么执行同一条命令”
不能灵活决定“接下来执行什么任务”
```

## 不要误解成“每一步都回GPT”

GPT 在第3步已经完成完整虚拟99；第4步已经生成完整实测命令包。

因此：

```text
命令包内已定义的正常 PASS（通过）
/ FAIL（失败）
/ ROLLBACK（回滚）
→ 继续执行命令包
```

不需要每一步重新返回 GPT。

只有以下情况停止返回 GPT：

- 命令包完全没有覆盖的异常；
- 固定任务合同失效；
- correctness（正确性）、quality（质量）、stability（稳定性）、safety（安全性）失效；
- 继续执行必须超出原命令包允许范围。

## 主原则

```text
虚拟层可以反复迭代 = YES
真实实测层反复重规划 = NO
```

## 新优化路线

执行中如果发现一个命令包外的新优化方向，不要顺手测试，也不要插回当前流程。

记录为：

```text
独立99路径（INDEPENDENT_99_PATH）
```

当前任务继续按原命令包收口。

## 验收

```text
NO_FREE_EXPLORATION=YES
BOUNDED_EXECUTION_FLEXIBILITY=YES
PLAN_MUTATION_BY_CODEX=NO
COMPLETE_COMMAND_PACK_EXECUTION=YES
NO_REAL_EXECUTION_REPLAN_LOOP=YES
INDEPENDENT_NEW_RESEARCH_PATH=YES
```