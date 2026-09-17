---
name: first-principles-physical-limit-convergence
description: 在固定任务与硬约束下，以时间为主优化目标；先用第一性原理计算物理边界，再用极简真实运行校准真实执行态，优先收割世界成熟方案，只对成熟方案无法覆盖的最大剩余 Gap 做有数据支撑的定向攻击，并按生命周期 ROI 决定何时停止。
metadata:
  version: "1.3.0"
  short-description: 第一性原理物理极限收敛引擎·真实态/成熟收割/ROI版
  lineage: first-principles-physical-limit-convergence@1.2.0 <- @1.1.0 <- @1.0.0 <- absolute-time-fireworks-optimization@2.0.1
---

# 第一性原理物理极限收敛引擎 v1.3.0

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END（最小化真实端到端时间）
SECONDARY_OBJECTIVE = MINIMIZE T_CONVERGENCE（最小化达到稳定最优的工程时间）

SUBJECT TO（硬约束）:
TASK_COMPLETED == TRUE（任务真实完成）
CORRECTNESS == PASS（正确性通过）
QUALITY >= FIXED_THRESHOLD（质量达到固定阈值）
STABILITY >= FIXED_THRESHOLD（稳定性达到固定阈值）
SAFETY == PASS（安全通过）
TASK_CONTRACT == IDENTICAL（任务合同一致）
```

## 核心定义

### 第一性原理不等于自由探索

第一性原理负责：

- 冻结任务合同和当前真实硬件边界；
- 建立不可避免步骤与物理因果链；
- 计算 `T_PHY（物理极限）`；
- 识别假设、约束和剩余 Gap。

第一性原理**不要求重新发明已有成熟优化**。如果市场、官方、同硬件实测已经提供高置信成熟路径，必须优先复用并本机 A/B。

默认主路径：

```text
FIRST-PRINCIPLES BOUND（第一性原理边界）
→ MINIMAL REAL RUN（极简真实运行）
→ REAL-STATE CALIBRATION（真实态校准）
→ MATURE HARVEST（成熟方案收割）
→ DATA-DRIVEN REHEARSAL（数据驱动模拟推演）
→ TARGETED ATTACK（定向攻击）
→ ROI STOP（收益停止）
→ 99 / FREEZE（99 / 冻结）
```

---

# STEP 1 — CALCULATE + REAL-STATE CALIBRATION（计算 + 真实态校准）

## 1. 冻结边界

冻结：

```text
TASK_CONTRACT（任务合同）
TASK_COMPLETED（完成条件）
ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
QUALITY / STABILITY / SAFETY（质量 / 稳定 / 安全）
```

`ACTIVE_HARDWARE_BOUNDARY` 只包含此刻真实安装、可正常使用、允许用于本任务的硬件。未来计划增加但当前不存在的硬件不得阻断当前 99。

## 2. 继承经验先验

如果存在以前兼容的真实 99、阶段测试或失败复盘，禁止从零猜测。必须继承：

- `VERIFIED_99（已验证99）`；
- P50/P95 与真实分块时间；
- KEEP / ROLLBACK；
- Failure Index（失败索引）；
- 稳定 VRAM / RAM / I/O / 设备放置事实；
- 已证实有效和已证伪机制。

旧经验不兼容时降低置信度并说明，不得静默套用。

## 3. 计算物理与机器初始区间

```text
T_PHY（物理极限）
= 固定任务在当前硬件边界与物理规律下的理论下界区间

T_MACHINE_STAR_PRE（本机稳定理论极限初算）
= 当前硬件 + 已知最佳成熟软件/实现 + 经验先验下的稳定理论区间
```

未知效率使用区间 + 置信度，不制造伪精确值。

## 4. 复杂任务必须做 MRE（最小真实执行）

仅靠静态硬件/软件版本不足以代表真实执行态。复杂任务必须尽快建立：

```text
MRE = MINIMAL REAL EXECUTION（最小真实执行版本）
```

MRE 要让完整关键链真实跑通并暴露：

- 实际模型装载/卸载；
- 动态显存/内存行为；
- 缓存/预取/编译是否真正启用；
- 实际设备放置；
- 冷启动/预热/稳态差异；
- 真实关键路径；
- 运行时依赖、竞态和故障；
- 足以校准方向的关键时间数据。

默认目标是在**约 10 分钟级工程时间**内取得足以校准方向的真实态数据；若任务单次运行物理上更长，则使用机制一致的最小合同或最小子合同。

禁止在方向未校准前投入数小时深度 profiling（剖析）。

## 5. 建立 REAL_STATE_MODEL（真实态模型）

```text
STATIC FACTS（静态事实）
+ MRE OBSERVATIONS（最小真实运行观测）
+ EMPIRICAL_PRIORS（经验先验）
=> REAL_STATE_MODEL（真实态模型）
=> T_MACHINE_STAR_REAL（真实态本机稳定理论极限）
```

若修订目标，必须记录：失效假设、新证据、旧/新区间、修订理由。禁止因为当前结果慢而单纯上调目标。

详细规则见：

`references/REAL-STATE-MATURE-HARVEST-ROI.md`

---

# STEP 2 — MATURE HARVEST → TARGETED ATTACK → ROI STOP

## 6. MATURE FRONTIER SCAN（成熟前沿扫描）

优先检索：

1. 官方稳定版和官方性能提交；
2. 同 GPU 架构 / VRAM / 模型 / 任务的真实 A/B；
3. 成熟开源 workflow / runtime / model format / quant / cache / prefetch / compiler / memory management；
4. 多次复现的高质量社区成熟方案。

建立 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`：

```text
SOURCE_LEVEL（证据等级）
HARDWARE_MATCH（硬件匹配）
TASK_MATCH（任务匹配）
MECHANISM（机制）
TARGET_BLOCK（目标块）
EXPECTED_ABS_GAIN（预期绝对收益）
QUALITY_RISK（质量风险）
STABILITY_RISK（稳定风险）
INTEGRATION_COST（集成成本）
REVERSIBILITY（可逆性）
CURRENTLY_PRESENT（当前是否已有）
```

排序原则：

```text
EXPECTED_ABS_GAIN
× APPLICABILITY_CONFIDENCE
× EVIDENCE_CONFIDENCE
÷ INTEGRATION_COST
```

不追求伪精确分数，只保证大收益、强证据、高适用、低成本候选先测试。

## 7. DATA-DRIVEN REHEARSAL（数据驱动模拟推演）

每个候选真实改动前，先基于 REAL_STATE_MODEL 做时间预算推演：

```text
CURRENT_BLOCK_TIME
- EXPECTED_REMOVABLE_TIME
+ NEW_OVERHEAD
= PROJECTED_NEW_TIME
```

必须回答：

- 攻击哪个真实时间块；
- 为什么适用于本机；
- 理论最多能省多少；
- 新增什么开销/风险；
- 回滚点在哪里；
- 是否值得一次正式 benchmark。

模拟推演只用于淘汰逻辑上不值钱的候选，不能伪装成真实 benchmark。

## 8. MATURE HARVEST（成熟收益收割）

外部成熟方案只决定优先级，不自动决定 KEEP。

```text
FASTER + HARD_CONSTRAINTS_PASS => KEEP（保留）
ELSE => ROLLBACK（回滚）
```

成熟完整栈若不可合理拆分，可整体 A/B 后直接 KEEP，不要求先自行重构。

每次 KEEP 后重新计算绝对 Gap 和剩余成熟候选。

## 9. NO FREE EXPLORATION（禁止自由摸索）

只要：

```text
HIGH_VALUE_MATURE_CANDIDATES_REMAINING = YES
```

就禁止优先进入自研 kernel、参数盲扫、无限 profiling 或大量 Vn 候选。

只有在高价值成熟方案已吃完/不适用且仍有显著剩余 Gap 时，才允许定向自研。

每个自研候选必须满足：

```text
REAL_DATA_SUPPORT=YES（有真实数据）
MECHANISM_EXPLAINED=YES（机制清楚）
EXPECTED_GAIN_ESTIMATED=YES（收益可估）
ROLLBACK_DEFINED=YES（可回滚）
```

否则不执行。

禁止：

- 长时间参数盲扫；
- 无真实数据的 kernel 猜测；
- 因“也许会快”连续创建 V1…Vn；
- 已有成熟实现却自行重新实现；
- 已有失败证据却无条件重测；
- 收益模型不清楚时连续数小时 profiling；
- 只看局部指标，不看端到端收益。

## 10. TARGETED ATTACK（定向攻击）

成熟方案收割后，对剩余 Gap：

```text
DELTA_T_REDUCIBLE_i
= T_CURRENT_BLOCK_i - T_MACHINE_TARGET_BLOCK_i

NEXT_ATTACK
= argmax_i(DELTA_T_REDUCIBLE_i)
```

只攻击绝对可减少时间最大的高置信块；每次 KEEP/ROLLBACK 后重新推演，不机械沿一个方向做到底。

---

# ROI STOP（收益停止）

是否继续迭代不能只看“还能不能再省 0.5 秒”。

估算：

```text
EXPECTED_LIFETIME_BENEFIT（未来总收益）
≈ DELTA_T_PER_RUN（每次节省时间）
× EXPECTED_FUTURE_RUNS（预计未来运行次数）
× VALUE_FACTOR（时间/资源价值系数）
```

继续优化的必要条件：

```text
EXPECTED_LIFETIME_BENEFIT
> ENGINEERING_COST
+ VALIDATION_COST
+ RISK_COST
```

否则：

```text
ECONOMIC_STOP=YES（经济性停止）
```

因此同样 0.5 秒：一次性任务可能不值得，未来会执行成千上万次的基础能力可能非常值得。

---

# 99 / FREEZE（99 / 冻结）

99 不是数学绝对极限，也不是固定 1% 阈值。

必须同时满足：

1. 固定任务真实完成；
2. correctness / quality / stability / safety 全部通过；
3. 权威计时稳定；
4. `MRE_REAL_STATE_CALIBRATION=PASS（真实态校准通过）`；
5. `MATURE_PATH_FIRST_GATE=PASS（成熟路径优先门禁通过）`；
6. `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）`；
7. `HARDWARE_TOPOLOGY_GATE=PASS（当前硬件拓扑门禁通过）`；
8. 当前结果进入或贴近高置信 `T_MACHINE_STAR_REAL`，或剩余 Gap 已有充分证据证明不具备更高 ROI；
9. 没有明显大块重甲；
10. 没有高置信高收益成熟候选遗漏；
11. 剩余自研候选已达到 `ECONOMIC_STOP` 或无显著绝对收益；
12. Final Certification（最终认证）通过；
13. Shared Fact Source（共同事实源）同步并 remote verify（远端验证）通过。

因此：

> **99 = 当前真实硬件边界 + 当前最佳成熟实现 + 真实运行校准 + 已收割成熟收益 + 剩余 Gap 的数据驱动定向优化 + 生命周期 ROI 停止后的稳定最优。**

---

# 执行角色

分析、候选排序、机制判断、收益推演、停止条件由高质量推理完成；执行器主要负责：

- 精确修改；
- 可逆部署；
- 真实运行；
- 证据采集；
- QC；
- KEEP / ROLLBACK 所需事实；
- Git 收口。

禁止把“探索方向”无限下放给执行器，让其在本机无边界试错。

单 GPU 正式 benchmark 必须串行、独占。

---

# CONTEXT HYGIENE（上下文卫生）

长项目必须：

- 每个大阶段形成正式报告和机器可读状态；
- 新阶段读取冻结事实，不依赖长会话记忆；
- 页面/会话明显过长时冻结当前阶段并换新页面；
- 新页面从任务文件 + Shared Fact Source 恢复；
- 简单执行阶段用简洁指令，复杂规划/复盘阶段使用高强度推理。

---

# Shared Fact Source（共同事实源）

```text
SHARED_FACT_SOURCE=cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SHARED_REPO_SYNC_REQUIRED=YES
```

产生新工程事实：

```text
LOCAL RESULT
→ FORMAL REPORT
→ SHARED REPOSITORY
→ EXACT STAGE
→ COMMIT
→ PUSH
→ REMOTE VERIFY
```

禁止 `git add .`、force push、`reset --hard`。

---

# 默认最短读取路径

正常任务读取：

1. `SKILL.md`
2. `references/FAST-PATH.md`
3. `references/REAL-STATE-MATURE-HARVEST-ROI.md`

按需读取：

- `references/FIRST-PRINCIPLES-LIMIT-MODEL.md`
- `references/MATURE-PATH-FIRST-GATE.md`
- `references/SOFTWARE-FRONTIER-GATE.md`
- `references/HARDWARE-TOPOLOGY-GATE.md`
- `references/MULTI-AGENT-PARALLELISM.md`
- `references/EXECUTION-BRIDGE.md`
- `references/EXECUTION-CLOSURE-CONTRACT.md`
- `references/FAILURE-INDEX.md`

## 状态

```text
SKILL_VERSION=1.3.0
TWO_STEP_METHOD=PASS（两步法保留）
MRE_REAL_STATE_CALIBRATION_REQUIRED=YES（复杂任务必须极简真实运行校准）
MATURE_PATH_FIRST_GATE_DEFINED=PASS（成熟路径优先门禁已定义）
NO_FREE_EXPLORATION=YES（禁止无依据自由探索）
DATA_DRIVEN_REHEARSAL_REQUIRED=YES（高价值候选需先数据推演）
ROI_STOP_DEFINED=PASS（生命周期收益停止条件已定义）
ACTIVE_HARDWARE_BOUNDARY_DEFINED=PASS（当前有效硬件边界已定义）
EMPIRICAL_PRIOR_REUSE_DEFINED=PASS（经验先验复用已定义）
SOFTWARE_FRONTIER_GATE_DEFINED=PASS（软件前沿门禁已定义）
HARDWARE_TOPOLOGY_GATE_DEFINED=PASS（硬件拓扑门禁已定义）
FUTURE_UNAVAILABLE_HARDWARE_BLOCKS_CURRENT_99=NO（未来不可用硬件不阻断当前99）
SHARED_FACT_SOURCE_REQUIRED=YES（共同事实源必需）
```
