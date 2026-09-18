# GPT↔Codex v3.1 现实实现与案例验证命令 v1

状态：

```text
AUTHORIZED_CORE_3_REAL_IMPLEMENT_VERIFY
```

先读：

```text
skills/first-principles-physical-limit-convergence/SKILL.md
skills/gpt-codex-convergence-orchestrator/SKILL.md
docs/gpt-codex/20260918-v3.1-three-core/GPT-CODEX-THREE-CORE-FINAL-v1.md
```

只实现被冻结的最终链，不自行增加新架构。

## 本机实现位置

```text
C:\AI\GPT-Codex-Convergence-Orchestrator
```

优先只使用：

```text
Python stdlib
sqlite3
native git / GitHub API
existing Playwright Native AI Browser
existing Capacity Router
```

禁止：

```text
改变代理/网络
改变系统全局设置
force push
新建另一套 browser stack
自行增加新的 workflow engine
自行改变角色和四消息闭环
把旧 L0/L1/L2/L3/L4 当当前流程
```

## 需要实现

最小文件即可：

```text
orchestrator.py
storage.py
github_bus.py
chatgpt_wakeup.py
codex_executor.py
config.json
state/orchestrator.db
reports/
```

必须支持：

```text
000001 REQUEST
000002 COMMAND
000003 RESULT
000004 DECISION

logical_event_id dedupe
action_id dedupe
read-after-write verification
restart resume
non-force Git publish
```

## 现实案例

```text
TASK_ID=gpt-codex-real-case-v1
OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256
```

先做最小本地验证，随后直接进行真实 GPT↔Codex 四消息闭环。

真实认证中加入：

```text
duplicate wakeup
duplicate poll
Browser reconnect
Codex restart
```

最终只返回：

```text
CORE_3_REAL_IMPLEMENT_VERIFY=PASS/FAIL
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

如果出现冻结方案之外的问题：

```text
STOP
SAVE REALITY_DELTA
RETURN TO GPT
```

不要在现实执行中自行设计新方案。
