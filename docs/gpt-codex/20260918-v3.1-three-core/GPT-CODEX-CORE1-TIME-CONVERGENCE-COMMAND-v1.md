# GPT↔Codex 简化验证命令 v1.4.1

## READ

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.4.1-simple-fallback
file   = skills/gpt-codex-convergence-orchestrator/SKILL.md
~~~

## DO

不要继续复杂化 GitHub 写入故障。

按下面简单规则继续当前 GPT↔Codex 验证：

~~~text
GitHub 正常可写
-> 走 GitHub 共同工作区

GitHub 写不了 / 被 GITHUB_WRITE_SAFETY_CHECK 阻断 / 明显 transport 异常
-> 立即切页面直传
~~~

页面 fallback 时：

~~~text
Browser 直接把当前必要 REQUEST / RESULT 内容发给 GPT
GPT 页面直接返回 COMMAND / DECISION
Browser 原样读取
Codex 原样执行 / 消费
~~~

页面格式：

~~~text
GPT_COMMAND
<完整命令>
END_GPT_COMMAND
~~~

或：

~~~text
GPT_DECISION
<完整裁决>
END_GPT_DECISION
~~~

Codex 不得修改 GPT 业务语义。

不要因为 GitHub 临时不可写停主任务，也不要现场修 GitHub。

继续执行 3 个 clean run：

~~~text
gpt-codex-time-v4-r1
gpt-codex-time-v4-r2
gpt-codex-time-v4-r3
~~~

每轮记录：

~~~text
TRANSPORT_USED=GITHUB|PAGE
GPT_FIRST_ANSWER_SECONDS
COMMAND_READY_SECONDS
COMMAND_TO_RESULT_SECONDS
DECISION_READY_SECONDS
FINAL_CONSUME_SECONDS
T_VALID_SECONDS
~~~

首答 Thinking 仍按：

~~~text
simple 60s
normal 180s
large 600s
~~~

一旦 GPT 开始正文就停止 Thinking timeout。

## RETURN

只回传：

~~~text
CORE_1_TIME_CONVERGENCE=PASS/FAIL
WARM_RUNS_COMPLETED=<n>/3
FUNCTIONAL_VALID=<n>/3
TRANSPORT_USED_RUNS=<A,B,C>
T_VALID_RUNS=<a,b,c>
T_VALID_MIN_SECONDS=<value>
T_VALID_P50_SECONDS=<value>
T_VALID_MAX_SECONDS=<value>
P50_GPT_FIRST_ANSWER_SECONDS=<value>
P50_COMMAND_TO_RESULT_SECONDS=<value>
P50_FINAL_CONSUME_SECONDS=<value>
DUPLICATE_BUSINESS_EFFECT=<n>
CODEX_FREE_EXPLORATION=<n>
FINAL_TIME_FREEZE_RECOMMENDATION=YES/NO
~~~

如果 GitHub 恢复后方便，再同步最终报告到共同仓库；同步失败本身不阻塞任务完成。
