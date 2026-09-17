# first-principles-physical-limit-convergence v1.9.0

中文名：**第一性原理物理极限收敛引擎**  
英文名：**First-Principles Physical-Limit Convergence**

v1.9.0 保留 v1.8.0 的全部核心原则：canonical identity、技能优先、零自由探索、单一 `T_PHY_TOTAL_REFERENCE`、远端共同工作区、MRE、成熟方案收割、Virtual-99、Residual Virtual Convergence、组合生命周期 ROI 和 Final Certification。

本版只修正一个真实暴露出的收敛效率问题：

> GPT 已经一次性设计完整 Virtual-99 条件铁路后，不应再强制 Codex 每完成一个预定义 PASS/FAIL 就返回 GPT 重新授权。

因此新增：

```text
PREAUTHORIZED_BATCH_RAILROAD
```

正式路径变为：

```text
CANONICAL IDENTITY
-> NO FREE EXPLORATION
-> REMOTE WORKSPACE
-> SINGLE T_PHY_TOTAL_REFERENCE
-> MRE / REAL_STATE_MODEL
-> MATURE HARVEST
-> GPT COMPLETE VIRTUAL-99
-> GPT PREAUTHORIZED BATCH RAILROAD
-> CODEX CONTINUOUS DETERMINISTIC BATCH EXECUTION
-> BATCH BOUNDARY
-> GPT RESIDUAL VIRTUAL CONVERGENCE
-> PORTFOLIO ROI
-> FINAL CERTIFICATION
-> 99 / FREEZE
```

## 当前唯一母技能身份

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_SKILL_VERSION=1.9.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.9.0
```

历史 `absolute-time-fireworks-optimization` 只是祖先/兼容资产，不是当前母技能。

## 最强项目规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
CODEX_MAY_ADD_CANDIDATE=NO
CODEX_MAY_EXTEND_ITERATION=NO
CODEX_MAY_PROFILE_WITHOUT_GPT_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
PREAUTHORIZED_BATCH_EXECUTION=YES
```

## v1.9 新增的执行规则

如果结果已经被铁路预定义：

```text
EXPECTED_PASS
EXPECTED_FAIL
EXPECTED_NOT_APPLICABLE
```

Codex 可以按照 `NEXT_ON_*` 在同一个 batch 内继续，不需要每一步重新返回 GPT。

只有真正的 `MATERIAL_REPLAN_TRIGGER` 才提前停止：

- 未预定义结果；
- QC/correctness/stability/safety 失效；
- task/hardware/software/model 身份发生未授权变化；
- 后续关键前提被推翻且铁路无 fallback；
- control window 失稳；
- batch 总预算耗尽；
- Git/远端事实冲突。

特别规定：

```text
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

即“收益比预计大很多”不是重新开研究链的理由；已进入 mature matrix 的候选也不得在执行期无限拆成 preflight-A/B/C。

## 物理极限板

每个固定任务只保留：

```text
T_PHY_TOTAL_REFERENCE = 一个端到端时间数字或区间
```

它是理论物理参照，不等于机器 benchmark，也不直接等于 99 门槛。

## 共同工作区

共同工作区必须是项目声明的远端权威空间。本地路径只是执行副本或证据目录；新事实只有 push + remote verify 后才成为共同事实。

## 默认读取顺序

1. `SKILL.md`
2. `references/CANONICAL-IDENTITY-GATE.md`
3. `references/NO-FREE-EXPLORATION-GATE.md`
4. `references/PREAUTHORIZED-BATCH-RAILROAD.md`
5. `references/REMOTE-SHARED-WORKSPACE.md`
6. 项目远端工作区声明
7. GPT 当前完整 batch railroad

完整规则见 `SKILL.md`。
