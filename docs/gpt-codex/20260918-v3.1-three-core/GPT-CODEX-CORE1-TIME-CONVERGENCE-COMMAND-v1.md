# GPT↔Codex CORE 1 极限时间收敛命令 v1

状态：

~~~text
CORE_3_CORRECTNESS=PASS
ARCHITECTURE_CHANGE_ALLOWED=NO
CORE_1_TIME_CONVERGENCE=AUTHORIZED
~~~

## READ

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.8-self-contained-wakeup
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-REAL-CASE-V2-SHARED-RESULT.md
~~~

以及当前冻结技能：

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.8-self-contained-wakeup
file   = skills/gpt-codex-convergence-orchestrator/SKILL.md
~~~

## DO

只做 CORE 1 时间优化，不改变当前四消息架构、角色或业务语义。

冻结保持：

~~~text
Codex -> REQUEST
GPT -> COMMAND
Codex -> RESULT
GPT -> DECISION
Codex -> STOP
~~~

### A. 先做细粒度只读时间归因

从现有实现、日志和 real-case-v2 报告中拆出至少：

~~~text
request_publish
browser_wake_start
browser_wake_ready
command_remote_visible
command_consumed
effect_start
effect_verified
result_publish
second_wake_start
decision_remote_visible
decision_detected
tls_error_start/end if any
decision_consumed
stop
~~~

明确：

~~~text
EXTERNAL_GPT_BROWSER_TIME
GIT_NETWORK_TIME
LOCAL_POLL_WAIT
LOCAL_BACKOFF_WAIT
LOCAL_EXECUTION_TIME
TLS_RECOVERY_WAIT
FINAL_POST_DECISION_WAIT
~~~

### B. 只允许删除可避免等待

优先处理：

~~~text
1. 000004 DECISION 已远端可见后，Codex 应立即消费并 STOP；
   不为 page ACK 或无关后处理继续等待。

2. 等待预期 GitHub message 时先立即检查，再进入等待；
   transient TLS/network error 只恢复同一轮 remote check，
   不重启整个业务循环，不 replay 已完成 action。

3. 一旦观察到 branch/head 前进，立即重置等待并检查目标 message。

4. toy effect 的本地文件写入/验证本身应接近即时；
   COMMAND->RESULT 中若主要是 poll/sleep/backoff，
   只削减这些等待，不改变业务动作。
~~~

不得：

~~~text
换架构
换 Browser 栈
绕过 GitHub shared truth
取消去重/恢复
取消 remote verify
改变代理/系统设置
为了快而降低 VALID
~~~

### C. GPT Bus 自包含动作唤醒

r1 保留为失败证据，不覆盖。r1 已证明：GPT 页面正文开始输出，不代表 GitHub Bus 写动作发生。

后续每次 wakeup 必须使用：

~~~text
GPT_BUS_WAKEUP_V1
TASK_ID=<task>
REPOSITORY=cuiqinggang/codex-private-skills
BUS_BRANCH=<branch>
MESSAGE_SEQ=<seq>
MESSAGE_PATH=<queue path>
EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND|DECISION
REQUIRED_ACTION=WRITE_NEXT_BUS_MESSAGE_TO_GITHUB
~~~

附带固定指令：

~~~text
读取 GitHub request/result。
必须使用当前 ChatGPT 可用的 GitHub 写动作，把下一条 COMMAND/DECISION 直接提交到同一 BUS_BRANCH。
禁止只在聊天正文输出业务命令。
remote verify 后页面只回复 GPT_BUS_COMMIT_OK。
如果当前会话没有 GitHub 写动作/权限，只回复 GPT_BUS_WRITE_UNAVAILABLE。
如有授权/登录/审批等阻断，只回复 GPT_BUS_BLOCKED。
~~~

页面 turn 完成后：

~~~text
先查 GitHub
-> 目标 Bus message 已存在：继续
-> 不存在且页面=GPT_BUS_WRITE_UNAVAILABLE/BLOCKED：STOP + REALITY_DELTA
-> 不存在且页面只是业务正文：GPT_BUS_PROTOCOL_FAIL
   -> refresh/reconnect
   -> 同 TASK_ID / MESSAGE_SEQ / logical_event_id 重试一次相同 self-contained wakeup
   -> 第二次仍无远端消息：STOP + REALITY_DELTA
~~~

页面正文永远不能被 Codex 当作 COMMAND/DECISION。

### D. GPT Thinking 首答超时恢复

只测“多久开始回答”，不测“多久回答完”。

固定三档：

~~~text
SIMPLE = 60 秒
NORMAL = 180 秒
LARGE  = 600 秒
~~~

本项目：

~~~text
RESULT -> DECISION = SIMPLE = 60 秒
REQUEST -> COMMAND = NORMAL = 180 秒
~~~

计时：

~~~text
wakeup_sent -> first_visible_assistant_answer
~~~

规则：

~~~text
一旦 GPT 开始正常输出正文
-> 立即停止 Thinking timeout
-> 后续完整回答无论继续多久，都不因为本规则刷新

如果一直没有开始回答、仍停留在 Thinking/Generating：
-> 未超过上限：继续等待
-> 超过上限：按故障恢复
~~~

恢复前先检查 GitHub 是否已有目标消息；没有则 refresh/reconnect，并使用同一 TASK_ID / MESSAGE_SEQ / logical_event_id 重新 wake。必要时同一 profile 新开页面/会话。

记录：

~~~text
GPT_WAIT_CLASS
GPT_FIRST_ANSWER_LIMIT_SECONDS
GPT_FIRST_ANSWER_SECONDS
ANSWER_STARTED
GPT_THINKING_STUCK_COUNT
GPT_THINKING_STUCK_RECOVERY_SECONDS
~~~

### E. Warm clean timing certification

完成时间收敛后，用同一 frozen architecture 连续执行 3 个独立 warm clean case：

~~~text
gpt-codex-time-v2-r1
gpt-codex-time-v2-r2
gpt-codex-time-v2-r3
~~~

每个都完成：

~~~text
REQUEST -> COMMAND -> RESULT -> DECISION -> STOP
~~~

不主动注入故障；若自然出现 TLS/network fault，单独记录，不隐藏。

每轮记录：

~~~text
T_GPT_REQUEST_TO_COMMAND
T_CODEX_COMMAND_TO_RESULT
T_GPT_RESULT_TO_DECISION
T_FINAL_CONSUME
T_VALID
TLS_RECOVERY_WAIT
LOCAL_AVOIDABLE_WAIT
~~~

汇总：

~~~text
T_VALID_MIN
T_VALID_P50
T_VALID_MAX
各阶段 P50
自然故障次数
~~~

### F. 共享事实闭环

最终必须同时保存：

本机详细报告：

~~~text
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\CORE1-TIME-CONVERGENCE-v1.md
~~~

GitHub 共享报告：

~~~text
docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-CORE1-TIME-CONVERGENCE-v1.md
~~~

并 push + remote verify。

仅有本机报告不算完成。

## RETURN

只回传：

~~~text
CORE_1_TIME_CONVERGENCE=PASS/FAIL
ARCHITECTURE_CHANGED=NO
WARM_RUNS=3
T_VALID_RUNS=<a,b,c>
T_VALID_MIN_SECONDS=<value>
T_VALID_P50_SECONDS=<value>
T_VALID_MAX_SECONDS=<value>
P50_REQUEST_TO_COMMAND_SECONDS=<value>
P50_COMMAND_TO_RESULT_SECONDS=<value>
P50_RESULT_TO_DECISION_SECONDS=<value>
P50_FINAL_CONSUME_SECONDS=<value>
P50_TLS_RECOVERY_WAIT_SECONDS=<value>
P50_LOCAL_AVOIDABLE_WAIT_SECONDS=<value>
GPT_WAIT_CLASS=<SIMPLE/NORMAL/LARGE>
GPT_FIRST_ANSWER_LIMIT_SECONDS=<60/180/600>
GPT_FIRST_ANSWER_SECONDS=<value>
ANSWER_STARTED=<YES/NO>
GPT_BUS_ACTION_STATUS=<COMMIT_OK/WRITE_UNAVAILABLE/BLOCKED/PROTOCOL_FAIL>
GPT_BUS_PROTOCOL_RETRY_COUNT=<n>
GPT_THINKING_STUCK_COUNT=<n>
GPT_THINKING_STUCK_RECOVERY_SECONDS=<value>
FUNCTIONAL_VALID=3/3 or <n>/3
DUPLICATE_BUSINESS_EFFECT=0/<other>
REMOTE_REPORT_PATH=<path>
REMOTE_HEAD=<sha>
FINAL_TIME_FREEZE_RECOMMENDATION=YES/NO
~~~

如果发现必须改变架构才能继续优化：

~~~text
STOP
REALITY_DELTA
RETURN TO GPT
~~~

不要自行改架构。
