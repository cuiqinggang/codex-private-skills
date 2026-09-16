# FAST PATH — 两步物理极限收敛最短路径 v1.1

## STEP 1 — CALCULATE（第一步：计算）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）` 和 hard constraints（硬约束）。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻已经真实安装、可正常使用、并允许用于本任务的硬件。未来计划增加但当前不存在的硬件不进入本轮 99，也不得阻断本轮 99。
3. 继承最近一次兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）和已证伪机制；禁止从零重复探索。
4. 继承兼容的既有冻结 99；禁止为了展示提升而故意退回慢版本。
5. 复用已有事实，只补关键缺口。
6. 建立 `PHYSICAL_DAG（物理因果图）` 与 critical path（关键路径）。
7. 推导 `T_PHY（物理极限）=[LOW,HIGH]`。
8. 执行 `SOFTWARE_FRONTIER_SCAN（软件前沿扫描）`：当前版、官方最新稳定版、主要成熟优化版。
9. 执行 `HARDWARE_TOPOLOGY_SCAN（硬件拓扑扫描）`，但只扫描 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）` 内真实存在的 GPU、PCIe、显示器连接、主辅卡分工和功能拆分可能性。
10. 以“当前有效硬件边界 + 当前边界内最佳硬件拓扑 + 最佳成熟兼容软件栈 + 已验证经验先验”推导 `T_MACHINE_STAR（本机稳定理论极限）=[LOW,HIGH]`。
11. 建立 `ASSUMPTION_LEDGER（假设账本）`；未知量用区间 + 置信度。
12. 计算分块理论目标与 `ATTACK_ORDER（攻击顺序）`。
13. 判断多智能体模式；排他 GPU benchmark（基准测试）串行。

## STEP 2 — CONVERGE（第二步：收敛）

14. 安全去重甲，建立 `V1（第一最小正确执行版本）`。
15. 审核命令包：合同、计时、资源隔离、可逆性、证据、Git 收口。
16. 真实运行 V1，得到 `T_CURRENT（当前实测）`。
17. 计算 `DELTA_T_REDUCIBLE（可消灭时间差）`。
18. 永远优先攻击最大绝对 Gap（差距）。
19. 更快且硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
20. 每次 KEEP 后重新测量、重排 Gap；不机械跑完候选列表。
21. 接近目标后执行 `SOFTWARE_FRONTIER_GATE（软件前沿门禁）`。
22. 执行 `HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）`：只核验当前真实可用硬件。若当前只有单 GPU，则确认单卡拓扑和资源边界后即可 PASS；不存在的第二 GPU 不进入本轮门禁。
23. 如果当前已真实存在第二 GPU 等高价值候选，再比较单卡、双卡但单卡计算、显示迁移、功能拆分；联合计算只在成熟支持时进入。
24. 软件或当前硬件拓扑候选真实胜出后，更新 `BEST_SOFTWARE_STACK（最佳软件栈）` / `BEST_HARDWARE_TOPOLOGY（最佳硬件拓扑）`，必要时修订 `T_MACHINE_STAR`，再继续收敛。
25. Final Certification（最终认证）前再次确认当前有效硬件边界内无明显软件/硬件高收益遗漏。
26. 只有 `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）` + `HARDWARE_TOPOLOGY_GATE=PASS（硬件拓扑门禁通过）` + `SHARED_REPO_SYNC=PASS（共同仓库同步通过）` 才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
27. 冻结 99 后，把真实分块时间、有效/无效攻击、稳定配置和 Failure Index 写入 `EMPIRICAL_PRIORS（经验先验）`，供下一次硬件/软件/任务条件变化时直接继承。

```text
当前有什么硬件，就先把当前真实硬件做到自己的 99；
未来增加硬件后，再以旧 99 + 真实经验 + 新硬件事实重新计算新的 T_MACHINE_STAR；
不让未来假设阻断今天的稳定最优，也不让下一次重新从零探索。
```
