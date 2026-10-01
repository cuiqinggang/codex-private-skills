# Reality R1｜执行桥第一次真实触发

```ini
VERSION=0.1.1
SOURCE_COMMIT=5f0451d96ee25850b0de2348b588ec55414e766e
WORKFLOW_RUN_ID=36899361139
WORKFLOW=Extreme Time Windows Autonomous Bridge

CONTRACT_STATIC=PASS
POWERSHELL_PARSE=PASS
TASK_CONTRACT=PASS

WINDOWS_REALITY_JOB=QUEUED
WINDOWS_RUNNER_PICKUP=NO
BRIDGE_REALITY_CERTIFIED=NO
ROOT_CAUSE=NO_ONLINE_MATCHING_SELF_HOSTED_WINDOWS_RUNNER
```

## 判断

仓库侧“任务文件 → 工作流触发 → 合同检查”已经 Reality 通过。
当前不能继续把问题描述成“桥还只是设计”：它已经有一半真实链路。

未通过的是最后的物理连接：
GitHub 当前找不到可领取 `[self-hosted, Windows, X64]` job 的在线 runner。

## 处理

采用 GitHub 官方 self-hosted runner，不自研代理。
目标 Windows 一次性注册后，当前已 queued 的 ETAL-BRIDGE-SMOKE-001 应被自动领取；无需重新设计任务协议。

## 验收

只有以下链路真实完成才升级 Reality：

```text
queued
→ Windows领取
→ payload执行
→ result.json
→ artifact
→ PASS
```
