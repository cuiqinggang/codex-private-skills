# MATURE PATH FIRST（成熟路径优先门禁）

本规则属于 `first-principles-physical-limit-convergence v1.2.0`。

## 核心原则

在进入自研微优化、底层插桩和逐块攻击之前，先系统收割外部世界已经验证过的成熟收益。

```text
WORLD_KNOWN_BEST（外部已知成熟方案）
→ LOCAL_COMPATIBILITY_FILTER（本机兼容筛选）
→ LOCAL_A/B（本机同任务真实对比）
→ KEEP / ROLLBACK（保留 / 回滚）
→ RESIDUAL_GAP（剩余差距）
→ CUSTOM_ATTACK（定制攻击）
```

这不是放弃第一性原理，而是把“已经有人付过试错成本”的成果作为最先攻击的大块。

## 为什么必须先做成熟路径收割

若某类任务已有官方、硬件同代、同模型或同软件栈的成熟优化记录，则从零重新探索每个参数、kernel（内核）、缓存和调度机制，会重复支付大量试错成本。

因此目标不是“自己证明所有事情”，而是：

```text
MINIMIZE T_CONVERGENCE（最小化达到稳定最优所需的工程时间）
```

同时仍保持：

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END（最小化真实端到端时间）
```

## 成熟方案证据等级

优先级从高到低：

```text
L0 = 官方稳定版 / 官方性能提交 / 官方模型或硬件建议
L1 = 与本机同 GPU 架构、同 VRAM 档、同模型的真实 A/B 实测成熟方案
L2 = 相邻 GPU 架构或相近硬件的高质量公开 benchmark
L3 = 大量社区重复验证、机制清楚但硬件差异较大的方案
L4 = 单一经验帖 / 未复现 claim（主张）
```

L0-L2 优先进入 `HARVEST_CANDIDATES（成熟收割候选）`。
L3 作为补充。
L4 默认不直接消耗正式 benchmark 预算，除非剩余 Gap 足够大且机制高度吻合。

## 收割前必须做 Applicability Filter（适用性筛选）

成熟方案不能机械照搬。至少检查：

- GPU architecture（GPU架构）是否一致；
- VRAM / RAM 档位是否接近；
- model variant / quantization（模型版本 / 量化）是否一致；
- task shape（分辨率、帧数、步数、序列长度）是否接近；
- software version（软件版本）是否兼容；
- optimization mechanism（优化机制）是否真正作用于当前最大时间块；
- correctness / quality / reproducibility（正确性 / 质量 / 可复现性）是否满足本任务合同。

例如：减少采样步数的 Turbo / PDD 对 1-step P0 不构成可减少空间，不应因为公开加速比大就进入当前正式候选。

## Mature Harvest Matrix（成熟收益收割矩阵）

每个候选先只做纸面筛选：

```text
CANDIDATE（候选）
SOURCE_LEVEL（证据等级）
MECHANISM（机制）
TARGET_BLOCK（目标时间块）
EXPECTED_ABS_GAIN_S（预期绝对收益秒数）
APPLICABILITY（适用性）
QUALITY_RISK（质量风险）
STABILITY_RISK（稳定风险）
INTEGRATION_COST（集成成本）
REVERSIBILITY（可逆性）
```

排序采用：

```text
HARVEST_SCORE
≈ EXPECTED_ABS_GAIN_S
× APPLICABILITY_CONFIDENCE
× EVIDENCE_CONFIDENCE
÷ INTEGRATION_COST
```

不追求伪精确分数；其作用只是保证“大收益、强证据、低成本”的成熟方案先测试。

## 执行纪律

1. 先收集成熟方案，不立即改代码。
2. 去除与固定任务明显不适用的候选。
3. 优先复用现成 workflow / patch / official feature / version / model format（工作流 / 补丁 / 官方功能 / 版本 / 模型格式）。
4. 一个正式候选只改变一个可归因机制，除非外部成熟方案本身就是不可拆分的完整栈。
5. 完整成熟栈如果直接胜出，可以整体 KEEP；之后再做 ablation（消融）只为理解和进一步优化，不得要求先拆散才允许使用。
6. 每个候选仍必须本机真实 A/B；外部 benchmark 只决定优先级，不自动决定 KEEP。
7. 同任务更快 + 硬约束通过 => KEEP；否则 ROLLBACK。
8. 成熟候选全部高价值项收割完成以后，才进入深度自研插桩和定制攻击。

## 自研攻击的进入条件

满足以下任一：

```text
A. 所有高价值成熟候选已本机验证；
B. 成熟方案与当前最大 Gap 不匹配；
C. 成熟方案收益已被吃完，但仍存在显著绝对 Gap；
D. 当前任务/硬件组合没有成熟方案覆盖。
```

此时再执行：

```text
PROFILE（分块诊断）
→ RESIDUAL GAP（剩余差距）
→ FIRST-PRINCIPLES CUSTOM ATTACK（第一性原理定制攻击）
```

## 99 Gate（99门禁）

99 前必须同时回答：

```text
MATURE_FRONTIER_SCANNED=YES（成熟前沿已扫描）
HIGH_VALUE_MATURE_CANDIDATES_TESTED=YES（高价值成熟候选已验证）
BEST_MATURE_WINNERS_KEPT=YES（成熟胜出方案已保留）
RESIDUAL_HIGH_VALUE_MATURE_GAP=NO（不存在尚未收割的高价值成熟收益）
```

然后才允许用“没有高价值可行剩余 Gap”支持 99。

## 与 T_MACHINE_STAR（本机稳定理论极限）的关系

`T_MACHINE_STAR` 的计算应先吸收成熟世界经验，再用本机数据校正。

```text
T_MACHINE_STAR_Vn
= PHYSICS（物理规律）
+ ACTIVE_HARDWARE（当前有效硬件）
+ BEST_MATURE_SOFTWARE（最佳成熟软件）
+ EMPIRICAL_PRIORS（本机经验先验）
+ RESIDUAL_UNKNOWN_RANGE（剩余未知区间）
```

因此下一次同类任务不得重新只凭纸面理论估算；应优先继承已经形成的真实 P50/P95、分块时间、KEEP/ROLLBACK 历史、失败索引和成熟方案适用性结论。

## 一句话

> **先复制世界已经验证过的最快成熟路径，把最大成熟收益一次吃掉；再对剩余差距做第一性原理定制攻击，而不是把别人已经走完的路重新走一遍。**
