# Distribution Note — v3.1.0

正式 Skill ID 不变：

first-principles-physical-limit-convergence

当前中文名：

**第一性原理极限短时间引擎**

v3.1.0 是 v3.0.0 的执行约束升级。

## 三个核心不变

~~~text
1. 极限短时间
2. 成熟方案集群
3. 高智能虚拟成熟
~~~

## v3.1 新增：方法-执行一致性强制层

v3.0 的缺口不是方法方向错误，而是缺少“现实动作必须证明自己属于冻结方案”的硬门。

v3.1 固定：

~~~text
NO_REAL_ACTION_WITHOUT_FROZEN_AUTHORIZATION_PLAN=YES
PRE_ACTION_CONFORMANCE_GATE=MANDATORY
FAIL_CLOSED=YES
CURRENT_METHOD_PRECEDENCE=ABSOLUTE
LEGACY_EXECUTION_AUTHORITY=NONE
~~~

Step 2 只能来自 FROZEN CALIBRATION_PLAN。
Step 4 只能来自 FROZEN VIRTUAL_99_FINAL_PLAN。

现实失败不能现场继续找方案：

~~~text
FAIL
-> STOP
-> EVIDENCE
-> REALITY_DELTA
-> RETURN_TO_GPT
-> NEW VIRTUAL PLAN
-> REFREEZE
-> RECERTIFY
~~~

旧 L0/L1/L2/L3/L4 仅保留为历史证据标签，不再具有当前流程授权权。

正式分支：

codex/first-principles-physical-limit-convergence-v3.1.0

上一正式分支永久保留：

codex/first-principles-physical-limit-convergence-v3.0.0
