# Jev 概率攻击 Virtual-99 成熟方案 v1

状态：`VIRTUAL_99_FROZEN_CANDIDATE / NO_REAL_EXECUTION_YET`

所属母技能：`first-principles-physical-limit-convergence v3.1.2`

映射：

```text
CORE_1 极限短时间
  -> 最小化 probability-decision T_VALID
CORE_2 成熟方案集群
  -> ensemble / majority / probability pooling / calibration / fallback
CORE_3 高智能虚拟成熟
  -> 本文件冻结最终 Jev 决策架构
```

本文件不是第四核心，也不是新的 H3 算法。它只优化有限语义判断控制层。

---

## 1. 已知事实与边界

第一轮 H3-P0 Jev shadow 的控制台证据显示：

```text
CODE deterministic QC: 22/22 = 100%
MEGA:   92-96%, 1-2 critical errors/run, P50≈1.581s, P95≈2.200s, cost≈$0.000149/run
FAMILY: 100% x 5 runs, 0 critical errors, P50≈8.352s serial total, P95≈9.693s, cost≈$0.000193/run
CASE:   84% x 5 runs, 4 critical errors/run, P50≈46.470s, P95≈58.655s, cost≈$0.000391/run
```

这些数字当前属于 `CONSOLE_EVIDENCE_PENDING_REMOTE_RESULT_VERIFY`；正式验证时必须以结果 JSON/MD 为权威事实源。

固定职责：

```text
精确事实 / 算术 / QC / hash / 最终硬验收 -> CODE
闭合答案空间的语义判断                  -> JEV
开放式新方案 / 新代码 / 新算法           -> GPT/DeepSeek
```

禁止为了使用 Jev 而替换更快、更确定的普通代码。

---

## 2. Virtual-99 的核心判断

单次 Jev 不是最终产品；单次输出只是 `probabilistic proposal`。

系统优化对象改为：

```text
FAST PROBABILISTIC PROPOSALS
+ DIVERSITY
+ PROBABILITY FUSION
+ CONSENSUS GATE
+ CONDITIONAL RESCUE
+ GPT ESCALATION
```

目标不是强迫任何一次 Jev 推理 100% 正确，而是让错误无法轻易穿过系统级 gate。

---

## 3. 为什么不能只做机械重复

若每次错误近似独立，奇数次多数投票的理论正确率会快速上升：

| single p | 3-vote | 5-vote | 7-vote | 9-vote |
|---:|---:|---:|---:|---:|
| 0.84 | 93.1392% | 96.8241% | 98.4750% | 99.2515% |
| 0.92 | 98.1824% | 99.5475% | 99.8824% | 99.9686% |
| 0.94 | 98.9632% | 99.8030% | 99.9609% | 99.9920% |
| 0.96 | 99.5328% | 99.9398% | 99.9919% | 99.9989% |

但这些只是 `INDEPENDENCE_REFERENCE`，不是生产保证。

如果错误高度相关：

```text
P(error_next | error_previous) -> 1
```

那么重复 100 次也可能重复同一个错误。

因此 Virtual-99 的关键不是“多问几遍”，而是：

> **主动制造语义等价、非语义不同的多视角判断，从而降低错误相关性。**

---

## 4. 冻结的多视角集合

同一事实、同一任务合同、同一合法答案集合不允许改变；只允许改变不会改变语义真值的表示维度。

### VIEW A — canonical mega

原始 canonical state / question / criteria 顺序。

### VIEW B — order-diversified mega

固定可复现 permutation：改变 case 顺序、family 顺序、criteria key 顺序。

### VIEW C — locality-diversified mega

保持完整信息，但改变相邻问题组合；避免同 family 或同标签长期占据固定邻近位置。

### VIEW D — schema-equivalent mega

使用冻结的等价字段布局，例如 list/object 两种机器结构；不得增删事实。

### VIEW E — wording-equivalent mega

使用事先冻结、人工/高智能验证为语义等价的 question wording；运行时禁止自由改写。

所有 view 都必须：

```text
SAME_FACTS=YES
SAME_ANSWER_SPACE=YES
SAME_BUSINESS_CONTRACT=YES
NO_NEW_INFORMATION=YES
DETERMINISTIC_VIEW_ID=YES
```

---

## 5. Virtual-99 决策图

```text
                    ┌────────────────────────────┐
STATE ──CODE───────>│ deterministic pre-handler │
                    └──────────────┬─────────────┘
                                   │ semantic finite decision
                                   ▼
                    ┌────────────────────────────┐
                    │ STAGE A: PARALLEL PRIMARY  │
                    │ MEGA A + MEGA B + MEGA C   │
                    │ FAMILY anchor(s), parallel │
                    └──────────────┬─────────────┘
                                   │
                         probability vectors
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │ CONSENSUS + PROB FUSION    │
                    └───────┬───────────┬────────┘
                            │           │
                         SAFE         UNCERTAIN
                            │           │
                            ▼           ▼
                         ACCEPT   ┌──────────────────────┐
                                  │ STAGE B: RESCUE      │
                                  │ MEGA D + MEGA E      │
                                  │ 2nd family view      │
                                  │ only disputed scope  │
                                  └──────────┬───────────┘
                                             │
                                      fused consensus
                                             │
                                   ┌─────────┴─────────┐
                                   │                   │
                                 SAFE              CONFLICT
                                   │                   │
                                   ▼                   ▼
                                ACCEPT              GPT/DeepSeek
                                                        │
                                                        ▼
                                                   CODE verifier
```

Stage A 和 Stage B 内部请求只要不存在因果依赖，必须并行，不允许人为串行。

---

## 6. 双通道：MEGA 负责速度，FAMILY 负责语义锚定

第一轮证据已经显示：

```text
MEGA = fast but imperfect
FAMILY = slower serially but observed-stable
```

因此 Virtual-99 不在二者中二选一，而是组合：

```text
MEGA channel   = broad, fast, diverse proposals
FAMILY channel = local semantic anchor
```

### Stage A 自动接受规则

对每个 case：

#### 非关键 case

```text
family_answer == mega_majority(A,B,C)
AND mega_majority_count >= 2/3
AND calibrated aggregate gate == PASS
-> AUTO_ACCEPT
```

#### critical case

```text
family_answer == A == B == C
AND calibrated aggregate gate == PASS
-> AUTO_ACCEPT
```

critical case 不满足全一致时不得猜测，直接进入 Stage B。

---

## 7. Stage B 条件救援

只对 Stage A 未决 case/family 运行，禁止全量重算。

并行运行：

```text
MEGA D
MEGA E
SECOND_FAMILY_VIEW(disputed families only)
```

### Stage B 接受条件

#### 非关键

```text
5-view MEGA majority >= 4/5
AND family_view_1 == family_view_2
AND family_answer == mega_majority
AND calibrated aggregate gate == PASS
-> AUTO_ACCEPT
```

#### critical

```text
5-view MEGA majority >= 4/5
AND family_view_1 == family_view_2
AND family_answer == mega_majority
AND critical calibrated gate == PASS
-> AUTO_ACCEPT
```

否则：

```text
ESCALATE_TO_GPT=YES
```

不得继续无限 Jev 重采样。

---

## 8. 概率融合：不只数票

多数票只作为一层证据；最终聚合使用 probability vector。

对候选答案 `a`：

```text
S(a) = Σ_j w_j * log(max(eps, p_j(a)))
P*(a) = softmax(S(a))
```

其中：

```text
eps = fixed numerical floor
w_mega = calibration-derived bounded weight
w_family = calibration-derived bounded weight
```

第一版禁止无限拟合权重。权重范围冻结为：

```text
w_mega   in [0.5, 1.5]
w_family in [1.0, 3.0]
```

只允许从离散网格中通过历史 known-answer replay 选择，目标顺序固定：

```text
1. critical autoaccepted errors = 0
2. all autoaccepted errors = 0
3. maximize auto coverage
4. minimize P95 wall-clock
5. minimize cost
```

不能为了提高 coverage 牺牲前两项。

---

## 9. 相关错误必须成为一等指标

真实验证必须保存每个 case、每个 view、每次 repeat 的 error bit。

至少计算：

```text
pairwise_error_overlap
P(E_j | E_i)
per_case_error_frequency
all-view-common-error count
mega-vs-family disagreement rate
```

解释：

- 若 `P(E_j|E_i)` 接近基础错误率，重复/集成有效；
- 若显著升高，说明系统性相关错误，需要依靠 view diversity / family anchor；
- 若存在所有 view 与 family 同方向错误，则该 case 不允许 Jev 自动控制，必须升级 GPT 或 CODE。

---

## 10. 自适应早停，而不是固定每题跑 5 次

Virtual-99 只预授权两级：

```text
Stage A = 3 diversified MEGA + family anchor
Stage B = +2 diversified MEGA + second family view, only unresolved
```

Stage A 已安全的 case 立即停止，不支付 Stage B 成本。

所以平均请求量取决于 disagreement rate，而不是固定 5×。

定义：

```text
qB   = Stage B escalation rate
qGPT = GPT escalation rate
T_expected ≈ T_A + qB*T_B + qGPT*T_GPT
```

优化对象仍是 `T_VALID`。

---

## 11. 虚拟时间与成本模型

基于当前 console evidence：

```text
MEGA P50 ≈ 1.581 s
MEGA P95 ≈ 2.200 s
FAMILY serial-total P50 ≈ 8.352 s
FAMILY serial-total P95 ≈ 9.693 s
```

Stage A 不是 3×MEGA + 5×family 串行，而是并行：

```text
T_A ≈ max(T_mega_A, T_mega_B, T_mega_C, T_family_1..5) + fusion_overhead
```

真实 `T_A` 不能从 serial total 精确推出，必须在验证时记录单请求 latency。

成本上，按当前观测单轮成本估算：

```text
3*MEGA + one full set of FAMILY anchors
≈ 3*$0.00014902 + $0.00019337
≈ $0.00064043 per Stage-A full 25-case set
```

Stage B 全量最坏上限约再增加：

```text
2*$0.00014902 + $0.00019337
≈ $0.00049141
```

即使所有 case 都进入 Stage B，Jev 总成本仍约 `$0.00113` 量级；实际只对 disputed scope rescue，应更低。

成本因此不是第一约束，正确率与 wall-clock 才是。

---

## 12. Virtual-99 冻结成功条件

虚拟方案本身现在冻结；现实验证只检查以下合同，不允许现场改算法。

### 正确性

```text
AUTO_ACCEPTED_CRITICAL_ERRORS = 0
AUTO_ACCEPTED_ANY_ERRORS      = 0
ILLEGAL_OUTPUTS               = 0
```

### 覆盖率目标

```text
AUTO_COVERAGE_TARGET >= 0.95
GPT_ESCALATION_TARGET <= 0.05
```

若达不到覆盖率目标但仍零自动错误，则状态为 `SAFE_BUT_NOT_TIME_99`，不能靠放宽错误门禁升级。

### 时间目标

```text
STAGE_A_P95_TARGET <= 4.0 s
FULL_SYSTEM_P95_TARGET <= 5.0 s on known-answer replay
```

这是现实验证目标，不是当前已认证事实。

### 成本目标

```text
MEAN_JEV_COST_PER_25_CASE_SYSTEM <= $0.0015
```

### 稳定性

```text
H3_GPU_RUNS=0
FROZEN_H3_MUTATION=0
PRIVACY_DOWNGRADE=0
SECRET_PERSISTENCE=0
```

---

## 13. 后续现实验证协议（只验证，不设计）

验证任务固定命名：

`H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02`

必须：

```text
KNOWN_ANSWER_DATASET = same 25 cases
REPEATS = 20
VIEWS = A,B,C,D,E frozen above
NO_H3_GPU_RUN
NO_PROMPT_FREE_EXPLORATION
NO_THRESHOLD_TUNING_DURING_RUN
NO_ALGORITHM_CHANGE_DURING_RUN
```

验证运行只能产生：

```text
PASS
SAFE_BUT_NOT_TIME_99
FAIL_RETURN_TO_VIRTUAL
```

如果 FAIL，只记录 reality delta，返回本 Virtual-99 层重新设计；执行器不得现场寻找新路线。

---

## 14. 最终冻结一句话

> **CODE 处理确定性事实；Jev 用 3 路多样化 MEGA + 并行 FAMILY 锚定做第一阶段，冲突时只对争议范围增加 2 路 MEGA + 第二 FAMILY 视角；概率融合与共识同时通过才自动接受，否则升级 GPT。目标不是让一次 Jev 变成 100%，而是用低成本、多视角、低相关错误和条件救援把系统级自动错误压到 0，同时逼近 MEGA 的物理时间。**
