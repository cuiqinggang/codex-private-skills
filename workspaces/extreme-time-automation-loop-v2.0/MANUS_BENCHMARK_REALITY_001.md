# Manus 2.0 Benchmark Reality｜极限短时间自动化闭环 v2.0

```ini
TASK_ID=ETAL-v2.0-BENCHMARK-MANUS-001
ROLE=PAID_REFERENCE_ONLY
PRODUCTION_CANDIDATE=NO
USE_EXISTING_CREDITS_ONLY=YES
OBJECTIVE=MEASURE_T_REF_MANUS
```

## 目的

用现有 Manus 积分测出一个成熟商业整解的现实端到端参考：

```text
T_REF_MANUS
```

Manus 只作为 Benchmark，不进入正式生产主链。

## 同一真实任务

> 从共同私库恢复“极限短时间自动化闭环 v2.0”的当前状态，读取当前 R3 GPT CORE Reality Contract，核验当前官方事实，形成 Reality 结果，写回 GitHub main，并远端回读验证。

## 必须读取

- `00_START_HERE/COMMON-ENTRY.md`
- `skills/extreme-time-agent-constitution/SKILL.md`
- `workspaces/extreme-time-automation-loop-v2.0/README.md`
- `workspaces/extreme-time-automation-loop-v2.0/REALITY_CONTRACT.md`
- `workspaces/extreme-time-automation-loop-v2.0/MATURE_SOLUTION_COMPETITION_R3_GPT_CORE.md`

## 输出

写入：

`workspaces/extreme-time-automation-loop-v2.0/reality/MANUS-BENCHMARK-001.md`

至少记录：

```ini
TASK_ID=ETAL-v2.0-BENCHMARK-MANUS-001
FLOW_START=
FLOW_END=
T_REF_MANUS=
RESULT=PASS|FAIL
USER_INTERVENTIONS=
RECOVERY_EVENTS=
FALSE_COMPLETION_EVENTS=
CREDITS_CONSUMED=
```

## FINAL_VALID

- 目标文件真实存在于 GitHub main；
- 写后必须重新从远端读取；
- 不允许用户搬运中间信息；
- 普通失败由 Manus 自己恢复；
- 所有人工介入、失败、等待和 credits 如实记录；
- 不以 Manus 自报 Done 代替现实验证。
