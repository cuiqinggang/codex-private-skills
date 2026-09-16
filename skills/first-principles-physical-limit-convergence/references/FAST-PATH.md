# FAST PATH — 成熟收割优先的物理极限收敛最短路径 v1.2

## STEP 1 — CALCULATE + HARVEST PLAN（第一步：计算 + 成熟收割计划）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）` 和 hard constraints（硬约束）。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻已经真实安装、可正常使用、并允许用于本任务的硬件。未来计划增加但当前不存在的硬件不进入本轮 99，也不得阻断本轮 99。
3. 继承最近一次兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）和已证伪机制；禁止从零重复探索。
4. 复用已有事实，只补关键缺口。
5. 建立 `PHYSICAL_DAG（物理因果图）` 与 critical path（关键路径）。
6. 推导 `T_PHY（物理极限）=[LOW,HIGH]`。
7. 执行 `MATURE_FRONTIER_SCAN（成熟前沿扫描）`：官方稳定方案、官方性能提交、同 GPU 架构/同 VRAM/同模型的实测方案、主要成熟社区方案。
8. 对成熟方案执行 `APPLICABILITY_FILTER（适用性筛选）`：GPU 架构、VRAM/RAM、模型/量化、任务 shape（形状）、软件版本、质量/稳定/可复现要求必须匹配。
9. 建立 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`，按“预期绝对收益秒数 × 适用性置信度 × 证据置信度 ÷ 集成成本”排序；先挑大收益、强证据、低成本候选。
10. 执行 `SOFTWARE_FRONTIER_SCAN（软件前沿扫描）`：当前版、官方最新稳定版、主要成熟优化版。
11. 执行 `HARDWARE_TOPOLOGY_SCAN（硬件拓扑扫描）`，但只扫描 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）` 内真实存在的 GPU、PCIe、显示器连接、主辅卡分工和功能拆分可能性。
12. 以“当前有效硬件边界 + 最佳成熟软件/实现 + 当前边界内最佳硬件拓扑 + 已验证经验先验”推导 `T_MACHINE_STAR（本机稳定理论极限）=[LOW,HIGH]`。
13. 建立 `ASSUMPTION_LEDGER（假设账本）`；未知量用区间 + 置信度。
14. 输出两条攻击序列：`MATURE_HARVEST_ORDER（成熟收割顺序）` 和 `CUSTOM_ATTACK_ORDER（定制攻击顺序）`。
15. 判断多智能体模式；排他 GPU benchmark（基准测试）串行。

## STEP 2 — HARVEST → CUSTOM CONVERGE（第二步：先成熟收割，再定制收敛）

16. 安全去重甲，建立 `V1（第一最小正确执行版本）`。
17. 审核命令包：合同、计时、资源隔离、可逆性、证据、Git 收口。
18. 真实运行 V1，得到 `T_CURRENT（当前实测）`。

### PHASE A — MATURE HARVEST（阶段A：成熟收益收割）

19. 按 `MATURE_HARVEST_ORDER` 优先测试已经被外部真实验证、且与当前任务高度匹配的成熟方案；禁止先进入自研 kernel/微参数探索。
20. 优先直接复用成熟 workflow / version / official feature / model format / patch（工作流 / 版本 / 官方功能 / 模型格式 / 补丁）。
21. 外部 benchmark（基准测试）只决定测试优先级，不自动决定本机 KEEP。
22. 同任务更快且硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
23. 成熟完整栈如果本身不可合理拆分，可以整体 A/B 后直接 KEEP；不要求为了理解机制先把成熟栈重新拆散。
24. 每次 KEEP 后重新计算绝对 Gap，并重新排序剩余成熟候选；不机械跑完低价值列表。

### PHASE B — RESIDUAL CUSTOM ATTACK（阶段B：剩余差距定制攻击）

25. 只有当高价值成熟候选已经收割完、明显不适用，或仍存在显著剩余 Gap 时，才进入深度 profiling（分块诊断）和自研攻击。
26. 计算 `DELTA_T_REDUCIBLE（可消灭时间差）`。
27. 永远优先攻击最大绝对剩余 Gap（差距），而不是最大百分比或最容易测的参数。
28. 更快且硬约束通过 => KEEP；否则 ROLLBACK。
29. 每次 KEEP 后重新测量、重排 Gap；禁止因为已经开始某个自研方向就机械做到底。

### FINAL GATES（最终门禁）

30. 99 前执行 `SOFTWARE_FRONTIER_GATE（软件前沿门禁）`，确认当前成熟软件赢家和最新高价值候选没有遗漏。
31. 执行 `HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）`：只核验当前真实可用硬件。若当前只有单 GPU，则确认单卡拓扑和资源边界后即可 PASS；不存在的第二 GPU 不进入本轮门禁。
32. Final Certification（最终认证）前确认：`MATURE_FRONTIER_SCANNED=YES`、`HIGH_VALUE_MATURE_CANDIDATES_TESTED=YES`、`RESIDUAL_HIGH_VALUE_MATURE_GAP=NO`。
33. 只有 `MATURE_PATH_FIRST_GATE=PASS（成熟路径优先门禁通过）` + `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）` + `HARDWARE_TOPOLOGY_GATE=PASS（硬件拓扑门禁通过）` + `SHARED_REPO_SYNC=PASS（共同仓库同步通过）` 才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
34. 冻结 99 后，把真实分块时间、成熟方案赢家、有效/无效攻击、稳定配置和 Failure Index 写入 `EMPIRICAL_PRIORS（经验先验）`，供下一次硬件/软件/任务条件变化时直接继承。

```text
先复制世界已经验证过的最快成熟路径，把最大成熟收益一次吃掉；
再对剩余 Gap 做第一性原理定制攻击；
当前有什么硬件，就先把当前真实硬件做到自己的 99；
下一次不重新从零探索，而是从成熟世界经验 + 本机经验先验继续向前。
```
