---
name: first-principles-physical-limit-convergence
description: 在固定任务与硬约束下，先计算第一性原理物理极限，再用极简真实运行校准真实可实现极限；先吸收世界成熟方案，在推演层形成完整虚拟99路径，再由Codex做短时确定性验证；成熟大收益收割后必须再次做残余收益虚拟收敛，禁止数小时开放式探索；最终按剩余优化组合的未来生命周期总收益与总成本决定停止。
metadata:
  version: "1.5.0"
  short-description: 第一性原理物理极限收敛引擎·双层虚拟收敛/执行预算版
  lineage: first-principles-physical-limit-convergence@1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理物理极限收敛引擎 v1.5.0

## 总目标

```text
PRIMARY_OBJECTIVE（主目标）
= 最小化真实端到端执行时间

SECONDARY_OBJECTIVE（第二目标）
= 最小化达到稳定最优所需的工程时间与智能体资源成本
```

硬约束永远优先：任务必须真实完成，correctness（正确性）、quality（质量）、stability（稳定性）、safety（安全）必须通过；不得为了提速偷偷改变任务合同。

---

# 核心原则

## 1. 第一性原理不是自由探索

第一性原理负责：

- 冻结任务合同；
- 冻结当前真实硬件边界；
- 建立物理因果链；
- 计算 `T_PHY（第一性原理物理极限）`；
- 区分不可避免成本与可消灭成本；
- 给现实优化提供终极参照。

它**不要求重新发明官方、市场和成熟开源项目已经反复验证过的优化**。

只要存在高适用、高证据的成熟方案，就优先吸收成熟收益；禁止先进入无边界自研。

## 2. 复杂系统必须先得到“真实运行态”

静态硬件型号、软件版本、模型大小不能代表真正运行时的状态。

复杂任务必须尽快完成一次 `MRE（极简真实运行）`，让最小完整关键链真实跑通，得到真实：

- 阶段时间；
- 设备放置；
- 模型装载/卸载；
- 显存/内存；
- 缓存/预取/编译是否真正启用；
- 冷启动/预热/稳态差异；
- 实际运行故障和依赖；
- 真实关键路径。

## 3. 实际执行前先形成完整虚拟99铁路

禁止：

```text
发现一个点
→ 试一个点
→ 再发现一个点
→ 再试一个点
→ V1…Vn
```

正式路径：

```text
第一性原理极限
→ 极简真实运行
→ 真实态现实极限
→ 成熟方案吸收
→ 完整虚拟运行到99
→ 形成成熟执行铁路
→ Codex按铁路快速验证
```

## 4. 成熟大收益收割后，必须再次虚拟收敛

成熟方案通常先吃掉大头收益。此时剩余收益往往更小、更细、更相互耦合，但**不能因此把它交给 Codex 数小时慢慢摸索**。

必须用已经更完整的真实运行数据，再做一次：

```text
RESIDUAL_VIRTUAL_CONVERGENCE（残余收益虚拟收敛）
```

把剩余全部可行优化作为一个组合，在 GPT / 高质量推理层重新推演到停止点，形成新的短验证铁路。

## 5. 停止条件看“剩余优化组合”的长期总收益

不能因为某一个点只省 0.1 秒、0.5 秒就停止，也不能因为未来收益很大就默认允许数小时开放式执行。

必须同时满足两层判断：

1. 剩余优化组合在未来生命周期中的总收益是否大于总成本；
2. 这些优化是否已经被推演成短、确定、可验证的执行步骤。

如果还需要数小时开放式试错才能知道方向，说明**虚拟路径没有成熟**，应退回推演层，而不是继续消耗 Codex / GPU 配额。

---

# STEP 1 — 计算极限 + 极简真实运行 + 真实态校准

## 1.1 冻结任务合同

必须冻结：

```text
TASK_CONTRACT（任务合同）
TASK_COMPLETED（完成条件）
CORRECTNESS_GATE（正确性门禁）
QUALITY_GATE（质量门禁）
STABILITY_GATE（稳定门禁）
SAFETY_GATE（安全门禁）
TIMING_BOUNDARY（权威计时边界）
```

## 1.2 冻结当前有效硬件边界

```text
ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
= 此刻真实安装 + 可正常使用 + 本任务允许使用的硬件
```

未来计划增加但当前不存在的硬件，不进入本轮99，也不得阻断本轮99。

## 1.3 继承历史经验

若存在兼容历史任务，必须优先继承：

- `VERIFIED_99（已验证99）`；
- P50 / P95；
- KEEP / ROLLBACK（保留 / 回滚）；
- Failure Index（失败索引）；
- 真实阶段成本；
- 稳定 VRAM / RAM / I/O / 设备放置事实；
- 已证实有效和已证伪机制。

有证据时禁止重新从零探索。

## 1.4 计算第一性原理物理极限

```text
T_PHY（第一性原理物理极限）
= 固定任务在当前硬件边界、物理规律和不可避免工作量下的理论下界区间
```

未知效率使用区间 + 置信度，禁止伪精确。

## 1.5 计算现实极限初稿

```text
T_MACHINE_STAR_PRE（本机现实极限初算）
= 当前硬件
+ 当前软件
+ 已知成熟实现
+ 历史经验先验
下的稳定理论区间初稿
```

## 1.6 做一次 MRE（极简真实运行）

复杂系统必须尽快让最小完整链真实运行。

默认目标：约10分钟级工程时间内获得足以校准方向的数据；若任务本身物理运行时间更长，则使用机制一致的最小合同或最小子合同。

MRE不是性能终测，而是“真实态校准器”。

## 1.7 建立 REAL_STATE_MODEL（真实态模型）

```text
T_PHY
+ STATIC_FACTS（静态事实）
+ MRE_OBSERVATIONS（极简真实运行数据）
+ EMPIRICAL_PRIORS（经验先验）
= REAL_STATE_MODEL（真实态模型）
→ T_MACHINE_STAR_REAL（真实态本机稳定理论极限）
```

如现实数据推翻初始假设，必须记录：失效假设、新证据、旧区间、新区间、修订原因。

这是模型校正，不是为了通过99而随意放宽目标。

---

# STEP 2 — 成熟方案吸收 + 完整虚拟99路径 + 快速验证 + 残余虚拟收敛

## 2.1 扫描世界成熟方案

优先顺序：

1. 官方稳定方案与官方性能提交；
2. 同硬件、同模型、同任务或高度相似任务的真实成熟方案；
3. 反复验证的成熟开源工程；
4. 本机历史成功经验包；
5. 大量社区重复验证且机制清楚的方案。

成熟方案可包括：workflow（工作流）、runtime（运行时）、model format（模型格式）、quantization（量化）、cache（缓存）、prefetch（预取）、compiler（编译）、memory management（内存管理）、model management（模型管理）、device placement（设备分配）等。

## 2.2 建立 MATURE_HARVEST_MATRIX（成熟收益收割矩阵）

至少记录：

```text
SOURCE_LEVEL（来源等级）
HARDWARE_MATCH（硬件匹配）
TASK_MATCH（任务匹配）
MECHANISM（机制）
TARGET_BLOCK（目标时间块）
EXPECTED_ABS_GAIN（预期绝对收益）
QUALITY_RISK（质量风险）
STABILITY_RISK（稳定风险）
INTEGRATION_COST（集成成本）
REVERSIBILITY（可逆性）
CURRENTLY_PRESENT（当前是否已有）
```

优先“大收益、强证据、高适用、低成本、可逆”。

## 2.3 构建 VIRTUAL_MATURE_PATH（虚拟成熟路径）

不是只评估一个候选，而是把从当前真实状态到99的完整路线先推演出来：

```text
CURRENT_REAL_STATE（当前真实态）
→ 成熟方案1
→ 成熟方案2
→ 剩余最大Gap攻击1
→ 剩余最大Gap攻击2
→ ……
→ 99
```

每一步必须包含：

```text
STEP（步骤）
CURRENT_STATE（当前状态）
TARGET_BLOCK（攻击块）
MECHANISM（方法）
SOURCE（成熟来源/真实数据）
EXPECTED_REMOVABLE_TIME（预计可消灭时间）
NEW_OVERHEAD（新增开销）
PROJECTED_RESULT（预计结果）
RISK（风险）
ROLLBACK（回滚）
VERIFICATION（Codex验证方法）
EXPECTED_EXECUTION_TIME（预计执行时间）
EXPECTED_GPU_RUNS（预计GPU运行次数）
EXPECTED_CODEX_COST（预计Codex成本）
```

前一步预计结果必须成为后一步输入；禁止简单累加各点理论收益。

## 2.4 Codex只做快速验证

Codex默认角色：

```text
VALIDATOR / EXECUTOR（验证器 / 执行器）
```

不负责开放式寻找优化方向。

Codex只执行已经具备以下条件的步骤：

- 明确目标；
- 明确修改；
- 明确预计结果；
- 明确计时和QC；
- 明确成功/失败条件；
- 明确回滚；
- 明确时间/运行次数/配额预算；
- 明确停止点。

如果：

```text
ACTUAL_RESULT（实测） != PROJECTED_RESULT（预计）
```

立即停止自由延伸，保存证据，把新事实返回高质量推理层重新计算剩余虚拟路径。

## 2.5 成熟大收益后必须做 RESIDUAL_VIRTUAL_CONVERGENCE（残余收益虚拟收敛）

成熟方案大头吃完后，利用更新后的真实数据重新执行一次虚拟攻击迭代。

把剩余优化点按真实依赖组成：

```text
RESIDUAL_VIRTUAL_PATH（残余虚拟路径）
```

每个点都必须有：

```text
CURRENT_BLOCK_TIME（当前块时间）
MECHANISM（机制）
SOURCE（成熟依据/真实证据）
EXPECTED_GAIN（预计收益）
INTERACTION（交互）
NEW_OVERHEAD（新增开销）
VALIDATION_COST（验证成本）
QUALITY/STABILITY_RISK（质量/稳定风险）
ROLLBACK（回滚）
```

这一阶段的主要复杂工作仍在 GPT / 高质量推理层完成。

## 2.6 禁止小时级开放式验证

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
（禁止数小时开放式验证）
```

正常验证应是分钟级或接近固定任务自身必要运行时间；任务本身物理上很长时可以按任务物理时长缩放，但额外探索工程时间不得无限增长。

如果某个优化需要不断试参数、改代码、再测数小时才能知道方向：

```text
VALIDATION_PLAN_NOT_MATURE=YES（验证计划不成熟）
→ STOP EXECUTION（停止执行）
→ RETURN TO VIRTUAL REHEARSAL（退回虚拟推演）
```

如果实际执行明显超过预计预算且没有对应信息增益：

```text
BUDGET_DRIFT=YES（预算漂移）
→ SAFE STOP（安全停止）
→ 保存已有证据
→ 回到虚拟推演层
```

## 2.7 自研攻击的唯一入口

只有成熟方案无法覆盖显著剩余 Gap，而且真实数据已明确指向具体机制时，才允许定向自研。

每个自研步骤必须同时满足：

```text
REAL_DATA_SUPPORT=YES（有真实数据）
MECHANISM_EXPLAINED=YES（机制清楚）
EXPECTED_GAIN_ESTIMATED=YES（收益已估算）
ROLLBACK_DEFINED=YES（回滚明确）
EXECUTION_BUDGET_DEFINED=YES（执行预算明确）
```

否则不执行。

---

# PORTFOLIO ROI（剩余组合收益停止）

## 3.1 不能按单点停止

剩余可行优化：

```text
S = {优化点1, 优化点2, …, 优化点n}
```

必须按真实顺序在 `RESIDUAL_VIRTUAL_PATH（残余虚拟路径）` 中整体推演。

## 3.2 组合单次总收益

```text
DELTA_T_PORTFOLIO（组合单次总节省）
= T_CURRENT（当前一次任务时间）
- T_PROJECTED_FINAL（全部剩余优化完成后的预计一次任务时间）
```

使用顺序推演后的最终差值，禁止简单求和。

## 3.3 未来生命周期总收益

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO（组合未来总收益）
≈ DELTA_T_PORTFOLIO
× EXPECTED_FUTURE_RUNS（预计未来运行次数）
× VALUE_FACTOR（时间/算力/等待价值系数）
+ 其他可量化资源收益
```

## 3.4 剩余组合总成本

```text
PORTFOLIO_COST（组合总成本）
= GPT/Codex 配额与推理成本
+ 工程实施成本
+ 实机验证成本
+ GPU/CPU/电力/等待成本
+ 风险成本
+ 集成交互成本
+ 必要维护成本
```

如果：

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO > PORTFOLIO_COST
```

继续把这些优化纳入残余虚拟路径。

否则：

```text
PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）
```

**重要：**即使未来组合收益很大，也不等于允许数小时开放式探索；大收益只说明“值得继续设计和验证”，实际执行仍必须先被压缩成短、确定、有边界的成熟验证路线。

---

# 99 / FREEZE（99 / 冻结）

99不是数学绝对极限，也不是固定1%阈值。

必须同时满足：

1. 固定任务真实完成；
2. correctness / quality / stability / safety 全部通过；
3. 权威计时稳定；
4. `T_PHY（第一性原理物理极限）` 已计算；
5. `MRE_REAL_STATE_CALIBRATION=PASS（极简真实运行与真实态校准通过）`；
6. `T_MACHINE_STAR_REAL（真实态本机稳定理论极限）` 已建立；
7. `MATURE_PATH_FIRST_GATE=PASS（成熟路径优先门禁通过）`；
8. 首轮 `VIRTUAL_MATURE_PATH_COMPLETE=YES（完整虚拟成熟路径已形成）`；
9. 成熟大收益已系统收割；
10. `RESIDUAL_VIRTUAL_PATH_COMPLETE=YES（残余收益虚拟路径已形成）`；
11. `PORTFOLIO_ROI_EVALUATED=YES（剩余组合生命周期收益已计算）`；
12. `CODEX_VALIDATION_PATH_BOUNDED=YES（Codex验证路径短且有边界）`；
13. `NO_MULTI_HOUR_EXPLORATION_REQUIRED=YES（不依赖数小时自由探索）`；
14. `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）`；
15. `HARDWARE_TOPOLOGY_GATE=PASS（当前硬件拓扑门禁通过）`；
16. 当前结果进入/贴近高置信 `T_MACHINE_STAR_REAL`，或剩余组合已满足 `PORTFOLIO_ECONOMIC_STOP`；
17. Final Certification（最终认证）通过；
18. Shared Fact Source（共同事实源）同步并 remote verify（远端验证）通过。

因此：

> **99 = 当前真实硬件边界 + 真实运行校准 + 世界成熟大收益 + 首轮完整虚拟99铁路 + Codex短验证 + 成熟收割后的残余虚拟收敛 + 剩余组合生命周期ROI停止后的稳定最优。**

---

# 执行与上下文纪律

- 高质量推理层负责：极限计算、真实态建模、成熟方案吸收、两轮虚拟路径、收益/成本推演、停止条件。
- Codex负责：精确执行、短验证、QC、证据、回滚、Git收口。
- 单GPU正式 benchmark（基准测试）必须串行、独占。
- 页面/会话明显过长时，冻结阶段报告并换新页面；新页面通过任务文件 + Shared Fact Source 恢复。
- 所有新工程事实必须形成正式报告、机器可读状态并同步共同工作区。

---

# 默认最短读取路径

正常任务优先读取：

1. `SKILL.md`
2. `references/FAST-PATH.md`
3. `references/REAL-STATE-MATURE-HARVEST-ROI.md`
4. `references/RESIDUAL-VIRTUAL-CONVERGENCE-BUDGET.md`

按需读取：

- `references/FIRST-PRINCIPLES-LIMIT-MODEL.md`
- `references/SOFTWARE-FRONTIER-GATE.md`
- `references/HARDWARE-TOPOLOGY-GATE.md`
- `references/MATURE-PATH-FIRST-GATE.md`
- `references/MULTI-AGENT-PARALLELISM.md`
- `references/EXECUTION-BRIDGE.md`
- `references/EXECUTION-CLOSURE-CONTRACT.md`
- `references/FAILURE-INDEX.md`

## 状态

```text
SKILL_VERSION=1.5.0
TWO_MAJOR_STEPS=PASS（两大步结构通过）
FIRST_PRINCIPLES_BOUND_DEFINED=PASS（第一性原理边界已定义）
MRE_REAL_STATE_CALIBRATION_DEFINED=PASS（极简真实运行/真实态校准已定义）
MATURE_HARVEST_DEFINED=PASS（成熟方案收割已定义）
FULL_VIRTUAL_99_PATH_DEFINED=PASS（完整虚拟99路径已定义）
RESIDUAL_VIRTUAL_CONVERGENCE_DEFINED=PASS（残余收益虚拟收敛已定义）
PORTFOLIO_LIFETIME_ROI_DEFINED=PASS（组合生命周期收益已定义）
CODEX_BOUNDED_VALIDATION_DEFINED=PASS（Codex短验证边界已定义）
NO_MULTI_HOUR_OPEN_ENDED_EXPLORATION=YES（禁止数小时开放式探索）
CONTEXT_HYGIENE_DEFINED=PASS（上下文卫生已定义）
```
