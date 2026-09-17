# FAST PATH — 第一性原理 + 真实态 + 双层虚拟成熟路径 v1.5

## STEP 1 — CALCULATE + REAL RUN（计算 + 极简真实运行）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）`、correctness / quality / stability / safety（正确性 / 质量 / 稳定 / 安全）和权威计时边界。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻真实安装、可正常使用、允许用于本任务的硬件。
3. 继承兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）、KEEP / ROLLBACK（保留 / 回滚）和已证伪机制；禁止从零重复探索。
4. 建立 `PHYSICAL_DAG（物理因果图）` 与关键路径。
5. 推导 `T_PHY（第一性原理物理极限）=[LOW,HIGH]`。
6. 根据当前硬件、当前软件、成熟实现和经验先验，先算 `T_MACHINE_STAR_PRE（本机现实极限初算）=[LOW,HIGH]`。
7. 对复杂系统必须尽快做 `MRE（极简真实运行）`：让最小完整链真实跑通。默认目标是在约10分钟级工程时间内得到足够真实态数据；若任务本身物理上更长，则使用机制一致的最小合同/最小子合同。
8. MRE 必须暴露真实：各阶段时间、冷/热状态、设备放置、模型装载/卸载、显存/内存、缓存/预取/编译、依赖和运行故障。
9. 用 `T_PHY + STATIC_FACTS（静态事实） + MRE_OBSERVATIONS（极简真实运行观测） + EMPIRICAL_PRIORS（经验先验）` 建立 `REAL_STATE_MODEL（真实态模型）`。
10. 校准为 `T_MACHINE_STAR_REAL（真实态本机稳定理论极限）`；记录被修正的假设和证据，禁止因为结果慢而随意放宽目标。

## STEP 2 — MATURE HARVEST + FULL VIRTUAL 99 PATH（成熟收割 + 完整虚拟99路径）

11. 执行 `MATURE_FRONTIER_SCAN（成熟前沿扫描）`：官方成熟方案、同硬件/同模型实测方案、成熟开源路径、本机历史成功经验。
12. 建立 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`，去掉与当前真实瓶颈、任务合同或硬件不匹配的方案。
13. 先吸收“大收益、强证据、高适用、低成本、可逆”的成熟模块。
14. 基于 `REAL_STATE_MODEL（真实态模型）`，先构建从当前真实态到99的 `VIRTUAL_MATURE_PATH（虚拟成熟路径）`：

```text
当前真实状态
→ 成熟方案1
→ 成熟方案2
→ 剩余最大Gap攻击1
→ 剩余最大Gap攻击2
→ ……
→ 99
```

15. 每一步必须写清：当前状态、攻击时间块、机制、成熟来源/真实数据依据、预计可消灭时间、新增开销、预计结果、风险、回滚和 Codex 验证方法。
16. 前一步预计结果必须成为后一步输入；禁止把各候选收益简单相加而忽略重叠、交互和新增成本。
17. 在实际执行前，必须先把“从当前真实态到99”的整条虚拟成熟路径推演完成。
18. 虚拟路径无法解释的关键 Gap 才允许进入定向自研；不得进入自由探索。

## STEP 3 — CODEX FAST VALIDATION（Codex快速验证）

19. Codex 的默认角色是 `VALIDATOR / EXECUTOR（验证器 / 执行器）`：精确部署、指定运行、证据采集、QC、KEEP/ROLLBACK、Git 收口；不负责自己寻找方向。
20. 实际执行拆成短、明确、有边界的小验证任务，按虚拟成熟路径顺序执行。
21. 实测与预计一致且更快、硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
22. 如果 `ACTUAL_RESULT（实测结果） != PROJECTED_RESULT（预计结果）`，立即停止自由延伸，把新事实回传高质量推理层，重新计算剩余虚拟路径。
23. 禁止因为某个方向已经开始就连续产生 V1…Vn 的探索链。

## STEP 4 — RESIDUAL VIRTUAL CONVERGENCE（残余收益再次虚拟收敛）

24. 成熟大收益收割后，不把剩余小收益交给 Codex 慢慢探索。
25. 用最新真实数据、成熟方案结果、Failure Index 和经验先验，再执行一次 `RESIDUAL_VIRTUAL_CONVERGENCE（残余收益虚拟收敛）`。
26. 把所有剩余可行优化按真实依赖组成 `RESIDUAL_VIRTUAL_PATH（残余虚拟路径）`；每个点必须有机制、预计收益、交互、新增开销、验证成本、风险和回滚。
27. 这一阶段的主要工作在 GPT / 高质量推理层完成；Codex 仍只做短而确定的验证。
28. 如果某个剩余优化需要“不断试参数、改代码、再测数小时”才能知道方向，则：

```text
VALIDATION_PLAN_NOT_MATURE=YES（验证计划不成熟）
→ STOP EXECUTION（停止执行）
→ RETURN TO VIRTUAL REHEARSAL（退回虚拟推演）
```

29. 正常验证应为分钟级或接近固定任务自身必要运行时间；任务本身物理上很长时可按物理时长缩放，但额外探索时间不得无限增长。
30. 每次验证前写明 `EXPECTED_EXECUTION_TIME（预计执行时间）`、`EXPECTED_GPU_RUNS（预计GPU运行次数）`、`EXPECTED_CODEX_COST（预计Codex成本）`、证据产出和停止条件；明显超预算且信息增益不足则安全停止并回到推演层。

## STEP 5 — PORTFOLIO ROI STOP（组合收益停止）

31. 停止条件不能逐个点孤立判断。把所有剩余可行优化视为组合 `S={优化点1…n}`，按真实顺序推演。
32. 计算：

```text
DELTA_T_PORTFOLIO（组合单次总节省）
= T_CURRENT（当前一次运行时间）
- T_PROJECTED_FINAL（剩余组合全部完成后的预计一次运行时间）
```

禁止把各点理论收益直接相加造成重复计算。
33. 计算未来生命周期总收益：

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO（组合未来总收益）
≈ DELTA_T_PORTFOLIO
× EXPECTED_FUTURE_RUNS（预计未来运行次数）
× VALUE_FACTOR（时间/资源价值系数）
+ 其他可量化资源收益
```

34. 计算剩余组合总成本：

```text
PORTFOLIO_COST（组合总成本）
= GPT/Codex 配额成本
+ 工程实施成本
+ 实机验证成本
+ 风险成本
+ 集成交互成本
+ 必要维护成本
```

35. 若 `EXPECTED_LIFETIME_BENEFIT_PORTFOLIO > PORTFOLIO_COST`，继续把剩余组合纳入虚拟路径；否则 `PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）`。
36. 对高频基础能力，即使单点收益很小，只要组合长期收益足够大仍应继续；但继续的方式仍是“再次虚拟收敛 → 短验证”，不是“数小时本机摸索”。

## FINAL — 99 / FREEZE（99 / 冻结）

37. 必须确认：`T_PHY` 已计算、MRE 已完成、`T_MACHINE_STAR_REAL` 已校准、成熟方案已系统吸收、首次 `VIRTUAL_MATURE_PATH` 已完整推演。
38. 成熟收割后，`RESIDUAL_VIRTUAL_PATH_COMPLETE=YES（残余虚拟路径已完成）`。
39. `CODEX_VALIDATION_PATH_BOUNDED=YES（Codex验证路径短且有边界）`，并且不需要数小时开放式探索。
40. 剩余优化组合已完成生命周期 ROI 计算：要么值得继续且已纳入路径，要么 `PORTFOLIO_ECONOMIC_STOP=YES`。
41. correctness / quality / stability / safety 全部通过。
42. 完成 Final Certification（最终认证）和 Shared Fact Source（共同事实源）收口后，才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
43. 冻结后，把真实时间、成熟方案赢家、失败路线、两轮虚拟路径、组合 ROI、执行预算漂移、Failure Index 写入 `EMPIRICAL_PRIORS（经验先验）`。
44. 页面/会话过长时冻结阶段报告并换新页面，新页面从任务文件 + 共同事实源恢复。

```text
先算物理极限；
再用极简真实运行得到真实态和现实极限；
先吃掉世界成熟方案的大收益；
先在推演层形成完整虚拟99铁路；
Codex只做短验证；
成熟大头吃完以后，再做一次残余收益虚拟收敛，把剩余小收益组合和停止点算清；
只有短而确定的执行才交给Codex；
任何需要数小时开放式探索的计划都视为虚拟路径尚未成熟；
最后按剩余全部优化组合在未来大规模运行中的总收益与总成本决定是否继续。
```
