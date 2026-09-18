---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。当前版本只服从 first-principles-physical-limit-convergence v3.1.1 的三核心白名单：极限短时间、成熟方案集群、高智能虚拟成熟。Codex 负责主动循环和确定性执行，GPT 负责按需规划/裁决，GitHub 是共享事实源，AI Browser 只负责唤醒 GPT。Browser 入口从已安装 playwright-native-ai-browser/SKILL.md 解析。GitHub 总线回复类型使用唯一白名单：REQUEST 只能由 GPT 回复 COMMAND；RESULT 只能由 GPT 回复 DECISION；页面 ACK 永远不能作为 GitHub 总线消息类型。
metadata:
  version: "1.3.8"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "CODEX_GITHUB_GPT_CLOSED_LOOP"
---

# GPT↔Codex 自动闭环 v1.3.8

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

Browser wakeup 必须是**自包含动作命令**，不能依赖当前 ChatGPT 会话记得旧上下文。

每次 wakeup 固定包含：

```text
GPT_BUS_WAKEUP_V1
TASK_ID=<...>
REPOSITORY=cuiqinggang/codex-private-skills
BUS_BRANCH=<...>
MESSAGE_SEQ=<...>
MESSAGE_PATH=<...>
EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND|DECISION
REQUIRED_ACTION=WRITE_NEXT_BUS_MESSAGE_TO_GITHUB
```

并明确告诉 GPT：

```text
1. 读取 BUS_BRANCH 上 MESSAGE_PATH 与 TASK 证据。
2. 必须使用当前 ChatGPT 可用的 GitHub 写动作，把下一条不可变 Bus message + payload 直接提交到同一 BUS_BRANCH。
3. REQUEST 的下一条必须是 COMMAND；RESULT 的下一条必须是 DECISION。
4. 禁止把业务 COMMAND / DECISION 只写在聊天正文里。
5. GitHub remote verify 成功后，页面只回复：
   GPT_BUS_COMMIT_OK TASK_ID=<...> SEQ=<...> HEAD=<sha>
6. 如果当前会话没有 GitHub 写动作/权限，页面只回复：
   GPT_BUS_WRITE_UNAVAILABLE TASK_ID=<...>
7. 如果遇到登录、授权、审批或其他阻断，页面只回复：
   GPT_BUS_BLOCKED TASK_ID=<...> REASON=<short>
```

其中：

```text
REQUEST wakeup -> EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND
RESULT wakeup  -> EXPECTED_GPT_BUS_REPLY_TYPE=DECISION
```

页面回复不是业务事实源，只用于 transport 状态。

如果 assistant turn 已经完成，但 GitHub 仍没有目标 Bus message：

```text
GPT_BUS_COMMIT_OK       -> 重新查 GitHub；仍无则 PROTOCOL_FAIL
GPT_BUS_WRITE_UNAVAILABLE -> 立即 STOP + REALITY_DELTA
GPT_BUS_BLOCKED         -> 立即 STOP + REALITY_DELTA
其他页面业务正文        -> GPT_BUS_PROTOCOL_FAIL
                           不得把正文当 COMMAND/DECISION
                           刷新/重连后用同一个 logical_event_id 重试一次自包含 wakeup
                           第二次仍失败 -> STOP + REALITY_DELTA
```

这样刷新、新标签或新会话都能仅凭 wakeup + GitHub 恢复，不依赖聊天历史。

## GPT“正在思考”首答超时恢复

这是一个简单规则：**只限制“开始回答以前”的 Thinking 时间，不限制完整回答时长。**

固定三档：

~~~text
SIMPLE = 60 秒
NORMAL = 180 秒
LARGE  = 600 秒
~~~

当前 GPT↔Codex：

~~~text
RESULT -> DECISION = SIMPLE = 60 秒
REQUEST -> COMMAND = NORMAL = 180 秒
~~~

只有明确的大型复杂规划才使用：

~~~text
LARGE = 600 秒
~~~

计时定义：

~~~text
T_START = Browser 成功发送 wakeup
T_FIRST_ANSWER = GPT 页面第一次出现正常 assistant 正文输出
T_THINKING = T_FIRST_ANSWER - T_START
~~~

规则：

~~~text
GPT 已开始正常输出正文
-> ANSWER_STARTED=YES
-> 立即停止 Thinking 超时计时
-> 后续回答继续完成，视为正常

GPT 尚未开始正文，仍停留在 Thinking/Generating
-> elapsed <= 当前档位上限：继续等待
-> elapsed >  当前档位上限：一律按故障恢复
~~~

恢复前先查 GitHub；如果目标 COMMAND / DECISION 已经存在，直接继续。

否则：

~~~text
refresh / reconnect 当前 ChatGPT
-> 复用同一个 TASK_ID / MESSAGE_SEQ / logical_event_id 重新 wake
-> 必要时同一 profile 新开页面/会话恢复
~~~

禁止：

~~~text
回答已经开始后因为总耗时长而刷新
无限停留在 Thinking
超时后继续等待
创建新的业务 REQUEST
改变 MESSAGE_SEQ
产生第二个 logical_event_id
改变任务或方案
~~~

记录：

~~~text
GPT_WAIT_CLASS=SIMPLE|NORMAL|LARGE
GPT_FIRST_ANSWER_LIMIT_SECONDS
GPT_FIRST_ANSWER_SECONDS
ANSWER_STARTED=YES|NO
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

> **GitHub Bus 是唯一业务事实源；每次 GPT wakeup 都必须自包含并明确要求执行 GitHub 写动作。页面只能返回 BUS_COMMIT_OK / BUS_WRITE_UNAVAILABLE / BUS_BLOCKED，不得承载业务 COMMAND/DECISION。**
