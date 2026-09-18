# GPT↔Codex v3.1.1 现实实现与案例验证命令 v1.1

状态：

```text
AUTHORIZED_CORE_3_REAL_IMPLEMENT_VERIFY
REALITY_DELTA_01_RESOLVED_VIRTUALLY
```

## READ

1. 母方法：
```text
branch = codex/first-principles-physical-limit-convergence-v3.1.1
file   = skills/first-principles-physical-limit-convergence/SKILL.md
```

2. GPT↔Codex 技能：
```text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.1-browser-entry
file   = skills/gpt-codex-convergence-orchestrator/SKILL.md
```

3. 修正后的冻结方案：
```text
branch = codex/gpt-codex-convergence-orchestrator-v1.3.1-browser-entry
file   = docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-THREE-CORE-FINAL-v1.md
```

## Browser 入口规则

不要再读取猜测的：

```text
C:\AI\Playwright-Native-AI-Browser\scripts\chatgpt-business-entry.js
C:\AI\Playwright-Native-AI-Browser\references\...
```

先读取：

```text
C:\Users\A\.codex\skills\playwright-native-ai-browser\SKILL.md
```

如果它是 Junction/Symlink，解析 Target。

然后严格按照 **SKILL.md 当前明确声明/引用的正式业务入口与恢复约定** 调用 Browser。

只在 SKILL.md 本身或它明确指向的正式入口真实不存在时，才停止并回传新的 REALITY_DELTA。

## DO

继续上次已停止的同一任务，不重做已经完成的无关探索：

```text
TASK_ID=gpt-codex-real-case-v1
```

实现最小 GPT↔Codex 四消息链与 SQLite 去重/恢复：

```text
000001 REQUEST
-> Browser wake GPT
-> 000002 COMMAND
-> Codex execute + verify
-> 000003 RESULT
-> Browser wake GPT
-> 000004 DECISION
-> Codex STOP
```

现实案例：

```text
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

并验证：

```text
duplicate wakeup
duplicate poll
Browser reconnect
Codex restart
```

不要自行增加新架构、workflow engine 或 Browser 栈；不要改变代理/系统设置。

## RETURN

完成后只回传：

```text
CORE_3_REAL_IMPLEMENT_VERIFY=PASS/FAIL
BROWSER_ENTRY_RESOLVED=<actual canonical entry>
FOUR_MESSAGE_LOOP=PASS/FAIL
TOY_RESULT=PASS/FAIL
MANUAL_MIDDLE_COPY_PASTE=<n>
DUPLICATE_BUSINESS_EFFECT=<n>
BROWSER_RECONNECT=PASS/FAIL
CODEX_RESTART_RESUME=PASS/FAIL
CODEX_FREE_EXPLORATION=<n>
T_VALID_SECONDS=<value>
REMOTE_HEAD=<sha>
REPORT_PATH=<path>
```

若出现冻结方案之外的新问题：

```text
STOP
SAVE REALITY_DELTA
RETURN TO GPT
```
