---
name: extreme-time-automation-bridge
version: "0.1.1"
description: 极限短时间自动化闭环的无决策权执行桥。GPT负责判断，桥只负责领取、执行、记录、回传；正式任务运行期间用户人工介入必须为0。
---

# 极限短时间自动化执行桥 v0.1.1

```ini
STATUS=PARTIAL_REALITY
VERSION=0.1.1
REALITY_CERTIFIED=NO
STATIC_GATE=PASS
WINDOWS_REALITY=QUEUED_WAITING_SELF_HOSTED_RUNNER
REALITY_RUN_ID=36899361139

CORE_BRAIN=GPT
BRIDGE_DECISION_POWER=NONE
USER_INTERVENTION_DURING_TASK=0

TRANSPORT=GitHub
WINDOWS_EXECUTOR=GitHub_SELF_HOSTED_RUNNER
MIN_TASK_ENTRY=workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

## 已经实际完成

1. GitHub任务入口已建立。
2. GitHub Actions工作流已由真实提交触发。
3. PowerShell解析门禁已真实 PASS。
4. 任务JSON合同门禁已真实 PASS。
5. Windows Reality job 已进入 queued。
6. 首个 Reality 冒烟任务：ETAL-BRIDGE-SMOKE-001。

## 当前唯一现实缺口

尚无在线 Windows self-hosted runner 领取 Reality job，因此不得宣布执行桥 Reality PASS。

当前不是“方案未知”，而是：

```text
仓库侧任务总线 PASS
→ 等待一次性接入 Windows runner
→ 自动领取已经排队的冒烟任务
→ 产出机器证据
```

## 架构

```text
GPT
→ GitHub任务JSON
→ GitHub Actions
→ Windows self-hosted runner
→ 受版本控制payload
→ result/stdout/stderr/artifact
→ 可选回调
```

执行桥没有方案决策权；失败必须原样回传。

## 安全与权限边界

- 不修改 FlClash / Windows 网络代理。
- 不执行 Windows 系统破坏性动作。
- payload 只允许来自固定 bridge/payloads 目录。
- 执行器带基础 fail-closed 字符串门禁。
- 推荐 runner 在专用普通用户上下文运行；需要桌面/剪贴板时优先交互用户会话，不默认使用 session 0 服务。

## 计时

首次桥建设单独记录为 T_PLATFORM_BOOTSTRAP。
Case 001 只有在桥 Reality PASS 后才正式起表；这样不会把“临时修基础设施”伪装成标准题路径时间，也不会把其成本丢掉。

## 当前下一步

执行 `bootstrap/Install-GitHubSelfHostedRunner.ps1` 在目标 Windows 上完成一次性 runner 接入。
脚本优先尝试复用已登录的 GitHub CLI 自动获取短时注册令牌；否则接受显式 RegistrationToken。
