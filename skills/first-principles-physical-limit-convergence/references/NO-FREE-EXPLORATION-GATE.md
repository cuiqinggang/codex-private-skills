# NO-FREE-EXPLORATION-GATE

版本：v1.7.0

本文件是 `first-principles-physical-limit-convergence` 在项目方法层级中的最高优先级执行门禁之一；它不能被普通任务命令弱化。更高层级的系统、安全和平台规则仍然优先。

## 1. 角色冻结

```text
GPT / 高质量推理层
= 设计者、候选选择者、验证铁路制定者、结果裁决者、停止条件制定者

Codex / 本地执行器
= DETERMINISTIC_VALIDATOR_EXECUTOR
```

Codex 不拥有独立实验设计权。

## 2. Codex 永久禁止自行决定

```text
DESIGN_NEW_TEST=NO
ADD_NEW_CANDIDATE=NO
CHANGE_CANDIDATE_ORDER=NO
EXTEND_RUN_COUNT=NO
START_PROFILER=NO
START_PARAMETER_SEARCH=NO
START_VERSION_SWEEP=NO
START_KERNEL_EXPLORATION=NO
START_QUANTIZATION_SWEEP=NO
START_CACHE_OR_PREFETCH_EXPLORATION=NO
DERIVE_AND_RUN_NEXT_EXPERIMENT=NO
```

这些动作只有在 GPT 已经把它们写入完整验证铁路时才可以成为允许步骤。

## 3. 每个验证铁路必须完整

至少包括：

- objective；
- current state / baseline；
- exact allowed change；
- allowed files/components；
- seeds and run count；
- timing boundary；
- QC gate；
- bounded projected result；
- PASS / FAIL / INCONCLUSIVE 规则；
- rollback；
- stop point；
- maximum GPU runs；
- time budget；
- Codex budget；
- 每一种预定义结果之后的动作。

缺项：

```text
VALIDATION_PLAN_NOT_MATURE=YES
→ STOP
→ RETURN_TO_GPT
```

## 4. 结果处理

只有铁路内预定义的分支可以自动执行。

```text
EXPECTED_PASS
→ predefined KEEP/next stop action

EXPECTED_FAIL
→ predefined ROLLBACK/stop action

PREDEFINED_INCONCLUSIVE
→ predefined stop action

UNEXPECTED_RESULT
→ SAVE EVIDENCE
→ SAFE STOP / predefined restore
→ RETURN_TO_GPT
```

绝不允许：

```text
结果异常
→ Codex猜原因
→ 顺手profile
→ 修改参数
→ 再跑
```

## 5. 预算

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
```

若等待审批、网络、Git、启动、模型加载或其他事件使时间明显超过预算，而铁路没有明确允许继续：保存状态并停止；不得把“已经花了很多时间”当成继续探索的理由。

## 6. 命令冲突

任务命令可以增加更严格限制，但不能允许技能明确禁止的自由探索。

```text
COMMAND_CONFLICT_WITH_NO_FREE_EXPLORATION=YES
→ SKILL_RULE_WINS_WITHIN_PROJECT
→ DO_NOT_EXECUTE_UNSPECIFIED_ACTION
→ REPORT CONFLICT
→ RETURN_TO_GPT
```

## 7. 恢复

AI/Codex会话断线不等于本地实验失败。恢复后只允许按照既有铁路检查 PID、listener、heartbeat、result、summary、restore proof 等预定义状态。若既有实验完整，直接收口；若状态未被铁路覆盖，返回 GPT，不发明恢复实验。

## 8. 验收句

任何执行任务开头都应能回答：

```text
SKILL_VERSION_VERIFIED=YES
NO_FREE_EXPLORATION=YES
GPT_COMPLETE_VALIDATION_RAILROAD_PRESENT=YES
CURRENT_STEP_EXPLICITLY_AUTHORIZED=YES
```

任何一项不是 YES：不开始新的 GPU/性能实验。
