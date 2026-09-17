# PREAUTHORIZED BATCH RAILROAD — v1.9.0

本规则解决 v1.8.0 暴露出的一个收敛效率缺陷：已经由 GPT 在 Virtual-99 阶段完整设计好的条件铁路，不应被强制拆成“执行一步→返回 GPT→再授权一步”的微循环。

## 1. 核心原则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
PREAUTHORIZED_BATCH_EXECUTION=YES
MICRO_REPLAN_LOOP=NO
```

“批次连续执行”不等于 Codex 获得实验设计权。只有 GPT 事先写入批次铁路的候选、顺序、条件分支、预算和停止规则可以执行。

## 2. 批次铁路必须提前完整

每个 batch 至少定义：

```text
BATCH_ID
BATCH_ENTRY_STATE
PREAUTHORIZED_STAGES[]
FOR_EACH_STAGE:
  OBJECTIVE
  BASELINE_RULE
  EXACT_ALLOWED_CHANGE
  ALLOWED_FILES_OR_COMPONENTS
  SEEDS_AND_RUN_COUNT
  TIMING_BOUNDARY
  QC_GATE
  PASS_RULE
  FAIL_RULE
  NOT_APPLICABLE_RULE
  INCONCLUSIVE_RULE
  ROLLBACK
  NEXT_ON_PASS
  NEXT_ON_FAIL
  NEXT_ON_NOT_APPLICABLE
  NEXT_ON_INCONCLUSIVE
  MAX_GPU_RUNS
  TIME_BUDGET
BATCH_GLOBAL_GPU_BUDGET
BATCH_GLOBAL_WALL_BUDGET
BATCH_STOP_POINT
FINAL_RETURN_TO_GPT_POINT
```

缺关键字段则整个相关 stage 不成熟，不得由 Codex补齐。

## 3. 允许自动继续的结果

当结果完全落入预定义分支时：

```text
EXPECTED_PASS          -> execute NEXT_ON_PASS
EXPECTED_FAIL          -> rollback as predefined -> execute NEXT_ON_FAIL
EXPECTED_NOT_APPLICABLE-> execute NEXT_ON_NOT_APPLICABLE
```

不要求每个 stage 都返回 GPT。

## 4. 必须返回 GPT 的情况

只有以下情况触发 `MATERIAL_REPLAN_TRIGGER=YES`：

1. 出现铁路没有定义的结果或错误；
2. correctness / quality / stability / safety 合同失效；
3. task contract、硬件边界、关键软件身份或模型身份发生未授权变化；
4. 下一阶段依赖的前提被真实结果推翻，且铁路没有预定义替代分支；
5. 控制组失稳导致 A/B 无法裁决；
6. 达到 batch 全局 GPU / wall-time 预算；
7. Git / 远端事实冲突使当前 batch 基线不再可信。

随后：

```text
SAVE EVIDENCE
SAFE STOP / RESTORE
PUSH IF APPROPRIATE
REMOTE VERIFY
RETURN_TO_GPT
```

## 5. 不应触发重规划的情况

只要后续分支仍然成立，以下情况**不单独触发**重新 Virtual-99：

```text
GAIN_LARGER_THAN_PROJECTED
GAIN_SMALLER_THAN_PROJECTED_BUT_PASS
EXPECTED_FAIL
EXPECTED_NOT_APPLICABLE
EXPECTED_ROLLBACK
```

尤其：

```text
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
```

“比预期快很多”不是开启新研究链的授权。

## 6. 禁止微型预检链

```text
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

同一个候选如果在 Virtual-99 阶段已经被选为值得做 bounded real A/B，则执行阶段不得因为兼容性未知无限拆成：

```text
PREFLIGHT-A -> GPT -> PREFLIGHT-B -> GPT -> PREFLIGHT-C -> ...
```

正确做法只有两种：

A. Virtual-99 阶段一次性把必要的有限 preflight chain 写完整；或
B. 直接在 bounded A/B stage 内把“加载失败/格式不兼容/机制未激活”作为预定义 FAIL/NOT_APPLICABLE，安全回滚并结束该候选。

## 7. 何时做 Residual Virtual Convergence

Residual Virtual Convergence 在**批次边界**执行，而不是每个正常 stage 后执行：

```text
PREAUTHORIZED_BATCH_COMPLETE
-> RETURN_TO_GPT
-> RESIDUAL_VIRTUAL_CONVERGENCE
-> NEXT_BATCH or FINAL_CERTIFICATION
```

若 batch 内出现 MATERIAL_REPLAN_TRIGGER，可提前返回 GPT。

## 8. ROI 与停止

评估的是组合生命周期收益，而不是为了理论完整性无限追小收益：

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO > TOTAL_VALIDATION_AND_INTEGRATION_COST
```

候选若剩余可消灭时间很小、风险高、需要软件版本迁移或会开启长研究链，可直接判：

```text
PORTFOLIO_ROI_NEGATIVE_OR_INSUFFICIENT
-> EXHAUSTED / DEFERRED
```

无需为了“把所有候选都测一遍”继续。

## 9. 验收语句

```text
PREAUTHORIZED_BATCH_EXECUTION_DEFINED=PASS
NO_FREE_EXPLORATION_PRESERVED=PASS
NO_REPLAN_ON_MAGNITUDE_SURPRISE=PASS
NO_OPEN_ENDED_PREFLIGHT_CHAIN=PASS
RETURN_TO_GPT_AT_BATCH_BOUNDARY=PASS
MATERIAL_REPLAN_TRIGGER_DEFINED=PASS
```
