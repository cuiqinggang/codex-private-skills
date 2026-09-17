# FAST PATH — 第一性原理 + 真实态 + 虚拟成熟路径 v1.4

## STEP 1 — CALCULATE + REAL RUN（计算 + 极简真实运行）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）`、hard constraints（硬约束）。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻真实安装、可正常使用、允许用于本任务的硬件。
3. 继承最近兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）和已证伪机制；禁止从零重复探索。
4. 建立 `PHYSICAL_DAG（物理因果图）` 与关键路径。
5. 推导 `T_PHY（第一性原理物理极限）=[LOW,HIGH]`。
6. 根据当前硬件、当前软件、已知成熟实现和经验先验，计算 `T_MACHINE_STAR_PRE（现实极限初算）=[LOW,HIGH]`。
7. 对复杂系统必须尽快做 `MRE（极简真实运行）`：让最小完整链真实跑通。默认目标是在约10分钟级工程时间内获得足够真实数据；任务本身更长时，使用机制一致的最小合同。
8. MRE 必须暴露真实：各阶段时间、冷/热状态、设备放置、模型装载/卸载、显存/内存、缓存/预取/编译、依赖和运行故障。
9. 用 `T_PHY + STATIC FACTS（静态事实） + MRE OBSERVATIONS（极简真实运行观测） + EMPIRICAL_PRIORS（经验先验）` 建立 `REAL_STATE_MODEL（真实态模型）`。
10. 校准为 `T_MACHINE_STAR_REAL（真实态本机稳定理论极限）`；必须记录被修正的假设和证据，禁止因为结果慢而随意放宽目标。

## STEP 2 — MATURE HARVEST + VIRTUAL 99 PATH（成熟收割 + 虚拟99路径）

11. 执行 `MATURE_FRONTIER_SCAN（成熟前沿扫描）`：官方成熟方案、同硬件/同模型实测方案、成熟开源路径、本机历史成功经验。
12. 建立 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`，去掉与当前真实瓶颈和任务合同不匹配的方案。
13. 优先吸收“大收益、强证据、高适用、低成本、可逆”的成熟模块。
14. **不要只对单个候选做零散判断。**基于 `REAL_STATE_MODEL（真实态模型）`，必须先构建完整的 `VIRTUAL_MATURE_PATH（虚拟成熟路径）`：

```text
当前真实状态
→ 成熟方案1
→ 成熟方案2
→ 剩余最大Gap攻击1
→ 剩余最大Gap攻击2
→ ……
→ 99
```

15. 每一步都必须写清：当前状态、攻击时间块、采用机制、成熟来源/真实数据依据、预计可消灭时间、新增开销、预计结果、风险、回滚、Codex验证方式。
16. 每一步预计结果成为下一步的输入；禁止把各候选收益简单相加而忽略重叠和交互。
17. 在真正长时间执行前，必须先把“从当前真实态到99”的整条虚拟成熟路径完整推演出来。
18. 如果虚拟路径无法解释某个关键Gap，才允许把该Gap列为后续定向自研项；不得直接进入自由探索。

## STEP 3 — CODEX VALIDATION（Codex快速验证）

19. Codex 主要负责：精确部署、指定运行、证据采集、QC、KEEP/ROLLBACK、Git收口；不负责自行发明优化路线。
20. 实际执行应拆成短而明确的小验证任务，按虚拟成熟路径顺序执行。
21. 实测与预计一致且更快、硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
22. 如果 `ACTUAL_RESULT（实测结果） != PROJECTED_RESULT（预计结果）`，停止自由延伸，回到高质量推理层，用新数据重新计算剩余虚拟路径，再继续。
23. 禁止因为某个方向已经开始就连续产生 V1…Vn 的探索链。

## STEP 4 — PORTFOLIO ROI STOP（组合收益停止）

24. 停止条件不能逐个点孤立判断，也不能只问“这个点还能不能省0.5秒”。
25. 把所有剩余可行优化视为组合 `S={优化点1…n}`，在虚拟路径中按真实依赖顺序推演。
26. 计算：

```text
DELTA_T_PORTFOLIO（组合单次总节省）
= T_CURRENT（当前一次运行时间）
- T_PROJECTED_FINAL（剩余组合全部完成后的预计一次运行时间）
```

禁止把各点理论收益直接相加造成重复计算。
27. 计算未来生命周期总收益：

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO（组合未来总收益）
≈ DELTA_T_PORTFOLIO
× EXPECTED_FUTURE_RUNS（预计未来运行次数）
× VALUE_FACTOR（时间/资源价值系数）
+ 其他可量化资源收益
```

28. 计算剩余组合总成本：

```text
PORTFOLIO_COST（组合总成本）
= 工程实施成本
+ 验证成本
+ 风险成本
+ 集成交互成本
+ 必要维护成本
```

29. 如果 `EXPECTED_LIFETIME_BENEFIT_PORTFOLIO > PORTFOLIO_COST`，继续把这些优化纳入虚拟99路径；否则 `PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）`。
30. 对高频基础能力，即使单点收益很小，只要未来运行次数足够大，仍应继续；对低频一次性任务则反之。

## FINAL — 99 / FREEZE（99 / 冻结）

31. 必须确认：`T_PHY` 已计算、MRE 已完成、`T_MACHINE_STAR_REAL` 已校准、成熟方案已系统吸收、`VIRTUAL_MATURE_PATH` 已完整推演到99。
32. 实际执行必须按成熟路径验证；偏离时必须重新推演，禁止无边界自由探索。
33. 剩余优化必须按组合生命周期收益判断：要么高收益已吃完，要么 `PORTFOLIO_ECONOMIC_STOP=YES`。
34. correctness / quality / stability / safety 全部通过。
35. 完成 Final Certification（最终认证）和 Shared Fact Source（共同事实源）收口后，才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
36. 冻结后，把真实时间、成熟方案赢家、失败路线、虚拟路径、组合ROI停止依据、Failure Index 写入 `EMPIRICAL_PRIORS（经验先验）`。
37. 页面/会话过长时冻结阶段报告并换新页面，新页面从任务文件 + 共同事实源恢复。

```text
先算物理极限；
再用极简真实运行得到真实态和现实极限区间；
再把世界成熟方案吸收进来；
在真实数据上先把“从现在到99”的整条虚拟成熟路径完整跑通；
Codex只按这条路径做短而明确的验证；
最后不是看单个小优化点，而是看剩余全部优化组合在未来大规模运行中的总收益是否大于整个组合的总成本。
```
