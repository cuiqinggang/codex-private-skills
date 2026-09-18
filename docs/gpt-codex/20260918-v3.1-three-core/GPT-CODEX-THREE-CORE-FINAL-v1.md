# GPT↔Codex 三核心最终方案 v1.2 — v3.1.1

状态：

```text
CORE_1=COMPLETE
CORE_2=COMPLETE
CORE_3=REFROZEN_AFTER_REALITY_DELTA_02
```

## REALITY_DELTA-02

gpt-codex-real-case-v1 的远端 GitHub bus 已成功写入 000004，但：

```text
000004.type=ACK
```

冻结方案要求：

```text
000004.type=DECISION
```

000004 payload 实际已经包含：

```text
accepted=true
status=PASS
result_message_id=000003 RESULT
verification exact_readback=true
verification sha256=<expected>
```

因此：

```text
BUS_WRITE=PASS
GPT_BUSINESS_JUDGMENT=PASS
FINAL_MESSAGE_TYPE=FAIL
```

根因是页面 transport ACK 与 GitHub bus DECISION 语义未被显式分离。

## CORE 3 唯一修正

新增唯一 bus 回复白名单：

```text
REQUEST -> COMMAND
RESULT  -> DECISION
```

```text
ACK = page/browser transport only
ACK != GitHub bus message
```

publish 前必须验证 parent.type -> reply.type。

000004 DECISION payload 至少：

```text
result_message_id
accepted
status
control_action
verification
```

PASS 时：

```text
accepted=true
status=PASS
control_action=STOP
```

## 下一次认证

保留 real-case-v1 作为失败证据，不覆盖。

重新执行：

```text
TASK_ID=gpt-codex-real-case-v2
```

必须严格：

```text
000001 REQUEST
-> 000002 COMMAND
-> 000003 RESULT
-> 000004 DECISION
-> Codex STOP
```

## 当前实测时间基线（v1，非 VALID）

来自远端消息 created_at：

```text
000001 REQUEST = 14:54:10.563120Z
000002 COMMAND = 14:56:43.602139Z
000003 RESULT  = 14:58:39.288871Z
000004 ACK     = 15:01:09.991Z
```

分段：

```text
REQUEST -> COMMAND = 153.039 s
COMMAND -> RESULT  = 115.687 s
RESULT -> ACK      = 150.702 s
000001 -> 000004   = 419.428 s ≈ 6m59.4s
```

两次 GPT 方向等待约占 72.4%。

由于 000004 类型错误，本轮：

```text
T_VALID = NOT_VALID
```

但 419.428 s 可作为下一轮性能对照的预基线。

下一轮 correctness PASS 后，必须记录真实 T_VALID 和各分段；如果仍有明显可避免等待，再返回 CORE 1 做极限时间优化。
