# GPT↔Codex CORE 1 极限时间收敛命令 v1

状态：

~~~text
CORE_3_CORRECTNESS=PASS
ARCHITECTURE_CHANGE_ALLOWED=NO
CORE_1_TIME_CONVERGENCE=AUTHORIZED
~~~

## READ

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.4-thinking-watchdog
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-REAL-CASE-V2-SHARED-RESULT.md
~~~

以及当前冻结技能：

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.4-thinking-watchdog
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

### C. GPT Thinking Watchdog

不要用单一固定秒数判定故障。对每次 GPT wake 同时观察：

~~~text
目标 GitHub COMMAND/DECISION 是否出现
页面回复/DOM/Thinking 状态是否仍有进展
同类 wake + 同复杂度历史成功区间
Browser SKILL/正式配置的健康约定
~~~

状态：

~~~text
NORMAL_PROGRESS          -> 继续
SLOW_BUT_PROGRESSING     -> 继续，不刷新
SUSPECT_STALL            -> 加密观察 + health probe
CONFIRMED_STUCK          -> 执行恢复阶梯
~~~

确认卡死后严格：

~~~text
R0 先查 GitHub；已有目标回复则直接继续
R1 当前页停止生成（如可用）+ reload/hard refresh + 同 logical_event_id re-wake
R2 同一 profile 新页面/标签打开同一 conversation + 同 logical_event_id re-wake
R3 原 conversation 失效则新 ChatGPT 页面/新会话，从 GitHub 重新恢复上下文 + 同 logical_event_id re-wake
~~~

每一级前后都先查 GitHub；目标消息一出现立即停止恢复。

R0-R3 全部失败：

~~~text
BLOCKED
SAVE REALITY_DELTA
RETURN TO GPT
~~~

禁止无限恢复循环。

OpenAI 官方“看起来无限挂起时先短暂等待，然后停止/重试、刷新、必要时新开聊天”的排障步骤只作为无进展 guard；不要把它误写成模型固定最大思考时间。

记录：

~~~text
GPT_THINKING_STATE
GPT_THINKING_STUCK_COUNT
STUCK_CLASSIFICATION_REASON
RECOVERY_LEVEL_USED
GPT_THINKING_STUCK_RECOVERY_SECONDS
THINKING_BASELINE_SOURCE
~~~

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
GPT_THINKING_STATE=<state>
GPT_THINKING_STUCK_COUNT=<n>
STUCK_CLASSIFICATION_REASON=<reason>
RECOVERY_LEVEL_USED=<R0/R1/R2/R3/NONE>
GPT_THINKING_STUCK_RECOVERY_SECONDS=<value>
THINKING_BASELINE_SOURCE=<history/browser-contract/official-guard>
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
