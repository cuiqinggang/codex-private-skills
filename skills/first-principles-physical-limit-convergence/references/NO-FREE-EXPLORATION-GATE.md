# NO-FREE-EXPLORATION-GATE

当前技能版本：v1.9.0  
核心禁止自由探索行为由 v1.7.0 建立；v1.8.0 增加 canonical identity gate；v1.9.0 增加预授权批次连续执行，消除“每步都回 GPT”的微循环，同时不放松任何实验设计权限。

开始本门禁前必须满足：

```text
CANONICAL_IDENTITY_GATE=PASS
SKILL_ID=first-principles-physical-limit-convergence
SKILL_VERSION=1.9.0
```

## 1. 角色冻结

```text
GPT / 高质量推理层
= 设计者、候选选择者、批次铁路制定者、重规划裁决者、停止条件制定者

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
DERIVE_NEW_EXPERIMENT=NO
```

只有 GPT 已经写入完整 batch railroad 的步骤才可执行。

## 3. 每个验证 stage 必须完整

至少包括：

- objective；
- current state / baseline rule；
- exact allowed change；
- allowed files/components；
- seeds and run count；
- timing boundary；
- QC gate；
- bounded projected result；
- PASS / FAIL / NOT_APPLICABLE / INCONCLUSIVE；
- rollback；
- maximum GPU runs；
- time budget；
- NEXT_ON_PASS / NEXT_ON_FAIL / NEXT_ON_NOT_APPLICABLE / NEXT_ON_INCONCLUSIVE。

整个 batch 还必须有 global GPU/wall budget、batch stop point 和 final return-to-GPT point。

缺项：

```text
VALIDATION_PLAN_NOT_MATURE=YES
-> DO NOT START THAT STAGE
```

## 4. 结果处理

只有铁路内预定义分支可以自动执行。

```text
EXPECTED_PASS
-> predefined KEEP
-> NEXT_ON_PASS

EXPECTED_FAIL
-> predefined ROLLBACK
-> NEXT_ON_FAIL

EXPECTED_NOT_APPLICABLE
-> NEXT_ON_NOT_APPLICABLE

PREDEFINED_INCONCLUSIVE
-> follow explicitly predefined action; default is STOP/RETURN GPT

UNEXPECTED_RESULT
-> SAVE EVIDENCE
-> SAFE STOP / predefined restore
-> RETURN_TO_GPT
```

当 PASS/FAIL/NOT_APPLICABLE 完全落入预定义分支时，Codex **可以继续当前批次下一 stage**，不需要每一步重新授权。

## 5. 不允许因收益幅度惊讶而重规划

```text
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
```

以下本身不构成重规划触发器：

- 实际收益远大于预测；
- 实际收益小于预测但仍满足 PASS；
- 预定义 FAIL；
- 预定义 ROLLBACK；
- 预定义 NOT_APPLICABLE。

只要后续铁路条件仍有效，就继续 batch。

## 6. MATERIAL_REPLAN_TRIGGER

只有以下情况必须提前回 GPT：

1. 铁路没有定义的结果/异常；
2. correctness / quality / stability / safety 失效；
3. task contract、硬件、关键软件或模型身份出现未授权变化；
4. 下一 stage 的关键前提被真实结果推翻且无预定义 fallback；
5. control window 失稳；
6. batch 全局预算耗尽；
7. Git/远端事实冲突；
8. 继续执行将越过 allowed-change 边界。

处理：

```text
SAVE EVIDENCE
SAFE STOP / RESTORE
PUSH / REMOTE VERIFY WHEN APPROPRIATE
RETURN_TO_GPT
```

## 7. 禁止开放式 preflight 链

```text
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

已经进入 Virtual-99 mature matrix 的候选，不允许执行期无限拆成：

```text
PREFLIGHT-A -> GPT -> PREFLIGHT-B -> GPT -> PREFLIGHT-C -> ...
```

必须在 Virtual 阶段一次性设计有限 preflight，或把实际 load/compatibility failure 直接定义为 bounded A/B 的 FAIL/NOT_APPLICABLE。

## 8. 预算

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
```

若超过 batch 预算且铁路未定义继续条件：保存状态、安全停止、返回 GPT。

## 9. 命令冲突

任务命令可以增加更严格限制，但不能允许技能明确禁止的自由探索。

```text
COMMAND_CONFLICT_WITH_NO_FREE_EXPLORATION=YES
-> SKILL_RULE_WINS_WITHIN_PROJECT
-> DO_NOT_EXECUTE_UNSPECIFIED_ACTION
-> REPORT CONFLICT
-> RETURN_TO_GPT
```

## 10. 恢复

AI/Codex会话断线不等于本地实验失败。恢复后只允许按照既有 batch railroad 检查 PID、listener、heartbeat、result、summary、restore proof。若状态仍落在预定义分支，继续该 batch；否则返回 GPT。

## 11. 验收句

```text
CANONICAL_IDENTITY_GATE=PASS
SKILL_VERSION_VERIFIED=YES
NO_FREE_EXPLORATION=YES
GPT_COMPLETE_BATCH_RAILROAD_PRESENT=YES
CURRENT_STAGE_PREAUTHORIZED=YES
PREAUTHORIZED_BATCH_EXECUTION=YES
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

任何一项不是 YES：不开始新的 GPU/性能实验。
