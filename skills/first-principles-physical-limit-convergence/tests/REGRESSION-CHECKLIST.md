# Regression Checklist — v2.0.0

## Core method

- [x] 主流程仍只有四步。
- [x] `NO_FREE_EXPLORATION=YES`。
- [x] Codex 仅有有限执行灵活性。
- [x] 新研究方向保持 `INDEPENDENT_99_PATH`。
- [x] 正常 PASS/FAIL/ROLLBACK 分支不要求逐步返回 GPT。

## Stochastic systems

- [x] 区分 `ATTEMPT` 与 `DELIVERY`。
- [x] 必须判断随机变量是否属于用户 TASK 语义。
- [x] 支持 GPT 预授权 `QC FAIL -> NEW RANDOM STATE -> RETRY SAME PATH`。
- [x] retry 不等于 Codex 自由探索。
- [x] 正式指标支持 `T_TFVR`。
- [x] 记录 first-attempt pass rate / attempts-to-success / invalid rejected / invalid delivered。
- [x] 不把 accepted 20/20 PASS 表述为未来随机过程数学上绝对终止。
- [x] exact-seed 任务禁止自动换种。

## Failure classification

- [x] control-plane failure 与 algorithm failure 分离。
- [x] execution-environment failure 与 random-attempt QC failure 分离。
- [x] source identity mismatch 不得伪装成候选失败。
- [x] capacity 错误不得重放已完成本地工作。

## Automation

- [x] GitHub 是 shared truth workspace。
- [x] GPT=planner/judge，Codex=deterministic executor。
- [x] 浏览器桥接只负责 transport。
- [x] checkpoint / DO_NOT_REPEAT / ACTION_ID 幂等规则存在。
- [x] capacity router 接口存在。
- [x] 用户保留 STOP / PAUSE / sensitive approval / task-contract change。

## H3-P0 real application

```text
H3_P0_DELIVERY_SYSTEM_99=YES
FINAL_ACCEPTED_QC=20/20
FIRST_ATTEMPT_PASS_RATE=90%
MEAN_ATTEMPTS_PER_TASK=1.10
T_TFVR_P50=6.076s
T_TFVR_P95=11.974s
INVALID_OUTPUT_DELIVERED=0
FINAL_99=YES
FREEZE=YES
```

## Non-regression assertions

```text
SIMPLE_FOUR_STEP_METHOD=PASS
NO_REAL_EXECUTION_REPLAN_LOOP=PASS
STOCHASTIC_VERIFIED_DELIVERY=PASS
AUTOMATION_DOES_NOT_TRANSFER_RESEARCH_AUTHORITY_TO_CODEX=PASS
H3_HISTORY_FAILURES_PRESERVED=YES
```
