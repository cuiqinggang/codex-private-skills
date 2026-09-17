# RESIDUAL VIRTUAL CONVERGENCE + EXECUTION BUDGET（残余收益虚拟收敛 + 执行预算）

本规则属于 `first-principles-physical-limit-convergence v1.5.0`。

## 核心修正

成熟方案收割完成后，剩余优化通常已经从“大块收益”进入“小块、细节、交互收益”阶段。这里**不能重新退化成 Codex（执行器）数小时探索**。

正确路径是：

```text
成熟方案已吸收
+ 最新真实运行数据
+ 历史 EMPIRICAL_PRIORS（经验先验）
+ Failure Index（失败索引）
↓
RESIDUAL VIRTUAL CONVERGENCE（残余收益虚拟收敛）
↓
把剩余全部可行优化作为一个组合，在推演层继续跑到停止点
↓
形成短、确定、可验证的执行铁路
↓
Codex 只做逐段验证
```

“剩余约10%”只是一种常见情形，不是固定比例。真正判断标准是：主要成熟大收益已被系统吸收，剩余收益需要更细的真实态推演。

---

## 1. 为什么要再做一次残余虚拟收敛

成熟收割以后，真实状态已经比初始阶段清楚得多：

- 主要模型和关键路径已真实运行；
- 大块成熟优化已吃掉；
- 冷/热状态、加载、驻留、传输、缓存、预取、编译等事实更完整；
- 已经拥有成功/失败候选和 Failure Index；
- 剩余 Gap 更小，也更适合高质量推理层做精细推演。

因此此时最有价值的工作不是增加大量本机试验，而是用最新真实数据重新执行一遍：

```text
VIRTUAL ATTACK ITERATION（虚拟攻击迭代）
```

目标是把剩余优化组合的顺序、收益、依赖、风险和停止点先在推演层收敛。

---

## 2. 残余虚拟路径必须产出

对剩余每个优化点记录：

```text
POINT（优化点）
CURRENT_BLOCK_TIME（当前块时间）
MECHANISM（机制）
SOURCE（成熟依据/真实证据）
EXPECTED_GAIN（预计收益）
INTERACTION（与其他点交互）
NEW_OVERHEAD（新增开销）
QUALITY/STABILITY_RISK（质量/稳定风险）
VERIFICATION_STEP（验证步骤）
EXPECTED_VALIDATION_COST（预计验证成本）
ROLLBACK（回滚）
```

然后按真实依赖顺序组成：

```text
RESIDUAL_VIRTUAL_PATH（残余虚拟成熟路径）
```

前一步的预计结果必须成为后一步的输入；禁止把多个小收益直接相加。

---

## 3. 停止条件看“剩余组合”而不是单点

剩余可行优化组合：

```text
S = {p1, p2, ... pn}
```

先在虚拟路径中推演组合全部完成后的预计时间：

```text
DELTA_T_PORTFOLIO（组合单次总节省）
= T_CURRENT - T_PROJECTED_FINAL
```

再计算未来生命周期总收益：

```text
LIFETIME_BENEFIT_PORTFOLIO（组合生命周期总收益）
≈ DELTA_T_PORTFOLIO
× EXPECTED_FUTURE_RUNS（未来预计运行次数）
× VALUE_FACTOR（时间/算力/等待价值系数）
+ 其他可量化资源收益
```

比较的成本必须是**整个剩余组合的总成本**：

```text
PORTFOLIO_COST
= GPT/Codex 配额与推理成本
+ 工程实施成本
+ 实机验证成本
+ GPU/CPU/电力/时间成本
+ 风险成本
+ 集成维护成本
```

只有：

```text
LIFETIME_BENEFIT_PORTFOLIO > PORTFOLIO_COST
```

才继续把这些点纳入虚拟路径。

如果组合收益不足，则：

```text
PORTFOLIO_ECONOMIC_STOP=YES（组合经济性停止）
```

---

## 4. Codex 不是探索者，而是验证器

在残余收益阶段，Codex 默认角色：

```text
VALIDATOR / EXECUTOR（验证器 / 执行器）
```

不是：

```text
OPEN-ENDED EXPLORER（开放式探索者）
```

每次交给 Codex 的任务必须已经具备：

- 明确目标；
- 明确修改；
- 明确预期；
- 明确测量；
- 明确成功/失败条件；
- 明确回滚；
- 明确停止点。

如果这些信息不完整，说明虚拟路径没有成熟，任务应返回 GPT 推理层继续推演，而不是让 Codex 自己找路。

---

## 5. 禁止小时级探索式验证

默认执行纪律：

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
（禁止数小时开放式验证）
```

正常验证应是短、确定、可边界化的步骤，通常为分钟级，或最多接近固定任务自身必要运行时间。

对于复杂任务，若一次真实任务本身物理上就很长，可按任务物理时长放宽；但**额外的探索工程时间**仍不得无限增长。

如果某个候选预计需要数小时不断试参数、改代码、再测才能知道方向：

```text
VALIDATION_PLAN_NOT_MATURE=YES
→ STOP EXECUTION
→ RETURN TO VIRTUAL REHEARSAL
```

即：不是“继续跑”，而是“重新设计虚拟路径”。

---

## 6. 执行预算门禁

每个实际验证步骤在启动前必须给出：

```text
EXPECTED_EXECUTION_TIME（预计执行时间）
EXPECTED_GPU_RUNS（预计GPU运行次数）
EXPECTED_CODEX_COST（预计Codex/智能体成本）
EXPECTED_EVIDENCE_OUTPUT（预计证据产出）
STOP_CONDITION（停止条件）
```

如果实际执行明显超过预计预算且没有产生对应的信息增益：

```text
BUDGET_DRIFT=YES（预算漂移）
→ SAFE STOP（安全停止）
→ 保存现有证据
→ 回到虚拟推演层
```

禁止因为“已经跑了一半”继续沉没成本。

---

## 7. 最终99前的残余收益门禁

最终冻结前必须确认：

```text
MATURE_HARVEST_COMPLETE=YES（成熟大收益已收割）
RESIDUAL_VIRTUAL_PATH_COMPLETE=YES（残余虚拟路径已完整推演）
PORTFOLIO_ROI_EVALUATED=YES（剩余组合收益已计算）
CODEX_VALIDATION_PATH_BOUNDED=YES（实际验证路径短且有边界）
NO_MULTI_HOUR_EXPLORATION_REQUIRED=YES（不需要数小时自由探索）
```

如果还需要靠数小时自由探索才能判断是否存在价值，说明当前还没有形成可冻结的成熟99路径。

---

## 一句话

> **成熟大收益吃完以后，不是把剩余10%左右交给 Codex 慢慢啃，而是利用此时已经非常完整的真实运行数据，再做一次残余收益的虚拟攻击收敛；先在 GPT 推演层把小收益组合、依赖、长期总收益和停止点算清楚，形成短而确定的高速铁路，再让 Codex 只做简单验证。任何需要数小时开放式探索的验证计划都视为“虚拟路径尚未成熟”，必须退回重算。**
