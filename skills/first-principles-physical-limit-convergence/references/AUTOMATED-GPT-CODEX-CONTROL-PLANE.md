# GPT-Codex 自动控制面

状态：`UNDER_VALIDATION / OPTIONAL_EXECUTION_LAYER`

## 1. 定位

自动控制面不是独立于 `first-principles-physical-limit-convergence` 的另一套方法，而是该母技能的**可选执行控制层**。

四步法仍然只有：

```text
第1步：物理极限
第2步：本机现实最优区间
第3步：GPT Virtual-99
第4步：Codex 完整实测命令包
```

自动化只负责把第3步与第4步之间、以及第4步返回 GPT 的人工搬运去掉：

```text
规划/裁决仍由 GPT 完成
执行仍由 Codex 完成
GitHub 保存编号化事实
AI Browser 只负责唤醒 GPT
```

如果自动化本身增加了大量等待、重复执行、状态不一致或人工看守，则它不满足第一性原理的时间目标，不能启用。

## 2. 核心架构：Codex-first

唯一常驻主动方是 Codex：

```text
CODEX = LOOP_OWNER / ACTIVE_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = NUMBERED_MESSAGE_BUS + SHARED_TRUTH
AI_BROWSER = CODEX_TO_GPT_WAKEUP_TRANSPORT
CAPACITY_ROUTER = CODEX_MODEL_AVAILABILITY
```

GPT 不轮询仓库；Codex 在需要 GPT 决策时写编号请求并唤醒 GPT。

GPT 被唤醒后直接读取 GitHub 请求与证据，完成规划/裁决，再直接在 GitHub 写下一条编号命令。

Codex 只消费 GitHub 的已核验命令，不把 ChatGPT 页面长文本当业务事实源。

## 3. 最高执行宪法

```text
NO_FREE_EXPLORATION=YES
CODEX_PLAN_AUTHORITY=NONE
BOUNDED_EXECUTION_FLEXIBILITY=YES
GPT_PLAN_AUTHORITY=YES
```

一句话：

> Codex 可以灵活决定“怎么完成一个已经授权的动作”，绝不能决定“接下来做什么”。

Codex 可以：

- PowerShell / `.ps1` 等价改写；
- 路径修正；
- 日志、备份、报告；
- checkpoint/resume；
- Git冲突、浏览器重连、capacity恢复；
- 执行 GPT 已冻结的 PASS/FAIL/ROLLBACK/RETRY 状态机。

Codex 不可以：

- 新增或删除候选；
- 修改候选顺序；
- 修改模型、版本、seed、step、sampler、scheduler；
- 修改运行次数、GPU预算、时间预算；
- 修改质量门禁、统计规则、成功定义；
- 自行开启 profiler、kernel trace、参数/版本 sweep；
- 因一个结果“有意思”而派生新实验；
- 没有 GPT 授权时自行填补下一步。

没有授权动作时唯一合法路径：

```text
CHECKPOINT
-> 写 CODEX->GPT 编号请求
-> push + remote verify
-> AI Browser 唤醒 GPT
-> 等待 GPT 写回下一编号命令
```

## 4. 编号化共同工作区

每个任务：

```text
workspaces/<TASK_ID>/
  TASK.md
  STATE.json
  queue/
    000001-CODEX-REQUEST-GPT.json
    000002-GPT-COMMAND-CODEX.json
    000003-CODEX-RESULT-GPT.json
    000004-GPT-DECISION-CODEX.json
    ...
  payloads/
  ARTIFACTS.md
  EVENTS.jsonl
```

每条编号消息不可覆盖。新信息只能增加更高序号。

`STATE.json` 至少保存：

```text
TASK_ID
PHASE
STATUS
LAST_REMOTE_HEAD
LAST_CONSUMED_SEQ
MAX_REMOTE_SEQ
COMPLETED_STEPS
DO_NOT_REPEAT
NEXT_ACTION
REQUESTED_MODEL
ACTUAL_MODEL
FALLBACK_REASON
UPDATED_AT
```

## 5. Codex 主循环

```text
START/RESUME
-> capacity router preflight
-> git fetch + remote verify
-> read STATE + queue
-> 有已授权 GPT->CODEX 消息：幂等检查 -> 执行 -> 写 RESULT -> push/verify
-> 无已授权消息但需要 GPT：写 REQUEST -> push/verify -> Browser wake GPT
-> 等待 GitHub 出现 GPT 下一编号消息
-> LOOP
```

普通命令包内已经覆盖的 PASS/FAIL/ROLLBACK 不调用 GPT，直接继续。

只有：

- 新任务初次规划；
- `RETURN_TO_GPT`；
- 命令包外异常；
- Final Certification；
- TASK_CONTRACT 改变；

才请求 GPT。

## 6. Browser 最小职责

复用现有成熟浏览器技能：

```text
C:\AI\Playwright-Native-AI-Browser
skills/chatgpt-web-plan-bridge-latest
```

Browser 只负责：

- 打开/复用指定 ChatGPT 会话；
- 发送最小 wakeup：TASK_ID / SEQ / repo / branch / request path；
- 等待短 ACK / BLOCKED / USER_APPROVAL_REQUIRED；
- 保存 transport 证据。

Browser **不搬运完整命令、完整结果或大段业务正文**。

## 7. 幂等、断点与 DO_NOT_REPEAT

每个动作绑定：

```text
ACTION_ID = TASK_ID + MESSAGE_SEQ + SOURCE_COMMIT + ACTION_TYPE
```

如果 ACTION_ID 已完成：

```text
REPLAY=NO
```

必须保存：

```text
COMPLETED_STEPS
DO_NOT_REPEAT
```

模型 capacity、浏览器掉线、Windows重启、重复 GitHub poll、重复 wakeup 都不得重放已完成本地工作。

## 8. Capacity Router

复用：

```text
skills/codex-capacity-aware-model-router
```

capacity 属于控制面：

```text
checkpoint
-> failover
-> resume same Codex loop
```

如果全部模型不可用：

```text
BLOCKED_REMOTE_CAPACITY
```

不改业务裁决，不重放本地工作。

## 9. 用户审批边界

自动循环必须停在：

- 登录/验证码；
- 账户/支付/安全设置；
- 代理/网络改变；
- 管理员/系统敏感操作；
- 大规模删除；
- TASK_CONTRACT 改变；
- 未授权新研究方向；
- 用户 STOP / PAUSE。

普通冻结命令执行、状态同步、Git提交与 transport 不需要用户复制粘贴。

## 10. 成熟度阶梯

自动控制面必须按以下顺序成熟，禁止跳级：

```text
L0 SPEC_READY
-> L1 SHADOW_PILOT_PASS
-> L2 ASSISTED_REAL_TASK_PASS
-> L3 MULTI_SCENARIO_REGRESSION_PASS
-> L4 MATURE_REUSABLE
```

### L0 — SPEC_READY

架构、状态机、编号总线、幂等、权限边界写清楚，但尚未真实闭环。

### L1 — SHADOW_PILOT_PASS

使用 toy task 完整证明：

```text
Codex主动请求GPT
-> GPT直接写GitHub命令
-> Codex执行
-> Codex写结果
-> GPT裁决
-> Codex冻结
```

要求：

```text
MANUAL_COPY_PASTE_REQUIRED=NO
NO_FREE_EXPLORATION=YES
NO_REPLAY=YES
```

### L2 — ASSISTED_REAL_TASK_PASS

选一个低风险、真实、可回滚任务，完整跑通同一闭环。

验证的不是 toy transport，而是：

```text
真实任务合同
+ GPT真实规划
+ Codex真实执行
+ 多轮结果/裁决
+ checkpoint/resume
+ final freeze
```

用户只允许做 STOP/敏感审批，不做普通搬运。

### L3 — MULTI_SCENARIO_REGRESSION_PASS

至少覆盖不同任务类别与异常：

- 一次即可完成；
- 多轮 GPT↔Codex；
- 正常 PASS/FAIL/ROLLBACK；
- 浏览器中断恢复；
- capacity mock/真实自然触发；
- Windows/Orchestrator重启；
- duplicate poll/wakeup；
- unknown exception -> BLOCKED；
- user STOP。

### L4 — MATURE_REUSABLE

只有 L1-L3 全部有真实证据后才允许：

```text
AUTOMATION_MODULE=MATURE_REUSABLE
```

此时其他技能包可按需唤醒。

## 11. 何时自动唤醒

只有达到 `MATURE_REUSABLE` 后，母技能才允许在下列条件自动建议/调用：

```text
预计需要 GPT<->Codex 两轮及以上；
或任务包含长时间本地执行；
或需要 checkpoint/resume；
或用户人工搬运本身已经成为显著时间成本；
或已有冻结命令包需要多阶段执行/裁决。
```

短任务、一次性命令、需要高频人工视觉判断的任务可以不用自动控制面。

原则：

> 自动化本身也必须服从第一性原理时间目标；如果自动化的启动/维护成本大于人工执行收益，就不唤醒。

## 12. 当前状态

截至当前：

```text
AUTOMATION_CONTROL_PLANE=L0_SPEC_READY
CODEX_FIRST_ARCHITECTURE=FROZEN
SHADOW_PILOT=NOT_YET_EXECUTED
ASSISTED_REAL_TASK=NOT_YET_EXECUTED
MULTI_SCENARIO_REGRESSION=NOT_YET_EXECUTED
MATURE_REUSABLE=NO
```

对应专门技能：

```text
gpt-codex-convergence-orchestrator v1.1.0
```

真实测试前不得把它描述为成熟无人值守系统。

## 13. 最终原则

> 自动化是第一性原理收敛引擎的执行控制层：它自动化 transport、状态同步、checkpoint 与已授权状态机；不自动化 GPT 的研究决策权，也不赋予 Codex 业务规划权。