# R4 Candidate｜Windows 官方 Service 常驻化

状态：**仅候选，尚未 Reality 认证，不升级版本。**

## 目标

把已经通过临时 Reality 的 runner：

`C:\actions-runner-etal / DESKTOP-4A1EGTM-etal`

改成 GitHub 官方 Windows service 模式。

GitHub 官方要求：Windows runner 如果最初没有按 service 模式配置，需要先移除 runner，再重新运行 `config.cmd --runasservice`。

## 文件

- `bootstrap/Convert-GitHubSelfHostedRunnerToService.ps1`
- `bootstrap/Verify-GitHubSelfHostedRunnerService.ps1`

## 转换行为

```text
管理员 PowerShell
→ 停止临时 Runner.Listener
→ gh 请求短时 remove-token
→ config.cmd remove
→ gh 请求短时 registration-token
→ config.cmd --unattended ... --runasservice
→ 验证 Windows Service=Running
→ 验证 GitHub runner=online
```

token 不写入仓库、不写报告。

## 不做

- 不修改 FlClash
- 不修改系统代理
- 不使用 Scheduled Task
- 不使用 Startup/注册表 Run
- 不开始 Case 001

## Reality Gate

只有在真实目标 Windows 上得到：

```ini
SERVICE_STATUS=Running
SERVICE_START_MODE=Auto
RUNNER_STATUS=online
RUNNER_LABELS=self-hosted,Windows,X64
```

并随后完成新的自动 Reality task，才可把 persistence 标记为 PASS。

完整桥还必须另外验证 GPT 自动续跑；在此之前 `REALITY_CERTIFIED=NO`。
