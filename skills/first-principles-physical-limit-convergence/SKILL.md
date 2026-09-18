---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎。v3.0 继承 v2.0 全部已验证能力，把最高层方法压缩为三条：极限短时间是唯一优化指标；先吸收现实世界成熟方案集群；由高智能在虚拟层完成组合、排错与成熟化，现实层只做最小标定和最终认证。保留随机系统 T_TFVR、GPT-Codex 自动控制面、checkpoint/idempotency、失败分层与历史 99 证据。
metadata:
  version: "3.0.0"
  short-description: 第一性原理极限短时间引擎·成熟方案集群·高智能虚拟成熟
  lineage: first-principles-physical-limit-convergence@3.0.0 <- @2.0.0 <- @1.9.0 <- @1.8.0 <- @1.7.0 <- @1.6.0 <- @1.5.0 <- @1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理极限短时间引擎 v3.0.0

> **用成熟世界已有的答案，经高智能虚拟成熟，得到达到有效结果的极限短时间路径。**

正式 Skill ID 继续使用：

`first-principles-physical-limit-convergence`

旧中文名“第一性原理物理极限收敛引擎”和历史分支/资料全部保留为兼容入口；v3.0 是继承式升级，不是重建。

---

# 一、三个核心原则

## 1. 极限短时间：唯一优化指标

先冻结什么叫“有效完成”，以及当前允许使用的现实资源；之后唯一比较：

```text
T_VALID = 从任务开始到第一个 VALID 现实结果出现的端到端时间
T* = min(T_VALID)
```

`VALID` 至少由任务本身明确：

```text
TASK_COMPLETED
CORRECTNESS
QUALITY
SAFETY
STABILITY
TASK-SPECIFIC HARD CONSTRAINTS
```

资源、成本、硬件、权限、法律边界等若与任务有关，必须进入“现实边界或 VALID 合同”；它们不是第二个优化目标。

任何不能减少 `T_VALID`、也不能维持 VALID 的动作，都不是当前 99 路径的优化动作。

## 2. 成熟方案集群：先用世界已经有的答案

任何自主研究前，先判断任务需要的必要能力是否已经存在成熟解。

默认假设：

```text
WORLD_SOLVED = YES
```

把任务拆成必要能力集合 `P={p1...pn}`。若：

```text
每个 REQUIRED_PRIMITIVE 都存在成熟实现
AND
这些成熟实现存在可行组合路径
```

则：

```text
REINVENTION_BAN = ON
NOVEL_RESEARCH_ALLOWED = NO
```

只允许：

```text
DISCOVER
COPY
ADAPT
COMPOSE
MATCH
VERIFY
TIME_OPTIMIZE
```

只有在成熟方案集群已经被证据证明无法满足冻结 TASK，并明确指出：

```text
UNSOLVED_PRIMITIVE
EVIDENCE
```

后，才允许为该缺口建立 `INDEPENDENT_99_PATH`。

## 3. 高智能虚拟成熟：先虚拟解决，再现实证明

成熟方案找到以后，不立即让执行器逐条试错。

优先由高智能在虚拟层完成：

```text
搜索
-> 匹配
-> 组合
-> 冲突消解
-> 故障推演
-> 时间估算
-> 删除低收益路径
-> 冻结 VIRTUAL_99_FINAL_PLAN
```

核心规则：

```text
SEARCH_COST_PAID_VIRTUALLY_FIRST = YES
REAL_EXECUTION = CALIBRATION + CERTIFICATION
NO_FREE_EXPLORATION = YES
CODEX_PLAN_AUTHORITY = NONE
```

现实执行器可以改变“如何完成同一个已授权动作”，不能改变“接下来做什么”。

---

# 二、运行流程：一个强闸口 + 四步

## Gate 0：成熟方案集群闸口

先回答：

```text
任务需要哪些 REQUIRED_PRIMITIVES？
哪些已经有成熟方案？
是否存在完整可组合路径？
是否真的存在未解决 primitive？
```

如果成熟覆盖完整，直接进入成熟方案矩阵，禁止重新发明。

如果只缺一小块，只研究该缺口；已成熟部分仍继承，不重做。

---

## Step 1：冻结 VALID、现实边界与物理时间

冻结：

```text
TASK
VALID_CONTRACT
INITIAL_REAL_STATE
ACTIVE_RESOURCE_BOUNDARY
TIMING_BOUNDARY
USER_SEMANTICS
```

计算：

```text
T_PHY_VALID
```

含义：在冻结任务与资源边界下，达到 VALID 状态的第一性物理时间参照。

它是方向标，不等于现实机器一定能达到。

---

## Step 2：最小真实标定

只做足够建立现实事实的最小真实运行，继承已有可靠证据，不为了“重新测一次”而重做已经证明的工作。

得到：

```text
T_REAL_BASELINE
REAL_STATE_VALID_RANGE
T_COMPUTE
T_IO
T_WAIT
T_CONTROL
T_VERIFY
```

以及当前硬件/软件/驻留/失败机制。

目的只有一个：知道现实时间花在哪里，以及哪些时间仍可减少。

---

## Step 3：成熟方案矩阵 -> GPT Virtual-99

每个成熟候选至少记录：

```text
SOURCE
HARDWARE_MATCH
TASK_MATCH
MECHANISM
EXPECTED_DELTA_T
QUALITY_RISK
STABILITY_RISK
INTEGRATION_COST
REVERSIBLE
```

然后：

```text
CURRENT
-> mature route / cluster
-> interaction correction
-> residual gap
-> compare T_PHY_VALID
-> compare REAL_STATE_VALID_RANGE
-> freeze VIRTUAL_99_FINAL_PLAN
```

停止条件：

1. 已进入现实最优区间；
2. 剩余可验证收益很小；
3. 剩余候选不成熟或风险大于时间收益；
4. 需要新的明确独立研究缺口。

---

## Step 4：确定性现实认证

把冻结方案交给执行器。

执行器职责：

```text
EXECUTE
VERIFY
RECORD
CHECKPOINT/RESUME
ROLLBACK WHEN AUTHORIZED
REPORT
PUSH
REMOTE VERIFY
STOP
```

如果出现命令包外问题：

```text
保存证据
-> 安全停止
-> 返回 GPT
```

不得自行创造新候选、参数、模型、版本、实验或研究路线。

---

# 三、随机/发散系统：仍然只优化“首个有效结果时间”

v2.0 的随机系统能力全部继承。

定义：

```text
ATTEMPT = 一次候选
DELIVERY = 最终允许交付的 VALID 结果
```

正式指标：

```text
T_TFVR = Time To First Valid Result
```

如果随机变量不属于用户任务语义，可冻结：

```text
fast proposal
-> deterministic verifier
-> FAIL: reject
-> resample same frozen path
-> first PASS: ACCEPT
```

若用户要求 exact seed / exact reproducibility / benchmark A/B，则随机变量属于 TASK，不得自动替换。

多温度、多 seed、多路径、Best-of-N、verifier 等都只是减少 `T_VALID` 的成熟手段，不是新的优化目标。

---

# 四、99 的定义

99 不是“距离物理极限只差 1%”。

```text
固定 TASK
+ VALID
+ 现实资源边界
+ 成熟方案集群
+ 最小真实标定
+ GPT Virtual-99
+ 现实认证
+ Quality/Stability/Safety PASS
+ Remote Verify
= 当前现实边界下的稳定最优 99
```

随机任务必须区分：

```text
SINGLE_ATTEMPT_99
DELIVERY_SYSTEM_99
```

不得把交付级成功误写成单次候选 100% 成功。

---

# 五、失败分层

任何失败先分类，避免把控制问题误判成算法问题：

```text
CONTROL_PLANE_FAILURE
EXECUTION_ENVIRONMENT_FAILURE
SOURCE_IDENTITY_FAILURE
RANDOM_ATTEMPT_QC_FAILURE
ALGORITHM_QUALITY_FAILURE
PERFORMANCE_FAILURE
DELIVERY_SYSTEM_FAILURE
```

失败分层只服务于更快回到正确路径，不构成新的优化目标。

---

# 六、自动执行控制层

GPT-Codex 自动化仍是本技能的可选执行控制层，不是新的方法步骤。

当前推荐：

```text
GPT = planner / judge / Virtual-99
Codex = loop owner / deterministic executor
GitHub = numbered message bus + shared truth
AI Browser = wakeup only
Capacity Router = model availability
```

最高规则：

```text
GPT_PLAN_AUTHORITY = YES
CODEX_PLAN_AUTHORITY = NONE
BOUNDED_EXECUTION_FLEXIBILITY = YES
NO_FREE_EXPLORATION = YES
```

具体协议继续由：

`gpt-codex-convergence-orchestrator@1.1.0`

以及：

`references/AUTOMATED-GPT-CODEX-CONTROL-PLANE.md`

提供。

自动化成熟度仍必须按真实验证推进；v3.0 方法升级不会把尚未执行的 L1/L2/L3 自动改成 PASS。

---

# 七、H3-P0：首个完整实证继续有效

H3-P0 冻结事实保持不变：

```text
20 formal delivery tasks
22 total attempts
first-attempt pass = 18/20 = 90%
mean attempts = 1.10
T_TFVR mean = 6.804s
P50 = 6.076s
P95 = 11.974s
max = 12.862s
final accepted QC = 20/20
invalid output delivered = 0
DELIVERY_SYSTEM_99 = YES
```

事实源：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-FINAL-99-FREEZE-v1.md`

v3.0 不重写该案例，只把它纳入新的统一解释：在 VALID 硬约束下最小化首个有效交付时间。

---

# 八、继承与兼容

v3.0 是 v2.0 的迭代升级，不删除历史。

```text
CANONICAL_SKILL_ID = first-principles-physical-limit-convergence
CURRENT_DISPLAY_NAME = 第一性原理极限短时间引擎
LEGACY_DISPLAY_NAME = 第一性原理物理极限收敛引擎
CURRENT_BRANCH = codex/first-principles-physical-limit-convergence-v3.0.0
PREVIOUS_BRANCH = codex/first-principles-physical-limit-convergence-v2.0.0
```

以下继续保留并可检索、读取、引用：

- v1.x / v2.0 分支；
- 历史成功案例；
- 所有 `references/`、`sources/`、`templates/`、`tests/`；
- 旧技能名和祖先技能映射；
- H3-P0、随机交付、自动控制面、Failure Index、KEEP/ROLLBACK、远端共同事实源等已验证能力。

若历史表述与 v3.0 顶层三原则冲突，以 v3.0 顶层定义为当前裁决；历史内容仍作为证据、案例或实现细节存在。

---

# 九、远端事实与冻结

阶段结果继续遵循：

```text
remote read
-> execute
-> evidence
-> commit
-> push
-> remote verify
```

报告至少保存：

```text
TASK_ID
BRANCH
LAST_REMOTE_HEAD
COMPLETED_STEPS
DO_NOT_REPEAT
NEXT_ACTION
ARTIFACT_PATHS
```

---

# 最终一句话

> **极限短时间是唯一指标；成熟方案集群提供现实已有答案；高智能先把答案虚拟成熟，现实只做最少标定和最终证明。**
