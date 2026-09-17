---
name: gpt-codex-convergence-orchestrator
description: 自动化 GPT 规划器与 Codex 确定性执行器之间的收敛工作流。以 GitHub 为共同事实源，以现有 ChatGPT/Playwright AI Browser 技能为 transport，以 Codex 为本地执行器，以 capacity router、checkpoint、idempotency 和 DO_NOT_REPEAT 保证长任务可恢复。用于去除用户在 GPT 与 Codex 之间反复复制粘贴的纯搬运动作，同时保持研究决策权仍在 GPT、执行权仍受冻结命令包约束。
metadata:
  version: "1.0.0"
  method_dependency: "first-principles-physical-limit-convergence@2.0.0"
  browser_dependency: "chatgpt-web-plan-bridge-latest / local playwright-native-ai-browser"
  capacity_dependency: "codex-capacity-aware-model-router"
---

# GPT-Codex Convergence Orchestrator v1.0.0

## 1. 目标

把人工 transport：

```text
GPT -> 人复制 -> Codex
Codex -> 人复制 -> GPT
```

改成自动闭环：

```text
GPT planner/judge
<-> AI Browser transport
<-> GitHub shared workspace
<-> Orchestrator
<-> Codex deterministic executor
```

用户不再负责文本搬运，只保留：

```text
STOP
PAUSE
APPROVE_SENSITIVE_ACTION
CHANGE_TASK_CONTRACT
```

## 2. 不改变角色

```text
GPT_ROLE=PLANNER/JUDGE/VIRTUAL_99
CODEX_ROLE=DETERMINISTIC_EXECUTOR
GITHUB_ROLE=SHARED_TRUTH
BROWSER_ROLE=TRANSPORT
ORCHESTRATOR_ROLE=STATE_MACHINE
```

自动化绝不把“下一步研究什么”的决定权交给 Codex。

## 3. 共同工作区

每个任务：

```text
workspaces/<TASK_ID>/
  TASK.md
  STATE.json
  GPT-PLAN.md
  CODEX-COMMAND.md
  CODEX-RESULT.md
  CODEX-RESULT.json
  GPT-DECISION.md
  ARTIFACTS.md
  EVENTS.jsonl
```

`STATE.json` 至少：

```text
TASK_ID
REVISION
PHASE
STATUS
OWNER
SOURCE_COMMIT
LAST_REMOTE_HEAD
COMPLETED_STEPS
DO_NOT_REPEAT
NEXT_ACTION
REQUESTED_MODEL
ACTUAL_MODEL
FALLBACK_REASON
CHATGPT_CONVERSATION_REF
LAST_CONSUMED_GPT_REVISION
LAST_CONSUMED_CODEX_REVISION
UPDATED_AT
```

## 4. 状态机

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

状态推进必须基于远端 commit + schema 校验，不基于聊天猜测。

## 5. GPT -> Codex Transport

GPT 输出必须包含机器可解析控制包：

```text
CONTROL_ACTION=EXECUTE | FREEZE | BLOCKED | USER_APPROVAL_REQUIRED
TASK_ID=<...>
REVISION=<n>
SOURCE_RESULT_COMMIT=<sha>
COMMAND_BODY=<...>
EXPECTED_NEXT_STATE=<...>
```

浏览器 transport 捕获后：

1. 写 `GPT-DECISION.md`；
2. 若 `EXECUTE`，生成 `CODEX-COMMAND.md`；
3. 更新 `STATE.json`；
4. commit/push/remote verify；
5. 才允许 Codex 消费。

## 6. Codex -> GPT Transport

Codex 只读取远端已核验的 `CODEX-COMMAND.md`。

完成后：

```text
CODEX-RESULT.md
CODEX-RESULT.json
ARTIFACTS.md
STATE.status=READY_FOR_GPT
```

commit/push/remote verify 后，Orchestrator 才通过 AI Browser 把本轮结果送给 GPT。

## 7. Browser 依赖

优先复用现有成熟 transport：

```text
skills/chatgpt-web-plan-bridge-latest
```

本机封袋浏览器存在时优先：

```text
C:\AI\Playwright-Native-AI-Browser
skill=playwright-native-ai-browser
```

浏览器层只负责：

- 打开/复用指定 ChatGPT 会话；
- 发送结构化结果包；
- 等待完整答复；
- 抓取答复；
- 保存截图/DOM/ACK 证据。

禁止自动：密码、验证码、支付、账户安全操作、绕过限制。

## 8. Capacity Router

每次启动 Codex turn 前调用：

```text
codex-capacity-aware-model-router
```

出现 model capacity：

```text
checkpoint
-> failover
-> continue same logical task
```

绝不重放 `COMPLETED_STEPS`。

## 9. 幂等和去重

每个动作 ID：

```text
ACTION_ID = TASK_ID + REVISION + SOURCE_COMMIT + ACTION_TYPE
```

如果 ACTION_ID 已成功：

```text
REPLAY=NO
```

GitHub poll/webhook 重复、ChatGPT 页面刷新、Codex模型切换、Windows进程重启都不得重复提交已完成 GPU/benchmark/文件写动作。

## 10. DO_NOT_REPEAT

必须显式记录：

```text
COMPLETED_STEPS
DO_NOT_REPEAT
```

例如：

```text
DO_NOT_REPEAT:
- GPU_SUBMIT:930103:attempt1
- WARMUP:940098
- COMMIT:abc123
```

## 11. 异常分类

```text
BROWSER_TRANSPORT_FAILURE -> CONTROL_PLANE_FAILURE
MODEL_CAPACITY -> CONTROL_PLANE_FAILURE
WINDOWS_EXECUTOR_FAILURE -> EXECUTION_ENVIRONMENT_FAILURE
BUSINESS_QC_FAIL -> 由当前命令包处理
UNKNOWN_OUT_OF_CONTRACT -> BLOCKED_RETURN_TO_GPT
```

## 12. 自动化边界

可以无人值守执行：

- Git fetch/pull/status/read；
- 冻结命令包内已授权操作；
- 写报告/状态；
- commit/push/remote verify；
- ChatGPT 结果 transport；
- capacity failover；
- checkpoint/resume。

必须停给用户：

- 登录/验证码；
- 代理/网络改变；
- 管理员/系统级敏感操作；
- 大规模删除；
- task contract 改变；
- 新研究方向需要授权；
- 账户/支付/安全设置。

## 13. Pilot 方案

第一版不直接无人值守跑 H3。

先做 `SHADOW_PILOT`：

```text
Toy task
-> GPT 生成一个简单确定性命令
-> Browser 自动抓取
-> GitHub 写 command
-> Codex执行
-> GitHub写 result
-> Browser自动送回GPT
-> GPT FREEZE
```

验收通过后，再用一个低风险真实项目做 `ASSISTED_PILOT`，最后才开启 `NORMAL_AUTONOMOUS_TRANSPORT`。

## 14. 验收

```text
A1 GPT->Codex transport one-time only
A2 Codex->GPT transport one-time only
A3 duplicate poll/webhook no replay
A4 browser disconnect checkpointed
A5 capacity failover no local replay
A6 Windows restart resumes state
A7 user STOP halts loop
A8 unknown exception BLOCKED, no free exploration
A9 full toy task completes with zero manual copy/paste
A10 GitHub remote state and local state converge
```

## 15. 最终原则

> 自动化 transport、状态同步、checkpoint 和预授权状态机；不自动化未经 GPT 冻结的研究决策。