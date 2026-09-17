---
name: gpt-codex-convergence-orchestrator
description: 自动化 Codex 主动执行器与 GPT 按需规划器之间的收敛工作流。Codex 是唯一常驻主动循环，但没有业务规划权；只允许在已授权动作的执行方法上有限灵活。GitHub 是编号化命令/结果总线和共同事实源，AI Browser 只负责 Codex 唤醒 GPT，GPT 被唤醒后直接读写 GitHub 的下一条编号消息。用于去除用户在 GPT 与 Codex 之间反复复制粘贴的纯搬运动作，同时保持 GPT 负责规划/判断、Codex 负责确定性执行。
metadata:
  version: "1.1.0"
  method_dependency: "first-principles-physical-limit-convergence@2.0.0"
  browser_dependency: "chatgpt-web-plan-bridge-latest / local playwright-native-ai-browser"
  capacity_dependency: "codex-capacity-aware-model-router"
  architecture: "CODEX_FIRST_NUMBERED_GITHUB_BUS"
---

# GPT-Codex Convergence Orchestrator v1.1.0

## 0. 最高执行宪法：Codex 只能干活，不能决定干什么活

本技能直接继承 `first-principles-physical-limit-convergence` 的执行权边界：

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR + LOOP_OWNER
CODEX_PLAN_AUTHORITY=NONE
BOUNDED_EXECUTION_FLEXIBILITY=YES
GPT_PLAN_AUTHORITY=YES
```

一句话：

> **Codex 可以灵活决定“怎么完成同一个已经授权的动作”，绝不能灵活决定“接下来做什么”。**

### 0.1 Codex 允许的执行层灵活性

只允许为了完成**同一个已经授权的动作**，采用不改变任务含义的等价执行方法，例如：

- PowerShell 引号复杂时改成等价 `.ps1`；
- 相对路径失败时改成等价绝对路径；
- 使用同义命令完成同一个明确动作；
- 创建日志、临时文件、备份、报告；
- 会话/进程中断后恢复同一个未完成动作；
- 在命令包已经授权的 retry / rollback 分支内执行；
- 处理 Git fetch/push 冲突、编号冲突、浏览器重连、模型 capacity 等控制面恢复；
- 校验输入、哈希、远端 HEAD、PID、端口、文件是否已存在，避免重复执行。

这些都属于：

```text
HOW_TO_EXECUTE = CODEX_ALLOWED
```

### 0.2 Codex 绝对禁止的方案层自主权

Codex 不得自行：

- 选择“更好的”业务路线；
- 决定下一研究方向；
- 新增候选、删除候选、调整候选顺序；
- 修改模型、版本、seed、step、sampler、scheduler、分辨率、帧数；
- 修改运行次数、时间预算、GPU预算；
- 修改质量门禁、成功/失败阈值、统计规则；
- 开 profiler、kernel trace、参数 sweep、版本 sweep；
- 因为一个结果“看起来有意思”而继续派生新实验；
- 在 GPT 未授权时把一个局部失败扩展成新的研究任务；
- 把自己的推测写成下一条业务命令并执行；
- 用浏览器搜索、仓库搜索或本地代码探索来替代 GPT 的方案裁决。

这些都属于：

```text
WHAT_TO_DO_NEXT = GPT_ONLY
```

### 0.3 没有授权动作时 Codex 的唯一合法行为

如果当前没有可消费的 `GPT->CODEX` 编号命令，且当前冻结命令包也没有覆盖下一动作：

```text
保存当前状态
→ 写 CODEX->GPT REQUEST 新编号消息
→ push + remote verify
→ AI Browser 唤醒 GPT
→ 等待 GPT 在 GitHub 写下一条授权命令
```

Codex **不得填补这个空白**。

如果 GPT 不可用：

```text
CHECKPOINT
→ WAIT / BLOCKED
```

而不是自由探索。

### 0.4 Codex 可以判断“什么时候问 GPT”，但不能替 GPT 回答

Codex 只允许根据**已经冻结的触发规则**判断：

```text
NEED_GPT=YES/NO
```

例如：

- 命令包写明 `RETURN_TO_GPT`；
- 出现命令包外异常；
- Final Certification 需要裁决；
- 用户改变 TASK_CONTRACT。

Codex 不能因为自己认为“这个方向更有价值”而主动改变工作内容。

---

## 1. 核心架构

```text
CODEX = LOOP_OWNER / ACTIVE_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = NUMBERED_MESSAGE_BUS + SHARED_TRUTH
AI_BROWSER = CODEX_TO_GPT_WAKEUP_TRANSPORT
CAPACITY_ROUTER = CODEX_MODEL_AVAILABILITY
```

关键修正：**流程从 Codex 出发，不从 GPT 出发；但启动权不等于规划权。**

GPT 不是 daemon，也不负责轮询仓库。Codex 常驻或按计划恢复，持续读取 GitHub 远端状态；需要 GPT 决策时，由 Codex 写请求消息并通过 AI Browser 唤醒 GPT。

## 2. 角色边界

```text
GPT_ROLE=PLANNER/JUDGE/VIRTUAL_99
CODEX_ROLE=DETERMINISTIC_EXECUTOR + LOOP_OWNER
CODEX_PLAN_AUTHORITY=NONE
GITHUB_ROLE=SHARED_TRUTH + NUMBERED_BUS
BROWSER_ROLE=WAKEUP/ACK_TRANSPORT
ORCHESTRATOR_ROLE=CODEX_SIDE_STATE_MACHINE
```

Codex 可以决定的只有执行控制：

- 当前有没有待执行的已冻结命令；
- 当前命令包的哪一个**预先定义分支**已经被客观条件触发；
- 是否达到“需要 GPT”的**既定触发条件**；
- transport/checkpoint/idempotency 如何恢复；
- 同一个授权动作采用哪种等价执行形式。

Codex 不可以决定任何业务规划内容。

## 3. 编号化 GitHub 总线

正式协议见：

```text
references/CODEX-FIRST-NUMBERED-BUS-v1.md
```

每个任务：

```text
workspaces/<TASK_ID>/
  TASK.md
  STATE.json
  queue/
    000001-CODEX-REQUEST-GPT.json
    000002-GPT-COMMAND-CODEX.json
    000003-CODEX-RESULT-GPT.json
    000004-GPT-COMMAND-CODEX.json
    ...
  payloads/
    000001.md
    000002.md
    000003.md
  ARTIFACTS.md
  EVENTS.jsonl
```

每条消息不可变；新信息只能增加新序号，禁止覆盖旧消息。

## 4. Codex 主循环

```text
START/RESUME
→ capacity router preflight
→ git fetch + remote verify
→ read STATE + max(queue.seq)
→ find next READY message addressed to CODEX
    ├─ 有：幂等检查 → 确定性执行 → 写 RESULT 新消息 → push+verify
    └─ 无：按冻结规则判断是否需要 GPT
          ├─ 否：继续命令包内既定动作或等待
          └─ 是：写 CODEX->GPT REQUEST 新消息 → push+verify
                 → AI Browser wake GPT
                 → 等待 GitHub 出现 GPT->CODEX 更高序号消息
→ LOOP
```

Codex 不把 ChatGPT DOM 中的长文本当作命令事实源，也不自己生成缺失的业务命令。

## 5. GPT 被动调用模型

浏览器只向 GPT 发送最小 wakeup：

```text
TASK_ID=<...>
REQUEST_SEQ=<000001>
REPOSITORY=cuiqinggang/codex-private-skills
BRANCH=<...>
REQUEST_FILE=<queue/path>
请读取 GitHub 请求与证据，完成判断，并直接写下一条 GPT->CODEX 编号消息到同一 workspace。
```

GPT 完成：

1. 从 GitHub 读取请求、状态和证据；
2. 规划/判断；
3. 在 GitHub 创建下一条单调序号消息和 payload；
4. remote verify；
5. 页面只返回短 ACK：

```text
GPT_COMMIT_OK TASK_ID=<...> SEQ=<000002> HEAD=<sha>
```

Codex真正消费的是 GitHub 消息，不是 ACK 文本。

## 6. 何时请求 GPT

只有冻结规则允许的场景：

- 新任务第一次需要规划；
- 冻结命令包明确要求 `RETURN_TO_GPT`；
- 命令包外异常；
- Final Certification 需要 GPT 裁决；
- 用户改变 TASK_CONTRACT。

普通 PASS/FAIL/ROLLBACK 如果命令包已经写明，Codex直接继续，不调用 GPT；但只能走**命令包预先定义的分支**。

## 7. 状态机

控制状态以 Codex 为中心：

```text
NEW
→ CODEX_REQUESTING_GPT
→ WAITING_FOR_GPT_COMMIT
→ READY_FOR_CODEX
→ CODEX_RUNNING
→ CODEX_RESULT_COMMITTED
→ CODEX_REQUESTING_GPT | READY_FOR_CODEX | FREEZE | BLOCKED | USER_APPROVAL_REQUIRED
```

`STATE.json` 与 queue 都必须以远端 commit 为事实依据。

## 8. 幂等与去重

```text
ACTION_ID = TASK_ID + MESSAGE_SEQ + SOURCE_COMMIT + ACTION_TYPE
```

如果 ACTION_ID 已完成：

```text
REPLAY=NO
```

浏览器重复 wakeup、GitHub poll 重复、Windows 重启、模型切换都不得重放已完成本地动作。

## 9. DO_NOT_REPEAT

必须持续保存：

```text
COMPLETED_STEPS
DO_NOT_REPEAT
LAST_CONSUMED_SEQ
MAX_REMOTE_SEQ
```

例如：

```text
DO_NOT_REPEAT:
- GPU_SUBMIT:930103:attempt1
- WARMUP:940098
- COMMIT:abc123
```

## 10. Browser 最小职责

优先复用：

```text
C:\AI\Playwright-Native-AI-Browser
skills/chatgpt-web-plan-bridge-latest
```

Browser 只负责：

- 打开/复用指定 ChatGPT 会话；
- 发送 wakeup；
- 等待短 ACK / BLOCKED / USER_APPROVAL_REQUIRED；
- 保存 transport 证据。

Browser **不再搬运完整命令和完整结果**。

禁止自动密码、验证码、支付、账户安全操作、绕过限制。

## 11. Capacity Router

Codex 每次启动/恢复前调用：

```text
codex-capacity-aware-model-router
```

模型 capacity：

```text
checkpoint
→ failover
→ resume Codex loop
```

queue seq 不变；已完成本地动作不重放。Capacity Router 只能换执行模型，不能改变业务计划。

## 12. GitHub 并发与编号

新消息创建前：

1. fetch 远端；
2. 找最大 seq；
3. 分配 `max+1`；
4. 检查 parent message 仍是预期 head；
5. commit/push；
6. remote verify。

冲突时重新 fetch 后分配新 seq；禁止 force push。

## 13. 异常分类

```text
BROWSER_TRANSPORT_FAILURE -> CONTROL_PLANE_FAILURE
MODEL_CAPACITY -> CONTROL_PLANE_FAILURE
WINDOWS_EXECUTOR_FAILURE -> EXECUTION_ENVIRONMENT_FAILURE
BUSINESS_QC_FAIL -> CURRENT_COMMAND_PACKAGE_RULES
UNKNOWN_OUT_OF_CONTRACT -> REQUEST_GPT_OR_BLOCKED
```

任何异常都不得自动转化成“Codex开始研究”。

## 14. 自动化边界

可自动：

- Git read/fetch/status；
- 编号消息写入；
- 冻结命令执行；
- 报告/状态；
- commit/push/remote verify；
- GPT wakeup；
- capacity failover；
- checkpoint/resume；
- 同一授权动作的等价执行实现。

必须停给用户：

- 登录/验证码；
- 代理/网络改变；
- 管理员/系统敏感操作；
- 大规模删除；
- TASK_CONTRACT 改变；
- 用户明确 STOP/PAUSE；
- 未授权敏感动作。

必须交给 GPT 而非 Codex：

- 任何新的业务路线；
- 新候选/参数/实验；
- 失败后的新研究方向；
- 最终方法判断。

## 15. Pilot 顺序

第一版：`CODEX_FIRST_SHADOW_PILOT`

```text
用户只给 Codex 一个起始 TASK
→ Codex 写 000001 REQUEST_GPT
→ Browser 唤醒 GPT
→ GPT 直接写 000002 COMMAND_CODEX 到 GitHub
→ Codex watcher 读取 000002 并执行 toy task
→ Codex 写 000003 RESULT_GPT
→ Browser 唤醒 GPT
→ GPT 写 000004 FREEZE_DECISION
→ Codex 读取并结束
```

验收目标：

```text
MANUAL_COPY_PASTE_REQUIRED=NO
CODEX_IS_LOOP_OWNER=YES
CODEX_PLAN_AUTHORITY=NONE
NO_FREE_EXPLORATION=YES
GPT_DIRECT_GITHUB_WRITE=YES
BROWSER_LONG_PAYLOAD_TRANSPORT=NO
```

Shadow Pilot PASS 后再做低风险真实任务 Assisted Pilot。

## 16. 验收

```text
A1 Codex主动创建第一个 REQUEST，但不自行写业务方案
A2 GPT收到 wakeup 后直接写 GitHub 下一编号消息
A3 Codex只消费 GitHub命令，不消费ChatGPT长回复
A4 Codex执行后直接写RESULT编号消息
A5 GPT再次被唤醒并直接写最终裁决
A6 duplicate browser wakeup no duplicate GPT command
A7 duplicate GitHub poll no Codex replay
A8 browser disconnect resumes same request seq
A9 capacity failover no local replay and no plan mutation
A10 Windows/orchestrator restart resumes from STATE+queue
A11 user STOP halts loop
A12 unknown exception -> request GPT/BLOCKED; NO FREE EXPLORATION
A13 Codex cannot create an unauthorized candidate/experiment in fault injection
A14 full toy task zero manual copy/paste
A15 remote/local state converge
```

## 17. 最终原则

> **Codex 始终是主动执行循环，但永远不是业务决策者；GPT 始终是被调用的大脑；GitHub 始终是代码对代码的命令与结果总线；浏览器只负责唤醒，不负责搬运业务正文。**