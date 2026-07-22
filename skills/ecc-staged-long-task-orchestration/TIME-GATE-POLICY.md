# TIME-GATE-POLICY

## 总规则

时间规则不能一刀切。必须先声明任务模式：

```text
ENDURANCE_VALIDATION
PRODUCTION_WITH_TIME_BUDGET
```

## ENDURANCE_VALIDATION

用于验证长任务能力、防早停、checkpoint、恢复和持续执行能力。

### L4-2H

```text
minimum_elapsed_minutes >= 120
checkpoint_interval_minutes = 15
required_checkpoint_count_minimum >= 8
```

### L5-8H

```text
minimum_elapsed_minutes >= 480
checkpoint_interval_minutes = 30 或 60
required_checkpoint_count_minimum >= 8
```

硬规则：这种任务必须跑满最低时间。缺少 start_time、end_time、elapsed_minutes、checkpoint evidence 时不能 PASS。

## PRODUCTION_WITH_TIME_BUDGET

用于真实生产任务或 mature skill replay。

```text
time_budget_minutes = 120 或 480
finish_when_all_gates_pass = true
no_forced_waiting = true
```

硬规则：这种任务不强制耗满时间。如果 mature skill 让任务 30 分钟完成，并且所有 gates PASS，应立即结束。空转凑时间是失败行为。

## 禁止混用

- 只有 `ENDURANCE_VALIDATION` 才能使用 `minimum_elapsed_minutes`。
- `PRODUCTION_WITH_TIME_BUDGET` 不能为了凑时间空转。
- 使用 mature skill 提前完成是优点，不是失败。
