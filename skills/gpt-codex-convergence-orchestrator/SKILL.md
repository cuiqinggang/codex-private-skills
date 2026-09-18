---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。当前版本只服从 first-principles-physical-limit-convergence v3.1.1 的三核心白名单：极限短时间、成熟方案集群、高智能虚拟成熟。Codex 负责主动循环和确定性执行，GPT 负责按需规划/裁决，GitHub 是共享事实源，AI Browser 只负责唤醒 GPT。Browser 入口从已安装 playwright-native-ai-browser/SKILL.md 解析。GitHub 总线回复类型使用唯一白名单：REQUEST 只能由 GPT 回复 COMMAND；RESULT 只能由 GPT 回复 DECISION；页面 ACK 永远不能作为 GitHub 总线消息类型。
metadata:
  version: "1.3.5"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "CODEX_GITHUB_GPT_CLOSED_LOOP"
---

# GPT↔Codex 自动闭环 v1.3.5

## CORE 1：极限短时间

目标：

```text
从 Codex 收到起始任务
到 GPT 最终 DECISION 被 Codex 消费并停止
得到第一个完整 VALID 自动闭环
```

唯一指标：

```text
T_VALID
```

VALID：

```text
用户中间复制粘贴 = 0
Codex 主动发起
GPT 直接读写 GitHub
Codex 只执行 GPT 已写入 GitHub 的 COMMAND
真实任务结果通过验证
最终 GPT GitHub 消息必须是 DECISION
重复 wakeup/poll 不产生重复业务结果
中断后能继续同一个任务
Codex 不自行规划下一业务动作
代理/系统设置不改变
```

## CORE 2：成熟方案集群

冻结复用：

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

## CORE 3：高智能虚拟成熟

唯一闭环：

```text
Codex
-> 000001 REQUEST -> GitHub
-> Browser wake GPT
-> GPT reads GitHub
-> 000002 COMMAND -> GitHub
-> Codex execute + verify
-> 000003 RESULT -> GitHub
-> Browser wake GPT
-> GPT reads GitHub
-> 000004 DECISION -> GitHub
-> Codex consumes DECISION
-> STOP
```

### GitHub 总线类型白名单

只允许：

```text
parent.type=REQUEST
-> GPT reply.type MUST = COMMAND

parent.type=RESULT
-> GPT reply.type MUST = DECISION
```

除此之外：

```text
PUBLISH=DENY
```

特别规定：

```text
ACK = Browser/page transport acknowledgement only
ACK = NEVER a GitHub bus message type
```

在 GitHub publish 前必须先检查 parent.type 和 intended reply.type；不匹配就不发布。

### DECISION 最小内容

000004 必须至少包含：

```text
type=DECISION
result_message_id
accepted=true|false
status=PASS|FAIL
control_action=STOP|BLOCKED
verification
```

当 toy result 完全通过：

```text
accepted=true
status=PASS
control_action=STOP
```

页面可以另外返回短 ACK，但不能把 ACK 写入 GitHub queue。

---

# Browser 正式入口

先读取：

```text
C:\Users\A\.codex\skills\playwright-native-ai-browser\SKILL.md
```

若为 Junction/Symlink，解析 Target，再严格使用 SKILL.md 当前声明的正式业务入口与恢复约定。

禁止猜测旧 root\scripts / root\references 路径。

Browser wakeup 只发送：

```text
TASK_ID
BUS_BRANCH
MESSAGE_SEQ
MESSAGE_PATH
EXPECTED_GPT_BUS_REPLY_TYPE
```

其中：

```text
REQUEST wakeup -> EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND
RESULT wakeup  -> EXPECTED_GPT_BUS_REPLY_TYPE=DECISION
```

## GPT“正在思考”时间优先故障恢复

这是 Browser transport 的小故障恢复，不改变四消息架构。

核心判断只有两步：

~~~text
1. GitHub 是否已经出现当前期待的 COMMAND / DECISION？
   YES -> 直接继续

2. NO -> 当前等待时间是否已经超过同类成功回答的 NORMAL_WAIT_UPPER？
   NO  -> 继续等待
   YES -> GPT_THINKING_STUCK_HIGH_PROBABILITY
          立即进入恢复
~~~

其中：

~~~text
NORMAL_WAIT_UPPER
= 根据同类 wake / 相近任务复杂度的真实成功样本形成的正常等待上限
~~~

有足够历史样本时，优先使用真实成功分布的高位上界；样本不足时，沿用 Browser SKILL / 正式配置已有等待上限作为临时基线。不要凭空手写 5 秒、10 秒之类常量。

页面是否仍显示 Thinking、是否偶尔有 UI 变化，只作为记录信息，不能无限延长超过 NORMAL_WAIT_UPPER 后的等待。

超过 NORMAL_WAIT_UPPER 且 GitHub 无目标回复时，恢复：

~~~text
先再次检查 GitHub
-> 仍无目标回复
-> 刷新/重连当前 ChatGPT 会话
-> 使用同一个 TASK_ID / MESSAGE_SEQ / logical_event_id 重新 wake
-> 继续等待同一个目标消息
~~~

如果当前会话刷新后仍不可用，可在同一已登录 profile 新开页面/会话，并仍使用同一个 logical_event_id 从 GitHub 恢复上下文。

禁止：

~~~text
无限等待
因为页面还显示 Thinking 就无限延长
创建新的业务 REQUEST
改变 MESSAGE_SEQ
产生第二个 logical_event_id
改变任务或方案
~~~

必须记录：

~~~text
NORMAL_WAIT_UPPER_SECONDS
NORMAL_WAIT_BASELINE_SOURCE
GPT_THINKING_STUCK_COUNT
GPT_THINKING_STUCK_RECOVERY_SECONDS
~~~

---

# GitHub 消息与防重复

每个任务独立：

```text
bus/<TASK_ID>
```

消息只追加，不覆盖；envelope + payload 同一 commit；ref update non-force。

本机 SQLite 保存最小去重/恢复字段：

```text
message_id
logical_event_id
action_id
status
effect_fingerprint
remote_commit
```

规则：

```text
同 logical_event_id 已发布 -> 不再发布
同 action_id 已完成且效果仍成立 -> 不再执行
副作用后崩溃 -> 先验证现实效果，成立则补记录，不重复副作用
```

---

# 时间测量

每次真实认证必须记录：

```text
T0 = 000001 REQUEST published
T1 = 000002 COMMAND published
T2 = 000003 RESULT published
T3 = 000004 DECISION published
T4 = Codex consumed DECISION and STOP
```

计算：

```text
T_GPT_REQUEST_TO_COMMAND = T1-T0
T_CODEX_COMMAND_TO_RESULT = T2-T1
T_GPT_RESULT_TO_DECISION = T3-T2
T_FINAL_CONSUME = T4-T3
T_VALID = T4-T0
```

先 correctness PASS，再依据这些真实时间只优化最大瓶颈。

---

# 现实认证

上一轮 gpt-codex-real-case-v1 保留为失败证据，不覆盖。

重新用干净任务：

```text
TASK_ID=gpt-codex-real-case-v2
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

必须严格产生：

```text
000001 REQUEST
000002 COMMAND
000003 RESULT
000004 DECISION
STOP
```

同时验证：

```text
duplicate wakeup
duplicate poll
Browser reconnect
Codex restart
```

失败只保存 REALITY_DELTA 并返回 GPT，不现场改方案。

---

# 最终一句话

> **页面 ACK 只确认 transport；GitHub 总线只认 REQUEST→COMMAND、RESULT→DECISION；GPT 等待以历史正常时间上限为主判据，超过上限且 GitHub 无目标回复就立即恢复，并始终复用同一 logical_event_id。**
