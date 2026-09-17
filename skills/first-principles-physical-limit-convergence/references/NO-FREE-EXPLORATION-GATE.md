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
- 开性能剖析（profiler）、内核追踪（kernel trace）、参数搜索、版本搜索；
- 根据中间结果发明下一条优化路线。

## 但不要误解成“每一步都回GPT”

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
COMPLETE_COMMAND_PACK_EXECUTION=YES
NO_REAL_EXECUTION_REPLAN_LOOP=YES
INDEPENDENT_NEW_RESEARCH_PATH=YES
```
