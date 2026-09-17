# H3-P0 Codex-first 自动化架构 v1

状态：`DESIGN_FROZEN / SHADOW_PILOT_V2_READY`

## 核心结论

```text
CODEX_IS_LOOP_OWNER=YES
GPT_IS_ON_DEMAND_BRAIN=YES
GITHUB_IS_NUMBERED_BUS=YES
AI_BROWSER_IS_WAKEUP_ONLY=YES
MANUAL_COPY_PASTE_TARGET=ZERO
```

## 为什么必须从 Codex 出发

GPT 不具备常驻主动轮询能力；没有外部触发时不会自动检查仓库。

Codex 则具备：

- 本地执行；
- 文件/进程/GPU控制；
- GitHub 状态同步；
- checkpoint/resume；
- watcher/循环；
- 调用 AI Browser 唤醒 GPT。

因此自动闭环的主动心跳必须放在 Codex 侧。

## 最简链路

```text
用户 -> Codex（只在任务起点）

Codex
  -> GitHub: 000001 REQUEST_GPT
  -> AI Browser: wake GPT

GPT
  -> GitHub: 000002 COMMAND_CODEX
  -> Browser page: short ACK only

Codex watcher
  -> GitHub read 000002
  -> execute
  -> GitHub: 000003 RESULT_GPT
  -> AI Browser: wake GPT

GPT
  -> GitHub: 000004 DECISION_CODEX

Codex watcher
  -> execute/freeze/block
```

GitHub 是命令正文和结果正文的唯一正式 transport。浏览器只承担 GPT 的唤醒与 ACK，不再搬运长文本。

## 编号协议

正式规则：

```text
skills/gpt-codex-convergence-orchestrator/references/CODEX-FIRST-NUMBERED-BUS-v1.md
```

消息必须单调序号、不可覆盖、带 sender/receiver/type/source_commit/idempotency_key。

## 当前正式入口

```text
skill=gpt-codex-convergence-orchestrator v1.1.0
pilot=H3-P0-GPT-CODEX-AUTOMATION-PILOT-COMMAND-v2.md
```

第一阶段仅 toy task，不执行 H3 GPU。
