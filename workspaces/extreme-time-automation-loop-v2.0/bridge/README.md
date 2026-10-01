# v2.0 无人执行桥

## 最小任务入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

新任务文件进入 main 后，`.github/workflows/extreme-time-windows-bridge.yml` 自动触发。

## 目录

```text
bridge/
├─ tasks/       # 任务入口，只放JSON
├─ payloads/    # GPT生成、Git版本控制的PowerShell执行物
└─ runner/      # 无决策权执行器
```

## 首次Reality

`ETAL-BRIDGE-SMOKE-001` 只做安全的临时目录写入和环境回报，不改系统、不改代理。

若 workflow 的静态检查 PASS 但 self-hosted job 长时间排队，说明仓库侧已经接通，但 Windows 自托管 runner 尚未在线/注册；此时不能宣称桥 Reality PASS。

## Windows runner

Reality job 使用：

```text
[self-hosted, Windows, X64]
```

这是基础设施一次性安装项，不属于每个标准题的人工作业步骤。
