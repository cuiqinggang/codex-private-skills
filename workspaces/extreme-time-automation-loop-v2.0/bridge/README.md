# v2.0 无人执行桥

```ini
BRIDGE_SKILL_VERSION=0.1.1
STATIC_GATE=PASS
REALITY_RUN_ID=36899361139
WINDOWS_REALITY=QUEUED_WAITING_SELF_HOSTED_RUNNER
```

## 最小任务入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

新任务文件进入 main 后，`.github/workflows/extreme-time-windows-bridge.yml` 自动触发。

## 已实际验证

```text
任务文件提交
→ GitHub workflow触发
→ PowerShell解析 PASS
→ 任务JSON合同 PASS
→ Windows Reality job queued
```

当前卡点不是任务协议，而是还没有在线 `[self-hosted, Windows, X64]` runner。

## 一次性接入

使用：

```text
skills/extreme-time-automation-bridge/bootstrap/Install-GitHubSelfHostedRunner.ps1
```

它采用 GitHub 官方 runner，固定校验下载 SHA256，不修改网络代理。
默认跑在当前交互用户会话，并注册“登录时启动”的 Windows 计划任务。

## 首次 Reality

`ETAL-BRIDGE-SMOKE-001` 已经放入任务入口并处于 Reality 流程。
当 Windows runner 上线后，无需重新发 smoke；GitHub 会把排队 job 分配给匹配的在线 runner。

## 目录

```text
bridge/
├─ tasks/       # 最小任务入口
├─ payloads/    # GPT生成、Git版本控制的执行物
└─ runner/      # 无决策权执行器
```
