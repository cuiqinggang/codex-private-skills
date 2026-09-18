---
name: gpt-codex-convergence-orchestrator
description: GPT↔Codex 自动闭环执行技能。当前版本只服从 first-principles-physical-limit-convergence v3.1.1 的三核心白名单：极限短时间、成熟方案集群、高智能虚拟成熟。Codex 负责主动循环和确定性执行，GPT 负责按需规划/裁决，GitHub 是共享事实源，AI Browser 只负责唤醒 GPT。Browser 入口从已安装 playwright-native-ai-browser/SKILL.md 解析。GitHub 总线回复类型使用唯一白名单：REQUEST 只能由 GPT 回复 COMMAND；RESULT 只能由 GPT 回复 DECISION；页面 ACK 永远不能作为 GitHub 总线消息类型。
metadata:
  version: "1.3.4"
  method_dependency: "first-principles-physical-limit-convergence@3.1.1"
  architecture: "CODEX_GITHUB_GPT_CLOSED_LOOP"
---

# GPT↔Codex 自动闭环 v1.3.4

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

## GPT“正在思考”状态 Watchdog

这是 Browser transport 的故障恢复，不改变四消息架构。

### 1. 不用单一固定秒数判故障

时间只是一个信号。状态判断同时看：

```text
A. 期待的 GitHub COMMAND / DECISION 是否已经出现
B. 页面是否仍有真实输出进展
   - 回复文本/DOM 持续增长
   - Thinking/Generating 状态发生变化
   - 页面仍可响应
C. 当前 wake 类型与任务复杂度的历史正常完成区间
D. Browser SKILL / 正式配置里的响应等待/健康检查约定
E. OpenAI 官方“无限挂起”排障观察窗只作为无进展 guard，不作为模型最大思考时间
```

### 2. 状态分类

```text
NORMAL_PROGRESS
= GitHub 已有目标回复，或页面仍持续产生可观察进展

SLOW_BUT_PROGRESSING
= 已经较慢，但仍有输出/状态变化
-> 继续等待，不刷新

SUSPECT_STALL
= GitHub 无目标回复
+ 页面持续显示 Thinking/Generating
+ 一个完整观察窗口内无输出/DOM/状态进展

CONFIRMED_STUCK
= SUSPECT_STALL 持续
+ 已明显超过同类 wake/同复杂度历史正常区间或 Browser 正式健康上限
+ 再次 health probe 仍无进展
```

没有足够历史数据时，不猜“模型最大思考时间”；使用 Browser 正式约定 + 官方无进展排障窗口作为保守 guard，并持续积累真实成功样本。

### 3. 恢复阶梯

一旦 CONFIRMED_STUCK：

```text
R0 REMOTE_FIRST
   先查 GitHub
   -> 目标回复已存在：直接继续，禁止刷新/重发

R1 SAME_PAGE_RECOVERY
   -> 当前页仍健康：停止生成（如可用）
   -> reload / hard refresh 当前会话
   -> 同一 TASK_ID / MESSAGE_SEQ / logical_event_id 重新 wake

R2 SAME_CONVERSATION_NEW_PAGE
   -> 在同一已登录 profile 新开页面/标签
   -> 打开同一 conversation
   -> 同一 logical_event_id 重新 wake

R3 FRESH_CHAT_REHYDRATE
   -> 如果原 conversation 本身无法继续
   -> 新开 ChatGPT 页面/新会话
   -> 仍发送同一个最小 wakeup
   -> GPT 从 GitHub TASK/message/证据重新恢复上下文
   -> 不创建新的业务 request / seq / logical_event_id
```

每一级恢复前后都必须先查 GitHub；一旦目标消息出现，立即停止恢复链。

完整 R0-R3 走完仍无目标回复：

```text
BLOCKED
SAVE REALITY_DELTA
RETURN TO GPT
```

禁止再次无限循环 R0-R3。

### 4. 绝对不允许

```text
因为“时间长”但仍有输出进展就刷新
无限显示 Thinking 半小时不处理
改变 TASK_ID
改变 MESSAGE_SEQ
产生第二个 logical_event_id
产生第二个业务 REQUEST
修改业务方案
改变代理/网络设置
```

### 5. 必须记录

```text
GPT_THINKING_STATE
GPT_THINKING_STUCK_COUNT
STUCK_CLASSIFICATION_REASON
RECOVERY_LEVEL_USED
GPT_THINKING_STUCK_RECOVERY_SECONDS
THINKING_BASELINE_SOURCE
```

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

> **页面 ACK 只确认 transport；GitHub 总线只认 REQUEST→COMMAND、RESULT→DECISION；GPT Thinking 是否故障必须由“远端结果 + 页面进展 + 历史正常区间 + Browser 健康约定”共同判断，确认卡死后按 R0→R3 恢复，并始终复用同一 logical_event_id。**
