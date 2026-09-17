# GPT-Codex 自动控制面

## 目标

把人工流程：

```text
GPT 出命令
-> 人复制到 Codex
-> Codex 执行
-> 人复制结果回 GPT
```

升级为：

```text
GPT planner
<-> GitHub shared workspace
<-> Workflow Orchestrator
<-> Codex executor
<-> local tools / GPU / filesystem
```

ChatGPT 网站通过成熟浏览器桥接作为 GPT transport；用户不再负责文本搬运。

## 角色

```text
GPT = planner / judge / Virtual-99
Codex = deterministic executor
GitHub = shared truth workspace + event bus
AI Browser = ChatGPT transport
Capacity Router = Codex remote model availability
Orchestrator = state machine + checkpoint + idempotency
User = STOP / PAUSE / sensitive approval / contract change
```

## 共同工作区协议

每个任务固定目录：

```text
workspace/<TASK_ID>/
  TASK.md
  STATE.json
  PLAN.md
  COMMAND.md
  RESULT.md
  RESULT.json
  EVENTS.jsonl
  ARTIFACTS.md
```

`STATE.json` 至少：

```text
TASK_ID
PHASE
OWNER
STATUS
REVISION
LAST_REMOTE_HEAD
COMPLETED_STEPS
DO_NOT_REPEAT
NEXT_ACTION
REQUESTED_MODEL
ACTUAL_MODEL
FALLBACK_REASON
BROWSER_THREAD_REF
UPDATED_AT
```

## 状态机

```text
NEW
-> GPT_PLANNING
-> READY_FOR_CODEX
-> CODEX_RUNNING
-> RESULT_READY
-> READY_FOR_GPT
-> GPT_JUDGING
-> READY_FOR_CODEX | FREEZE | BLOCKED | USER_APPROVAL_REQUIRED
```

只有状态文件允许推动流程；不得仅凭聊天文本猜当前阶段。

## GPT -> Codex

GPT 写入：

```text
PLAN.md
COMMAND.md
STATE.status=READY_FOR_CODEX
```

Orchestrator 检测远端 commit，拉取并核对 SHA；Codex 只执行该版本的 `COMMAND.md`。

## Codex -> GPT

Codex 完成后写：

```text
RESULT.md
RESULT.json
ARTIFACTS.md
STATE.status=READY_FOR_GPT
```

然后：

```text
commit -> push -> remote verify
```

Orchestrator 只在远端 verify 后触发 GPT transport。

## ChatGPT Browser transport

复用：

```text
skills/chatgpt-web-plan-bridge-latest
```

或本机封袋 `playwright-native-ai-browser`。

Transport 必须：

1. 复用指定 ChatGPT 项目会话；
2. 从 GitHub 读取最新 `RESULT.md/STATE.json`；
3. 发送一个结构化消息；
4. 等待回复完成；
5. 将 GPT 输出提取为 `PLAN/COMMAND`；
6. 写回 GitHub；
7. 不自动处理登录、验证码、支付、安全提示。

## 幂等与去重

每个动作必须绑定：

```text
TASK_ID
REVISION
SOURCE_COMMIT
ACTION_ID
```

相同 ACTION_ID 已成功则：

```text
REPLAY=NO
```

Codex 本地长任务必须维护提交账本；浏览器 transport 也必须维护 `last_consumed_commit`，防止同一结果重复发给 GPT。

## DO_NOT_REPEAT

这是自动化能否安全运行的关键。

例：

```text
COMPLETED_STEPS:
- warmup 940098
- seed 930103 run

DO_NOT_REPEAT:
- warmup 940098
- GPU submit id abc123
```

模型 capacity、浏览器掉线、页面刷新、Windows shell 重启都不得让这些步骤重放。

## Capacity Router

复用：

```text
skills/codex-capacity-aware-model-router
```

capacity 是控制面错误：

```text
checkpoint
-> failover model
-> continue same logical task
```

如果全部模型不可用：

```text
BLOCKED_REMOTE_CAPACITY
```

不改业务裁决。

## Browser transport failure

分类为：

```text
CONTROL_PLANE_FAILURE
```

不是：

```text
ALGORITHM_FAILURE
```

必须保留远端状态并等待 transport 恢复。

## 用户审批边界

自动循环应默认暂停在：

- 登录/验证码；
- 账户/支付；
- 代理/网络设置改变；
- 系统级敏感修改；
- 删除大批文件；
- task contract 改变；
- 命令包外的新研究方向。

普通已冻结执行与报告搬运无需用户手工复制。

## 最小实现顺序

```text
Phase A: GitHub 状态机 + watcher
Phase B: Codex launcher + checkpoint/idempotency
Phase C: ChatGPT browser transport
Phase D: capacity router integration
Phase E: end-to-end shadow mode
Phase F: unattended normal mode with user stop switch
```

## 验收

至少验证：

```text
A1 GPT writes command -> Codex consumes once
A2 Codex result -> GPT receives once
A3 browser disconnect -> no local replay
A4 model capacity -> failover/checkpoint, no business reset
A5 duplicate GitHub webhook/poll -> idempotent
A6 manual user STOP -> whole loop halts
A7 unknown exception -> BLOCKED, no free exploration
A8 full toy task completes without copy/paste
```

## 最终原则

> 自动化的是 transport、状态同步和既定状态机，不是把研究决策权交给执行器。