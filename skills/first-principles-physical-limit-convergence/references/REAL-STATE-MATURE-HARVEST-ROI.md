# REAL STATE + MATURE HARVEST + ROI（真实态校准 + 成熟收割 + 收益停止）

本规则属于 `first-principles-physical-limit-convergence v1.3.0`，用于复杂任务中禁止“无数据支撑的自由探索式优化”。

## 核心原则

第一性原理负责确定不可违反的边界、因果结构和理论下界；它**不等于从零重新发明已有成熟优化**。

复杂任务默认采用：

```text
FIRST-PRINCIPLES BOUND（第一性原理边界）
→ MINIMAL REAL RUN（极简真实运行）
→ REAL-STATE CALIBRATION（真实态校准）
→ MATURE HARVEST（成熟方案收割）
→ DATA-DRIVEN REHEARSAL（数据驱动模拟推演）
→ TARGETED ATTACK（定向攻击）
→ ROI STOP（收益停止）
```

禁止：

```text
没有成熟证据
+ 没有真实运行数据
+ 没有可解释收益模型
=> 直接进入长时间自由探索 / 大规模插桩 / 参数扫荡 / 内核摸索
```

除非已经证明不存在高价值成熟路径，并且剩余 Gap 足够大。

---

# STEP 1 — CALCULATE + REAL-STATE CALIBRATION（计算 + 真实态校准）

## 1.1 冻结合同和边界

冻结：

- `TASK_CONTRACT（任务合同）`
- `TASK_COMPLETED（完成条件）`
- `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`
- correctness / quality / stability / safety（正确性 / 质量 / 稳定 / 安全）硬约束

## 1.2 先算两个理论区间

```text
T_PHY（物理极限）
= 固定任务在物理规律和当前硬件边界下不可突破的理论下界区间

T_MACHINE_STAR_PRE（本机理论极限初算）
= 当前硬件 + 已知最佳成熟软件/实现 + 已有经验先验下的稳定理论区间
```

未知效率只允许写区间和置信度，不伪造精确值。

## 1.3 必须做一次 Minimal Real Run（极简真实运行）

对于复杂系统，静态硬件/软件信息不足以代表真实执行态。必须尽快建立一个：

```text
MRE = MINIMAL REAL EXECUTION（最小真实执行版本）
```

目标不是追求性能，而是在尽可能短的时间内让完整关键链真实跑通，并暴露：

- 实际模型装载/卸载；
- 动态显存/内存行为；
- 编译/预取/缓存是否真正启用；
- 真实设备放置；
- 真实关键路径；
- 首次运行与稳态差异；
- 运行时故障、依赖、竞态；
- 真实 P50/P95 或至少关键分块时间；
- 与静态推算不一致的地方。

### 时间纪律

默认目标：在**约 10 分钟级**工程时间内形成足以校准方向的真实态数据；如果任务本身单次运行物理上超过该时长，则使用能保持机制一致的最小合同或最小可运行子合同。

不得为了“测得更完整”在方向未确认前投入数小时深度 profiling（剖析）。

## 1.4 真实态校准

用真实运行修正初算：

```text
STATIC FACTS（静态事实）
+ MRE OBSERVATIONS（最小真实运行观测）
+ EMPIRICAL PRIORS（经验先验）
=> REAL_STATE_MODEL（真实态模型）
=> T_MACHINE_STAR_REAL（真实态本机稳定理论区间）
```

如果初算与真实运行冲突，必须记录：

- 哪个假设失效；
- 新证据是什么；
- 为什么修订；
- 新区间和置信度。

这属于 `MODEL_CORRECTION（模型校正）`，不是为了通过 99 随意放宽目标。

---

# STEP 2 — MATURE HARVEST → REHEARSAL → TARGETED ATTACK（成熟收割 → 模拟推演 → 定向攻击）

## 2.1 成熟方案优先

先扫描：

1. 官方稳定方案与性能提交；
2. 与本机同 GPU 架构 / VRAM / 模型 / 任务高度相近的真实 A/B；
3. 成熟开源工程、工作流、模型格式、量化、缓存、预取、编译、内存管理方案；
4. 经过多次复现的社区成熟方案。

构建 `MATURE_HARVEST_MATRIX（成熟收益收割矩阵）`：

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

优先：大收益、强证据、高适用、低成本、可逆。

外部成熟方案只决定优先级；最终 KEEP/ROLLBACK 仍由本机同合同真实 A/B 决定。

## 2.2 Data-Driven Rehearsal（数据驱动模拟推演）

在真实改动前，先用 `REAL_STATE_MODEL` 对候选做一次逻辑/时间预算推演：

```text
CURRENT_BLOCK_TIME
- EXPECTED_REMOVABLE_TIME
+ NEW_OVERHEAD
= PROJECTED_NEW_TIME
```

必须明确：

- 作用在哪个真实时间块；
- 为什么在本机上适用；
- 理论上最多能省多少；
- 新增什么开销/风险；
- 最坏情况和回滚点；
- 是否值得消耗一次正式 benchmark 预算。

“模拟”不是伪造 benchmark；它只是用真实数据先淘汰逻辑上不可能高收益的候选。

## 2.3 Codex / 执行器职责

分析、候选排序、机制判断、停止条件由高质量推理完成；执行器主要负责：

- 精确修改；
- 可逆部署；
- 真实运行；
- 证据采集；
- QC；
- KEEP / ROLLBACK 所需事实；
- Git 收口。

禁止把“探索方向”无限下放给执行器，让其在本机无边界试错。

## 2.4 先吃成熟大块，再做自研

```text
HIGH_VALUE_MATURE_CANDIDATES_REMAINING = YES
=> 禁止优先进入自由自研
```

只有当：

```text
HIGH_VALUE_MATURE_CANDIDATES_REMAINING = NO
OR MATURE_PATH_NOT_APPLICABLE = YES
```

且仍存在显著 `RESIDUAL_GAP（剩余差距）`，才允许进入：

- 深度 profiling；
- 自定义 prefetch/offload；
- kernel / compiler / CUDA graph；
- 自定义缓存、调度、量化；
- 其他本机定向优化。

每个自研攻击必须同时具备：

```text
REAL_DATA_SUPPORT=YES
MECHANISM_EXPLAINED=YES
EXPECTED_GAIN_ESTIMATED=YES
ROLLBACK_DEFINED=YES
```

否则不执行。

---

# ROI STOP（收益停止条件）

停止条件不能只看“还能不能再省 0.5 秒”。

优化是否值得继续，应比较：

```text
EXPECTED_LIFETIME_BENEFIT（未来总收益）
vs
ENGINEERING_COST（继续迭代成本）
```

定义：

```text
EXPECTED_LIFETIME_BENEFIT
≈ DELTA_T_PER_RUN（每次节省时间）
× EXPECTED_FUTURE_RUNS（预计未来运行次数）
× VALUE_FACTOR（时间/资源价值系数）
```

如果还有资源成本、失败率或人工等待，可一起折算。

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

因此 0.5 秒在一次性任务上可能不值得，在未来执行数千次的基础能力上可能非常值得。

99 的经济含义：

> 在当前真实硬件/软件边界、成熟方案已系统收割、剩余高价值 Gap 已验证后，继续投入的预期总收益已经不足以覆盖继续迭代成本；此时冻结为当前稳定 99。

99 仍必须满足 correctness / quality / stability / safety 硬约束，不能用经济性掩盖错误。

---

# NO FREE EXPLORATION（禁止自由摸索）

以下行为默认禁止：

- 长时间参数盲扫；
- 没有真实数据支撑的 kernel 猜测；
- 因为“也许会快”连续创建 V1…Vn 候选；
- 已有成熟实现却自行重新实现；
- 已有失败证据却无条件重测；
- 在收益模型不清楚时连续数小时 profiling；
- 把局部指标变快当成端到端收益。

允许探索必须满足至少一项：

1. 没有成熟方案覆盖；
2. 成熟方案全部不适用/已证伪；
3. 剩余 Gap 很大且有真实数据指向明确机制；
4. 预计生命周期收益显著大于探索成本。

---

# CONTEXT HYGIENE（上下文卫生）

长项目必须防止上下文膨胀导致判断漂移：

- 每个大阶段形成正式阶段报告和机器可读状态；
- 新阶段优先读取冻结事实，而不是依赖长会话记忆；
- 页面/会话明显过长时，冻结当前阶段并在新页面继续；
- 新页面通过任务文件 + Shared Fact Source（共同事实源）恢复，不重新口述全部历史；
- 简单执行阶段使用简洁指令；复杂规划/复盘阶段使用高强度推理。

---

# 最短总流程

```text
1. 冻结任务合同与硬件边界
2. 第一性原理计算 T_PHY + T_MACHINE_STAR_PRE
3. 继承旧 99 / 经验先验 / Failure Index
4. 建立约10分钟级 MRE 极简真实运行
5. 得到 REAL_STATE_MODEL，校准 T_MACHINE_STAR_REAL
6. 扫描世界成熟方案
7. 建 Mature Harvest Matrix
8. 对高价值候选做数据驱动模拟推演
9. 先本机 A/B 收割成熟大收益
10. 重算剩余 Gap
11. 仅对有真实数据和明确收益的最大 Gap 定向自研攻击
12. 每轮 KEEP/ROLLBACK 后重新推演
13. 用生命周期 ROI 判断是否继续
14. 最终认证、99、冻结、经验回写
```

一句话：

> **先用第一性原理确定边界，再用极简真实运行把“纸面机器”变成“真实机器”；先复制世界已经反复验证的大收益，再只攻击成熟方案吃不掉的最大剩余 Gap；任何自研必须有真实数据、机制和收益预算，最后按整个未来生命周期的总收益而不是单次毫秒决定是否继续。**
