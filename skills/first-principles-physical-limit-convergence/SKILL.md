---
name: first-principles-physical-limit-convergence
description: 在固定任务与硬约束下，以单一端到端第一性原理物理极限为最终时间参照；先锁定当前母技能身份与版本谱系，再声明项目远端共同工作区并完成极简真实运行，由GPT/高质量推理层一次性设计完整虚拟99铁路。Codex只允许作为确定性验证器/执行器按铁路高速验证，绝对禁止自行发现候选、制定测试、扩展迭代、开放式profiling或自由探索。成熟大收益后再次做残余虚拟收敛，最终按组合生命周期ROI、最终认证与远端核验冻结99。
metadata:
  version: "1.8.0"
  short-description: 第一性原理物理极限收敛引擎·身份锁定/技能优先/零自由探索版
  lineage: first-principles-physical-limit-convergence@1.7.0 <- @1.6.0 <- @1.5.0 <- @1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理物理极限收敛引擎 v1.8.0

## 第 -2 门禁：CANONICAL IDENTITY / LINEAGE ISOLATION

这是 v1.8.0 新增的最高前置身份门禁。任何“更新母技能、读取母技能、把新规则写回母技能”的动作，在进入方法逻辑前必须先证明当前操作对象就是本技能，而不是历史祖先、兼容资产或旧工程入口。

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_DISPLAY_NAME_ZH=第一性原理物理极限收敛引擎
CANONICAL_DISPLAY_NAME_EN=First-Principles Physical-Limit Convergence
CANONICAL_SKILL_VERSION=1.8.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
```

### 历史祖先不是当前母技能

```text
LEGACY_ANCESTOR_SKILL_ID=absolute-time-fireworks-optimization
LEGACY_METHOD_SOURCE=mature-replication-four-column
LEGACY_ANCESTOR_IS_CURRENT_MOTHER_SKILL=NO
LEGACY_ANCESTOR_IS_CURRENT_UPGRADE_TARGET=NO
LEGACY_VERSION_NUMBER_CONTROLS_CURRENT_VERSION=NO
```

`absolute-time-fireworks-optimization` 是本方法演化历史中的祖先/旧工程资产；`mature-replication-four-column` 是历史方法来源/参考资产。它们可以保留历史案例、冻结资产、兼容材料，但**不得因为当前方法脱胎于它们，就把新的母技能规则继续写回旧 skill id**。

不同 skill id 的版本号属于各自独立谱系。旧技能存在 `v2.x` 不代表它比本技能 `v1.8.0` 更新，也不允许把本技能版本重新切回旧技能版本线。

### 每次正式读取或修改母技能前先验证身份

```text
REQUESTED_MOTHER_SKILL_ID
REQUESTED_DISPLAY_NAME
CURRENT_REMOTE_BRANCH
CURRENT_SKILL_PATH
CURRENT_SKILL_VERSION
LINEAGE_ROLE
```

必须满足：

```text
REQUESTED_MOTHER_SKILL_ID == first-principles-physical-limit-convergence
CURRENT_SKILL_PATH == skills/first-principles-physical-limit-convergence/
CURRENT_SKILL_VERSION == REQUIRED_SKILL_VERSION
LINEAGE_ROLE == CURRENT_MOTHER_SKILL
```

任何一项不成立：

```text
CANONICAL_IDENTITY_GATE=BLOCKED
→ DO NOT MODIFY LEGACY SKILL
→ LOCATE CURRENT VERSION BRANCH
→ READ CURRENT SKILL.md
→ REPORT MISMATCH / RETURN TO GPT
```

详细规则见：`references/CANONICAL-IDENTITY-GATE.md`。

---

## 第 -1 门禁：SKILL PRECEDENCE / NO FREE EXPLORATION

这是本技能在项目方法层级中的最高优先级执行规则。它不能被后续任务命令、临时说明、执行器自行判断或“为了完成任务”的扩展解释削弱；更高层级的系统、安全和平台约束仍然优先。

```text
SKILL_PRECEDENCE_GATE=ABSOLUTE_WITHIN_PROJECT
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
CODEX_MAY_ADD_CANDIDATE=NO
CODEX_MAY_EXTEND_ITERATION=NO
CODEX_MAY_PROFILE_WITHOUT_GPT_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
```

### 绝对禁止

Codex / 本地执行器不得自行：

- 发现一个优化点后顺手测试；
- 选择新的候选、替换候选或改变候选顺序；
- 自己制定 A/B、seed、运行次数、阈值或停止规则；
- 因结果“不理想”而自动追加第 4、第 5、第 N 次运行；
- 自己开启 profiler、kernel trace、VRAM 扫描、版本扫描或参数搜索；
- 从一个验证结果推导下一个实验并继续执行；
- 把“继续完成任务”“尽量优化”“做到99”等宽泛目标解释为自行设计子计划的授权；
- 在 GPT 方案缺项时自行补齐方案。

### 命令与技能冲突

若项目任务命令与本技能发生冲突：

```text
COMMAND_CONFLICT_WITH_SKILL=YES
→ NO_FREE_EXPLORATION_RULE_WINS
→ STOP UNSPECIFIED ACTION
→ PRESERVE FACTS
→ RETURN_TO_GPT
```

任务命令可以比本技能更严格、可以指定更具体的执行步骤，但不得弱化 `NO_FREE_EXPLORATION=YES`。

### 每次正式执行前必须先验证技能

```text
CANONICAL_IDENTITY_GATE=PASS
SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_SKILL_VERSION=<项目声明版本>
SKILL_VERSION_VERIFIED=YES
PROJECT_WORKSPACE_DECLARATION_GATE=PASS
```

若技能不存在、版本不符、无法读取、身份门禁不通过或项目没有声明所需版本：

```text
SKILL_PRECEDENCE_GATE=BLOCKED
→ NO GPU RUN
→ NO NEW EXPERIMENT
→ REPORT MISMATCH
→ RETURN_TO_GPT
```

### GPT 完整验证铁路的最小合同

任何允许 Codex 执行的验证步骤必须已经由 GPT / 高质量推理层明确给出：

```text
OBJECTIVE
CURRENT_STATE
ALLOWED_CHANGE
ALLOWED_FILES_OR_COMPONENTS
BASELINE
SEEDS_AND_RUN_COUNT
TIMING_BOUNDARY
QC_GATE
EXPECTED_BOUNDED_OUTCOME
SUCCESS_RULE
FAILURE_RULE
INCONCLUSIVE_RULE
ROLLBACK
STOP_POINT
MAX_GPU_RUNS
TIME_BUDGET
CODEX_BUDGET
NEXT_ACTION_AFTER_EACH_OUTCOME
```

缺任何关键项：

```text
VALIDATION_PLAN_NOT_MATURE=YES
→ STOP EXECUTION
→ RETURN_TO_GPT
```

意外结果的默认行为永远不是继续探索，而是：

```text
UNEXPECTED_RESULT=YES
→ SAVE EVIDENCE
→ RESTORE / SAFE STOP AS PREDEFINED
→ RETURN_TO_GPT
```

详细规则见：`references/NO-FREE-EXPLORATION-GATE.md`。

---

# 总目标

```text
PRIMARY_OBJECTIVE
= 最小化固定任务真实端到端执行时间

SECONDARY_OBJECTIVE
= 最小化达到稳定最优所需的工程时间、GPU时间与智能体资源成本
```

硬约束优先：任务必须真实完成，correctness、quality、stability、safety 全部通过；不得为了提速偷偷改变任务合同。

---

# 第0门禁：PROJECT REMOTE WORKSPACE

正式任务开始前必须声明项目自己的远端共同工作区：

```text
PROJECT_ID
SHARED_WORKSPACE_TYPE
SHARED_WORKSPACE_REMOTE
SHARED_WORKSPACE_BRANCH
SHARED_WORKSPACE_PROJECT_PATH
LOCAL_EXECUTION_CHECKOUT
REMOTE_VERIFY_REQUIRED=YES
```

硬规则：

```text
SHARED_WORKSPACE_IS_REMOTE=YES
LOCAL_PATH_IS_SHARED_WORKSPACE=NO
```

任何 `C:\...`、`D:\...`、`/home/...`、本机 clone 或 worktree 只能叫 `LOCAL_EXECUTION_CHECKOUT` 或 `LOCAL_EVIDENCE_ROOT`，不能叫共同工作区或共同事实源。

正确顺序：

```text
REMOTE LOCATE
→ FETCH/PULL
→ LOCAL CHECKOUT
→ EXECUTE PREDEFINED RAILROAD
→ REPORT
→ PUSH
→ REMOTE VERIFY
```

只有远端核验成功后：

```text
SHARED_FACT_CONFIRMED=YES
```

详细规则见：`references/REMOTE-SHARED-WORKSPACE.md`。

---

# 核心原则

## 1. 第一性原理只负责边界，不授权自由探索

第一性原理负责：冻结任务、硬件边界、物理因果链、不可避免工作量和最终时间下界；成熟方案负责吸收世界已经解决的工程收益；GPT负责完整虚拟推演；Codex只负责短验证。

## 2. 物理极限板只保留一个端到端时间标准

每个固定任务最终只发布一个正式对比标准：

```text
T_PHY_TOTAL_REFERENCE
= 固定任务在当前物理边界下的端到端理论最短时间
= 一个数字或一个区间
```

Generation、Path、I/O、load、decode 等分量可以在内部建模，但**不得再作为并列的正式“物理极限板”标准**。

用途只有一个：

```text
CURRENT / CANDIDATE / FINAL
↔ T_PHY_TOTAL_REFERENCE
```

`T_PHY_TOTAL_REFERENCE` 是理论物理参照，不是实测机器 benchmark，也不等于 99 通过门槛。未知效率允许使用区间和置信度，禁止伪精确。

## 3. 复杂系统先做 MRE

静态版本和模型大小不能代表运行态。复杂任务先让最小完整链真实跑通，得到冷态、预热、稳态、实际时间、设备放置、驻留、缓存、故障与质量事实。

MRE 是 `REAL_STATE_CALIBRATOR`，不是性能终测，也不授权 MRE 后立即进入下一实验。

## 4. 实际执行前先完整虚拟运行到99

禁止：

```text
发现一点 → 测一点 → 再发现一点 → 再测一点 → V1...Vn
```

正式路径：

```text
远端共同事实
→ T_PHY_TOTAL_REFERENCE
→ MRE
→ REAL_STATE_MODEL
→ 成熟方案收割
→ GPT完整虚拟99铁路
→ Codex按铁路短验证
→ 每个结果返回GPT裁决
→ 残余虚拟收敛
→ Final Certification
→ FREEZE
```

## 5. 成熟大收益后再次虚拟收敛

成熟候选验证完成后，Codex停止。GPT根据最新真实数据重新执行 `RESIDUAL_VIRTUAL_CONVERGENCE`，把剩余优化作为组合推演到停止点，再生成下一批完整验证铁路。

## 6. 停止条件看组合生命周期ROI，但执行仍必须短而确定

单个 0.1s / 0.5s 不能单独决定停止。GPT比较：

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO
vs
PORTFOLIO_COST
```

即使组合长期收益很大，也只代表值得继续设计；不代表允许 Codex 自由探索。

---

# STEP 1：边界 + 单一物理极限 + MRE + 真实态

## 1.1 冻结任务合同

```text
TASK_CONTRACT
TASK_COMPLETED
CORRECTNESS_GATE
QUALITY_GATE
STABILITY_GATE
SAFETY_GATE
TIMING_BOUNDARY
```

## 1.2 冻结当前有效硬件边界

```text
ACTIVE_HARDWARE_BOUNDARY
= 此刻真实安装 + 可正常使用 + 本任务允许使用的硬件
```

未来未安装硬件不得阻断当前 99。

## 1.3 继承历史共同事实

优先继承：已验证基线、P50/P95、KEEP/ROLLBACK、Failure Index、真实阶段时间、驻留/VRAM/RAM/I/O事实、已证实和已证伪机制。有兼容历史证据时禁止从零重探。

## 1.4 发布单一物理极限参照

只发布：

```text
T_PHY_TOTAL_REFERENCE=<number or interval>
```

必须写明任务合同、硬件边界、估算依据和置信度。分块极限只留在计算工作底稿，不进入对外极限板。

## 1.5 做一次 MRE

目标是在最小工程成本下校准真实态。MRE 固定结束条件必须提前写明；完成后立即停止，返回 GPT。

## 1.6 建立 REAL_STATE_MODEL

```text
T_PHY_TOTAL_REFERENCE
+ STATIC_FACTS
+ MRE_OBSERVATIONS
+ EMPIRICAL_PRIORS
= REAL_STATE_MODEL
```

现实数据推翻假设时记录失效假设、新证据和修订原因。不得为了“更容易达到99”而修改物理极限参照。

---

# STEP 2：成熟方案 + 完整虚拟99 + 确定性验证

## 2.1 建立 MATURE_HARVEST_MATRIX

优先证据：官方稳定方案、同硬件实测、成熟开源、本机历史成功、机制清晰的社区重复验证。

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

外部百分比只用于排序，不直接变成本机收益，也不自动 KEEP。

## 2.2 GPT 构建完整 VIRTUAL_MATURE_PATH

GPT必须在执行前一次性把当前批次从起点到停止点设计完整。每一步包含：

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

前一步结果决定后一步是否仍适用，但**这个条件分支必须提前写在铁路里**。未预定义的分支不得由 Codex 自行发明。

## 2.3 Codex执行规则

Codex只做：

```text
LOAD REQUIRED SKILL
→ VERIFY CANONICAL IDENTITY
→ VERIFY VERSION
→ VERIFY PROJECT WORKSPACE
→ VERIFY PREDEFINED RAILROAD COMPLETE
→ EXECUTE EXACT STEP
→ QC
→ WRITE EVIDENCE
→ ROLLBACK/KEEP ONLY BY PREDEFINED RULE
→ STOP
→ RETURN RESULT TO GPT
```

如果实测与预计不符、控制组漂移、环境异常、审批门禁等待、Git远端变化或其他异常没有预定义处理：保存事实并停止。

## 2.4 禁止数小时开放式验证

```text
NO_MULTI_HOUR_OPEN_ENDED_VALIDATION=YES
```

超过预定时间预算且没有铁路中定义的继续条件：

```text
BUDGET_DRIFT=YES
→ SAFE STOP
→ SAVE EVIDENCE
→ RETURN_TO_GPT
```

## 2.5 自研攻击入口

自研只允许由 GPT 在虚拟层提出；Codex不得自行进入。GPT提出的自研步骤必须同时有真实数据、明确机制、预计收益、可逆回滚和有限预算。

---

# RESIDUAL VIRTUAL CONVERGENCE

每批成熟验证后，Codex停止；GPT重新读取最新共同事实并做：

```text
CURRENT_WINNER
→ REMAINING_MATURE_CANDIDATES
→ RESIDUAL_GAPS
→ INTERACTIONS
→ EXPECTED_PORTFOLIO_GAIN
→ TOTAL_VALIDATION_COST
→ RISK
→ NEXT PREDEFINED RAILROAD or STOP
```

若没有 ROI 为正且高于测量噪声/风险、可被短验证的剩余组合：

```text
PORTFOLIO_ECONOMIC_STOP=YES
```

---

# 99 / FREEZE

99不是“距离物理极限只差1%”，也不是强迫达到某个旧预测秒数。

必须同时满足：

1. `CANONICAL_IDENTITY_GATE=PASS`；
2. `SKILL_PRECEDENCE_GATE=PASS`；
3. `NO_FREE_EXPLORATION=YES` 全过程未被破坏；
4. 项目远端工作区已声明并可核验；
5. 固定任务、correctness、quality、stability、safety 全通过；
6. 单一 `T_PHY_TOTAL_REFERENCE` 已发布；
7. MRE / REAL_STATE_MODEL 已完成；
8. 高价值成熟候选全部已有 KEEP / ROLLBACK / NOT_APPLICABLE / EXHAUSTED 裁决；
9. `VIRTUAL_MATURE_PATH_COMPLETE=YES`；
10. `RESIDUAL_VIRTUAL_CONVERGENCE_COMPLETE=YES`；
11. `PORTFOLIO_ROI_EVALUATED=YES`；
12. 没有剩余 ROI 为正且可在短边界内验证的高价值组合；
13. Final Certification 通过；
14. 正式配置、证据、Failure Index、经验先验已经远端冻结并 `REMOTE_VERIFY=PASS`。

因此：

> **99 = 当前真实硬件 + 固定任务 + 单一物理极限作终极参照 + 世界成熟收益 + GPT完整虚拟铁路 + Codex零自由探索的确定性验证 + 残余组合ROI收敛 + 最终认证后的稳定最优。**

若项目把 Generation 与 Path 分别定义为正式优化对象，可以有两个项目级 99；Total 可以只是组合观测。是否拆分 99 由项目任务合同决定，不改变“物理极限板只保留一个端到端 T_PHY_TOTAL_REFERENCE”的规则。

---

# 执行与上下文纪律

- GPT / 高质量推理层负责：极限、方案、候选、顺序、条件分支、预算、停止条件。
- Codex负责：验证当前母技能身份、读取技能、验证版本、精确执行、QC、证据、回滚、Git收口。
- 单GPU正式 benchmark 串行独占。
- 不允许因会话长度、capacity error、审批等待或恢复操作改变实验计划。
- 页面过长时先冻结远端阶段报告，再由新页面从共同事实恢复。
- 本地结果未 push + remote verify 前不是共同事实。

---

# 默认最短读取路径

每次执行优先读取：

1. `SKILL.md`
2. `references/CANONICAL-IDENTITY-GATE.md`
3. `references/NO-FREE-EXPLORATION-GATE.md`
4. `references/REMOTE-SHARED-WORKSPACE.md`
5. 项目远端工作区声明
6. GPT生成的当前验证铁路

其余 references 仅在 GPT 设计阶段按需读取；Codex不得因为“想了解更多”而扩大读取范围并自行设计实验。

## 状态

```text
SKILL_VERSION=1.8.0
CANONICAL_IDENTITY_GATE_DEFINED=PASS
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
LEGACY_ANCESTOR_MUTATION=NO
SKILL_PRECEDENCE_GATE_DEFINED=PASS
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
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
