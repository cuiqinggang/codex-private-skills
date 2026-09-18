# Execution Conformance Protocol v1 — v3.1

## 1. 修复目标

v3.0 已经定义了正确方法，但仍允许出现“方法写一套、现实执行另一套”的漂移。

v3.1 增加一个强制执行层。它不是第四个优化目标，也不是第四个方法核心；它只负责把既有三原则变成不可绕过的运行约束。

正式不变量：

~~~text
METHOD_LOGIC != EXECUTION_PERMISSION

任何现实动作都必须先证明：
它属于已经冻结的 VIRTUAL_99_FINAL_PLAN。
否则没有执行权限。
~~~

## 2. 五个强制对象

~~~text
CURRENT_METHOD_VERSION
TASK_CONTRACT
VALID_CONTRACT
VIRTUAL_99_FINAL_PLAN
METHOD_EXECUTION_CONTRACT
~~~

其中 VIRTUAL_99_FINAL_PLAN 必须有不可变 plan_id / plan_hash。

METHOD_EXECUTION_CONTRACT 必须把每一个允许的现实动作映射到：

~~~text
ACTION_ID
AUTHORIZED_STEP
ACTION_CLASS
IMMUTABLE_PARAMETERS
EXPECTED_EVIDENCE
VERIFIER
FAILURE_POLICY
~~~

## 3. Pre-Action Conformance Gate

任何现实动作执行前必须逐项通过：

~~~text
C1 CURRENT_METHOD_VERSION == canonical version
C2 TASK_CONTRACT frozen
C3 VALID_CONTRACT frozen
C4 required mature-solution-cluster evidence exists
C5 VIRTUAL_99_FINAL_PLAN == FROZEN
C6 plan_hash matches current execution contract
C7 ACTION_ID exists in frozen plan
C8 parameters stay inside frozen action contract
C9 action class is allowed
C10 expected evidence + verifier are defined
C11 no unresolved REALITY_DELTA exists
C12 no legacy workflow has higher authority
~~~

只有全部 PASS：

~~~text
EXECUTION_PERMISSION=ALLOW
~~~

任何一项 FAIL：

~~~text
EXECUTION_PERMISSION=DENY
FAIL_CLOSED=YES
SAVE_EVIDENCE
RETURN_TO_GPT
~~~

不得由 GPT、Codex、Browser、脚本或人工“先做了再说”。

## 4. 允许的现实动作类型

在冻结 Virtual-99 之后，只允许：

~~~text
MINIMAL_CALIBRATION
FINAL_CERTIFICATION
AUTHORIZED_CONTROL_RECOVERY
VERIFY
RECORD
CHECKPOINT_RESUME
AUTHORIZED_ROLLBACK
REMOTE_VERIFY
STOP
~~~

禁止：

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

执行器仍可在同一个授权动作内选择等价执行方式，但不得改变动作语义、参数边界、验证条件或后续路线。

## 5. 现实案例注入

现实认证必须使用预先冻结的 CERTIFICATION_CASE_BUNDLE。

它至少包含：

~~~text
CASE_TASK
EXPECTED_VALID_RESULT
AUTHORIZED_ACTION_SEQUENCE
FAULT_INJECTIONS
EXPECTED_RECOVERY
EVIDENCE_REQUIREMENTS
FINAL_VERIFIER
~~~

故障注入不是现场探索；它必须在 Virtual-99 阶段预先定义。

## 6. 失败处理

如果现实认证出现未预见问题：

~~~text
DO NOT PATCH AND CONTINUE
DO NOT LET EXECUTOR INVENT NEXT STEP

STOP
-> preserve evidence
-> create REALITY_DELTA
-> return to GPT
-> update Virtual-99
-> freeze new plan version
-> rerun full certification
~~~

现实层负责提供 delta；方案层仍由高智能 Virtual-99 负责。

## 7. 执行一致性硬指标

~~~text
EXECUTION_CONFORMANCE_RATE
= authorized executed actions / total executed actions
~~~

FINAL-99 的硬门：

~~~text
EXECUTION_CONFORMANCE_RATE=100%
UNAUTHORIZED_ACTION_COUNT=0
REAL_SEARCH_ACTION_COUNT=0
PLAN_MUTATION_DURING_REAL_EXECUTION=0
OUT_OF_PLAN_CONTINUE_COUNT=0
EVIDENCE_COVERAGE=100%
CURRENT_METHOD_PRECEDENCE=PASS
~~~

任何一个不满足：

~~~text
FINAL_99=NO
FREEZE=NO
~~~

“PASS_BY_DESIGN”不能替代运行证据。

## 8. 版本与旧流程优先级

~~~text
CURRENT_CANONICAL_METHOD > legacy process > historical status labels
~~~

旧 L0/L1/L2/L3/L4、旧 command pack、旧 pilot 名称可以作为历史证据继续保留，但：

~~~text
LEGACY_EXECUTION_AUTHORITY=NONE
LEGACY_MATURITY_LABEL_AUTHORITY=NONE
~~~

它们不得决定当前流程，不得授权现实动作。

当前正式生命周期只有：

~~~text
MATURE_SOLUTION_CLUSTER
-> MINIMAL_REAL_CALIBRATION
-> VIRTUAL_99_FROZEN
-> REAL_END_TO_END_CERTIFICATION
-> PASS: FINAL_99_FREEZE
-> FAIL: REALITY_DELTA_RETURN_TO_GPT
~~~

## 9. 核心结论

v3.1 不再接受“规则写在文档里，因此默认会被遵守”。

正式原则：

~~~text
NO ACTION WITHOUT PLAN PROOF
NO PLAN MUTATION IN REAL EXECUTION
FAIL CLOSED ON METHOD DRIFT
REALITY CERTIFIES; GPT REDESIGNS
~~~