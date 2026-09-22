# 极限短时间引擎 v4.5.3：活动时间运行协议

## 目的

把唯一锚定物 `T*=min(T_VALID_ACTIVE_GLOBAL)` 变成每轮都可见、可核验、可优化的工程记录。

## 每轮开始必须显示

```text
TASK_TIME_ID=<任务编号>
PROBLEM_ENTRY_NETWORK_TIMESTAMP=<任务最初进入时间>
SEGMENT_ID=<本轮有效工作段>
SEGMENT_START=<本轮开始网络时间>
ACTIVE_TOTAL_BEFORE=<本轮开始前累计有效智能体时间>
PHASE=VIRTUAL|REAL
STATUS=<当前状态>
OBJECTIVE=min(T_VALID_ACTIVE_GLOBAL)
```

## 每轮结束必须显示

```text
SEGMENT_END=<本轮结束网络时间>
SEGMENT_ACTIVE=<本轮有效工作时长>
ACTIVE_TOTAL_AFTER=<累计有效智能体时间>
PHASE=<虚/实>
STEP_RESULT=PASS|PARTIAL|FAIL
BOTTLENECK=<本轮瓶颈或 NONE>
NEXT_ACTION=<下一唯一动作>
```

若任务最终有效解决：

```text
FINAL_VALID=YES
FINAL_VALID_NETWORK_TIMESTAMP=<网络时间>
GLOBAL_TIMER_STATE=STOPPED
T_VALID_ACTIVE_GLOBAL=<最终累计有效智能体时间>
```

## 计时规则

1. GPT、Codex 及其直接执行工具真正解决问题的时间计入。
2. 用户离开、休息、现实事务造成的空档不计入。
3. 失败诊断、回虚、修正、重跑只要智能体在工作，全部计入。
4. 失败或换方案不得重置任务累计时间。
5. GPT/Codex 串行时可近似相加；并行时主时间取有效工作区间并集，重叠只计一次。
6. 局部时间仅用于定位瓶颈，不得替代全局唯一锚定物。
7. 每个阶段必须有明确开始与结束检查点，禁止存在“做过但未记时”的有效工作段。
8. 网络时间用于锚定每个时间段的开始/结束边界；不把人类空档直接算进主锚定时间。

## 当前任务结构：只有一虚一实

```text
TASK_TIME_ID=ESTE-20260922-001

PHASE=VIRTUAL
- 在这一阶段内部一次性完成：现实信息读取、方案成熟、执行链闭合、外部依赖闭合、冻结产物与冻结验收。
- 这些都是 VIRTUAL 内部动作/检查点，不是新的步骤，不编号 V1/V2/V3。
- 只有当全部虚完成条件同时 PASS，才发生唯一状态转换：

VIRTUAL -> REAL

PHASE=REAL
- 严格执行冻结方案并做最终现实验收。
- 这些都是 REAL 内部动作/检查点，不编号 R1/R2/R3。
- PASS：FINAL_VALID=YES，停表。
- FAIL：记录最小 Reality Delta，然后：

REAL -> VIRTUAL

累计有效时间继续，不重置。
```

检查点允许记录时间和瓶颈，但：
```text
CHECKPOINT_IS_METHOD_STEP=NO
NUMBERED_VIRTUAL_SUBSTEPS=FORBIDDEN
NUMBERED_REAL_SUBSTEPS=FORBIDDEN
```

## 极限短时间约束

每一步是否存在，只按这一问决定：

```text
它是否使预期 T_VALID_ACTIVE_GLOBAL 更短？
```

- 能避免高代价返工且检查成本更低：保留。
- 不能降低总有效工作时间：删除。
- 不确定：只做最小必要验证，禁止无限增加门禁。
