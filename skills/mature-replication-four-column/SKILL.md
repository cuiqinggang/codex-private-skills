---
name: mature-replication-four-column
description: Apply the First-Principles Four-Column Method v4.0 to minimize end-to-end physical time for a fixed task while preserving all requirements; use for performance optimization, mature-solution comparison, staged 99-point convergence, capability additions, and diagnosing unexplained time regressions.
metadata:
  version: "4.0.0"
  short-description: 第一性原理物理时间四列法 V4.0
---

# 第一性原理四列法 V4.0

在任务定义完全固定后，以第一性原理物理时间 `T_PHY` 为唯一终极参照，使用成熟方案作为现实证据和路径库，通过阶段性的 99 分冻结与局部迭代，持续降低真实端到端时间 `T_END_TO_END`。

兼容入口仍为 `mature-replication-four-column`。旧版“成熟能力/缺口/原因/成熟解法”不是 V4.0 的四列主结构；其五类归因仅在第四列诊断局部损失时按需使用。参见 [旧版兼容映射](references/legacy-method-mapping.md)。

当前通用工程执行入口已经升级为 `absolute-time-fireworks-optimization v2.0.0`。两者不是上下位理论，也不是两套竞争方法；v2.0 是同一四列思想经过完整工程实践后的通用执行版本。

## 先固定 TASK

优化前冻结任务合同：目标、成功条件、输入输出、必须保留的能力、不可删除步骤、安全要求、稳定性要求和质量底线。任务一旦固定，唯一优化指标是：

`minimize(T_END_TO_END)`

通过删除要求、缩小范围、跳过必要验证或降低质量得到的更短时间，标为 `INVALID_RESULT`，不得进入基线。

## 四列正式定义

严格按顺序填写，不得先写优化方案再补数字。

### 1. CURRENT

记录固定任务当前真实完成时间 `T_CURRENT`，并按启动、加载、计算、传输、保存、验证、返回等必要阶段分段计时。只用实测事实，不用“感觉很慢”“应该正常”等判断代替计时。

### 2. EXTERNAL FRONTIER

记录现实世界中同类任务已经达到的时间 `T_EXTERNAL`、来源、硬件、软件、任务合同和可比性。官方方案、成熟开源项目、公开 benchmark、同类硬件实测及已验证技能/工作流都可作为证据。

成熟方案是现实证据、经验库和路径库，不是最终参照。优秀部分可复制；不可比部分必须说明；若第一性原理证明存在更短路径，不必受现有方案限制。

### 3. FIRST-PRINCIPLES PHYSICAL TIME

从不可避免的物理步骤推导理论最短时间 `T_PHY`。可以先给 `T_PHY_RANGE`，随着证据增加再收窄。根据任务分析最低计算量、数据读取、显存/内存/磁盘/网络带宽、PCIe、必要编码解码、软件调度、安装验证、不可并行步骤与必要等待。

明确记录假设、测量值、计算式、不确定性和物理瓶颈。`T_PHY` 是长期方向，不是成熟方案、当前最好成绩或要求当轮必达的数字。

### 4. ITERATIVE CONVERGENCE

以一次一个局部假设循环：

`测量 → 比较 T_PHY → 参考成熟方案 → 找最大时间损失 → 设计一个局部优化 → 真实运行 → 重新计时 → 有效保留/无效回滚 → 继续`

每轮必须记录改动、对应损失、前后时间、任务合同是否保持、证据和保留/回滚结论。不得为局部问题大面积重构健康系统；只有证据证明整体架构阻碍接近 `T_PHY` 时，才允许架构级改造。

## 99 分冻结门禁

`99` 表示在当前硬件、软件、环境、固定任务和已知可验证方法下，经过系统搜索与实测后，没有发现还能带来显著、稳定时间收益的可行方案，即 `CURRENT_STAGE=CONVERGED`。

它不表示达到 `T_PHY`、超过所有外部方案、达到理论峰值 99%，也不表示永久真理。冻结时仍记录：

`PHYSICAL_GAP = T_99 - T_PHY`

若存在真正可比且显著更快的 `T_EXTERNAL`，原则上不得宣布 99，除非已经复现并接近、证明不可比、证明当前约束无法复现，或用另一条路径达到当前实际极限。

当新算法、kernel、模型、缓存或成熟项目证明存在显著稳定收益时，重新打开旧 99，完成新一轮迭代后冻结新的 99。

## 阶段与新增能力

每个新阶段必须站在上一阶段冻结基线上：

`Stage N → 99 → Freeze → Stage N+1 = Stage N + 新能力`

新增能力必须记录：

`ΔT = T(N+1) - T(N)`

并以该能力不可避免的计算/传输/加载、外部成熟实现和新的 `T_PHY` 解释合理范围。若实际 `ΔT` 数量级高于合理范围，先判为 `PATH_ARCHITECTURE_ERROR`，检查工作流路径、offload、模型加载、重复执行、参数、前置技能和是否走错成熟路线。禁止把时间崩塌接受为新常态。

## 证据与结案

- 时间必须来自同一固定任务、明确起止点和可复现运行；冷热启动差异分开记录。
- `VERIFIED`、`INFERRED`、`UNVERIFIED` 必须分开；外部数字只有可比性成立时才能约束 99。
- 保留上一阶段可恢复版本；无效实验回滚，不能污染冻结基线。
- 结案交付四列表、计时证据、`T_PHY` 推导、实验日志、99/非 99 结论、冻结版本、复现方法、残余 `PHYSICAL_GAP` 与重新打开条件。

执行时使用 [V4.0 工作表](references/four-column-worksheet.md)。需要完整原始定义时读取 [用户提供的 V4.0 原文](references/first-principles-four-column-v4.0-source.md)。
