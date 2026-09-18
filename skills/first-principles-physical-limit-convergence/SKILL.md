---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎。v3.1 继承 v3.0 的三个核心：极限短时间、成熟方案集群、高智能虚拟成熟；新增强制“方法-执行一致性层”，解决规则已经明确但现实执行仍可能退回旧流程的问题。任何现实动作必须先通过机器可检查的执行合同与 Pre-Action Conformance Gate；未授权动作一律 fail-closed、保存证据并返回 GPT。旧流程和旧成熟度标签只能作为历史证据，不能授权当前动作。
metadata:
  version: "3.1.0"
  short-description: 第一性原理极限短时间引擎·Virtual-99·方法执行一致性强制
  lineage: first-principles-physical-limit-convergence@3.1.0 <- @3.0.0 <- @2.0.0 <- @1.x
---

# 第一性原理极限短时间引擎 v3.1.0

> **用成熟世界已有的答案，经高智能虚拟成熟，得到达到有效结果的极限短时间路径；并且现实执行必须逐动作证明自己正在执行这条被冻结的路径。**

正式 Skill ID 保持不变：

first-principles-physical-limit-convergence

v3.1 是 v3.0 的执行约束升级，不改变 v3 的三个核心，不删除历史资料。

---

# 零、v3.1 修复的问题：方法正确不等于执行一定正确

v3.0 已经明确：

~~~text
1. 极限短时间
2. 成熟方案集群
3. 高智能虚拟成熟
~~~

但 v3.0 的缺口是：

~~~text
METHOD_LOGIC=DEFINED
并不能自动推出
REAL_EXECUTION=CONFORMANT
~~~

也就是说，文档即使写了 NO_FREE_EXPLORATION、CODEX_PLAN_AUTHORITY=NONE，执行者仍可能沿用旧习惯、旧 pilot、旧成熟度阶梯或临场设计。

v3.1 因此增加：

~~~text
METHOD_EXECUTION_CONFORMANCE_LAYER=MANDATORY
EXECUTION_MODE=FAIL_CLOSED
CURRENT_CANONICAL_METHOD_PRECEDENCE=ABSOLUTE
LEGACY_EXECUTION_AUTHORITY=NONE
~~~

这不是第四个优化目标，也不是第四个方法核心；它只是确保前三个核心真的被执行。

---

# 一、三个核心原则保持不变

## 1. 极限短时间：唯一优化指标

先冻结什么叫 VALID，以及现实资源边界；之后唯一比较：

~~~text
T_VALID = 从任务开始到第一个 VALID 现实结果出现的端到端时间
T* = min(T_VALID)
~~~

VALID 至少包含：

~~~text
TASK_COMPLETED
CORRECTNESS
QUALITY
SAFETY
STABILITY
TASK-SPECIFIC HARD CONSTRAINTS
~~~

资源、成本、权限、合法性、硬件等进入 VALID 或现实边界，不与时间并列成为第二优化目标。

## 2. 成熟方案集群：先用世界已经存在的答案

默认：

~~~text
WORLD_SOLVED=YES
~~~

先拆解 REQUIRED_PRIMITIVES。

若所有必要 primitive 已有成熟实现且可组合：

~~~text
REINVENTION_BAN=ON
NOVEL_RESEARCH_ALLOWED=NO
~~~

只允许：

~~~text
DISCOVER
COPY
ADAPT
COMPOSE
MATCH
VERIFY
TIME_OPTIMIZE
~~~

只有明确存在 UNSOLVED_PRIMITIVE + EVIDENCE 时，才允许建立独立研究路径。

## 3. 高智能虚拟成熟：先虚拟解决，再现实证明

成熟方案找到以后，不让现实执行器逐项试错。

优先在虚拟层完成：

~~~text
搜索
-> 匹配
-> 组合
-> 冲突消解
-> 故障推演
-> 时间估算
-> 删除低收益路径
-> 冻结 VIRTUAL_99_FINAL_PLAN
~~~

正式规则：

~~~text
SEARCH_COST_PAID_VIRTUALLY_FIRST=YES
REAL_EXECUTION=CALIBRATION+CERTIFICATION
NO_FREE_EXPLORATION=YES
CODEX_PLAN_AUTHORITY=NONE
~~~

---

# 二、v3.1 强制执行层

## 2.1 现实层只有两类合法授权计划

任何现实动作都必须属于一个被冻结的计划。

Step 2 使用：

~~~text
PLAN_TYPE=CALIBRATION_PLAN
PLAN_STATUS=FROZEN
~~~

Step 4 使用：

~~~text
PLAN_TYPE=VIRTUAL_99_FINAL_PLAN
PLAN_STATUS=FROZEN
~~~

因此：

~~~text
NO_REAL_ACTION_WITHOUT_FROZEN_AUTHORIZATION_PLAN=YES
~~~

Step 2 不得借“标定”自由探索。
Step 4 不得借“认证”现场修改方案。

## 2.2 METHOD_EXECUTION_CONTRACT

每次现实执行前必须存在机器可检查的执行合同。

至少冻结：

~~~text
METHOD_VERSION
TASK_ID
TASK_CONTRACT_HASH
VALID_CONTRACT_HASH
RESOURCE_BOUNDARY_HASH
PLAN_TYPE
PLAN_ID
PLAN_HASH
EXECUTION_MODE
AUTHORIZED_ACTIONS
FAILURE_POLICY
~~~

每个现实动作必须有：

~~~text
ACTION_ID
AUTHORIZED_STEP
ACTION_CLASS
IMMUTABLE_PARAMETERS
EXPECTED_EVIDENCE
VERIFIER
FAILURE_POLICY
~~~

Schema：

schemas/METHOD-EXECUTION-CONTRACT.schema.json

## 2.3 Pre-Action Conformance Gate

GPT、Codex、Browser、脚本或任何执行器在发出/执行现实动作以前，都必须证明：

~~~text
C1 method version 是当前 canonical
C2 TASK 已冻结
C3 VALID 已冻结
C4 Mature Solution Cluster 证据存在
C5 当前授权 plan 已 FROZEN
C6 plan hash 与 execution contract 一致
C7 ACTION_ID 在 plan 中
C8 参数没有越过冻结边界
C9 action class 合法
C10 verifier 与 expected evidence 已定义
C11 没有未解决 REALITY_DELTA
C12 旧流程没有获得当前授权
~~~

全部 PASS：

~~~text
EXECUTION_PERMISSION=ALLOW
~~~

任一 FAIL：

~~~text
EXECUTION_PERMISSION=DENY
FAIL_CLOSED=YES
SAVE_EVIDENCE
RETURN_TO_GPT
~~~

禁止“先执行、后解释”。

## 2.4 允许与禁止

现实层允许：

~~~text
MINIMAL_CALIBRATION
FINAL_CERTIFICATION
VERIFY
RECORD
CHECKPOINT_RESUME
AUTHORIZED_CONTROL_RECOVERY
AUTHORIZED_ROLLBACK
REMOTE_VERIFY
STOP
~~~

现实层禁止：

~~~text
SEARCH
NEW_CANDIDATE
NEW_EXPERIMENT
PARAMETER_SWEEP
MODEL_SWEEP
VERSION_SWEEP
PLAN_MUTATION
UNAUTHORIZED_RETRY
PATCH_IN_PLACE_TO_FIND_A_SOLUTION
~~~

执行器只拥有：

~~~text
HOW_TO_EXECUTE
~~~

不拥有：

~~~text
WHAT_TO_DO_NEXT
~~~

---

# 三、正式运行流程

## Gate 0：成熟方案集群闸口

先建立：

~~~text
REQUIRED_PRIMITIVES
MATURE_IMPLEMENTATIONS
COMPOSABILITY
UNSOLVED_PRIMITIVES
EVIDENCE
~~~

成熟覆盖完整时禁止重新发明。

## Step 1：冻结 VALID、现实边界与 T_PHY_VALID

冻结：

~~~text
TASK
VALID_CONTRACT
INITIAL_REAL_STATE
ACTIVE_RESOURCE_BOUNDARY
TIMING_BOUNDARY
USER_SEMANTICS
~~~

计算 T_PHY_VALID。

## Step 2：最小真实标定

先冻结 CALIBRATION_PLAN 和 METHOD_EXECUTION_CONTRACT，再运行最小必要现实测试。

目标只有：

~~~text
T_REAL_BASELINE
REAL_STATE_VALID_RANGE
T_COMPUTE
T_IO
T_WAIT
T_CONTROL
T_VERIFY
REAL_FAILURE_FACTS
~~~

不得在 Step 2 现场寻找“更好路线”。

## Step 3：成熟方案矩阵 -> GPT Virtual-99

成熟候选至少记录：

~~~text
SOURCE
HARDWARE_MATCH
TASK_MATCH
MECHANISM
EXPECTED_DELTA_T
QUALITY_RISK
STABILITY_RISK
INTEGRATION_COST
REVERSIBLE
~~~

随后：

~~~text
CURRENT
-> mature solution cluster
-> interaction correction
-> residual gap
-> compare T_PHY_VALID
-> compare REAL_STATE_VALID_RANGE
-> fault simulation
-> freeze VIRTUAL_99_FINAL_PLAN
~~~

冻结时必须产生：

~~~text
PLAN_ID
PLAN_HASH
AUTHORIZED_ACTION_SEQUENCE
EXPECTED_EVIDENCE
VERIFIERS
FAULT_INJECTIONS
EXPECTED_RECOVERY
FAILURE_POLICY
~~~

## Step 4：完整现实案例注入与确定性认证

现实认证不是继续研发。

必须先形成：

~~~text
CERTIFICATION_CASE_BUNDLE
~~~

至少包含：

~~~text
CASE_TASK
EXPECTED_VALID_RESULT
AUTHORIZED_ACTION_SEQUENCE
FAULT_INJECTIONS
EXPECTED_RECOVERY
EVIDENCE_REQUIREMENTS
FINAL_VERIFIER
~~~

然后逐动作经过 Pre-Action Conformance Gate 后执行。

### PASS

~~~text
REAL_END_TO_END_CERTIFICATION=PASS
EXECUTION_CONFORMANCE_RATE=100%
UNAUTHORIZED_ACTION_COUNT=0
PLAN_MUTATION_DURING_REAL_EXECUTION=0
-> FINAL_99_FREEZE
~~~

### FAIL

出现未预测现实问题时：

~~~text
STOP
-> preserve evidence
-> REALITY_DELTA
-> RETURN_TO_GPT
-> update Virtual-99
-> freeze new plan version
-> rerun certification
~~~

禁止：

~~~text
FAIL
-> Codex/GPT现场patch
-> 继续试
-> 边跑边重新设计
~~~

---

# 四、执行一致性是 FINAL-99 的硬门

定义：

~~~text
EXECUTION_CONFORMANCE_RATE
= authorized executed actions / total executed actions
~~~

FINAL-99 必须同时满足：

~~~text
EXECUTION_CONFORMANCE_RATE=100%
UNAUTHORIZED_ACTION_COUNT=0
REAL_SEARCH_ACTION_COUNT=0
PLAN_MUTATION_DURING_REAL_EXECUTION=0
OUT_OF_PLAN_CONTINUE_COUNT=0
EVIDENCE_COVERAGE=100%
CURRENT_METHOD_PRECEDENCE=PASS
~~~

任一不满足：

~~~text
FINAL_99=NO
FREEZE=NO
~~~

特别禁止：

~~~text
PASS_BY_DESIGN
~~~

代替真实运行证据。

设计写了“不会自由探索”，不等于现实已经证明“没有自由探索”。

---

# 五、随机/发散系统

v2/v3 已验证能力继续继承。

~~~text
ATTEMPT = 一次候选
DELIVERY = 最终有效交付
T_TFVR = Time To First Valid Result
~~~

如果随机变量不是用户任务语义：

~~~text
fast proposal
-> deterministic verifier
-> FAIL reject
-> resample within same frozen path
-> first PASS accept
~~~

如果 exact seed / exact reproducibility / benchmark A/B 属于 TASK，则不得换 seed。

随机重采样本身必须预先属于冻结 plan，不能由现实执行器临场添加。

---

# 六、失败分层

继续使用：

~~~text
CONTROL_PLANE_FAILURE
EXECUTION_ENVIRONMENT_FAILURE
SOURCE_IDENTITY_FAILURE
RANDOM_ATTEMPT_QC_FAILURE
ALGORITHM_QUALITY_FAILURE
PERFORMANCE_FAILURE
DELIVERY_SYSTEM_FAILURE
METHOD_EXECUTION_DRIFT
~~~

新增：

~~~text
METHOD_EXECUTION_DRIFT
~~~

一旦发生，优先级高于继续业务执行：

~~~text
STOP
-> EVIDENCE
-> RETURN_TO_GPT
~~~

---

# 七、自动执行控制层的从属关系

GPT-Codex 自动控制层只是本方法的执行设施，不能定义母方法。

当前母方法的 canonical 生命周期只有：

~~~text
MATURE_SOLUTION_CLUSTER
-> FROZEN_MINIMAL_CALIBRATION_PLAN
-> MINIMAL_REAL_CALIBRATION
-> VIRTUAL_99_FROZEN
-> REAL_END_TO_END_CERTIFICATION
-> PASS: FINAL_99_FREEZE
-> FAIL: REALITY_DELTA_RETURN_TO_GPT
~~~

旧的：

~~~text
L0 / L1 / L2 / L3 / L4
Shadow Pilot
Assisted Pilot
Multi-Scenario Regression
~~~

可以保留为历史证据标签，但：

~~~text
LEGACY_MATURITY_LABEL_AUTHORITY=NONE
LEGACY_EXECUTION_AUTHORITY=NONE
~~~

它们不得决定当前下一步，也不得绕过 v3.1 的执行合同。

GPT-Codex 子技能在真正用于现实认证以前，也必须先升级/适配到本 v3.1 conformance protocol。

---

# 八、成熟方案来源

v3.1 执行强制层不是从零发明。

已吸收的成熟 primitive 包括：

~~~text
Policy Decision / Policy Enforcement separation
Policy-as-code
Explicit state machine
Retry / Catch / Fail
Fail-closed behavior
Durable execution
Deterministic replay/resume
Auditable execution history
~~~

来源记录：

sources/EXECUTION-ENFORCEMENT-MATURE-CLUSTER.md

正式执行协议：

references/EXECUTION-CONFORMANCE-PROTOCOL-v1.md

回归检查：

tests/EXECUTION-CONFORMANCE-CHECKLIST-v1.md

---

# 九、H3-P0 历史实证继续有效

冻结事实保持：

~~~text
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
~~~

v3.1 不重开 H3-P0。

---

# 十、版本优先级与兼容

~~~text
CANONICAL_SKILL_ID=first-principles-physical-limit-convergence
CURRENT_VERSION=3.1.0
CURRENT_BRANCH=codex/first-principles-physical-limit-convergence-v3.1.0
PREVIOUS_VERSION=3.0.0
~~~

历史资料全部保留，但发生冲突时：

~~~text
v3.1 canonical rule
> v3.0
> v2/v1
> project-specific legacy workflow
> historical status labels
~~~

历史只能提供证据，不能偷偷恢复执行权。

---

# 最终一句话

> **v3.0 解决“应该怎么做”；v3.1 再解决“怎样保证现实只能按已经决定的方式做”：没有冻结计划证明，就没有现实执行权限；现实失败只产生证据和 REALITY_DELTA，真正改方案必须回到 GPT Virtual-99。**
