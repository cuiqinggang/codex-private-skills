# 极限短时间引擎 v4.5.2：活动时间运行协议

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

## 当前任务最短闭环

```text
TASK_TIME_ID=ESTE-20260922-001

VIRTUAL
V1 活动时间协议冻结
V2 冻结现实执行包，移除非必要 GitHub 实时单点依赖
V3 冻结闭环验证器 PASS
V4 VIRTUAL_COMPLETE 检查点

REAL
R1 按冻结执行包现实运行
R2 FAIL -> Reality Delta -> 回 VIRTUAL，主累计时间不重置
R3 PASS -> GPT 按 FINAL_VALID_CONDITION 最终验收
R4 FINAL_VALID=YES -> 停表 -> 输出最终时间与瓶颈统计
```

## 极限短时间约束

每一步是否存在，只按这一问决定：

```text
它是否使预期 T_VALID_ACTIVE_GLOBAL 更短？
```

- 能避免高代价返工且检查成本更低：保留。
- 不能降低总有效工作时间：删除。
- 不确定：只做最小必要验证，禁止无限增加门禁。
