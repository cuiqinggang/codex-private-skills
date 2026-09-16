---
name: first-principles-physical-limit-convergence
description: 在固定任务完成条件和硬约束下，以时间为唯一优化目标；先用第一性原理计算绝对物理极限区间 T_PHY 与本机稳定可实现极限区间 T_MACHINE_STAR，再从去重甲后的最小 V1 开始，按最大绝对可消灭时间 Gap 真实迭代，直到 99 / FREEZE。适用于工程、AI 推理、软件、工作流、生产与其他可以明确任务合同、资源约束和时间测量边界的问题。
metadata:
  version: "1.0.0"
  short-description: 第一性原理物理极限收敛引擎
  lineage: absolute-time-fireworks-optimization@2.0.1
---

# 第一性原理物理极限收敛引擎 v1.0.0

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END

SUBJECT TO:
TASK_COMPLETED == TRUE
CORRECTNESS == PASS
QUALITY >= FIXED_THRESHOLD
STABILITY >= FIXED_THRESHOLD
SAFETY == PASS
TASK_CONTRACT == IDENTICAL
```

本技能由 `absolute-time-fireworks-optimization v2.0.1` 演化而来。旧技能已经证明了“固定任务完成条件 + 去重甲 + 真实计时 + KEEP/ROLLBACK + 99/FREEZE”的有效性；本版不抛弃这些成熟执行纪律，只替换旧版的固定四列主流程。

## 唯一核心：两步法

### STEP 1 — CALCULATE：先算终点与最短攻击路线

不要求先制造一个低性能 CURRENT，也不要求先找到外部成熟方案。

固定 `TASK_CONTRACT` 后，利用已有真实硬件、软件、模型、执行图、数据流、依赖关系和资源约束，计算：

```text
T_PHY
= 同一固定任务在物理规律与不可避免操作约束下的绝对物理下界区间

T_MACHINE_STAR
= 同一固定任务在当前真实机器/运行环境上，
  在正确、稳定、可持续条件下理论可实现的极限区间
```

硬不变量：

```text
T_MACHINE_STAR >= T_PHY
```

任何未知现实效率、kernel 利用率、带宽利用率、并行重叠比例、调度损失等，优先表达为区间和 `ASSUMPTION_LEDGER`，而不是以“尚未实测”为理由取消第一性原理计算。

第一步必须产出：

- 固定任务合同与完成边界；
- 物理因果 DAG / critical path；
- 不可避免的操作、数据移动、同步与资源占用；
- `T_PHY=[LOW,HIGH]`；
- `T_MACHINE_STAR=[LOW,HIGH]`；
- 分块极限（若任务自然存在分块）；
- 每个假设、置信度和误差来源；
- 可删除 / 合并 / 旁路 / 后移 / 并行 / 常驻 / 缓存 / 预计算的候选；
- 第一版 `ATTACK_ORDER`；
- 是否使用多智能体，以及最优并行模式。

`EXTERNAL FRONTIER` 降级为 `OPTIONAL EVIDENCE`：它可以用来校验模型、借成熟实现、防漏机制，但不是终点，也不是必经步骤。

### STEP 2 — CONVERGE：V1 → 最大 Gap → 攻击 → 99

优先继承所有与本任务兼容的既有冻结 99。禁止为了展示提升百分比而故意退回 stock / raw baseline。

在第一次真实运行前，先移除第一步已经明确证明不属于任务完成关键路径的重甲，得到：

```text
V1 = FIRST MINIMUM VIABLE EXECUTION
```

V1 不是最终优化版；它是“攻击迭代开始前的第一个最小、正确、可测版本”。V1 命令包必须先经过审计，再真实运行。

测得 `T_CURRENT_BLOCK_i` 后，与第一步的本机目标比较：

```text
DELTA_T_REDUCIBLE_i
=
T_CURRENT_BLOCK_i
-
T_MACHINE_TARGET_BLOCK_i

NEXT_ATTACK
=
argmax_i(DELTA_T_REDUCIBLE_i)
```

重点是最大绝对可消灭时间，不是最大百分比，也不一定是当前耗时最大的块。

每轮只改变一个可解释的机制或一组不可拆分的同一机制，真实运行后：

```text
FASTER + HARD_CONSTRAINTS_PASS => KEEP
ELSE => ROLLBACK
```

然后重新测量 Gap，持续：

```text
V1 -> V2 -> V3 -> ... -> 99 -> FREEZE
```

## T_PHY 与 T_MACHINE_STAR 的关系

`T_PHY` 是终极物理参照，不允许由成熟方案定义。

`T_MACHINE_STAR` 是当前机器的现实理论目标。它可以随着新证据证明原假设错误或不完整而版本化修订，但禁止为了让 99 更容易通过而移动目标。

如果同一任务合同、同一计时边界下出现 `MEASURED < T_PHY`，优先检查任务合同、计时边界、缓存/结果身份、物理模型和测量。现实不能真正突破同一任务定义下正确计算的物理下界；冲突意味着模型、合同或测量至少有一项需要修正。

## 多智能体不是“越多越快”

先区分：

```text
T_EXEC = 被优化任务本身的真实完成时间
T_CONVERGENCE = 研究、计算、审计、编码、测试、证据分析与决策收敛所需墙钟时间
```

多智能体通常优化 `T_CONVERGENCE`；只有智能体编排本身属于固定任务运行时关键路径时，才进入 `T_EXEC`。

选择智能体数量：

```text
N_STAR = argmin_N(
    T_RESOURCE_CRITICAL_PATH(N)
  + T_COORDINATION(N)
  + T_MERGE(N)
  + T_CONTENTION(N)
)
```

只有同时满足以下条件才并行：至少两个独立子任务；子任务时间明显大于协调开销；不争用排他资源；输出可独立验证并安全合并；预计墙钟收益 > 0。

默认模式：

```text
AGENT_MODE = OFF | SUPPORT_PARALLEL | RESOURCE_PARTITIONED
```

对单 GPU 的权威 GPU benchmark，默认：

```text
GPU_BENCHMARK_SERIAL=YES
GPU_EXCLUSIVE=YES
```

详细规则见 `references/MULTI-AGENT-PARALLELISM.md`。

## 继承旧技能的成熟纪律

继续继承：TASK_COMPLETED / hard constraints；De-Armoring；真实端到端时间与权威分块计时；GPU 异步同步/CUDA Event；KEEP/ROLLBACK；99/FREEZE；可逆 instrumentation；已有事实优先与 gap-only verification；dirty worktree 保护；Failure Index；高价值决策回到推理大脑；共同事实源强制收口；正式报告 + 机器可读结果；精确 stage；禁止 `git add .`、force push、`reset --hard`、覆盖陌生修改；remote verify；只读任务不制造无意义 commit。

完整继承表见 `references/LEGACY-INHERITANCE-MAP.md`。

## SHARED FACT SOURCE CLOSURE GATE

```text
SHARED_FACT_SOURCE=cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SHARED_REPO_SYNC_REQUIRED=YES
```

凡产生后续需要复用的新工程事实：

```text
LOCAL RESULT
-> FORMAL REPORT / STRUCTURED FACT
-> SHARED REPOSITORY
-> EXACT STAGE
-> COMMIT
-> PUSH
-> REMOTE VERIFY
```

只有 `LOCAL_TASK_RESULT=PASS AND SHARED_REPO_SYNC=PASS` 才允许 `STAGE_COMPLETE=YES / FINAL=PASS / 99=YES / FREEZE=YES`。

只读回答、纯解释、未执行草案、读取已有事实且不产生新工程事实时允许 `SHARED_REPO_SYNC_REQUIRED=NO`。

## 99 / FREEZE

99 不是 `T_CURRENT/T_PHY=99%`，也不是任意固定 1% 阈值。只有固定任务真实完成、hard constraints 通过、权威计时稳定、当前结果已进入或贴近高置信 `T_MACHINE_STAR` 区间、剩余高置信机制的绝对收益不再显著高于测量噪声 + 工程/切换成本、没有明显大块重甲、目标没有为了过 99 被移动、shared-repo closure PASS，才允许 `99=YES / FREEZE=YES`。

## 默认最短读取路径

正常任务只读 `SKILL.md` 和 `references/FAST-PATH.md`。

按需读取：
- `references/FIRST-PRINCIPLES-LIMIT-MODEL.md`
- `references/MULTI-AGENT-PARALLELISM.md`
- `references/EXECUTION-BRIDGE.md`
- `references/EXECUTION-CLOSURE-CONTRACT.md`
- `references/FAILURE-INDEX.md`
- `references/RAPTOR-ITERATION-CASE.md`

## 状态声明

```text
SKILL_VERSION=1.0.0
METHOD_LOGIC_ACCEPTANCE=PASS
LEGACY_INHERITANCE_REVIEW=PASS
MULTI_AGENT_POLICY_DEFINED=PASS
H3_FIRST_APPLICATION=NOT_STARTED
H3_PHYSICAL_LIMIT_CALCULATION=NOT_STARTED
H3_V1_RUN=NOT_STARTED
RUNTIME_INSTALLATION=NOT_EXECUTED_BY_THIS_PACKAGE
```
