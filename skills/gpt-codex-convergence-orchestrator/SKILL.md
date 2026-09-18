---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。服从 first-principles-physical-limit-convergence v3.1.1 三核心。GPT 负责规划/裁决；Codex 负责主动循环、确定性执行和机械 Bus Relay；GitHub 是最终共享事实源；Playwright Native AI Browser 负责唤醒 GPT 并提取结构化 GPT_BUS_REPLY_V1。由于 ChatGPT 外部写安全检查可能阻止无人值守 GitHub 写动作，v1.4.0 不再要求 GPT 页面直接写 GitHub。
metadata:
  version: "1.4.0"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "GPT_STRUCTURED_REPLY_CODEX_RELAY_GITHUB_TRUTH"
---

# GPT↔Codex 自动闭环 v1.4.0

## CORE 1：极限短时间

唯一指标：

~~~text
T_VALID
= Codex 接收起始 TASK
-> 完整 REQUEST / COMMAND / RESULT / DECISION
-> Codex 消费 DECISION 并 STOP
~~~

VALID 必须：

~~~text
MANUAL_MIDDLE_COPY_PASTE=0
GPT_PLAN_AUTHORITY=YES
CODEX_PLAN_AUTHORITY=NONE
GITHUB_FINAL_TRUTH=YES
TOY_RESULT=PASS
DUPLICATE_BUSINESS_EFFECT=0
RESTART_RESUME=PASS
~~~

## CORE 2：成熟方案集群

直接复用：

~~~text
GitHub append-only bus
SQLite dedupe/resume
non-force Git updates
read-after-write verification
Playwright Native AI Browser
chatgpt-web-plan-bridge-latest 的成熟“页面答案 -> Codex”传输能力
Capacity Router
~~~

现实证据：

~~~text
GPT 直接写 GitHub：
- real-case-v2 曾成功
- 后续 warm timing 被 GITHUB_WRITE_SAFETY_CHECK 阻断
- GitHub app 权限即使允许 all actions，也不能保证绕过产品安全保护

因此无人值守稳定路径不再依赖 GPT 外部 write action。
~~~

## CORE 3：冻结闭环

~~~text
Codex
-> GitHub 000001 REQUEST
-> Browser wake GPT
-> GPT reads GitHub
-> GPT 页面输出 GPT_BUS_REPLY_V1 (COMMAND)
-> Browser 原样提取
-> Codex 机械校验 + relay publish
-> GitHub 000002 COMMAND
-> Codex execute + verify
-> GitHub 000003 RESULT
-> Browser wake GPT
-> GPT reads GitHub
-> GPT 页面输出 GPT_BUS_REPLY_V1 (DECISION)
-> Browser 原样提取
-> Codex 机械校验 + relay publish
-> GitHub 000004 DECISION
-> Codex consume DECISION
-> STOP
~~~

GitHub 仍是正式业务事实源；页面 reply 只是提交前 transport artifact。

## GPT_BUS_REPLY_V1

GPT 页面只能返回一个结构化对象：

~~~text
BEGIN_GPT_BUS_REPLY_V1
{
  "protocol": "GPT_BUS_REPLY_V1",
  "task_id": "<TASK_ID>",
  "parent_message_id": "<current request/result message_id>",
  "type": "COMMAND|DECISION",
  "logical_event_id": "<stable logical event id>",
  "payload": { ... }
}
END_GPT_BUS_REPLY_V1
~~~

类型白名单：

~~~text
parent REQUEST -> reply COMMAND
parent RESULT  -> reply DECISION
~~~

COMMAND payload 必须完整表达 GPT 的业务动作。
DECISION payload 至少：

~~~text
accepted
status
control_action
result_message_id
verification
~~~

## Codex Relay 权限边界

Codex 对 GPT_BUS_REPLY_V1 只允许：

~~~text
PARSE
SCHEMA_VALIDATE
PARENT_VALIDATE
TYPE_VALIDATE
TASK_VALIDATE
HASH
ADD_TRANSPORT_METADATA
PUBLISH
REMOTE_VERIFY
~~~

Codex 禁止：

~~~text
修改 payload 业务语义
补写 GPT 没有给出的业务参数
重排候选
改变 COMMAND / DECISION
自行产生新业务动作
~~~

发布后的 Bus envelope 可增加：

~~~text
sender=GPT
receiver=CODEX
relay_publisher=CODEX
source_reply_sha256=<hash of extracted GPT reply>
seq=<next seq>
created_at=<transport timestamp>
payload_sha256=<payload hash>
~~~

这表示：
- 业务语义作者 = GPT
- GitHub 提交执行者 = Codex relay

## Browser

正式入口始终从：

~~~text
C:\Users\A\.codex\skills\playwright-native-ai-browser\SKILL.md
~~~

解析。

Browser 负责：

~~~text
发送 wakeup
观察首答
等待完整 GPT_BUS_REPLY_V1
提取 BEGIN/END 之间原始内容
交给 Codex relay
保存 transport evidence
~~~

Browser 不解释业务内容。

## 首答 Thinking 超时

只限制“开始回答前”的 Thinking 时间：

~~~text
SIMPLE = 60 秒
NORMAL = 180 秒
LARGE  = 600 秒
~~~

当前：

~~~text
RESULT -> DECISION = SIMPLE
REQUEST -> COMMAND = NORMAL
~~~

一旦 GPT 开始正常正文：

~~~text
ANSWER_STARTED=YES
-> 停止 Thinking timeout
~~~

一直未开始正文并超时：

~~~text
check GitHub
-> refresh/reconnect
-> same TASK_ID / MESSAGE_SEQ / logical_event_id re-wake
~~~

## Relay 失败

以下任一出现：

~~~text
没有 BEGIN/END 标记
JSON 无效
task_id 不匹配
parent_message_id 不匹配
reply type 不匹配
logical_event_id 冲突
payload 不完整
~~~

则：

~~~text
GPT_BUS_REPLY_INVALID
-> 不发布
-> same logical_event_id 重试一次
-> 第二次仍失败：STOP + REALITY_DELTA
~~~

## 去重/恢复

~~~text
同 logical_event_id 已发布 -> 不再发布
同 action_id 已完成且现实效果仍成立 -> 不 replay
relay publish 后本地 ACK 丢失 -> 先查 GitHub 再决定
~~~

## 时间测量

记录：

~~~text
T0 REQUEST publish
T1 GPT COMMAND reply first complete
T1G COMMAND GitHub publish
T2 RESULT publish
T3 GPT DECISION reply first complete
T3G DECISION GitHub publish
T4 Codex consume DECISION + STOP

T_VALID=T4-T0
~~~

另外记录：

~~~text
GPT_FIRST_ANSWER_SECONDS
GPT_REPLY_COMPLETION_SECONDS
RELAY_PARSE_VALIDATE_SECONDS
RELAY_GITHUB_PUBLISH_SECONDS
LOCAL_AVOIDABLE_WAIT_SECONDS
~~~

## 当前现实验证

旧失败证据全部保留：

~~~text
gpt-codex-real-case-v1
gpt-codex-time-v1-r1
gpt-codex-time-v2-r1
~~~

新 warm clean tasks：

~~~text
gpt-codex-time-v3-r1
gpt-codex-time-v3-r2
gpt-codex-time-v3-r3
~~~

三次都必须：

~~~text
REQUEST -> GPT reply COMMAND -> relay 000002
-> RESULT -> GPT reply DECISION -> relay 000004
-> STOP
~~~

# 最终一句话

> **GPT 负责决定“写什么”，Codex 只负责把 GPT 的结构化回复原样搬进 GitHub；这样保留 GPT 规划权和 GitHub 最终事实源，同时避开 ChatGPT 无人值守外部写操作的安全阻断。**
