---
name: first-principles-physical-limit-convergence
description: 在固定任务与硬约束下，以单一端到端第一性原理物理极限为最终时间参照；锁定母技能身份与远端共同工作区，建立MRE/REAL_STATE_MODEL，收割成熟方案，由GPT一次性设计完整Virtual-99与预授权批次铁路。Codex只作为确定性验证器/执行器，可在批次内沿预定义PASS/FAIL/NOT_APPLICABLE分支连续执行，但绝对禁止自行发现候选、设计实验、扩展迭代、开放式profiling或自由探索。仅在批次边界或材料级重规划触发器出现时返回GPT，最终按残余虚拟收敛、组合生命周期ROI、最终认证与远端核验冻结99。
metadata:
  version: "1.9.0"
  short-description: 第一性原理物理极限收敛引擎·预授权批次铁路版
  lineage: first-principles-physical-limit-convergence@1.8.0 <- @1.7.0 <- @1.6.0 <- @1.5.0 <- @1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理物理极限收敛引擎 v1.9.0

## 第 -2 门禁：CANONICAL IDENTITY / LINEAGE ISOLATION

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_DISPLAY_NAME_ZH=第一性原理物理极限收敛引擎
CANONICAL_DISPLAY_NAME_EN=First-Principles Physical-Limit Convergence
CANONICAL_SKILL_VERSION=1.9.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.9.0
```

历史关系：

```text
LEGACY_ANCESTOR_SKILL_ID=absolute-time-fireworks-optimization
LEGACY_METHOD_SOURCE=mature-replication-four-column
LEGACY_ANCESTOR_IS_CURRENT_MOTHER_SKILL=NO
LEGACY_ANCESTOR_IS_CURRENT_UPGRADE_TARGET=NO
LEGACY_VERSION_NUMBER_CONTROLS_CURRENT_VERSION=NO
```

任何读取、修改、部署母技能动作前必须验证：

```text
REQUESTED_MOTHER_SKILL_ID
CURRENT_REMOTE_BRANCH
CURRENT_SKILL_PATH
CURRENT_SKILL_VERSION
LINEAGE_ROLE
```

若不匹配：

```text
CANONICAL_IDENTITY_GATE=BLOCKED
-> DO NOT MODIFY LEGACY SKILL
-> LOCATE CURRENT VERSION BRANCH
-> READ CURRENT SKILL.md
-> RETURN_TO_GPT IF STILL AMBIGUOUS
```

---

## 第 -1 门禁：SKILL PRECEDENCE / NO FREE EXPLORATION

```text
SKILL_PRECEDENCE_GATE=ABSOLUTE_WITHIN_PROJECT
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
CODEX_MAY_ADD_CANDIDATE=NO
CODEX_MAY_CHANGE_CANDIDATE_ORDER=NO
CODEX_MAY_EXTEND_ITERATION=NO
CODEX_MAY_PROFILE_WITHOUT_GPT_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
PREAUTHORIZED_BATCH_EXECUTION=YES
```

Codex 永久不得自行：

- 发现优化点后顺手测试；
- 增加、替换或重排候选；
- 自己制定 A/B、seed、run count、阈值、停止条件；
- 因结果慢/快而追加第4、第5、第N次运行；
- 开 profiler、kernel trace、VRAM sweep、版本 sweep、参数 search；
- 从结果自行推导新的实验；
- 在 GPT 铁路缺项时补计划；
- 把“做到99”“继续优化”解释成开放授权。

命令与技能冲突：

```text
COMMAND_CONFLICT_WITH_SKILL=YES
-> NO_FREE_EXPLORATION_RULE_WINS
-> STOP UNSPECIFIED ACTION
-> PRESERVE FACTS
-> RETURN_TO_GPT
```

---

# v1.9 核心修正：PREAUTHORIZED BATCH RAILROAD

v1.8 已正确要求 GPT 在执行前一次性设计完整 Virtual-99 条件铁路，但同时把“每个结果都返回 GPT”写得过强，会把一条已设计完整的铁路拆成：

```text
STEP-A -> GPT -> STEP-B -> GPT -> PREFLIGHT-C -> GPT -> ...
```

这与“实际执行前完整虚拟运行到99”的原意冲突，也增加工程时间和上下文成本。

v1.9 修正为：

```text
GPT DESIGN COMPLETE BATCH
-> CODEX EXECUTE PREAUTHORIZED STAGES
-> FOLLOW ONLY PREDEFINED BRANCHES
-> CHECKPOINT / QC / KEEP-ROLLBACK
-> CONTINUE INSIDE BATCH WHEN RESULT IS EXPECTED
-> RETURN TO GPT AT BATCH BOUNDARY
```

仍然：

```text
NO_FREE_EXPLORATION=YES
```

### 批次内可以自动继续的结果

如果铁路已明确写出下一步：

```text
EXPECTED_PASS
EXPECTED_FAIL
EXPECTED_NOT_APPLICABLE
```

Codex 按 `NEXT_ON_*` 连续执行，不需要每一步重新回 GPT。

### 必须提前回 GPT 的 MATERIAL_REPLAN_TRIGGER

只有以下情况：

1. 铁路没有覆盖的结果/错误；
2. correctness / quality / stability / safety 失效；
3. task contract、硬件、关键软件或模型身份发生未授权变化；
4. 下一阶段前提被真实证据推翻，且没有预定义 fallback；
5. control window 失稳导致裁决无效；
6. batch 全局 GPU / wall budget 到顶；
7. Git / 远端事实冲突；
8. 继续执行会超出原始允许变更范围。

处理：

```text
SAVE EVIDENCE
SAFE STOP / RESTORE
PUSH / REMOTE VERIFY WHEN APPROPRIATE
RETURN_TO_GPT
```

### 不触发重规划

只要后续条件分支仍然有效：

```text
GAIN_LARGER_THAN_PROJECTED
GAIN_SMALLER_THAN_PROJECTED_BUT_PASS
EXPECTED_FAIL
EXPECTED_ROLLBACK
EXPECTED_NOT_APPLICABLE
```

都不单独触发 GPT 重规划。

硬规则：

```text
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
```

“比预计快很多”不是开启新研究链的授权。

### 禁止无限 preflight 链

```text
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

对于已在 Virtual-99 中选中的成熟候选：

- 要么 GPT 在批次设计阶段一次性写完有限 preflight；
- 要么直接在 bounded A/B 中把 load fail / metadata incompatibility / mechanism inactive 写成 FAIL/NOT_APPLICABLE；
- 不允许执行期无限拆成 E2P -> E2M -> E2X -> ...。

详细规则：`references/PREAUTHORIZED-BATCH-RAILROAD.md`。

---

# 总目标

```text
PRIMARY_OBJECTIVE = MINIMIZE FIXED-TASK END-TO-END TIME
SECONDARY_OBJECTIVE = MINIMIZE ENGINEERING CONVERGENCE TIME / GPU COST / AGENT COST
```

硬约束：correctness、quality、stability、safety 优先；不得改变任务合同换取速度。

---

# 第0门禁：PROJECT REMOTE WORKSPACE

项目必须声明：

```text
PROJECT_ID
SHARED_WORKSPACE_TYPE
SHARED_WORKSPACE_REMOTE
SHARED_WORKSPACE_BRANCH
SHARED_WORKSPACE_PROJECT_PATH
LOCAL_EXECUTION_CHECKOUT
REMOTE_VERIFY_REQUIRED=YES
```

规则：

```text
SHARED_WORKSPACE_IS_REMOTE=YES
LOCAL_PATH_IS_SHARED_WORKSPACE=NO
```

流程：

```text
REMOTE LOCATE
-> FETCH/PULL
-> LOCAL CHECKOUT
-> EXECUTE PREAUTHORIZED RAILROAD
-> REPORT
-> PUSH
-> REMOTE VERIFY
```

只有远端核验后：

```text
SHARED_FACT_CONFIRMED=YES
```

---

# 核心原则

## 1. 第一性原理负责边界，不授权探索

第一性原理负责固定任务、硬件边界、不可避免物理工作量和最终时间参照；成熟方案负责吸收世界已解决的工程收益；GPT负责 Virtual-99 和铁路；Codex只负责确定性执行。

## 2. 单一物理极限板

每个固定任务只发布：

```text
T_PHY_TOTAL_REFERENCE=<one number or interval>
```

Generation、Path、I/O、load、decode 等只用于内部推导，不作为并列正式极限。

`T_PHY_TOTAL_REFERENCE` 是理论参照，不是当前机器 benchmark，也不是99阈值。

## 3. 复杂系统先做 MRE

MRE 获取：冷态、warm、steady、实际时间、设备放置、驻留、缓存、故障、QC。

```text
MRE_ROLE=REAL_STATE_CALIBRATOR
```

不是终测，不授权自由优化。

## 4. 实际执行前先完整 Virtual-99

禁止：

```text
发现一点 -> 测一点 -> 再发现 -> 再测 -> V1...Vn
```

正式路径：

```text
REMOTE SHARED FACTS
-> T_PHY_TOTAL_REFERENCE
-> MRE
-> REAL_STATE_MODEL
-> MATURE HARVEST
-> GPT COMPLETE VIRTUAL-99
-> GPT PREAUTHORIZED BATCH RAILROAD
-> CODEX BATCH EXECUTION
-> BATCH BOUNDARY
-> GPT RESIDUAL VIRTUAL CONVERGENCE
-> NEXT BATCH OR FINAL CERTIFICATION
-> FREEZE
```

---

# STEP 1：边界 + T_PHY + MRE + REAL_STATE_MODEL

## 1.1 TASK CONTRACT

```text
TASK_CONTRACT
TASK_COMPLETED
CORRECTNESS_GATE
QUALITY_GATE
STABILITY_GATE
SAFETY_GATE
TIMING_BOUNDARY
```

## 1.2 ACTIVE HARDWARE

```text
ACTIVE_HARDWARE_BOUNDARY
= 当前真实安装 + 可正常使用 + 本任务允许使用的硬件
```

未来未安装硬件不阻断当前99。

## 1.3 历史事实继承

继承已验证 baseline、P50/P95、KEEP/ROLLBACK、Failure Index、VRAM/RAM/I/O、已证实/证伪机制。兼容历史存在时禁止从零重探。

## 1.4 单一物理极限

```text
T_PHY_TOTAL_REFERENCE=<number or interval>
```

必须记录固定任务、硬件、推导依据、置信度。

## 1.5 MRE

MRE 的结束条件提前写明。完成后形成真实态，不自动开放优化。

## 1.6 REAL_STATE_MODEL

```text
T_PHY_TOTAL_REFERENCE
+ STATIC_FACTS
+ MRE_OBSERVATIONS
+ EMPIRICAL_PRIORS
= REAL_STATE_MODEL
```

现实数据推翻假设时记录 invalidated assumption，不为容易达99而修改物理参照。

---

# STEP 2：成熟方案 + Virtual-99 + 批次铁路

## 2.1 MATURE_HARVEST_MATRIX

每个候选至少记录：

```text
SOURCE_LEVEL
HARDWARE_MATCH
TASK_MATCH
MECHANISM
TARGET_BLOCK
EXPECTED_ABS_GAIN
QUALITY_RISK
STABILITY_RISK
INTEGRATION_COST
REVERSIBILITY
CURRENTLY_PRESENT
```

外部比例只用于排序，不直接变成本机收益。

## 2.2 GPT COMPLETE VIRTUAL_MATURE_PATH

GPT 在执行前一次性设计当前批次从起点到停止点：

```text
STEP
CURRENT_STATE
TARGET_BLOCK
MECHANISM
SOURCE
EXPECTED_REMOVABLE_TIME
NEW_OVERHEAD
PROJECTED_RESULT_RANGE
RISK
ROLLBACK
VERIFICATION_RAILROAD
MAX_GPU_RUNS
TIME_BUDGET
CODEX_BUDGET
STOP_POINT
```

条件分支必须提前写入。

## 2.3 批次铁路合同

每个 stage 至少有：

```text
OBJECTIVE
CURRENT_STATE / BASELINE_RULE
EXACT_ALLOWED_CHANGE
ALLOWED_FILES_OR_COMPONENTS
SEEDS_AND_RUN_COUNT
TIMING_BOUNDARY
QC_GATE
EXPECTED_BOUNDED_OUTCOME
SUCCESS_RULE
FAILURE_RULE
NOT_APPLICABLE_RULE
INCONCLUSIVE_RULE
ROLLBACK
NEXT_ON_PASS
NEXT_ON_FAIL
NEXT_ON_NOT_APPLICABLE
NEXT_ON_INCONCLUSIVE
MAX_GPU_RUNS
TIME_BUDGET
```

整个 batch 还必须有：

```text
BATCH_GLOBAL_GPU_BUDGET
BATCH_GLOBAL_WALL_BUDGET
BATCH_STOP_POINT
FINAL_RETURN_TO_GPT_POINT
```

缺关键字段：

```text
VALIDATION_PLAN_NOT_MATURE=YES
-> DO NOT START THAT STAGE
```

## 2.4 Codex 执行

```text
LOAD SKILL
-> VERIFY CANONICAL IDENTITY/VERSION
-> VERIFY PROJECT WORKSPACE
-> VERIFY COMPLETE PREAUTHORIZED BATCH
-> EXECUTE CURRENT STAGE
-> QC
-> WRITE EVIDENCE
-> KEEP/ROLLBACK/NOT_APPLICABLE BY PREDEFINED RULE
-> IF EXPECTED BRANCH: CONTINUE NEXT PREAUTHORIZED STAGE
-> IF MATERIAL_REPLAN_TRIGGER: STOP AND RETURN GPT
-> IF BATCH COMPLETE: REMOTE VERIFY AND RETURN GPT
```

## 2.5 禁止开放式长验证

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
```

超过 batch budget：安全停止，保存证据，返回 GPT。

## 2.6 自研入口

自研只能由 GPT 在 Virtual 层提出，必须有真实数据、明确机制、预计收益、回滚和有限预算。Codex不得自行进入。

---

# RESIDUAL VIRTUAL CONVERGENCE

只在：

```text
PREAUTHORIZED_BATCH_COMPLETE
```

或 `MATERIAL_REPLAN_TRIGGER=YES` 时重新进入 GPT。

正常 batch 边界做：

```text
CURRENT_WINNER
-> REMAINING_MATURE_CANDIDATES
-> RESIDUAL_GAPS
-> INTERACTIONS
-> EXPECTED_PORTFOLIO_GAIN
-> TOTAL_VALIDATION_COST
-> RISK
-> NEXT PREAUTHORIZED BATCH or FINAL CERTIFICATION
```

若没有 ROI 为正、收益高于噪声/风险且可短验证的组合：

```text
PORTFOLIO_ECONOMIC_STOP=YES
```

---

# ROI 与研究支线门禁

不是所有理论可优化点都值得验证。

如果候选：

- 剩余可消灭绝对时间小；
- 风险高；
- 需要升级/迁移整个软件栈；
- 需要新的 profiler / kernel research；
- 会开启多轮未知兼容性 preflight；
- 生命周期收益不足覆盖工程成本；

则 GPT 可直接：

```text
PORTFOLIO_ROI_NEGATIVE_OR_INSUFFICIENT
-> DEFERRED / EXHAUSTED
```

不为了“理论完整”继续。

---

# FINAL CERTIFICATION / 99 / FREEZE

99不是距离物理极限1%，也不是强迫达到旧预测秒数。

必须同时满足：

1. CANONICAL_IDENTITY_GATE=PASS；
2. SKILL_PRECEDENCE_GATE=PASS；
3. NO_FREE_EXPLORATION=YES 全过程未破坏；
4. 远端项目工作区声明并可核验；
5. 固定任务 correctness/quality/stability/safety 全通过；
6. 单一 T_PHY_TOTAL_REFERENCE 已发布；
7. MRE / REAL_STATE_MODEL 已完成；
8. 高价值成熟候选已 KEEP / ROLLBACK / NOT_APPLICABLE / EXHAUSTED / DEFERRED；
9. VIRTUAL_MATURE_PATH_COMPLETE=YES；
10. PREAUTHORIZED_BATCH_EXECUTION_COMPLETE=YES；
11. RESIDUAL_VIRTUAL_CONVERGENCE_COMPLETE=YES；
12. PORTFOLIO_ROI_EVALUATED=YES；
13. 无剩余 ROI 为正且值得短验证的高价值组合；
14. Final Certification 通过；
15. 最终配置、证据、Failure Index、经验先验远端冻结，REMOTE_VERIFY=PASS。

定义：

> 99 = 当前真实硬件 + 固定任务 + 单一物理极限参照 + 世界成熟收益 + GPT完整Virtual-99 + 预授权批次确定性执行 + 批次边界残余收敛 + 组合生命周期ROI停止 + 最终认证后的稳定最优。

---

# 执行纪律

- GPT：极限、候选、顺序、条件分支、批次预算、停止条件。
- Codex：身份验证、精确执行、QC、证据、回滚、按预定义分支连续执行、Git收口。
- 单GPU benchmark 串行独占。
- AI断线/capacity/审批等待不改变铁路。
- 本地结果未 push + remote verify 前不是共同事实。

---

# 默认最短读取顺序

1. `SKILL.md`
2. `references/CANONICAL-IDENTITY-GATE.md`
3. `references/NO-FREE-EXPLORATION-GATE.md`
4. `references/PREAUTHORIZED-BATCH-RAILROAD.md`
5. `references/REMOTE-SHARED-WORKSPACE.md`
6. 项目远端工作区声明
7. GPT 当前完整 batch railroad

---

# 状态

```text
SKILL_VERSION=1.9.0
CANONICAL_IDENTITY_GATE_DEFINED=PASS
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
SKILL_PRECEDENCE_GATE_DEFINED=PASS
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
PREAUTHORIZED_BATCH_EXECUTION=YES
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
MATERIAL_REPLAN_TRIGGER_DEFINED=PASS
RETURN_TO_GPT_AT_BATCH_BOUNDARY=PASS
SINGLE_T_PHY_TOTAL_REFERENCE_DEFINED=PASS
REMOTE_SHARED_WORKSPACE_DEFINED=PASS
MRE_REAL_STATE_CALIBRATION_DEFINED=PASS
MATURE_HARVEST_DEFINED=PASS
FULL_VIRTUAL_99_PATH_DEFINED=PASS
RESIDUAL_VIRTUAL_CONVERGENCE_DEFINED=PASS
PORTFOLIO_LIFETIME_ROI_DEFINED=PASS
NO_MULTI_HOUR_OPEN_ENDED_EXPLORATION=YES
REMOTE_VERIFY_REQUIRED=YES
```
