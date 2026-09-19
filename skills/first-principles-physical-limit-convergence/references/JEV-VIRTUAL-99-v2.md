# Jev Virtual-99 v2 — 极简职责边界

```text
STEP=2_VIRTUAL_99
ROLE=SIMPLIFICATION_CONVERGENCE
STATUS=ACTIVE_CANONICAL_FROZEN
PARENT_SKILL=first-principles-physical-limit-convergence@3.1.2
NEW_SKILL=NO
FOURTH_STEP=NO
HISTORY_DELETED=NO
```

本文件是当前 ACTIVE Virtual-99 的唯一设计权威。它属于母技能三步流程中的第 2 步，不建立第 4 步、子方法或新的优化体系。

旧 `JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.md/json`、Verify-02 RESULT、Reality Delta 与旧冻结记录只保留为 `HISTORY / EVIDENCE`，不再定义 ACTIVE 路径。

## 1. Reality delta 返回第 2 步

Verify-02 的正式状态为 `SAFE_BUT_NOT_TIME_99`：

```text
AUTO_COVERAGE=0.874000       target>=0.95
GPT_ESCALATION_RATE=0.126000 target<=0.05
STAGE_A_P95=13.281350s       target<=4.0s
FULL_SYSTEM_P95=17.311243s   target<=5.0s
AUTO_ACCEPTED_CRITICAL_ERRORS=0
AUTO_ACCEPTED_ANY_ERRORS=0
ILLEGAL_OUTPUTS=0
```

Reality Delta 证明 v1 的正确性防线有效，但 always-on ensemble 与 fallback 结构没有达到极限短时间。因此删除复杂 ACTIVE 路径，回到职责边界本身。

## 2. 冻结职责

```text
CODE
= state + frozen contract 能唯一确定答案的工作

JEV
= 无法由确定规则直接得到、答案空间闭合的有限语义判断

GPT/DeepSeek
= 开放问题，或单次最小 Jev 判断仍然无效/不确定的冲突
```

判定顺序固定：

```text
CAN_CODE_DETERMINE_FROM_STATE_AND_FROZEN_CONTRACT?
  YES -> CODE
  NO  -> IS_FINITE_CLOSED_SEMANTIC_DECISION?
           YES -> ONE MINIMAL JEV REQUEST
           NO  -> GPT/DeepSeek
```

不得为了使用 Jev 而把确定性规则改写成概率问题。

## 3. 25-case 最终职责表

这 25 个 case 是 frozen known-answer replay。每个 case 都给出了完整 state、问题类型、合法答案集合和冻结合同，因此 case 答案本身全部可由 CODE 唯一得到。

H02/H03 是元路由题：CODE 可确定性输出 `jev` / `gpt`；这不等于必须实际调用 Jev/GPT。

| Case | Family | Critical | ACTIVE result producer | Deterministic rule | Frozen output / downstream owner |
|---|---|---:|---|---|---|
| D01 | delivery | yes | CODE | `qc != PASS -> reject` | `false` |
| D02 | delivery | yes | CODE | QC、decode、finite、non-black、range、std 全过冻结门禁 | `true` |
| D03 | delivery | yes | CODE | Star7 attempt QC FAIL 且合同为 reject-and-resample | `reseed_same_star7` |
| D04 | delivery | no | CODE | 同 seed 在 Star7 与 original 1-step 均 FAIL | `stochastic_contract_limit` |
| D05 | delivery | no | CODE | 同 seed Star7 FAIL、original PASS | `star7_specific_quality_failure` |
| D06 | delivery | yes | CODE | fast retry 5–8s、90% first-pass；slow 90–100s 且不保证 | `reseed_same_fast_path` |
| D07 | delivery | no | CODE | 候选已在 known-bad seed QC FAIL | `false` |
| D08 | delivery | no | CODE | W4A8 是 independent 99 path，未获插入 frozen main 授权 | `false` |
| C01 | control | yes | CODE | remote capacity failure 不重放 ledger 已完成本地工作 | `false` |
| C02 | control | no | CODE | TokenDefaultDacl/executor launch failure 且 H3 未运行 | `control_plane` |
| C03 | control | no | CODE | 实验前 source identity mismatch | `source_or_execution_control` |
| C04 | control | no | CODE | 单 seed 异常、process/decode PASS、其他 seeds PASS | `stochastic_sample` |
| R01 | reopen | yes | CODE | 五个 frozen reopen 条件全 false | `false` |
| R02 | reopen | yes | CODE | hardware/model stack changed | `true` |
| R03 | reopen | yes | CODE | mature verified route + meaningful gain + quality PASS | `true` |
| R04 | reopen | yes | CODE | significant long-term production drift | `true` |
| R05 | reopen | yes | CODE | current QC gate proven insufficient | `true` |
| M01 | method | yes | CODE | 冻结证据中唯一 20/20 accepted winner | `star7_qc_reseed` |
| M02 | method | no | CODE | stochastic proposal + deterministic acceptance 的正式指标 | `T_TFVR` |
| M03 | method | yes | CODE | 质量声明定义在 delivered/accepted output | `accepted_output` |
| H01 | handler | yes | CODE | file existence 与 SHA256 是确定性程序 | `code` |
| H02 | handler | no | CODE | frozen role matrix：closed-set ambiguous semantics 路由 JEV | `jev`（下游职责；本 case 不调用） |
| H03 | handler | yes | CODE | frozen role matrix：open invention 路由 GPT | `gpt`（下游职责；本 case 不调用） |
| H04 | handler | yes | CODE | 公式固定后的 byte/bandwidth/FLOPs 算术 | `code` |
| H05 | handler | yes | CODE | ffprobe/decode/finite/SHA256 最终验收 | `code` |

冻结计数：

```text
ACTIVE_25_CASE_RESULT_PRODUCERS:
  CODE=25
  JEV=0
  GPT=0

DOWNSTREAM_ROLE_LABELS_RETURNED_BY_META_CASES:
  H02=JEV
  H03=GPT
```

## 4. 从 ACTIVE 路径删除的复杂结构

以下结构仍保留在 v1 与 Verify-02 历史证据中，但从 ACTIVE canonical path 删除：

- always-on MEGA A/B/C/D/E 五 view；
- always-on FAMILY anchors；
- 固定 Stage A + Stage B ensemble；
- second-family rescue；
- weight grid；
- log-probability fusion；
- LOO weight selection；
- majority/family 多层一致性门；
- 针对个别 case 增加额外 Jev 请求的补丁式逻辑；
- 以多请求相关性指标作为运行时决策依赖。

这些内容可继续作为历史分析指标，但没有 ACTIVE 执行权。

## 5. 保留结构及原因

| 保留结构 | 原因 |
|---|---|
| CODE deterministic pre-handler | 直接执行冻结规则，是最短且零概率错误的路径 |
| 单次最小 Jev typed fast path | 仅为未来确实无法 CODE 化、但答案空间闭合的输入保留 |
| GPT/DeepSeek conflict/open fallback | 处理开放问题或单次 Jev 仍不确定的冲突 |
| CODE final verifier | 执行合法输出、硬约束和最终 PASS/FAIL 验证 |
| 原始 v1、Verify-02、Reality Delta | HISTORY / EVIDENCE；不删除、不覆盖 |

Jev fast path 的唯一允许形态：

```text
ONE INPUT
ONE CLOSED ANSWER SPACE
ONE CANONICAL TYPED REQUEST
NO A/B/C/D/E
NO FAMILY ANCHOR
NO WEIGHT GRID
NO PROBABILITY FUSION
NO JEV RETRY LADDER

valid + sufficiently determinate -> candidate result
invalid / uncertain / conflict   -> GPT/DeepSeek
```

本 v2 不冻结新的数值 probability threshold。若没有既有合同能确定接受，视为不确定并升级 GPT；不得为了提高覆盖率现场调参。

## 6. ACTIVE 极简路径

```text
INPUT
  -> CODE deterministic pre-handler
       -> deterministic result found: DIRECT RESULT
       -> no deterministic result, finite closed semantics: ONE JEV REQUEST
       -> open problem: GPT/DeepSeek
  -> if Jev invalid/uncertain/conflicted: GPT/DeepSeek
  -> CODE final verifier
  -> VALID RESULT
```

对于当前 25-case replay：

```text
INPUT
-> CODE deterministic pre-handler
-> CODE final verifier
-> RESULT

JEV_REQUESTS=0
GPT_REQUESTS=0
H3_GPU_RUNS=0
```

## 7. 新旧 ACTIVE 复杂度

| 项目 | v1 ACTIVE | v2 ACTIVE（25-case） |
|---|---:|---:|
| Jev request batches / repeat | 11（A/B/C + 5 FAMILY1 + D/E + FAMILY2） | 0 |
| Fixed ensemble stages | 2（Stage A、Stage B） | 0 |
| Active views | 7 类（A–E、FAMILY1、FAMILY2） | 0 |
| Weight/fusion layers | weight grid + log fusion + consensus | 0 |
| Fallback layers | Stage B -> GPT，共2层 | 0 for current 25 cases；通用路径最多1层 GPT |
| External model calls | Jev always-on，冲突时 GPT | 0 |
| Final verifier | CODE | CODE |

通用未来输入的上限不是新的固定阶段：只有 CODE 无法决定时才发生 1 次 Jev；仍不确定时直接 GPT。

## 8. 硬约束

```text
AUTO_ACCEPTED_CRITICAL_ERRORS=0
AUTO_ACCEPTED_ANY_ERRORS=0
ILLEGAL_OUTPUTS=0
H3_GPU_RUNS=0
FROZEN_H3_MUTATION=0
PRIVACY_DOWNGRADE=0
SECRET_PERSISTENCE=0
NEW_SKILL=NO
FOURTH_STEP=NO
```

## 9. 下一次唯一 Real Verify 合同草案

```text
TASK_ID=H3-P0-JEV-VIRTUAL99-V2-REAL-VERIFY-01
STATUS=DRAFT_ONLY_DO_NOT_EXECUTE
METHOD_STEP=2_VIRTUAL_99_OUTPUT_VERIFICATION
DATASET=H3-P0-JEV-SHADOW-DATASET-v1.json
CASES=25
REPEATS=20
EXPECTED_DECISIONS=500

ACTIVE_PATH=CODE_PREHANDLER -> CODE_FINAL_VERIFIER
EXPECTED_JEV_REQUESTS=0
EXPECTED_GPT_REQUESTS=0
H3_GPU_RUNS=0
FROZEN_H3_MUTATION=0

PASS_REQUIRES:
  DETERMINISTIC_OUTPUT_ACCURACY=500/500
  AUTO_ACCEPTED_CRITICAL_ERRORS=0
  AUTO_ACCEPTED_ANY_ERRORS=0
  ILLEGAL_OUTPUTS=0
  ACTIVE_EXTERNAL_REQUESTS=0
  FULL_SYSTEM_P95_SECONDS<=5.0
  HISTORY_FILES_UNCHANGED=YES

FAIL_ACTION:
  SAVE_REALITY_DELTA
  RETURN_TO_STEP_2
  DO_NOT_PATCH_DURING_VERIFY
  DO_NOT_START_ANOTHER_ROUTE
```

这是合同草案，不是命令包。本轮禁止执行。

## 10. 冻结

```text
STEP=2_VIRTUAL_99
ROLE=SIMPLIFICATION_CONVERGENCE
NEW_SKILL=NO
FOURTH_STEP=NO
HISTORY_DELETED=NO
ACTIVE_COMPLEXITY_REMOVED=YES
V2_FROZEN=YES
```

STOP
