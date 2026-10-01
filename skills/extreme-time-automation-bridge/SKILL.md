---
name: extreme-time-automation-bridge
version: "0.1.3"
description: 极限短时间自动化闭环的无决策权执行桥。GPT负责判断，桥只负责领取、执行、记录、回传；正式任务运行期间用户人工介入必须为0。
---

# 极限短时间自动化执行桥 v0.1.3

```ini
STATUS=PARTIAL_REALITY
VERSION=0.1.3
REALITY_CERTIFIED=NO

STATIC_GATE=PASS
STATIC_VALIDATION_RUN_ID=36900593142

WINDOWS_REALITY=PASS
WINDOWS_SMOKE_TASK=ETAL-BRIDGE-SMOKE-001
WINDOWS_SMOKE_RUN_ID=36899361139
WINDOWS_SMOKE_ARTIFACT_ID=11186888753
WINDOWS_RUNNER_MODE=TEMPORARY_NON_PERSISTENT
PERSISTENCE_CONFIGURED=NO
CALLBACK_TESTED=NO

CORE_BRAIN=GPT
BRIDGE_DECISION_POWER=NONE
USER_INTERVENTION_DURING_TASK=0
TRANSPORT=GitHub
WINDOWS_EXECUTOR=GitHub_SELF_HOSTED_RUNNER
MIN_TASK_ENTRY=workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

## 当前现实

Windows Reality 执行层已经真实 PASS。

Run `36899361139`：
- `contract-static=success`
- `windows-reality=success`
- Runner：`DESKTOP-4A1EGTM-etal`
- Labels：`self-hosted, Windows, X64`
- `ETAL-BRIDGE-SMOKE-001` 真执行
- artifact：`etal-bridge-ETAL-BRIDGE-SMOKE-001-36899361139`
- artifact ID：`11186888753`
- `result.json.status=PASS`
- `exit_code=0`
- `duration_ms=9316.85`
- `stderr.txt` 为空

本轮使用临时非持久化 runner；任务完成后 runner 已停止。

## 为什么整体仍是 PARTIAL

尚未 Reality 验证：
1. Windows runner 长期常驻；
2. `ETAL_BRIDGE_CALLBACK_URL`；
3. Windows结果回来后自动唤醒 GPT；
4. GPT 自动生成下一任务并再次进入 Windows Reality。

因此：
`WINDOWS_REALITY=PASS`，但 `REALITY_CERTIFIED=NO`。

## v0.1.3 已验证修正

- workflow 顶层 concurrency 已删除；
- 并发串行门仅位于 `windows-reality` job；
- 静态合同门禁不再被离线 Windows runner 阻塞；
- 只有 tasks/*.json 变化或显式 workflow_dispatch 指定任务时才进入 Windows Reality。

## 最小入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

## 安全与权限

- 不修改 FlClash / Windows 网络代理。
- 不执行 Windows 系统破坏性动作。
- payload 只能来自固定 payload 目录。
- Reality 失败必须原样记录。

## 计时

首次桥建设单列 `T_PLATFORM_BOOTSTRAP`。
标准题001仍未正式起表。
