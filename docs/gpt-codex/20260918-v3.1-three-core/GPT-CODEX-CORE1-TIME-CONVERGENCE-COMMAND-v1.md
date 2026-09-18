# GPT↔Codex CORE 1 极限时间收敛命令 v1

状态：

~~~text
CORE_3_CORRECTNESS=PASS
ARCHITECTURE_CHANGE_ALLOWED=NO
CORE_1_TIME_CONVERGENCE=AUTHORIZED
~~~

## READ

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.3-thinking-stuck
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-REAL-CASE-V2-SHARED-RESULT.md
~~~

以及当前冻结技能：

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.3-thinking-stuck
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

### C. GPT thinking-stuck 小故障恢复

等待 GPT 回复时：

~~~text
THINKING_TIMEOUT_SECONDS = 从已安装 playwright-native-ai-browser/SKILL.md 或其当前正式配置读取
~~~

超过该正式等待上限仍显示“正在思考/生成中”时：

~~~text
先检查 GitHub 是否已有期待的 COMMAND/DECISION
-> 有：直接继续
-> 无：刷新/重连同一个 ChatGPT 会话
-> 复用同一个 TASK_ID / MESSAGE_SEQ / logical_event_id 重新 wake
-> 不创建新业务请求
~~~

记录：

~~~text
GPT_THINKING_STUCK_COUNT
GPT_THINKING_STUCK_RECOVERY_SECONDS
~~~

禁止无限等待半小时不处理。

### D. Warm clean timing certification

完成时间收敛后，用同一 frozen architecture 连续执行 3 个独立 warm clean case：

~~~text
gpt-codex-time-v1-r1
gpt-codex-time-v1-r2
gpt-codex-time-v1-r3
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

### E. 共享事实闭环

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
GPT_THINKING_STUCK_COUNT=<n>
GPT_THINKING_STUCK_RECOVERY_SECONDS=<value>
THINKING_TIMEOUT_SOURCE=<path/config>
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
