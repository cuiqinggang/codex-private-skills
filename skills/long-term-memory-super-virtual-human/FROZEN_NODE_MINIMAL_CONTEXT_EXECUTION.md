# 长期记忆超级虚拟人 v0.7.0｜冻结节点·动态短上下文执行

## 1. 第一性原理目标

唯一目标不变：T*=min(T_VALID)。页面更短、节点更多、并行更多都不是目标本身；只有在降低完整 T_VALID 时才成立。

每个节点结束后比较四类成本：继续当前页的理解/噪声/卡顿成本；换真 New chat 的保存与重理解成本；拆分并行的收益与协调成本；保留旧页造成的浏览器/内存/CPU资源成本。选择预计完整 T_VALID 最低的路径。

## 2. 最小完整闭环节点

节点不是最小动作，而是最小可独立验收闭环：一个主要目标 + 一组高度相关依赖 + 明确边界 + DONE_WHEN + 可独立验收结果。

过细会增加重理解、调度、保存和换页成本；过粗会增加上下文噪声、串行时间和故障半径。

## 3. Node Freeze 与 Version Freeze

Node Freeze 用于一个任务/阶段闭环完成，只保存有效结论、现实结果、证据、未决项和下一节点必要输入；完整讨论与失败尝试默认不进入下一工作上下文。

Version Freeze 只用于方法论、默认运行合同、架构或成熟能力发生实质变化。普通节点完成不强制升版本。

## 4. 页面决策

固定字数/轮数只保留为保险，不再作为主要触发器。

节点未闭环时，如果当前页继续最快就继续。节点已闭环后，先持久化/冻结，再比较继续当前页和真 New chat，哪个预计 T_VALID 更低就选哪个。下一节点明显独立或复杂时默认倾向真 New chat；多个相近且简单、共享大量上下文的节点可以留在同一页完成一批后统一冻结。

核心：SEMANTIC_BOUNDARY_BEATS_TOKEN_THRESHOLD。

## 5. 旧页面生命周期

旧页面不是资产，冻结状态才是资产。顺序固定为 Persist/Freeze First，Close Second。

如果旧页节点已完成、结论已持久化、无未决动作、无恢复/观察价值，则默认关闭，避免占用浏览器资源影响新页面和并行执行。只有逻辑上能证明保留有价值时才继续保留。

## 6. 并行原则

短上下文节点天然适合并行，但并行必须满足：依赖独立、无写冲突、无共享资源冲突、结果可合并。

可并行节点尽量同时执行，最大并行度由当前机器、浏览器、模型/工具吞吐和任务冲突动态决定。禁止为了多智能体而多智能体；若协调成本大于并行收益，则保持单路。

## 7. 多智能体

多智能体是执行策略，不是强制架构。适用于多个相互独立的小闭环、可并行检索/验证/实现、输入冻结且输出合同明确的节点。不适用于强串行依赖、多写者修改同一权威状态、或持续依赖复杂隐含上下文的任务。

所有并行节点必须从同一冻结父节点出发，并在合并前分别 Reality 验收。

## 8. ECC V3.1 的位置

ECC V3.1 是专业长流程工具，按需调用，不是 v0.7 强制运行层。

当任务需要长期连续性、Checkpoint、lease/fencing、takeover、Gate/Repair 时，由 ECC 持有长流程连续性；v0.7 Frozen Node 作为最小执行单元；节点可串行或并行；节点完成即冻结；ECC 只接收冻结结果，不承载完整页面历史。

简单任务不因为存在 ECC 而强制进入 ECC。

## 9. Codex / Runner / 审计

Codex、GitHub Runner、Reasonix、GPT 直接工具均属于执行器候选。选择标准只有一个：在 VALID 前提下完整 T_VALID 最低。

四角色独立审计不作为 v0.7 全局硬要求。它可用于高风险节点、结构性版本升级、复杂代码变更或用户明确要求。普通低风险节点采用最小充分验证，避免审计成本反过来拉长 T_VALID。

## 10. 冻结后新页最小入口

新页面不重放旧聊天，只读取：CURRENT_VERSION + PARENT_FROZEN_NODE + CURRENT_NODE_GOAL + HARD_BOUNDARIES + DONE_WHEN + 必要输入/证据定位。

原则：CONCLUSION_SURVIVES_HISTORY_DOES_NOT。历史失败尝试只保存在证据/日志中，除非与当前节点直接相关，否则不进入工作上下文。

## 11. 动态调度规则

如果预计 T_VALID(继续当前页) <= 预计 T_VALID(冻结+换页+重理解)，则 CONTINUE；否则 FREEZE → TRUE_NEW_CHAT。

如果存在独立节点集合 P，且预计 T_VALID(并行P) < 预计 T_VALID(串行P)，则 PARALLEL；否则 SERIAL。

不要求精确数学预测；允许用历史 Reality、当前页面长度、任务耦合度、机器负载和执行器吞吐做快速判断。

## 12. v0.7.0 核心合同

OBJECTIVE=T*=min(T_VALID)
LONG_TASK_NE_LONG_CONTEXT=YES
MIN_EXECUTION_UNIT=MINIMAL_COMPLETE_VALIDATABLE_NODE
NODE_FREEZE_REQUIRED_AT_SEMANTIC_BOUNDARY=YES
VERSION_FREEZE_ONLY_FOR_SYSTEMIC_CHANGE=YES
ROTATION_DECISION=DYNAMIC_T_VALID_MINIMIZATION
TRUE_NEW_CHAT_WHEN_ROTATION=YES
FULL_HISTORY_REPLAY=NO
CONCLUSION_SURVIVES_HISTORY_DOES_NOT=YES
PARALLELIZE_WHEN_INDEPENDENT_AND_FASTER=YES
MULTI_AGENT_REQUIRED=NO
ECC_REQUIRED=NO
ECC_MODE=ON_DEMAND_LONG_FLOW_TOOL
FOUR_ROLE_AUDIT_REQUIRED=NO
AUDIT_DEPTH=RISK_AND_VALIDITY_DRIVEN
CLOSE_VALUELESS_FROZEN_PAGES=YES
FIXED_CONTEXT_THRESHOLDS=FALLBACK_GUARD_ONLY

## 13. 当前成熟度边界

v0.7.0 当前先固化方法合同，不虚构动态调度器已经全自动实现。

既有 Reality 已支撑：true New chat + minimal handoff；checkpoint / exactly-once；干净 CEO 生命周期；页面关闭后恢复单空白页；v0.6 第一性原理故障分析；Goal Loop。

后续 Reality：同构任务继续当前页 vs 冻结换页 T_VALID 对比；多独立 Frozen Node 串行 vs 并行 T_VALID；不同并行度下机器负载与完整 T_VALID；自动页面价值判断与关闭；动态节点调度器。

## 14. v0.7.0 透明有界调度修正（2026-10-04）

用户现场观察到多个任务同时出现“系统正在进一步处理此请求”，但专用浏览器只有单页实际执行。该状态暴露出当前运行层仍可能把多个独立任务汇入单一全局 writer / 单 leased page 的 FIFO 队列，形成不可见等待。该行为与 v0.7“最小完整节点 + 可安全并行”的目标不一致。

新增运行合同（当前为待 Reality 的候选合同，不冒充已通过）：

```ini
OPAQUE_LONG_QUEUE=FORBIDDEN
TASK_UNIT=MINIMAL_COMPLETE_VALIDATABLE_NODE
NODE_STATUS_REQUIRED=YES
NODE_STATUS_SET=QUEUED|DISPATCHED|RUNNING|WAITING_EXTERNAL|BLOCKED|STALL_SUSPECTED|VALID|FAILED
QUEUE_POSITION_VISIBLE=REQUIRED_WHEN_QUEUED
ONE_DEDICATED_BROWSER_INSTANCE=YES
SECOND_PERSISTENT_BROWSER=FORBIDDEN
MULTI_PAGE_WITHIN_ONE_BROWSER=BOUNDED_AND_SCHEDULED
DEFAULT_PAGE_CONCURRENCY_CANDIDATE=3
HARD_PAGE_CAP_UNTIL_REALITY=3
SHARED_WRITE_CONFLICT=SERIALIZE
INDEPENDENT_READ_OR_EXECUTE=PARALLELIZE_WHEN_FASTER
CEO_PAGE=ROUTER_AND_ACCEPTANCE_GATE
EXECUTOR_PAGE=ONE_SMALL_NODE_OR_TIGHTLY_COUPLED_NODE_BATCH
EXECUTOR_REPORT_AFTER_EACH_NODE=YES
```

解释：
- “只允许一个专用浏览器”不等于“只能一个执行页面”。允许在同一个 persistent browser/context 内创建**受控、有上限、可追踪**的 executor 页面；
- 禁止多个 runtime/owner 各自启动浏览器或无限开标签页；
- 默认候选并发为 3，只是现场修正的运行上限候选；最终 2/3/4 的最优并行度必须由 R2 Reality 的完整 T_VALID 与机器负载决定；
- 有共享写状态、同一账号敏感 UI 写操作、同一权威文件写入时必须串行；纯读取、独立计算、独立验证可并行；
- 每个节点必须可看到明确状态，不能只显示“处理中”而无法区分真正运行、排队、等待外部返回或疑似卡死；
- CEO 页面只做任务拆分、优先级、派发、合并和验收；执行页不承担长期总控历史。

### 模型/Thinking 强度补充

执行页不得默认继承 High。默认遵循“最低充分能力”：

```ini
SIMPLE_EXECUTOR_DEFAULT=Instant_or_Medium
NORMAL_EXECUTOR_DEFAULT=Medium
HIGH=ONLY_WHEN_COMPLEXITY_OR_REWORK_RISK_JUSTIFIES
EXTRA_HIGH_OR_PRO=EXCEPTION_ONLY
CEO_ROUTER_DEFAULT=Medium
MODEL_EFFORT_READBACK_REQUIRED=YES
RESTORE_OR_SET_PER_STAGE=YES
```

High 是按任务需要提升的档位，不是专用浏览器的永久默认状态。R14 中恢复到 High 只证明切换与恢复能力，不构成“所有后续执行都应 High”的默认策略。

### 黑箱状态判定

ChatGPT 页面出现“系统正在进一步处理此请求/处理完毕将给出回复”只表示该 turn 尚未给出最终回复，不能单独证明“仍在有效推进”。

外部 supervisor 必须结合：
- 最近可观测进展时间；
- turn 是否 active；
- 页面/工具是否有新证据；
- 任务是否已实际 dispatch；
- 队列位置；
- silence window / hard deadline；

将状态归类为 RUNNING、WAITING_EXTERNAL、QUEUED 或 STALL_SUSPECTED；达到确认停滞门后才执行 checkpoint → abort/fence → true New chat / 其他有效恢复路径。

