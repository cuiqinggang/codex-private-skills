# GPT↔Codex 三核心最终方案 v1 — v3.1

状态：

```text
CORE_1=COMPLETE
CORE_2=COMPLETE
CORE_3=FROZEN_READY_FOR_REAL_IMPLEMENT_VERIFY
```

方法依赖：

```text
first-principles-physical-limit-convergence v3.1.0
```

## CORE 1 — 极限短时间

### TASK

建立一个无需用户在 GPT 与 Codex 之间搬运正文的真实自动闭环。

### VALID

必须同时成立：

```text
Codex 从起始任务主动发起
GPT 由 Browser 按需唤醒
GPT 自己读取 GitHub 请求
GPT 自己把命令写入 GitHub
Codex 只读取 GitHub 命令执行
Codex 把结果写入 GitHub
GPT 再次读取结果并写最终判断
Codex 消费最终判断并停止
用户中间复制粘贴 = 0
真实任务结果 = PASS
重复 wakeup/poll 不产生重复业务结果
Codex/Browser 中断后可继续同一任务
Codex 不自行规划新业务路线
代理/系统设置不改变
```

### 唯一指标

```text
T_VALID =
从 Codex 收到起始 TASK
到 Codex 消费 GPT 最终 DECISION 并停止
的端到端时间
```

## CORE 2 — 成熟方案集群

当前必要 primitive 已有成熟解，不存在需要自创新理论的缺口。

冻结复用：

```text
GitHub commit/branch
  = 远端共享事实源 + 不可变消息记录

GitHub non-force fast-forward update
  = 防覆盖并发写入

SQLite
  = 本机 action 去重 / resume ledger

stable logical_event_id + action_id
  = 重复 transport 不重复语义动作

read-after-write verification
  = 现实副作用确认

existing Playwright Native AI Browser
  = 唤醒 GPT

existing Capacity Router
  = Codex model availability
```

结论：

```text
WORLD_SOLVED=YES
UNSOLVED_REQUIRED_PRIMITIVE=NONE
NEW_AUTOMATION_THEORY=NO
```

## CORE 3 — 高智能虚拟成熟

### 3.1 最终角色

```text
CODEX = LOOP_OWNER + DETERMINISTIC_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = SHARED_TRUTH + MESSAGE_BUS
BROWSER = GPT_WAKEUP_ONLY
SQLITE = LOCAL_DEDUPE/RESUME
CAPACITY_ROUTER = MODEL_AVAILABILITY_ONLY
```

### 3.2 最终闭环

只保留一条：

```text
Codex
-> 000001 REQUEST -> GitHub
-> Browser wake GPT
-> GPT reads GitHub
-> 000002 COMMAND -> GitHub
-> Codex reads GitHub
-> execute + verify
-> 000003 RESULT -> GitHub
-> Browser wake GPT
-> GPT reads GitHub
-> 000004 DECISION -> GitHub
-> Codex reads DECISION
-> STOP
```

### 3.3 最小消息规则

每个任务：

```text
bus/<TASK_ID>

workspaces/<TASK_ID>/
  TASK.md
  queue/
  payloads/
  RESULT.md
```

每条消息：

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

规则：

```text
append only
envelope + payload = same Git commit
Git ref update = non-force
conflict = refetch, never overwrite
```

### 3.4 最小防重复/恢复

SQLite 只保存：

```text
message_id
logical_event_id
action_id
status
effect_fingerprint
remote_commit
```

三条规则：

```text
同 logical_event_id 已发布 -> 不再发布
同 action_id 已完成且效果仍成立 -> 不再执行
副作用后崩溃 -> 先验证现实效果，成立则补记录，不重复副作用
```

### 3.5 Browser

只发送：

```text
TASK_ID
BUS_BRANCH
MESSAGE_SEQ
MESSAGE_PATH
```

不搬运业务正文。

### 3.6 GPT

```text
被唤醒
-> 从 GitHub 读当前 message/TASK/证据
-> 做规划或裁决
-> 检查同 parent 是否已有自己的回复
-> 无则写下一条消息
-> 有则不重复写
-> 短 ACK
```

### 3.7 Codex

```text
读取 GitHub
-> COMMAND：去重 -> 执行 -> 验证 -> RESULT -> wake GPT
-> DECISION：STOP/FREEZE/BLOCKED
-> 无授权动作：REQUEST GPT 或等待
```

未知问题：

```text
保存证据
-> STOP
-> 返回 GPT
```

不在现实中自行造新路线。

## 第一个现实案例

```text
TASK_ID=gpt-codex-real-case-v1
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

完整认证：

```text
000001 REQUEST
-> 000002 COMMAND
-> toy-result.txt real effect
-> 000003 RESULT
-> 000004 DECISION
-> STOP
```

同时验证四个最关键恢复条件：

```text
duplicate wakeup -> GPT message 不重复
duplicate poll -> Codex effect 不重复
Browser reconnect -> 原任务继续
Codex restart -> 原任务继续且已完成 effect 不 replay
```

PASS：

```text
FOUR_MESSAGE_LOOP=PASS
TOY_RESULT=PASS
MANUAL_MIDDLE_COPY_PASTE=0
DUPLICATE_BUSINESS_EFFECT=0
BROWSER_RECONNECT=PASS
CODEX_RESTART_RESUME=PASS
CODEX_FREE_EXPLORATION=0
FINAL_DECISION_CONSUMED=PASS
```

FAIL：

```text
保存 REALITY_DELTA
-> 返回 CORE 3
-> 重新虚拟成熟
-> 重新冻结
-> 再验证
```

## FINAL

这就是当前唯一冻结方案。

没有 L1/L2/L3/L4。
没有第二套研发流程。
现实阶段只负责实现并验证本方案。
