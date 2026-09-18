# GPT↔Codex CORE 1 + Relay 时间收敛命令 v1.4

状态：

~~~text
REALITY_DELTA_GITHUB_WRITE_SAFETY=ABSORBED
GPT_DIRECT_GITHUB_WRITE_REQUIRED=NO
ARCHITECTURE=GPT_STRUCTURED_REPLY_CODEX_RELAY_GITHUB_TRUTH
~~~

## READ

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.4.0-relay
file   = skills/gpt-codex-convergence-orchestrator/SKILL.md
~~~

同时读取共同报告：

~~~text
branch = codex/gpt-codex-convergence-orchestrator-v1.4.0-relay
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-CORE1-TIME-CONVERGENCE-v1.md
~~~

## DO

不要再要求 GPT 页面直接调用 GitHub write action。

使用现有正式 Playwright Native AI Browser / chatgpt-web-plan-bridge 路径：

~~~text
Codex GitHub REQUEST
-> Browser wake GPT
-> GPT 页面输出 GPT_BUS_REPLY_V1
-> Browser 原样提取
-> Codex 机械 relay 到 GitHub COMMAND
-> Codex execute + RESULT
-> Browser wake GPT
-> GPT 页面输出 GPT_BUS_REPLY_V1 DECISION
-> Browser 原样提取
-> Codex 机械 relay 到 GitHub DECISION
-> Codex STOP
~~~

### GPT 页面格式

COMMAND：

~~~text
BEGIN_GPT_BUS_REPLY_V1
{
  "protocol":"GPT_BUS_REPLY_V1",
  "task_id":"<task>",
  "parent_message_id":"<000001 REQUEST message_id>",
  "type":"COMMAND",
  "logical_event_id":"<stable id>",
  "payload":{...complete command...}
}
END_GPT_BUS_REPLY_V1
~~~

DECISION 同结构，type=DECISION，payload 包含 accepted/status/control_action/result_message_id/verification。

### Relay

Codex 只能：

~~~text
parse
validate task/parent/type
hash raw reply
publish exact payload
add transport metadata
remote verify
~~~

禁止修改业务 payload。

### 首答故障

继续使用：

~~~text
RESULT->DECISION 首答 60 秒
REQUEST->COMMAND 首答 180 秒
大型复杂规划 600 秒
~~~

只限制开始回答前；正文一旦开始就停止 Thinking timeout。

### Clean runs

不要修补旧失败 branch。

新建并连续完成：

~~~text
gpt-codex-time-v3-r1
gpt-codex-time-v3-r2
gpt-codex-time-v3-r3
~~~

每轮必须：

~~~text
000001 REQUEST
000002 COMMAND (Codex relay, semantic author GPT)
000003 RESULT
000004 DECISION (Codex relay, semantic author GPT)
STOP
~~~

记录：

~~~text
GPT_FIRST_ANSWER_SECONDS
GPT_REPLY_COMPLETION_SECONDS
RELAY_PARSE_VALIDATE_SECONDS
RELAY_GITHUB_PUBLISH_SECONDS
COMMAND_TO_RESULT_SECONDS
FINAL_CONSUME_SECONDS
T_VALID_SECONDS
~~~

## 共享报告

最终同时保存：

~~~text
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\CORE1-TIME-CONVERGENCE-v1.4.md

docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-CORE1-TIME-CONVERGENCE-v1.4.md
~~~

push + remote verify。

## RETURN

只回传：

~~~text
CORE_1_TIME_CONVERGENCE=PASS/FAIL
ARCHITECTURE=GPT_STRUCTURED_REPLY_CODEX_RELAY_GITHUB_TRUTH
WARM_RUNS_COMPLETED=<n>/3
FUNCTIONAL_VALID=<n>/3
T_VALID_RUNS=<a,b,c>
T_VALID_MIN_SECONDS=<value>
T_VALID_P50_SECONDS=<value>
T_VALID_MAX_SECONDS=<value>
P50_GPT_FIRST_ANSWER_SECONDS=<value>
P50_GPT_REPLY_COMPLETION_SECONDS=<value>
P50_RELAY_PARSE_VALIDATE_SECONDS=<value>
P50_RELAY_GITHUB_PUBLISH_SECONDS=<value>
P50_COMMAND_TO_RESULT_SECONDS=<value>
P50_FINAL_CONSUME_SECONDS=<value>
DUPLICATE_BUSINESS_EFFECT=<n>
CODEX_SEMANTIC_MODIFICATION_COUNT=0
REMOTE_REPORT_PATH=<path>
REMOTE_HEAD=<sha>
FINAL_TIME_FREEZE_RECOMMENDATION=YES/NO
~~~

出现 GPT_BUS_REPLY_V1 无效时只允许同 logical_event_id 重试一次；仍失败就 STOP + REALITY_DELTA。
