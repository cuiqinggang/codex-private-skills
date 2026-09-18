# v3.1 Execution-Enforcement Mature Solution Cluster — Official Sources

本文件记录 v3.1“方法-执行一致性强制层”使用的现实成熟结构。目的不是照搬某一个产品，而是吸收已经成熟的 primitive，再组合进本技能。

## 1. Policy Decision / Policy Enforcement separation

Open Policy Agent 官方文档把 OPA 定义为 Policy Decision Point，应用侧作为 Policy Enforcement Point；策略判断和执行位置分离，且策略可作为代码统一执行。

- https://www.openpolicyagent.org/docs
- https://www.openpolicyagent.org/docs/deploy

映射到 v3.1：

- VIRTUAL_99_FINAL_PLAN / METHOD_EXECUTION_CONTRACT = policy truth
- PRE_ACTION_CONFORMANCE_GATE = policy decision
- GPT / Codex / Browser / scripts = enforcement points
- 未通过 gate = 不允许执行

## 2. Explicit state machine + Retry/Catch/Fail

AWS Step Functions 官方文档使用显式状态机定义动作、Retry、Catch、Timeout 和 Fail 行为。未定义的异常不会自然变成新的业务路线。

- https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
- https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
- https://docs.aws.amazon.com/step-functions/latest/dg/state-fail.html

映射到 v3.1：

- 冻结 plan 定义允许状态转换
- 已授权 retry/rollback 才能执行
- out-of-plan 默认 FAIL_CLOSED
- 未知异常 -> STOP / RETURN_TO_GPT

## 3. Durable execution / deterministic replay

Temporal 官方文档把 durable execution 的核心定位为：发生崩溃、网络或基础设施故障后从原位置恢复；Temporal 的确定性工作流资料强调相同输入/历史应产生相同命令序列，才能可靠 replay/resume。

- https://docs.temporal.io/
- https://learn.temporal.io/assets/files/temporal-102-with-java-replay2025-468b8109d5a9ce33b36c2910c48433d9.pdf

映射到 v3.1：

- CHECKPOINT/RESUME 不能改变业务方案
- 恢复只能继续冻结 action
- 运行恢复不等于重新规划
- plan mutation 必须返回 GPT 并产生新的 frozen plan version

## 4. v3.1 组合结论

现实成熟结构共同指向同一个执行规律：

~~~text
POLICY / PLAN FIRST
-> MACHINE-CHECKABLE AUTHORIZATION
-> EXPLICIT STATE TRANSITION
-> FAIL CLOSED
-> DURABLE RESUME WITHOUT PLAN MUTATION
-> AUDITABLE EVIDENCE
~~~

因此 v3.1 的执行一致性层属于成熟方案集群的组合适配，不是重新发明一套可靠自动化理论。
