# GPT↔Codex v3.1.1 现实实现与案例验证命令 v1.2

状态：

```text
AUTHORIZED_CORE_3_REVERIFY_AFTER_REALITY_DELTA_02
```

## READ

母方法：
```text
branch = codex/first-principles-physical-limit-convergence-v3.1.1
file   = skills/first-principles-physical-limit-convergence/SKILL.md
```

GPT↔Codex 当前技能：
```text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.2-final-decision
file   = skills/gpt-codex-convergence-orchestrator/SKILL.md
```

冻结方案：
```text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.2-final-decision
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-THREE-CORE-FINAL-v1.md
```

## DO

先保留 `gpt-codex-real-case-v1` 及其 000004 ACK 作为失败证据，不覆盖、不追加修复消息。

在实现中加入最小 bus 类型校验：

```text
parent REQUEST -> GPT bus reply MUST be COMMAND
parent RESULT  -> GPT bus reply MUST be DECISION
otherwise PUBLISH DENY
```

明确：

```text
Browser/page ACK 只属于 transport
ACK 禁止写入 GitHub bus
```

然后用全新干净任务：

```text
TASK_ID=gpt-codex-real-case-v2
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

运行完整真实链：

```text
000001 REQUEST
-> Browser wake GPT with EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND
-> 000002 COMMAND
-> Codex execute + verify
-> 000003 RESULT
-> Browser wake GPT with EXPECTED_GPT_BUS_REPLY_TYPE=DECISION
-> 000004 DECISION
-> Codex consume DECISION
-> STOP
```

000004 DECISION 至少要求：

```text
type=DECISION
accepted=true|false
status=PASS|FAIL
control_action=STOP|BLOCKED
result_message_id=<000003>
verification=<readback+sha>
```

同时继续验证：

```text
duplicate wakeup
duplicate poll
Browser reconnect
Codex restart
```

并记录：

```text
T0 request published
T1 command published
T2 result published
T3 decision published
T4 Codex consumed decision and stopped
```

计算全部分段时间与 T_VALID。

不要自行增加新架构，不要改变代理/系统设置。

## RETURN

完成后只回传：

```text
CORE_3_REAL_IMPLEMENT_VERIFY=PASS/FAIL
BUS_BRANCH=<branch>
FOUR_MESSAGE_TYPES=<000001..000004 types>
FINAL_000004_TYPE=<type>
TOY_RESULT=PASS/FAIL
MANUAL_MIDDLE_COPY_PASTE=<n>
DUPLICATE_BUSINESS_EFFECT=<n>
BROWSER_RECONNECT=PASS/FAIL
CODEX_RESTART_RESUME=PASS/FAIL
CODEX_FREE_EXPLORATION=<n>
T_GPT_REQUEST_TO_COMMAND_SECONDS=<value>
T_CODEX_COMMAND_TO_RESULT_SECONDS=<value>
T_GPT_RESULT_TO_DECISION_SECONDS=<value>
T_FINAL_CONSUME_SECONDS=<value>
T_VALID_SECONDS=<value>
REMOTE_HEAD=<sha>
REPORT_PATH=<path>
```

如果 correctness PASS 但 T_VALID 仍明显偏慢，只报告真实分段数据，不自行改变架构；由 GPT 回到 CORE 1 做极限时间优化。

若出现冻结方案之外的新问题：

```text
STOP
SAVE REALITY_DELTA
RETURN TO GPT
```
