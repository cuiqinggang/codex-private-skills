# 极限短时间自动化闭环 v2.0｜当前接续摘要

```ini
PAGE_NAME=极限短时间自动化闭环 v2.0
PROJECT_VERSION=v2.0

STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION=极限短时间智能体宪法 v0.3
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1

OBJECTIVE=T*=min(T_VALID)
USER_INTERVENTIONS=0

EXECUTION_BRIDGE=极限短时间自动化执行桥 v0.1.3
BRIDGE_STATUS=PARTIAL_REALITY
BRIDGE_REALITY_CERTIFIED=NO
STATIC_VALIDATION_RUN_ID=36900593142
WINDOWS_SMOKE_RUN_ID=36899361139
```

## 当前正式目标

T_VALID 是从原始现实需求被候选系统接受，到成熟版完成并通过真实最终验收的全部现实时间。

必须计入：需求理解、成熟方案搜索/比较、组合、执行、等待、失败、根因分析、换路/修复、重试、自动验收。

正式任务一旦开始：

```text
USER_INTERVENTIONS=0
```

若需要用户复制命令、转述结果、决定下一步或人工补验收，则该路径无有效 T_VALID。

## 路径A

```text
GPT判断
→ 无决策权执行桥
→ Windows Reality
→ 自动记录/验证/回传
→ GPT继续判断
→ 循环
→ FINAL_VALID
```

角色固定：
- GPT：唯一决策大脑。
- 执行桥：领取、执行、记录、回传；无方案决策权。
- Windows：Reality 环境。
- GitHub：任务、版本、证据总线。

Codex、Manus 不参与路径A。

## 当前执行桥

技能包：

```text
skills/extreme-time-automation-bridge/
VERSION=0.1.3
```

最小任务入口：

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

已完成：
- GitHub任务入口；
- GitHub Actions工作流；
- Windows PowerShell无决策执行器；
- result/stdout/stderr结构；
- artifact回传；
- 可选上层 callback；
- 安全 smoke；
- Windows self-hosted runner bootstrap。

首次仓库侧 Reality：
- Run 36899361139；
- contract-static PASS；
- windows-reality queued；
- Windows runner pickup NO。

v0.1.3 调度修复 Reality：
- Commit 4ede02697a647c34e89dd91551578c0b6e910673；
- Run 36900593142；
- contract-static PASS；
- windows-reality skipped expected；
- 证明离线 Windows runner 不再阻塞静态门禁。

## 当前唯一第一优先级

不要开始标准题001计时。

先完成：

```text
目标 Windows self-hosted runner 在线
→ ETAL-BRIDGE-SMOKE-001 被领取
→ payload执行
→ result.json
→ artifact
→ PASS
```

然后验证：

```text
Windows结果
→ 自动回调/调度
→ GPT自动继续下一轮
```

只有整个循环在 `USER_INTERVENTIONS=0` 下成立，执行桥才升级 Reality PASS。

首次平台建设时间单列为 `T_PLATFORM_BOOTSTRAP`；成熟基础设施复用后不重复计入每个标准题 T_VALID。
