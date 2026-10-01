# v2.0 无人执行桥

```ini
BRIDGE_SKILL_VERSION=0.1.2
STATIC_GATE=PASS
REALITY_RUN_ID=36899361139
WINDOWS_REALITY=QUEUED_WAITING_SELF_HOSTED_RUNNER
```

## 最小任务入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

新任务 JSON 进入 main 后，工作流先做静态门禁；只有发现恰好一个任务 JSON 发生变化，才调度本地 Windows。

## 当前已走通

```text
任务JSON提交
→ GitHub workflow触发
→ PowerShell解析 PASS
→ 任务合同 PASS
→ Windows Reality queued
```

当前唯一缺口：
目标 Windows 尚无在线 [self-hosted, Windows, X64] runner。

## 一次性接入

```text
skills/extreme-time-automation-bridge/bootstrap/Install-GitHubSelfHostedRunner.ps1
```

安装后当前已排队的 ETAL-BRIDGE-SMOKE-001 可以直接被领取，不需要重新设计桥。

## 非任务提交

v0.1.2 起，技能包/文档/执行器更新只做 hosted 静态检查，不再制造本地 runner 队列。
