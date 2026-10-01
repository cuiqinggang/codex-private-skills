---
name: extreme-time-automation-bridge
version: "0.1.2"
description: 极限短时间自动化闭环的无决策权执行桥。GPT负责判断，桥只负责领取、执行、记录、回传；正式任务运行期间用户人工介入必须为0。
---

# 极限短时间自动化执行桥 v0.1.2

```ini
STATUS=PARTIAL_REALITY
VERSION=0.1.2
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

## 当前现实

首个任务 ETAL-BRIDGE-SMOKE-001 已真实触发工作流：
- PowerShell解析 PASS；
- 任务合同 PASS；
- Windows Reality job 已 queued；
- 当前唯一阻塞是目标 Windows 尚无在线 self-hosted runner。

## v0.1.2 修正

只有真正新增/修改任务 JSON 时才调度 self-hosted Windows。
技能包、说明文档、runner代码等普通更新只跑 GitHub-hosted 静态门禁，不再占用本地 runner 队列。

## 最小入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

任务 JSON 只引用同一 Git 提交中的 payload。桥不做方案判断。

## 安全与权限

- 不修改 FlClash / Windows 网络代理。
- 不执行 Windows 系统破坏性动作。
- payload 只能来自固定 payload 目录。
- 建议普通交互用户上下文运行，以保留桌面/用户配置能力。

## 一次性接入

`bootstrap/Install-GitHubSelfHostedRunner.ps1`
会使用 GitHub 官方 Actions Runner；优先复用参数/环境变量中的注册 token，否则尝试已登录 GitHub CLI 自动申请短时 token。

## 计时

桥的首次建设单列 T_PLATFORM_BOOTSTRAP。
标准题001只有在桥 Reality PASS 后才正式起表。
