# GPT↔Codex 三核心最终方案 v1.1 — v3.1.1

状态：

```text
CORE_1=COMPLETE
CORE_2=COMPLETE
CORE_3=REFROZEN_AFTER_BROWSER_ENTRY_REALITY_DELTA
```

## REALITY_DELTA-01

现实执行发现：

```text
C:\AI\Playwright-Native-AI-Browser\scripts\chatgpt-business-entry.js
C:\AI\Playwright-Native-AI-Browser\references\MATURE-OPERATIONS-CONTRACT.md
C:\AI\Playwright-Native-AI-Browser\references\GPT-BUSINESS-VALIDATION-SOP.md
```

这些写死路径不存在。

同时真实存在：

```text
C:\Users\A\.codex\skills\playwright-native-ai-browser\SKILL.md
```

修正结论：

```text
Browser 能力不判定为缺失。
错误在于冻结方案写死/猜测了旧入口位置。
```

## CORE 3 修正

Browser 唯一定位逻辑改为：

```text
读取 C:\Users\A\.codex\skills\playwright-native-ai-browser\SKILL.md
-> 若为 Junction/Symlink，解析 Target
-> 读取 SKILL.md 当前正式入口/恢复约定
-> 使用它明确声明的业务入口
```

只有：

```text
SKILL.md 不存在
或
SKILL.md 明确声明的正式入口也不存在
```

才：

```text
STOP
REALITY_DELTA
RETURN_TO_GPT
```

禁止继续猜测旧的 root\scripts 或 root\references 路径。

## 冻结完整链

```text
Codex
-> 000001 REQUEST -> GitHub
-> 通过 installed playwright-native-ai-browser/SKILL.md 解析正式 Browser 入口
-> Browser wake GPT
-> GPT reads GitHub
-> 000002 COMMAND -> GitHub
-> Codex reads GitHub
-> execute + verify
-> 000003 RESULT -> GitHub
-> Browser wake GPT
-> GPT reads GitHub
-> 000004 DECISION -> GitHub
-> Codex reads DECISION
-> STOP
```

其余 CORE 1、CORE 2、GitHub、SQLite、去重、恢复和现实案例定义保持 v1 不变。

当前唯一现实案例仍为：

```text
TASK_ID=gpt-codex-real-case-v1
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

这就是修正后的冻结 CORE 3。
