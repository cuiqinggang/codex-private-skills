---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。当前版本只服从 first-principles-physical-limit-convergence v3.1 的三核心白名单：极限短时间、成熟方案集群、高智能虚拟成熟。Codex 负责主动循环和确定性执行，GPT 负责按需规划/裁决，GitHub 是共享事实源，AI Browser 只负责唤醒 GPT。旧 L0/L1/L2/L3/L4 仅为历史资料，不具有当前方法权。
metadata:
  version: "1.3.0"
  method_dependency: "first-principles-physical-limit-convergence@3.1.0"
  architecture: "CODEX_GITHUB_GPT_CLOSED_LOOP"
---

# GPT↔Codex 自动闭环 v1.3.0

## 唯一方法映射

本技能只允许映射到 v3.1 三核心：

### CORE 1：极限短时间

目标：

```text
从 Codex 收到起始任务
到 GPT 最终判断被 Codex 消费并停止
得到第一个完整 VALID 自动闭环
```

唯一时间指标：

```text
T_VALID
```

VALID：

```text
用户中间复制粘贴 = 0
Codex 主动发起
GPT 直接读写 GitHub
Codex 只执行 GPT 已写入 GitHub 的命令
真实任务结果通过验证
重复 wakeup/poll 不产生重复业务结果
中断后能继续同一个任务
Codex 不自行规划下一业务动作
代理/系统设置不改变
```

### CORE 2：成熟方案集群

只复用当前已经成熟且匹配的能力：

```text
GitHub commit/branch = 远端共享事实源
non-force fast-forward update = 防覆盖并发工作
SQLite = 本机 durable action ledger
stable logical_event_id / action_id = 去重
existing Playwright Native AI Browser = GPT wakeup
existing Capacity Router = Codex model availability
read-after-write verification = 副作用确认
```

不部署新的 workflow engine，不新建 Browser 栈，不重新研究可靠自动化理论。

### CORE 3：高智能虚拟成熟

最终冻结链只有：

```text
Codex
-> GitHub: REQUEST
-> Browser: wake GPT
-> GPT
-> GitHub: COMMAND
-> Codex
-> execute + verify
-> GitHub: RESULT
-> Browser: wake GPT
-> GPT
-> GitHub: DECISION
-> Codex
-> STOP
```

这条链就是当前 FINAL VIRTUAL-99。

现实实现和案例验证只验证这条链，不现场改架构。

---

# 角色

```text
CODEX = LOOP_OWNER + DETERMINISTIC_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = SHARED_TRUTH + IMMUTABLE MESSAGE BUS
AI_BROWSER = GPT_WAKEUP_ONLY
SQLITE = LOCAL_DEDUPE/RESUME LEDGER
CAPACITY_ROUTER = MODEL_AVAILABILITY ONLY
```

Codex 可以决定同一个已授权动作怎么完成，但不能决定下一业务动作。

---

# GitHub 消息

每个任务使用独立 bus branch：

```text
bus/<TASK_ID>
```

目录：

```text
workspaces/<TASK_ID>/
  TASK.md
  queue/
  payloads/
  RESULT.md
```

正式闭环四条消息：

```text
000001 CODEX -> GPT REQUEST
000002 GPT   -> CODEX COMMAND
000003 CODEX -> GPT RESULT
000004 GPT   -> CODEX DECISION
```

消息只追加，不覆盖。

每条消息至少有：

```text
task_id
seq
message_id
parent_message_id
logical_event_id
sender
receiver
type
payload_path
payload_sha256
created_at
```

envelope + payload 同一个 Git commit 发布。

Git ref 更新必须 non-force；冲突就重新读取，不覆盖别人工作。

---

# 防重复与恢复

本机 SQLite 只保存：

```text
message_id
logical_event_id
action_id
status
effect_fingerprint
remote_commit
```

规则只有三条：

1. 同一个 logical_event_id 已发布 -> 不再发布第二条语义相同消息。
2. 同一个 action_id 已完成且结果仍通过验证 -> 不再执行。
3. 如果进程在副作用后崩溃 -> 先检查现实结果；已经成立就补记录，不重复副作用。

不宣称全局 exactly-once；目标只是：

```text
重复 transport
不能产生重复 VALID 业务结果
```

---

# Browser

Browser 唤醒 GPT 时只发送：

```text
TASK_ID
BUS_BRANCH
MESSAGE_SEQ
MESSAGE_PATH
```

GPT 自己从 GitHub 读取正文。

Browser 不搬运完整命令/结果。

---

# GPT

GPT 被唤醒后：

```text
读取当前 GitHub message
-> 读取 TASK/必要证据
-> 做规划或裁决
-> 检查是否已经对同一 parent 写过回复
-> 未写过：写下一条 GitHub message
-> 已写过：不重复写
-> 返回短 ACK
```

---

# Codex

Codex 循环：

```text
读取 GitHub
-> 有 GPT COMMAND：去重 -> 执行 -> 验证 -> 写 RESULT -> wake GPT
-> 有 GPT DECISION：执行 FREEZE/BLOCKED/STOP
-> 没有授权业务动作：REQUEST GPT 或等待
```

未知问题：

```text
保存证据
-> STOP
-> 返回 GPT
```

禁止现实中自行产生新方案。

---

# 第一个现实认证案例

```text
TASK_ID=gpt-codex-real-case-v1
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

真实路径：

```text
000001 REQUEST
-> GPT 000002 COMMAND
-> Codex 创建并验证 toy-result.txt
-> 000003 RESULT
-> GPT 000004 DECISION
-> Codex STOP
```

同一次认证额外验证：

```text
duplicate wakeup -> no duplicate GPT message
duplicate poll -> no duplicate Codex effect
Browser reconnect -> same task continues
Codex restart -> same task continues, completed effect not replayed
```

通过条件：

```text
FOUR_MESSAGE_LOOP=PASS
TOY_RESULT=PASS
MANUAL_MIDDLE_COPY_PASTE=0
DUPLICATE_BUSINESS_EFFECT=0
RESTART_RESUME=PASS
CODEX_FREE_EXPLORATION=0
FINAL_DECISION_CONSUMED=PASS
```

通过后即认为当前冻结方案的现实认证成立。

---

# 历史资料

旧：

```text
L0/L1/L2/L3/L4
Shadow Pilot
Assisted Pilot
旧 H3-P0 自动化命令
```

只允许作为历史证据。

当前下一步不得由这些旧标签决定。

---

# 最终一句话

> **Codex 主动、GPT 决策、GitHub 传事实、Browser 只唤醒；成熟机制只作为工具，完整现实闭环一次验证被冻结的最终方案。**
