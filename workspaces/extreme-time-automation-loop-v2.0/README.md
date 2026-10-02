# 极限短时间自动化闭环 v2.0

```ini
PROJECT=极限短时间自动化闭环
VERSION=v2.0
PAGE_NAME=极限短时间自动化闭环 v2.0

STATE=10
PHASE=PRIMARY_ROUTE_REALITY_AND_CONTINUITY
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION_VERSION=v0.3.1
CONSTITUTION_FREEZE_ID=ETAC-v0.3.1-FREEZE-R1

OBJECTIVE=T*=min(T_VALID)
USER_INTERVENTIONS_TARGET=0

PRIMARY_BRAIN_CANDIDATE=GPT
EXECUTION_BRIDGE=GPT直连Windows双路执行桥 v0.2.0
BRIDGE_DECISION_POWER=NONE
DIRECT_REMOTE_REALITY=PASS
GITHUB_RUNNER_REALITY=PASS
RUNNER_PERSISTENCE=USER_LOGON_SCHEDULED_TASK
BRIDGE_REALITY_CERTIFIED=NO
```

## 当前方法

v2.0 的目的不是“搭流程”，而是让现实任务以完整有效时间最短的方式完成。

默认参考链：

```text
用户现实目标
→ GPT / 当前最合适的高智能判断核心
→ 选择最短有效成熟工具或最小必要实现
→ 现实执行
→ 自动回传 / 验证
→ FINAL_VALID
```

GPT 当前是主脑首选候选，但具体工具、执行器和编排都可以由 Reality 替换。

## 已通过

### Windows 双路执行

1. Desktop Commander Remote 直连：已真实完成本地读取、写入、命令/进程执行。
2. GitHub Actions + Windows self-hosted runner：最新 Reality Run `36917244551` 成功，artifact ID `11189839827`。
3. runner 已通过 `ETAL-GitHub-Actions-Runner` 用户登录计划任务持久化并曾验证 online。

## 当前仍未完成

- Desktop Commander Remote 本机进程长期自动常驻的最新 Reality；
- GPT 页面 / 上下文过长时自动 Checkpoint 与换页恢复；
- Windows 结果触发 GPT 后自动继续下一判断；
- GPT 自动形成下一任务并再次现实执行；
- GPT 服务本身不可用时的独立强备份。

因此项目仍：
`VIRTUAL_MATURE=NO`、`BRIDGE_REALITY_CERTIFIED=NO`。

## 与旧 v5.6.5 的关系

v5.6.5 保留为历史成熟参照和故障经验来源。

当前正式推进方法是 v2.0；不因为历史规则存在就强制复制旧格式。任何旧机制只有在 Reality 证明能改善完整 T_VALID 时才继续保留。
