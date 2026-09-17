---
name: gpt-codex-convergence-orchestrator
description: 自动化 Codex 主动执行器与 GPT 按需规划器之间的收敛工作流。Codex 是唯一常驻主动循环，GitHub 是编号化命令/结果总线和共同事实源，AI Browser 只负责 Codex 唤醒 GPT，GPT 被唤醒后直接读写 GitHub 的下一条编号消息。用于去除用户在 GPT 与 Codex 之间反复复制粘贴的纯搬运动作，同时保持 GPT 负责规划/判断、Codex 负责确定性执行。
metadata:
  version: "1.1.0"
  method_dependency: "first-principles-physical-limit-convergence@2.0.0"
  browser_dependency: "chatgpt-web-plan-bridge-latest / local playwright-native-ai-browser"
  capacity_dependency: "codex-capacity-aware-model-router"
  architecture: "CODEX_FIRST_NUMBERED_GITHUB_BUS"
---

# GPT-Codex Convergence Orchestrator v1.1.0

## 1. 核心架构

```text
CODEX = LOOP_OWNER / ACTIVE_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = NUMBERED_MESSAGE_BUS + SHARED_TRUTH
AI_BROWSER = CODEX_TO_GPT_WAKEUP_TRANSPORT
CAPACITY_ROUTER = CODEX_MODEL_AVAILABILITY
```

关键修正：**流程从 Codex 出发，不从 GPT 出发。**

GPT 不是 daemon，也不负责轮询仓库。Codex 常驻或按计划恢复，持续读取 GitHub 远端状态；需要 GPT 决策时，由 Codex 写请求消息并通过 AI Browser 唤醒 GPT。

## 2. 角色边界

```text
GPT_ROLE=PLANNER/JUDGE/VIRTUAL_99
CODEX_ROLE=DETERMINISTIC_EXECUTOR + LOOP_OWNER
GITHUB_ROLE=SHARED_TRUTH + NUMBERED_BUS
BROWSER_ROLE=WAKEUP/ACK_TRANSPORT
ORCHESTRATOR_ROLE=CODEX_SIDE_STATE_MACHINE
```

Codex 可以决定：

- 当前有没有待执行的已冻结命令；
- 是否达到“需要 GPT”的既定触发条件；
- transport/checkpoint/idempotency 如何恢复。

Codex 不可以决定：

- 下一研究路线；
- 新候选；
- 新实验参数；
- 命令包外的业务方案。

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
    └─ 无：判断是否需要 GPT
          ├─ 否：继续命令包内既定动作或等待
          └─ 是：写 CODEX->GPT REQUEST 新消息 → push+verify
                 → AI Browser wake GPT
                 → 等待 GitHub 出现 GPT->CODEX 更高序号消息
→ LOOP
```

Codex 不把 ChatGPT DOM 中的长文本当作命令事实源。

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

只有：

- 新任务第一次需要规划；
- 冻结命令包明确要求 `RETURN_TO_GPT`；
- 命令包外异常；
- Final Certification 需要 GPT 裁决；
- 用户改变 TASK_CONTRACT。

普通 PASS/FAIL/ROLLBACK 如果命令包已经写明，Codex直接继续，不调用 GPT。

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

queue seq 不变；已完成本地动作不重放。

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

## 14. 自动化边界

可自动：

- Git read/fetch/status；
- 编号消息写入；
- 冻结命令执行；
- 报告/状态；
- commit/push/remote verify；
- GPT wakeup；
- capacity failover；
- checkpoint/resume。

必须停给用户：

- 登录/验证码；
- 代理/网络改变；
- 管理员/系统敏感操作；
- 大规模删除；
- TASK_CONTRACT 改变；
- 用户明确 STOP/PAUSE；
- 未授权敏感动作。

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
GPT_DIRECT_GITHUB_WRITE=YES
BROWSER_LONG_PAYLOAD_TRANSPORT=NO
```

Shadow Pilot PASS 后再做低风险真实任务 Assisted Pilot。

## 16. 验收

```text
A1 Codex主动创建第一个 REQUEST
A2 GPT收到 wakeup 后直接写 GitHub 下一编号消息
A3 Codex只消费 GitHub命令，不消费ChatGPT长回复
A4 Codex执行后直接写RESULT编号消息
A5 GPT再次被唤醒并直接写最终裁决
A6 duplicate browser wakeup no duplicate GPT command
A7 duplicate GitHub poll no Codex replay
A8 browser disconnect resumes same request seq
A9 capacity failover no local replay
A10 Windows/orchestrator restart resumes from STATE+queue
A11 user STOP halts loop
A12 unknown exception no free exploration
A13 full toy task zero manual copy/paste
A14 remote/local state converge
```

## 17. 最终原则

> **Codex 始终是主动执行循环；GPT 始终是被调用的大脑；GitHub 始终是代码对代码的命令与结果总线；浏览器只负责唤醒，不负责搬运业务正文。**