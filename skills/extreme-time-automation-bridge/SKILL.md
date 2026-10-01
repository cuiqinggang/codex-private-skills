---
name: extreme-time-automation-bridge
version: "0.2.0"
description: 极限短时间自动化闭环的无决策权执行桥。GPT负责判断，桥只负责领取、执行、记录、回传；正式任务运行期间用户人工介入必须为0。
---

# 极限短时间自动化执行桥 v0.2.0

```ini
STATUS=PARTIAL_REALITY
VERSION=0.2.0
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
DIRECT_REMOTE_FIRST=YES
PRIMARY_TRANSPORT=Desktop_Commander_Remote
PRIMARY_WINDOWS_EXECUTOR=Desktop_Commander_Remote
FALLBACK_TRANSPORT=GitHub
FALLBACK_WINDOWS_EXECUTOR=GitHub_SELF_HOSTED_RUNNER
DIRECT_REMOTE_REALITY=PASS
DIRECT_REMOTE_SCOPE=LOCAL_FILE_AND_PROCESS_TASKS
PRIMARY_ROUTE_CERTIFIED=YES
FALLBACK_PERSISTENCE=USER_LOGON_SCHEDULED_TASK
FALLBACK_TASK_NAME=ETAL-GitHub-Actions-Runner
FALLBACK_RUNNER=DESKTOP-4A1EGTM-etal
FALLBACK_RUNNER_STATUS=online
FALLBACK_LONGPATH_FIX=JOB_ENV_CORE_LONGPATHS
FALLBACK_ROUTE_RETEST=PASS
FALLBACK_REALITY_RUN_ID=36917244551
FALLBACK_REALITY_ARTIFACT_ID=11189839827
MIN_TASK_ENTRY=workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

## 当前现实

### 主路：Desktop Commander Remote

已真实验证设备发现、Downloads/文件元数据读取、本地文件写入与回读、临时文件清理、本机命令/进程执行、Git 仓库读取。满足能力覆盖时，主路直接进入 Windows，不再先经过 GitHub。

完整进入条件、降级规则与健康检查见 `DUAL_ROUTE.md`。

### 备路：GitHub Actions + Windows self-hosted runner

Windows Reality 执行层已再次真实 PASS；当前使用用户登录计划任务常驻，runner 在线。Windows checkout 通过 job 环境强制注入 `core.longpaths=true`，不依赖临时 HOME、用户 Git 配置或管理员权限。

最新复验：Run `36917244551` = success；`windows-reality`、任务执行、artifact 上传全部成功；artifact ID `11189839827`。

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
