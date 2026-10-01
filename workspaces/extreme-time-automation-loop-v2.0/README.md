# 极限短时间自动化闭环 v2.0

```ini
PROJECT=极限短时间自动化闭环
VERSION=v2.0
PAGE_NAME=极限短时间自动化闭环 v2.0

STATE=10
PHASE=AUTONOMOUS_BRIDGE_REALITY_CONNECT
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION_VERSION=v0.3
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1

OBJECTIVE=T*=min(T_VALID)
USER_INTERVENTIONS=0

CORE_BRAIN=GPT
EXECUTION_BRIDGE=extreme-time-automation-bridge-v0.1.3
BRIDGE_DECISION_POWER=NONE
BRIDGE_REALITY_CERTIFIED=NO
```

## 1. 唯一目标

```text
T* = min(T_VALID)
```

T_VALID 指：从原始现实需求进入候选系统，到成熟版完成并通过真实最终验收的全部现实时间。

正式任务运行后必须无人值守：

```text
USER_INTERVENTIONS=0
```

需要用户做人肉中继的路径直接无效。

## 2. 当前路径A

```text
GPT唯一决策
→ 无决策权执行桥
→ Windows Reality
→ 自动证据/回传
→ GPT继续判断
→ ...
→ FINAL_VALID
```

执行桥不得选择技术路线、改目标、判断根因、自动修方案或宣布 FINAL_VALID。

## 3. 当前执行桥

```text
skills/extreme-time-automation-bridge/
VERSION=0.1.3
STATUS=PARTIAL_REALITY
```

任务入口：

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

已验证：
- Run 36899361139：仓库侧合同门禁 PASS，Windows job 因无在线 self-hosted runner 排队。
- Run 36900593142：v0.1.3 静态调度隔离 PASS；非任务提交正确跳过 Windows Reality。

## 4. 当前阻塞

第一阻塞：目标 Windows 尚未接成匹配 `[self-hosted, Windows, X64]` 的在线 runner。

第二阻塞：`ETAL_BRIDGE_CALLBACK_URL` 所代表的“结果回来后自动唤醒 GPT”还未 Reality 打通。

## 5. 下一步

当前不要启动标准题001正式 T_VALID。

先完成：

```text
Windows runner 接通
→ ETAL-BRIDGE-SMOKE-001 真执行
→ result.json
→ artifact
→ PASS
→ 自动回调 GPT
→ GPT自动继续下一轮
```

整个桥连续满足 `USER_INTERVENTIONS=0` 后，才升级桥 Reality PASS，再启动标准题001完整生命周期 Reality。

首次桥建设时间单列 `T_PLATFORM_BOOTSTRAP`。
