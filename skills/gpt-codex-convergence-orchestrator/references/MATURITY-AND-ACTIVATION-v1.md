# GPT-Codex Convergence Orchestrator — 成熟度与唤醒规则 v1

## 1. 定位

本技能是 `first-principles-physical-limit-convergence` 的可选执行控制层。

它的价值不是替代 GPT 或 Codex，而是把人工搬运：

```text
GPT -> 人复制 -> Codex
Codex -> 人复制 -> GPT
```

变成可恢复、可审计、幂等的自动控制面。

它也必须服从第一性原理时间目标：如果自动化开销高于人工搬运收益，就不应唤醒。

## 2. 成熟度阶梯

禁止跳级：

```text
L0 SPEC_READY
-> L1 SHADOW_PILOT_PASS
-> L2 ASSISTED_REAL_TASK_PASS
-> L3 MULTI_SCENARIO_REGRESSION_PASS
-> L4 MATURE_REUSABLE
```

### L0 SPEC_READY

架构、编号总线、GitHub事实源、Codex-first状态机、权限边界、幂等、checkpoint、capacity router 已设计。

当前正式状态即为 L0。

### L1 SHADOW_PILOT_PASS

在 toy task 上完整真实运行：

```text
Codex主动发REQUEST
-> Browser唤醒GPT
-> GPT直接写GitHub COMMAND
-> Codex监仓执行
-> Codex写RESULT
-> Browser再次唤醒GPT
-> GPT写FREEZE/BLOCKED
-> Codex收口
```

必须：

```text
MANUAL_COPY_PASTE_REQUIRED=NO
NO_FREE_EXPLORATION=YES
NO_REPLAY=YES
GITHUB_REMOTE_TRUTH=YES
```

### L2 ASSISTED_REAL_TASK_PASS

选择一个低风险、真实、可回滚任务，完整运行多轮 GPT↔Codex 闭环。

用户只允许：

```text
START
STOP/PAUSE
APPROVE_SENSITIVE_ACTION
CHANGE_TASK_CONTRACT
```

普通 transport 不再人工搬运。

### L3 MULTI_SCENARIO_REGRESSION_PASS

至少覆盖：

- 单轮任务；
- 多轮任务；
- PASS/FAIL/ROLLBACK；
- Browser掉线；
- capacity；
- Windows/Orchestrator重启；
- duplicate poll/wakeup；
- Git冲突；
- unknown exception；
- user STOP；
- Codex越权诱导测试。

所有情况必须保持：

```text
CODEX_PLAN_AUTHORITY=NONE
LOCAL_WORK_REPLAY=NO
```

### L4 MATURE_REUSABLE

只有 L1-L3 都有真实证据后才允许：

```text
AUTOMATION_MODULE=MATURE_REUSABLE
```

此时才可被其他技能包作为成熟依赖唤醒。

## 3. 唤醒条件

只有 L4 后才允许自动/默认建议唤醒。

适合唤醒：

```text
预计 GPT<->Codex >= 2轮
长时间本地执行
需要 checkpoint/resume
需要多阶段命令包 + GPT裁决
人工复制粘贴已成为显著时间成本
跨会话/跨页面长任务
```

不适合默认唤醒：

```text
一次性短命令
单轮即可完成
高频人工视觉判断
TASK_CONTRACT 尚未冻结
敏感操作需要持续人工批准
```

## 4. Codex 权限固定

无论成熟度到哪一级：

```text
NO_FREE_EXPLORATION=YES
CODEX_PLAN_AUTHORITY=NONE
BOUNDED_EXECUTION_FLEXIBILITY=YES
WHAT_TO_DO_NEXT=GPT_ONLY
```

达到 L4 只表示 transport/control plane 成熟，不增加 Codex 的规划权。

## 5. 当前状态

```text
AUTOMATION_MATURITY=L0_SPEC_READY
SHADOW_PILOT=NOT_YET_EXECUTED
ASSISTED_REAL_TASK=NOT_YET_EXECUTED
MULTI_SCENARIO_REGRESSION=NOT_YET_EXECUTED
MATURE_REUSABLE=NO
```
