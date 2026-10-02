# 长期记忆超级虚拟人｜长流程防漂移 Reality 对比 v0.1

## 目的

不凭感觉决定“单一决策文件”还是当前组合更好。用同批真实长任务比较完整 T_VALID。

## 候选 A｜单一权威 Source of Truth

```text
一个任务文件
= FINAL_GOAL + SCOPE + BOUNDARIES + DONE_WHEN + CURRENT_STATE
```

所有动作与其冲突即停止或显式改版。

这是最轻的成熟基线。

## 候选 B｜稳定规则 + 单任务 Source of Truth + Checkpoint

```text
稳定规则
+ 当前任务合同
+ 阶段 Checkpoint
+ Reality 验证
```

这是本技能当前候选。Checkpoint 只负责恢复，不替代任务合同。

## 候选 C｜完整 Spec-Driven 流程

参考成熟 SDD 结构：

```text
Constitution
→ Specify
→ Plan
→ Tasks
→ Implement
→ Converge
```

只用于复杂度足以抵消额外流程成本的任务。

## 统一 Reality

同一批真实任务、相同起点、相同 FINAL_VALID。

唯一比较值：
```text
T_VALID_A
T_VALID_B
T_VALID_C
```

辅助记录但不升级为第二目标：
- 漂移次数；
- 非目标范围新增量；
- 返工次数；
- Checkpoint 恢复次数；
- 人工干预次数。

## 判定

没有 FINAL_VALID 的候选不参与“谁更快”。

当前不宣布 B 优于 A 或 C。Reality 结果若证明单一 Source of Truth 更快，就收缩；若完整 SDD 在复杂任务更快，则仅在该类任务按需启用。
