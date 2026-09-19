# H3-P0 Jev Probability-Attack Verify-02 Command v1

状态：`FROZEN_VALIDATION_COMMAND / DO_NOT_RUN_UNTIL_EXPLICITLY_REQUESTED`

任务：`H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02`

## 0. 唯一目的

现实环境只验证已经冻结的 Virtual-99 算法，不允许边运行边改方案。

权威设计：

```text
skills/first-principles-physical-limit-convergence/references/JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.md
skills/first-principles-physical-limit-convergence/references/JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.json
```

如果验证失败：记录 reality delta -> STOP -> 返回 GPT Virtual-99。执行器不得自行修正算法。

## 1. 固定输入

```text
DATASET=docs/h3-p0/20260919-jev-shadow/H3-P0-JEV-SHADOW-DATASET-v1.json
KNOWN_ANSWER_CASES=25
REPEATS=20
MODEL=typesafe/jev-1.13
H3_GPU_RUNS=0
```

原 H3-P0 FINAL_99 全部只读。

## 2. 冻结 View

只允许 Virtual-99 文件定义的 A/B/C/D/E 五个等义 view。

禁止：

```text
运行时自由改写 prompt
运行时新增候选
根据中途结果改变 view 定义
根据中途结果改变阈值选择算法
改变答案空间
向 state 注入 gold answer
```

## 3. Stage A

同时启动：

```text
MEGA_A
MEGA_B
MEGA_C
FAMILY anchors for all families
```

要求真实并发；记录每个 HTTP request 的：

```text
start_ns
end_ns
latency_ms
cost
model
provider
view_id
family_id if any
```

不得用串行总和冒充并行 wall-clock。

## 4. Stage A Gate

完全按 Virtual-99：

```text
noncritical: family == mega majority >=2/3 + calibrated gate
critical: family == A == B == C + calibrated gate
```

Stage A 已接受 case 不得进入 Stage B。

## 5. Stage B

仅 unresolved scope，并行：

```text
MEGA_D
MEGA_E
SECOND_FAMILY_VIEW(disputed families only)
```

接受条件完全按冻结 JSON；否则 `ESCALATE_TO_GPT`。本次 known-answer 验证只记录 GPT escalation，不实际调用 GPT 改答案，避免把 Jev 子系统能力与 GPT 能力混合。

## 6. 概率融合与权重

只允许冻结网格：

```text
w_mega   ∈ {0.5,0.75,1.0,1.25,1.5}
w_family ∈ {1.0,1.5,2.0,2.5,3.0}
```

选择优先级固定：

```text
zero critical auto errors
-> zero all auto errors
-> maximum auto coverage
-> minimum P95 wall-clock
-> minimum cost
```

不得为了 coverage 牺牲零错误门禁。

## 7. 防过拟合

权重/门禁评价必须使用 leave-one-case-out replay：每次留出 1 个 case，只用其余 case 选择允许网格参数，再评价被留出的 case；25 case 全部轮换。

如果某个 family case 数过少导致参数不可识别，使用全局冻结默认权重：`w_mega=1.0, w_family=2.0`，不得现场手工挑选。

## 8. 必须计算的误差结构

保存每个 repeat × case × view 的：

```text
predicted answer
full probability vector
correct bit
confidence
```

并计算：

```text
pairwise_error_overlap
conditional_error_persistence P(Ej|Ei)
per_case_error_frequency
all_view_common_error_count
mega_family_disagreement_rate
```

## 9. 验收

PASS 必须同时满足：

```text
AUTO_ACCEPTED_CRITICAL_ERRORS=0
AUTO_ACCEPTED_ANY_ERRORS=0
ILLEGAL_OUTPUTS=0
AUTO_COVERAGE>=0.95
GPT_ESCALATION_RATE<=0.05
STAGE_A_P95_SECONDS<=4.0
FULL_SYSTEM_P95_SECONDS<=5.0
MEAN_JEV_COST_PER_25_CASE_SYSTEM_USD<=0.0015
H3_GPU_RUNS=0
FROZEN_H3_MUTATION=0
PRIVACY_DOWNGRADE=0
SECRET_PERSISTENCE=0
```

如果零错误满足但时间/覆盖率未达到：

`SAFE_BUT_NOT_TIME_99`

任何自动接受错误：

`FAIL_RETURN_TO_VIRTUAL`

## 10. 输出

只生成：

```text
H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02-RESULT-v1.json
H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02-RESULT-v1.md
```

结果必须含：

```text
ROLE
AUTO_COVERAGE
GPT_ESCALATION_RATE
CRITICAL_AUTO_ERRORS
ALL_AUTO_ERRORS
STAGE_A_P50/P95
FULL_SYSTEM_P50/P95
MEAN/P95_COST
VIEW_ERROR_CORRELATION
COMMON_ERROR_CASES
WEIGHTS_SELECTED_BY_LOO
REMOTE_HEAD
```

## 11. 固定停止条件

本命令执行结束后必须 STOP。

禁止自动：

```text
升级 v3.1.3
改 Virtual-99
跑 H3 GPU
增加新模型
重新设计 prompt
```

---

一句话：**验证器只负责证明冻结的 Jev Virtual-99 是否成立，不负责把失败方案现场修好。**
