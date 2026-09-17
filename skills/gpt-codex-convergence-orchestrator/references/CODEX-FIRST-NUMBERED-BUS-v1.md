# Codex-first 编号化任务总线 v1

## 1. 唯一主动方

```text
LOOP_OWNER = CODEX
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = NUMBERED_MESSAGE_BUS + SHARED_TRUTH
AI_BROWSER = CODEX_TO_GPT_WAKEUP_TRANSPORT
```

Codex 常驻/周期运行，负责观察远端状态并决定“当前应该执行冻结命令，还是请求 GPT 决策”。

GPT 不承担 daemon/watch/poll 职责；GPT 只有被 Codex 通过 AI Browser 唤醒后才进行规划、判断和写入下一消息。

## 2. 消息目录

每个任务：

```text
workspaces/<TASK_ID>/
  TASK.md
  STATE.json
  queue/
    000001-CODEX-REQUEST-GPT.json
    000002-GPT-COMMAND-CODEX.json
    000003-CODEX-RESULT-GPT.json
    000004-GPT-COMMAND-CODEX.json
    ...
  payloads/
    000001.md
    000002.md
    000003.md
  ARTIFACTS.md
  EVENTS.jsonl
```

序号必须单调递增、六位零填充。一个序号只代表一个不可变消息。

## 3. 消息 envelope

每条 `queue/*.json` 至少：

```json
{
  "task_id": "...",
  "seq": 1,
  "message_id": "<TASK_ID>:000001",
  "parent_message_id": null,
  "sender": "CODEX",
  "receiver": "GPT",
  "type": "REQUEST_PLAN",
  "status": "READY",
  "payload_path": "payloads/000001.md",
  "source_commit": "...",
  "idempotency_key": "...",
  "created_at": "..."
}
```

`payload_path` 承载长文本，envelope 只承载控制信息。

## 4. Codex 主循环

```text
启动/恢复
→ git fetch + remote verify
→ 读取 STATE + queue 最大序号
→ 查找下一个 receiver=CODEX 且 status=READY 的消息
    → 有：按冻结内容确定性执行
    → 无：判断是否需要 GPT
         → 不需要：等待/继续本地已授权动作
         → 需要：写下一条 CODEX->GPT REQUEST，push+verify
                  → AI Browser 唤醒 GPT，并只发送 TASK_ID + seq + repo/ref
                  → 等待 GitHub 出现更高 seq 的 GPT->CODEX 消息
→ 循环
```

Codex 不从 ChatGPT DOM 抓取业务命令作为事实源。真正的下一命令必须来自 GitHub 编号消息。

## 5. GPT 行为

GPT 被浏览器唤醒后收到最小请求：

```text
TASK_ID
REQUEST_SEQ
REPOSITORY
BRANCH
REQUEST_FILE
```

GPT：

1. 从 GitHub 读取指定请求与相关证据；
2. 做规划/判断；
3. 直接在同一 workspace 写入下一条单调序号消息；
4. push/remote verify；
5. 页面只返回短 ACK，例如：

```text
GPT_COMMIT_OK TASK_ID=<...> SEQ=<000002> HEAD=<sha>
```

Codex 不依赖 ACK 中的命令正文；ACK 只是 transport 证据。

## 6. 编号规则

- Codex 与 GPT 共用同一全局序列；
- 任何新消息先读当前远端最大 seq，再分配 `max+1`；
- 写入前必须确认父消息仍是当前未消费 head；
- 并发冲突时禁止 force push，重新 fetch 后再分配新 seq；
- 已存在的 `message_id` 永远不可覆盖。

## 7. 消费规则

Codex 只消费：

```text
receiver=CODEX
status=READY
seq > LAST_CONSUMED_SEQ
```

消费前生成：

```text
ACTION_ID = task_id + seq + source_commit + type
```

如果 ACTION_ID 已完成：`REPLAY=NO`。

执行完成后不修改原消息；写一个新的 RESULT 消息。

## 8. GPT 请求触发条件

Codex 只有在以下情况才唤醒 GPT：

- 新任务需要第一版规划；
- 当前冻结命令包要求 `RETURN_TO_GPT`；
- 命令包外异常；
- Final Certification 需要 GPT 最终裁决；
- 用户改变 task contract。

普通 PASS/FAIL/ROLLBACK 分支若已在命令包定义，Codex直接继续，不唤醒 GPT。

## 9. Browser 最小职责

AI Browser 只做：

```text
确保指定 ChatGPT 会话可用
→ 发送最小 wakeup 消息
→ 等待 GPT_COMMIT_OK / BLOCKED / USER_APPROVAL_REQUIRED ACK
→ 保存 transport 证据
```

浏览器不再搬运完整命令/完整结果，不承担共享事实源。

## 10. 故障恢复

### Browser 失败

GitHub 请求已存在则不重复创建；恢复 Browser 后用同一个 `REQUEST_SEQ` 再次 wakeup。

### GPT 页面回复丢失

Codex先检查 GitHub 是否已有更高 seq 的 GPT 消息；如果有，直接继续，禁止再次请求 GPT 产生重复命令。

### Codex/Windows 重启

从 `STATE.json + queue + action ledger` 恢复，不重跑已完成动作。

### Model capacity

由 `codex-capacity-aware-model-router` 处理；不改变 queue seq，不重放本地工作。

## 11. 人类边界

用户只处理：

```text
STOP
PAUSE
登录/验证码
敏感权限批准
task contract 改变
```

普通文本搬运应为零。

## 12. 核心结论

```text
CODEX_IS_LOOP_OWNER=YES
GPT_IS_DAEMON=NO
GITHUB_IS_COMMAND_SOURCE=YES
BROWSER_CARRIES_LONG_BUSINESS_PAYLOAD=NO
NUMBERED_IMMUTABLE_MESSAGES=YES
MANUAL_COPY_PASTE_TARGET=ZERO
```