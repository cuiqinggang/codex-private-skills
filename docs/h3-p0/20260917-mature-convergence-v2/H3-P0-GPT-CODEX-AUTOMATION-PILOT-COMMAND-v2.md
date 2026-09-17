# H3-P0 GPT-Codex 自动闭环 Shadow Pilot v2（Codex-first）

状态：`READY_TO_EXECUTE / CODEX_FIRST / TOY_ONLY / NO_H3_GPU`

## 1. 出发点

唯一主动方：

```text
LOOP_OWNER=CODEX
GPT=ON_DEMAND_PLANNER_JUDGE
GITHUB=NUMBERED_MESSAGE_BUS
AI_BROWSER=GPT_WAKEUP_ONLY
```

用户只把初始任务交给 Codex。之后普通轮次不再人工复制粘贴。

## 2. 先读

```text
skills/gpt-codex-convergence-orchestrator/SKILL.md
skills/gpt-codex-convergence-orchestrator/references/CODEX-FIRST-NUMBERED-BUS-v1.md
skills/gpt-codex-convergence-orchestrator/schemas/STATE.schema.json
skills/chatgpt-web-plan-bridge-latest/SKILL.md
skills/codex-capacity-aware-model-router/SKILL.md
```

## 3. 正式安装目录

```text
C:\AI\GPT-Codex-Convergence-Orchestrator
```

至少实现：

```text
orchestrator.py
config.json
adapters\github_bus.py
adapters\chatgpt_wakeup.py
adapters\codex_executor.py
adapters\capacity_router.py
state\
logs\
reports\CODEX-FIRST-SHADOW-PILOT.md
```

## 4. Workspace

```text
workspaces/gpt-codex-shadow-pilot-v2/
  TASK.md
  STATE.json
  queue/
  payloads/
  ARTIFACTS.md
  EVENTS.jsonl
```

所有 queue 消息使用六位单调序号，旧消息不可覆盖。

## 5. Toy Task

最终要求 Codex 创建：

```text
toy-result.txt
```

内容完全等于：

```text
GPT_CODEX_CODE_TO_CODE_OK
```

然后读取并计算 SHA256。

## 6. 完整流程

### A. Codex 主动启动

用户只给 Codex 本命令包。

Codex：

1. 初始化 workspace；
2. 写 `000001-CODEX-REQUEST-GPT.json` + `payloads/000001.md`；
3. commit/push/remote verify；
4. payload 只说明 toy task 的目标与约束，不自行写最终实现命令；
5. 通过现有 AI Browser 向 GPT 发送最小 wakeup：TASK_ID / REQUEST_SEQ / repo / branch / request path。

### B. GPT 直接写 GitHub

GPT 被唤醒后必须：

1. 自己读取 GitHub 的 `000001` 请求；
2. 做规划；
3. 直接创建：

```text
000002-GPT-COMMAND-CODEX.json
payloads/000002.md
```

4. remote verify；
5. 页面只回复：

```text
GPT_COMMIT_OK TASK_ID=gpt-codex-shadow-pilot-v2 SEQ=000002 HEAD=<sha>
```

浏览器不搬运命令正文。

### C. Codex 监仓库执行

Codex watcher 发现 seq=000002 且 receiver=CODEX：

1. 生成 ACTION_ID；
2. 去重；
3. 只读取 GitHub payload 执行；
4. 创建 toy-result.txt；
5. 验证内容和 SHA；
6. 写：

```text
000003-CODEX-RESULT-GPT.json
payloads/000003.md
```

7. push + remote verify；
8. 再次用 Browser 只发送 wakeup：TASK_ID / RESULT_SEQ=000003 / repo/ref。

### D. GPT 最终裁决直接写仓库

GPT 读取 000003 后直接创建：

```text
000004-GPT-DECISION-CODEX.json
payloads/000004.md
```

如果 toy task 正确：

```text
CONTROL_ACTION=FREEZE
```

否则 `BLOCKED`。

页面只回复短 ACK。

### E. Codex 收口

Codex watcher 读取 000004：

- FREEZE -> 写 STATE=FREEZE，生成报告，push/verify，停止；
- BLOCKED -> 保存证据停止；
- 不允许自行发明第五条业务消息。

## 7. 故障注入

必须验证：

```text
A1 Codex 主动产生 000001
A2 GPT 直接 GitHub 写 000002
A3 Browser 不携带长命令正文
A4 Codex 只消费 000002 GitHub payload
A5 Codex 直接写 000003
A6 GPT 直接写 000004
A7 重复 wakeup 不产生重复 GPT command
A8 重复 poll 不重跑 Codex action
A9 Browser 中断后恢复同一 request seq
A10 capacity failover 不重放本地工作
A11 orchestrator/Windows重启从 STATE+queue 恢复
A12 STOP 文件立即停止
A13 unknown status -> BLOCKED，不自由探索
A14 全流程用户复制粘贴次数=0（初始启动命令不计）
```

## 8. 成功条件

```text
CODEX_IS_LOOP_OWNER=YES
GPT_DIRECT_GITHUB_WRITE=YES
GITHUB_IS_COMMAND_SOURCE=YES
BROWSER_LONG_PAYLOAD_TRANSPORT=NO
NUMBERED_BUS=PASS
IDEMPOTENCY=PASS
CHECKPOINT_RESUME=PASS
MANUAL_COPY_PASTE_REQUIRED=NO
TOY_TASK_RESULT=PASS
NO_H3_GPU_RUN=YES
AUTOMATION_SHADOW_PILOT_V2=PASS
READY_FOR_ASSISTED_REAL_TASK_PILOT=YES
```

## 9. 禁止

- 不运行 H3 GPU；
- 不修改代理/网络；
- 不新造浏览器栈；
- 不让 GPT 轮询仓库；
- 不让 Codex从ChatGPT长回复直接执行；
- 不把浏览器 DOM 当事实源；
- 不覆盖已存在编号消息；
- 不 force push；
- 不让 Codex自由研究。

## 10. 交付

本机报告：

```text
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\CODEX-FIRST-SHADOW-PILOT.md
C:\AI\GPT-Codex-Convergence-Orchestrator\reports\CODEX-FIRST-SHADOW-PILOT.json
```

项目摘要：

```text
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-GPT-CODEX-AUTOMATION-PILOT-RESULT-v2.md
```

commit/push/remote verify 后 STOP RETURN TO GPT。