# FAST PATH — 真实态校准 + 成熟收割优先 v1.3

## STEP 1 — CALCULATE + REAL-STATE CALIBRATION（计算 + 真实态校准）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）`、hard constraints（硬约束）。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻真实安装、可正常使用、允许用于本任务的硬件。
3. 继承最近兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）和已证伪机制；禁止从零重复探索。
4. 建立 `PHYSICAL_DAG（物理因果图）` 与 critical path（关键路径）。
5. 推导 `T_PHY（物理极限）=[LOW,HIGH]`。
6. 根据当前硬件、已知成熟软件/实现和经验先验，先算 `T_MACHINE_STAR_PRE（本机理论极限初算）=[LOW,HIGH]`。
7. 对复杂系统必须尽快建立 `MRE（最小真实执行版本）`，让完整关键链真实跑通；默认目标是在约 10 分钟级工程时间内得到足够的真实态数据。若单次任务物理上更长，则使用机制一致的最小合同/最小子合同。
8. MRE 必须暴露真实：模型装载/卸载、设备放置、DynamicVRAM/内存行为、缓存/预取/编译是否真正启用、首次运行与稳态差异、主要故障与真实关键路径。
9. 用 `STATIC FACTS + MRE OBSERVATIONS + EMPIRICAL PRIORS` 建立 `REAL_STATE_MODEL（真实态模型）`。
10. 基于真实态修订为 `T_MACHINE_STAR_REAL（真实态本机稳定理论极限）`；如修订，必须记录失效假设、证据、旧/新区间和原因，禁止因为跑得慢而随意放宽目标。
11. 执行 `MATURE_FRONTIER_SCAN（成熟前沿扫描）`：官方稳定方案、官方性能提交、同 GPU 架构/同 VRAM/同模型真实 A/B、成熟开源方案。
12. 建 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`；按“预期绝对收益 × 适用性 × 证据强度 ÷ 集成成本”排序。
13. 对高价值候选先做 `DATA_DRIVEN_REHEARSAL（数据驱动模拟推演）`：明确作用块、最多可省多少、新增开销/风险、回滚点、是否值得一次正式 benchmark。
14. 输出：`MATURE_HARVEST_ORDER（成熟收割顺序）` 与 `CUSTOM_ATTACK_ORDER（定制攻击顺序）`。
15. 排他 GPU benchmark（基准测试）串行；复杂规划/复盘用高强度推理，简单执行保持简洁。

## STEP 2 — HARVEST → TARGETED ATTACK → ROI STOP（成熟收割 → 定向攻击 → 收益停止）

### PHASE A — MATURE HARVEST（成熟收益收割）

16. 优先复用已被外部真实验证、且与当前任务高度匹配的成熟 workflow / version / official feature / model format / patch（工作流 / 版本 / 官方功能 / 模型格式 / 补丁）。
17. 外部 benchmark 只决定优先级，不自动决定本机 KEEP。
18. 同任务更快且硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
19. 成熟完整栈若不可合理拆分，可整体 A/B 后直接 KEEP；不要求先自行重构。
20. 每次 KEEP 后重新计算绝对 Gap，重新排序剩余成熟候选；不机械跑完低价值列表。

### PHASE B — RESIDUAL TARGETED ATTACK（剩余差距定向攻击）

21. 只有当 `HIGH_VALUE_MATURE_CANDIDATES_REMAINING=NO` 或成熟方案明显不适用，并且仍存在显著剩余 Gap 时，才允许进入深度 profiling（分块诊断）和自研攻击。
22. 每个自研候选必须满足：`REAL_DATA_SUPPORT=YES`、`MECHANISM_EXPLAINED=YES`、`EXPECTED_GAIN_ESTIMATED=YES`、`ROLLBACK_DEFINED=YES`。
23. 计算 `DELTA_T_REDUCIBLE（可消灭时间差）`，永远优先攻击最大绝对剩余 Gap。
24. 禁止长时间参数盲扫、无数据 kernel 猜测、连续创建“也许会快”的 Vn、已有成熟实现却自行重写、已有失败证据却无条件重测。
25. 更快且硬约束通过 => KEEP；否则 ROLLBACK；每次裁决后重新推演。

### PHASE C — ROI STOP（收益停止）

26. 不以“还能不能再省 0.5 秒”决定是否继续。
27. 估算：`EXPECTED_LIFETIME_BENEFIT ≈ DELTA_T_PER_RUN × EXPECTED_FUTURE_RUNS × VALUE_FACTOR`。
28. 只有当 `EXPECTED_LIFETIME_BENEFIT > ENGINEERING_COST + VALIDATION_COST + RISK_COST` 才继续迭代。
29. 如果继续优化的预期生命周期总收益不足以覆盖继续迭代成本，标记 `ECONOMIC_STOP=YES（经济性停止）`。
30. 对高频基础能力，小的单次节省仍可能非常值得；对一次性任务，同样的单次节省可能不值得。

### FINAL GATES（最终门禁）

31. 99 前确认 `MRE_REAL_STATE_CALIBRATION=PASS（真实态校准通过）`。
32. 确认 `MATURE_PATH_FIRST_GATE=PASS（成熟路径优先门禁通过）`。
33. 执行 `SOFTWARE_FRONTIER_GATE（软件前沿门禁）` 与当前边界内 `HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）`。
34. 确认 `RESIDUAL_HIGH_VALUE_GAP=NO` 或剩余 Gap 已触发合理 `ECONOMIC_STOP`。
35. 完成 Final Certification（最终认证）与 Shared Fact Source（共同事实源）同步后，才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
36. 冻结后把真实分块时间、成熟方案赢家、失败路线、Failure Index、MRE 真实态和 ROI 停止依据写入 `EMPIRICAL_PRIORS（经验先验）`。
37. 页面/会话过长时冻结阶段报告并换新页面；新页面从任务文件 + Shared Fact Source 恢复，禁止依赖超长会话继续硬撑。

```text
先算物理边界；
再用极简真实运行把纸面状态校准成真实运行状态；
先吃掉世界成熟方案已经验证的大收益；
再只攻击成熟方案吃不掉的最大剩余 Gap；
任何自研必须有真实数据、机制、收益预算和回滚；
最后按未来生命周期总收益，而不是单次毫秒，决定是否继续。
```
