# FAST PATH — 远端共同工作区 + 第一性原理 + 真实态 + 双层虚拟成熟路径 v1.6

## STEP 0 — PROJECT REMOTE WORKSPACE（项目远端共同工作区）

0.1 先声明：

```text
PROJECT_ID（项目ID）
SHARED_WORKSPACE_TYPE（共同工作区类型）
SHARED_WORKSPACE_REMOTE（远端共同工作区）
SHARED_WORKSPACE_BRANCH（远端分支，如适用）
SHARED_WORKSPACE_PROJECT_PATH（远端项目路径，如适用）
LOCAL_EXECUTION_CHECKOUT（本地执行副本，可选）
REMOTE_VERIFY_REQUIRED=YES（必须远端核验）
```

0.2 硬规则：

```text
SHARED_WORKSPACE_IS_REMOTE=YES（共同工作区必须是远端在线空间）
LOCAL_PATH_IS_SHARED_WORKSPACE=NO（本地路径绝不等于共同工作区）
```

0.3 不同项目可以使用不同远端共同工作区；不得默认沿用上一个项目的仓库。

0.4 读取顺序固定为：

```text
REMOTE LOCATE（远端定位）
→ FETCH / PULL（拉取）
→ LOCAL CHECKOUT（本地检出）
→ EXECUTE（执行）
→ REPORT（报告）
→ PUSH（推送）
→ REMOTE VERIFY（远端核验）
```

0.5 如果项目远端共同工作区没有声明清楚，`PROJECT_WORKSPACE_DECLARATION_GATE=BLOCKED（项目工作区声明门禁阻断）`，不得通过本机递归搜索来猜共同工作区。

## STEP 1 — CALCULATE + REAL RUN（计算 + 极简真实运行）

1. 冻结 `TASK_CONTRACT（任务合同）`、`TASK_COMPLETED（完成条件）`、correctness / quality / stability / safety（正确性 / 质量 / 稳定 / 安全）和权威计时边界。
2. 冻结 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`：只包含此刻真实安装、可正常使用、允许用于本任务的硬件。
3. 从本项目远端 `SHARED_FACT_SOURCE（共同事实源）` 继承兼容的 `VERIFIED_99（已验证99）`、`EMPIRICAL_PRIORS（经验先验）`、Failure Index（失败索引）、KEEP / ROLLBACK（保留 / 回滚）和已证伪机制；禁止从零重复探索。
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

15. 每一步写清：当前状态、攻击时间块、机制、成熟来源/真实数据依据、预计可消灭时间、新增开销、预计结果、风险、回滚、Codex验证方法、预计执行时间、预计GPU运行次数、预计Codex成本。
16. 前一步预计结果必须成为后一步输入；禁止简单相加各候选收益而忽略重叠、交互和新增成本。
17. 实际执行前必须先把“从当前真实态到99”的整条虚拟成熟路径推演完成。
18. 虚拟路径无法解释的关键 Gap 才允许进入定向自研；不得进入自由探索。

## STEP 3 — CODEX FAST VALIDATION（Codex快速验证）

19. Codex默认角色是 `VALIDATOR / EXECUTOR（验证器 / 执行器）`：精确部署、指定运行、证据采集、QC、KEEP/ROLLBACK、Git收口；不负责自己寻找方向。
20. 实际执行拆成短、明确、有边界的小验证任务，按虚拟成熟路径顺序执行。
21. 实测与预计一致且更快、硬约束通过 => `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
22. 如果 `ACTUAL_RESULT（实测结果） != PROJECTED_RESULT（预计结果）`，立即停止自由延伸，把新事实回传高质量推理层，重新计算剩余虚拟路径。
23. 每个产生新工程事实的步骤完成后，先形成正式报告/机器状态，再推送到本项目远端共同工作区并 `REMOTE_VERIFY（远端核验）`；本地提交不等于共同事实完成。

## STEP 4 — RESIDUAL VIRTUAL CONVERGENCE（残余收益再次虚拟收敛）

24. 成熟大收益收割后，不把剩余小收益交给 Codex 慢慢探索。
25. 用最新真实数据、成熟方案结果、Failure Index 和经验先验，再执行一次 `RESIDUAL_VIRTUAL_CONVERGENCE（残余收益虚拟收敛）`。
26. 把所有剩余可行优化按真实依赖组成 `RESIDUAL_VIRTUAL_PATH（残余虚拟路径）`；每个点必须有机制、预计收益、交互、新增开销、验证成本、风险和回滚。
27. 这一阶段的主要工作在 GPT / 高质量推理层完成；Codex 仍只做短而确定的验证。
28. 如果某个剩余优化需要不断试参数、改代码、再测数小时才能知道方向，则：

```text
VALIDATION_PLAN_NOT_MATURE=YES（验证计划不成熟）
→ STOP EXECUTION（停止执行）
→ RETURN TO VIRTUAL REHEARSAL（退回虚拟推演）
```

29. 正常验证应为分钟级或接近固定任务自身必要运行时间；额外探索时间不得无限增长。
30. 每次验证前写明 `EXPECTED_EXECUTION_TIME（预计执行时间）`、`EXPECTED_GPU_RUNS（预计GPU运行次数）`、`EXPECTED_CODEX_COST（预计Codex成本）`、证据产出和停止条件；明显超预算且信息增益不足则安全停止并回到推演层。

## STEP 5 — PORTFOLIO ROI STOP（组合收益停止）

31. 停止条件不能逐个点孤立判断。把所有剩余可行优化视为组合 `S={优化点1…n}`，按真实顺序推演。
32. `DELTA_T_PORTFOLIO（组合单次总节省） = T_CURRENT（当前一次运行时间） - T_PROJECTED_FINAL（剩余组合完成后的预计一次运行时间）`。
33. `EXPECTED_LIFETIME_BENEFIT_PORTFOLIO（组合未来总收益） ≈ DELTA_T_PORTFOLIO × EXPECTED_FUTURE_RUNS（预计未来运行次数） × VALUE_FACTOR（时间/资源价值系数） + 其他可量化资源收益`。
34. `PORTFOLIO_COST（组合总成本） = GPT/Codex配额成本 + 工程实施成本 + 实机验证成本 + 风险成本 + 集成交互成本 + 必要维护成本`。
35. 若组合未来总收益大于组合总成本，继续把剩余组合纳入虚拟路径；否则 `PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）`。
36. 对高频基础能力，即使单点收益很小，只要组合长期收益足够大仍应继续；但继续方式仍是“再次虚拟收敛 → 短验证”，不是数小时本机摸索。

## FINAL — 99 / FREEZE（99 / 冻结）

37. `PROJECT_WORKSPACE_DECLARATION_GATE=PASS（项目工作区声明门禁通过）`。
38. `T_PHY（第一性原理物理极限）` 已计算、MRE 已完成、`T_MACHINE_STAR_REAL（真实态本机稳定理论极限）` 已校准、成熟方案已系统吸收、首次 `VIRTUAL_MATURE_PATH（虚拟成熟路径）` 已完整推演。
39. `RESIDUAL_VIRTUAL_PATH_COMPLETE=YES（残余虚拟路径已完成）`。
40. `CODEX_VALIDATION_PATH_BOUNDED=YES（Codex验证路径短且有边界）`，并且不需要数小时开放式探索。
41. 剩余组合已完成生命周期收益计算：要么值得继续且已纳入路径，要么 `PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）`。
42. correctness / quality / stability / safety 全部通过。
43. Final Certification（最终认证）通过。
44. 所有正式新工程事实已经推送到本项目 `SHARED_WORKSPACE_REMOTE（远端共同工作区）` 并 `REMOTE_VERIFY=PASS（远端核验通过）`，才允许 `99=YES / FREEZE=YES / FINAL=PASS`。
45. 冻结后，把真实时间、成熟方案赢家、失败路线、两轮虚拟路径、组合收益、执行预算漂移、Failure Index 写入远端 `EMPIRICAL_PRIORS（经验先验）`。
46. 页面/会话过长时冻结阶段报告并换新页面，新页面从任务文件 + 远端共同事实源恢复。

```text
先声明本项目的远端共同工作区；
本地目录只作为执行副本；
再算物理极限；
用极简真实运行得到真实态和现实极限；
先吃掉世界成熟方案的大收益；
先在推演层形成完整虚拟99铁路；
Codex只做短验证；
成熟大头吃完以后，再做残余收益虚拟收敛；
最后按剩余组合未来总收益与总成本决定是否继续；
所有正式新事实必须写回远端共同工作区并远端核验后才算完成。
```
