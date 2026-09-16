# FAST PATH — 两步物理极限收敛最短路径 v1.1

## STEP 1 — CALCULATE（第一步：计算）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）` 和 hard constraints（硬约束）。
2. 继承兼容的既有冻结 99；禁止为了展示提升而故意退回慢版本。
3. 复用已有事实，只补关键缺口。
4. 建立 `PHYSICAL_DAG（物理因果图）` 与 critical path（关键路径）。
5. 推导 `T_PHY（物理极限）=[LOW,HIGH]`。
6. 执行 `SOFTWARE_FRONTIER_SCAN（软件前沿扫描）`：当前版、官方最新稳定版、主要成熟优化版。
7. 执行 `HARDWARE_TOPOLOGY_SCAN（硬件拓扑扫描）`：GPU 数量/容量、PCIe 链路、显示器连接、主辅卡分工以及可行的功能拆分/联合计算。
8. 以“当前硬件 + 最佳硬件拓扑 + 最佳成熟兼容软件栈”推导 `T_MACHINE_STAR（本机稳定理论极限）=[LOW,HIGH]`；不得只按当前已安装版本和当前接线方式计算。
9. 建立 `ASSUMPTION_LEDGER（假设账本）`；未知量用区间 + 置信度。
10. 计算分块理论目标与 `ATTACK_ORDER（攻击顺序）`。
11. 判断多智能体模式；排他 GPU benchmark（基准测试）串行。

## STEP 2 — CONVERGE（第二步：收敛）

12. 安全去重甲，建立 `V1（第一最小正确执行版本）`。
13. 审核命令包：合同、计时、资源隔离、可逆性、证据、Git 收口。
14. 真实运行 V1，得到 `T_CURRENT（当前实测）`。
15. 计算 `DELTA_T_REDUCIBLE（可消灭时间差）`。
16. 永远优先攻击最大绝对 Gap（差距）。
17. 更快且硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
18. 每次 KEEP 后重新测量、重排 Gap；不机械跑完候选列表。
19. 接近目标后执行 `SOFTWARE_FRONTIER_GATE（软件前沿门禁）`。
20. 如果存在第二 GPU 等高价值硬件候选，执行 `HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）`：至少比较单卡、双卡但单卡计算、显示迁移、功能拆分；联合计算只在成熟支持时进入。
21. 软件或硬件拓扑候选真实胜出后，更新 `BEST_SOFTWARE_STACK（最佳软件栈）` / `BEST_HARDWARE_TOPOLOGY（最佳硬件拓扑）`，必要时下修 `T_MACHINE_STAR`，再继续收敛。
22. Final Certification（最终认证）前再次确认无明显软件/硬件高收益遗漏。
23. 只有 `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）` + `HARDWARE_TOPOLOGY_GATE=PASS（硬件拓扑门禁通过）` + `SHARED_REPO_SYNC=PASS（共同仓库同步通过）` 才允许 `99=YES / FREEZE=YES / FINAL=PASS`。

```text
先算物理终点，再把最佳软件栈和最佳硬件拓扑纳入本机终点；
V1 后持续攻击最大绝对 Gap；
99 代表“当前硬件 + 当前最佳硬件分工 + 当前最佳成熟兼容软件栈”的稳定最优。
```
