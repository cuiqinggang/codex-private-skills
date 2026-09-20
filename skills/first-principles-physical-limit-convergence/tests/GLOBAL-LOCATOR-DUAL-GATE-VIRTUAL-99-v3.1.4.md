# Global Locator Dual Gate Virtual-99 v3.1.4

```text
PAGE=playwright浏览器自动化3
TASK=全局定位双门禁
SEQ=1
REAL_EXECUTION=NO
```

| Case | 条件 | 预期 | 实际 |
|---|---|---|---|
| G01 | GPT 命令有完整标签，Codex 接收 | PASS | PASS |
| G02 | GPT 漏标签，Codex 全局 AGENTS 门禁 | BLOCK | BLOCK |
| G03 | 当前任务未加载本技能，但全局 AGENTS 已加载 | BLOCK_IF_NO_LOCATOR | BLOCK_IF_NO_LOCATOR |
| G04 | 页面名未知，发送端不猜并禁止正式下发 | BLOCK | BLOCK |
| G05 | Codex 执行后最后一行原样回传定位标签 | PASS | PASS |
| G06 | Codex 最后一行标签不一致 | BLOCK | BLOCK |

```text
EXPECTED_CASES=6
ACTUAL_CORRECT=6
VIRTUAL_PASS=6/6
VIRTUAL_ACCURACY=100%
SENDER_GATE=PASS
GLOBAL_RECEIVER_GATE=PASS
SKILL_LOAD_INDEPENDENCE=PASS
CLOSED_LOOP=PASS
```

STOP
