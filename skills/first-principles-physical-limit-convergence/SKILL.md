---
name: first-principles-physical-limit-convergence
description: 第一性原理物理极限收敛引擎。固定任务后，先计算端到端物理极限，再基于本机真实状态建立现实最优区间；由 GPT 在虚拟层完成成熟方案组合与 99 攻击，最后生成完整 Codex 命令包并确定性执行。v2.0 新增随机系统的“交付级成功/Time To First Valid Result”规则，以及 GPT-Codex-GitHub-浏览器桥接-容量路由的自动控制面。主流程仍严格保持四步，禁止 Codex 自由探索。
metadata:
  version: "2.0.0"
  short-description: 第一性原理物理极限收敛引擎·随机交付与自动闭环版
  lineage: first-principles-physical-limit-convergence@1.9.0 <- @1.8.0 <- @1.7.0 <- @1.6.0 <- @1.5.0 <- @1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理物理极限收敛引擎 v2.0.0

> 核心目标：**简单、完整、一次规划、一次执行、最后收口。**

v2.0 不增加第五步。新增内容全部是四步法的横向规则：

1. 对随机系统区分 `attempt（候选尝试）` 与 `delivery（最终交付）`；
2. 用 `T_TFVR = Time To First Valid Result（首个有效结果时间）` 评价随机系统；
3. 把 GPT/Codex 之间的文本搬运自动化为控制面，不再要求人工复制粘贴；
4. 远端模型容量、Windows执行器、浏览器运输等错误与业务算法失败分层。

---

# 一、最高规则

## 1. 当前母技能身份

```text
SKILL_ID = first-principles-physical-limit-convergence
中文名 = 第一性原理物理极限收敛引擎
VERSION = 2.0.0
CANONICAL_BRANCH = codex/first-principles-physical-limit-convergence-v2.0.0
```

历史 `absolute-time-fireworks-optimization` 只是祖先技能，不是当前母技能。

## 2. 禁止自由探索

```text
NO_FREE_EXPLORATION = YES
CODEX_ROLE = 确定性执行器 / 验证器
GPT_ROLE = 规划器 / 裁决器 / Virtual-99
```

Codex 不得自行：

- 增加新候选；
- 改候选顺序；
- 发明新实验；
- 改模型、版本、参数、阈值；
- 启用未授权 profiler / kernel trace / sweep；
- 根据一次结果继续发明下一轮。

## 3. 有限执行灵活性

Codex 可以改变“如何完成同一个授权动作”，不能改变“下一步做什么”。

允许：

- PowerShell 与 `.ps1` 等价改写；
- 绝对路径替换；
- 日志、备份、报告；
- 同一任务的 checkpoint/resume；
- 命令包明确授权的条件分支与条件循环；
- 随机系统中，若命令包已经授权 `QC FAIL -> draw new random seed -> retry same fast path`，则换种属于同一方案执行，不属于自由探索。

禁止：

- 临场新增候选；
- 改成功定义；
- 为了“看起来更快”改变任务合同；
- 把控制面故障当成业务失败；
- 因会话/模型切换而重放已经完成的本地工作。

如果既定步骤无法在边界内完成：

```text
保存证据 -> 安全停止 -> 返回 GPT
```

---

# 二、整个方法仍然只有四步

```text
第1步：物理极限
第2步：本机现实最优区间
第3步：GPT Virtual-99
第4步：Codex 完整实测命令包
```

---

# 第1步：第一性原理物理极限

先冻结：

```text
TASK
TASK_COMPLETED
CORRECTNESS
QUALITY
STABILITY
SAFETY
TIMING_BOUNDARY
ACTIVE_HARDWARE_BOUNDARY
```

正式发布一个端到端物理参照：

```text
T_PHY_TOTAL_REFERENCE
```

## 1.1 随机系统必须再冻结 attempt / delivery 语义

如果任务本质含随机变量，例如生成模型 seed、随机搜索、Monte Carlo 候选、非确定性启发式，则必须明确：

```text
ATTEMPT = 一次随机候选计算
DELIVERY = 最终允许交付给用户的有效结果
```

必须回答：

```text
随机变量是不是用户任务语义？
```

- 如果用户要求 exact seed / exact reproducibility，则 seed 属于 TASK，不能自动改；
- 如果 seed 只是内部随机初始条件，则它不是交付语义，失败后可以按冻结策略重新采样。

随机任务的物理目标仍是“在质量/正确性硬约束下最短完成”，不能因为某个随机 attempt 失败就人为提高物理极限。

---

# 第2步：本机现实最优区间

复杂任务先做最小真实执行，继承：

- 历史基线；
- P50 / P95；
- KEEP / ROLLBACK；
- GPU / VRAM / RAM；
- 驻留、加载、卸载；
- 已验证成功/失败机制；
- 当前软件与硬件约束。

然后计算：

```text
REAL_STATE_OPTIMUM_RANGE
```

## 2.1 随机任务追加现实统计

如果 attempt 可能失败，必须同时记录：

```text
FIRST_ATTEMPT_PASS_RATE
ATTEMPT_PASS_RATE
MEAN_ATTEMPTS_PER_TASK
ATTEMPTS_P50/P95/MAX
INVALID_OUTPUTS_REJECTED
INVALID_OUTPUT_DELIVERED
T_TFVR Mean/P50/P95/Max
```

正式时间指标优先使用：

```text
T_TFVR = 从 task 第一次提交，到首个通过确定性验证器并被 ACCEPT 的结果出现
```

不要只用某个固定随机样本的单次 runtime 代表用户完成时间。

---

# 第3步：GPT Virtual-99

循环只发生在 GPT 虚拟层。

## 3.1 成熟方案矩阵

每个候选至少判断：

```text
SOURCE
HARDWARE_MATCH
TASK_MATCH
MECHANISM
TARGET_BLOCK
EXPECTED_GAIN
QUALITY_RISK
STABILITY_RISK
INTEGRATION_COST
REVERSIBLE
```

## 3.2 虚拟组合

```text
CURRENT
-> mature route 1
-> mature route 2
-> interaction / duplicated gain correction
-> residual gap
-> continue until stop condition
```

对比：

```text
Virtual result
<-> REAL_STATE_OPTIMUM_RANGE
<-> T_PHY_TOTAL_REFERENCE
```

## 3.3 随机系统的优先 Virtual 模式

如果单次候选成功率已经较高，且存在可靠、便宜的 deterministic verifier（确定性验证器），必须优先评估：

```text
fast stochastic proposal
-> deterministic verifier
-> invalid proposal rejected
-> resample
-> first valid result delivered
```

这是系统级优化候选，不等于“算法不稳定所以降低标准”。

硬规则：

```text
QC 不能降低
FAIL 输出不能交付
随机 retry 不应人工挑历史 PASS seed
新 attempt 必须按冻结随机源策略产生
```

有限实验不能证明随机系统未来数学上绝对终止，因此禁止把“20/20 accepted PASS”表述为“未来任何随机序列绝对100%会终止”。

工程可冻结的是：

```text
INVALID_OUTPUT_DELIVERED = 0
FINAL_ACCEPTED_QC = certification sample all PASS
```

## 3.4 停止条件

满足任一：

1. 虚拟方案进入现实最优区间；
2. 剩余收益小；
3. 风险/成本大于收益；
4. 剩余方案不成熟；
5. 需要新的独立研究方向。

冻结：

```text
VIRTUAL_99_FINAL_PLAN
```

---

# 第4步：Codex 完整实测命令包

命令包至少包含：

```text
OBJECTIVE
CURRENT_STATE
ALLOWED_CHANGE
ALLOWED_FILES_OR_COMPONENTS
BASELINE
CANDIDATE_ORDER
SEEDS_AND_RUN_COUNT or RANDOM_SOURCE_POLICY
TIMING_BOUNDARY
QC_GATE
SUCCESS_RULE
FAILURE_RULE
ROLLBACK
GPU_BUDGET
TIME_BUDGET
FINAL_CERTIFICATION
REMOTE_FREEZE
```

## 4.1 预授权状态机

命令包可以包含确定的状态机，例如：

```text
RUN
-> QC PASS: ACCEPT
-> QC FAIL: REJECT + NEW RANDOM SEED + RUN SAME PATH
```

这不是 Codex 自由探索，因为：

- 候选没变；
- TASK 没变；
- QC 没变；
- 分支由 GPT 预先冻结；
- Codex 只是执行状态机。

## 4.2 正常执行

```text
读取技能
-> 核验版本/远端事实源
-> 读取完整命令包
-> 执行既定状态机
-> 生成证据
-> push
-> remote verify
-> STOP
```

正常 PASS/FAIL/ROLLBACK 分支不需要每一步返回 GPT。

---

# 三、失败分层规则

任何失败先分类：

```text
CONTROL_PLANE_FAILURE
EXECUTION_ENVIRONMENT_FAILURE
SOURCE_IDENTITY_FAILURE
RANDOM_ATTEMPT_QC_FAILURE
ALGORITHM_QUALITY_FAILURE
PERFORMANCE_FAILURE
DELIVERY_SYSTEM_FAILURE
```

不同层级不得混判。

例：

- `Selected model is at capacity` = 控制面容量问题，不是 GPU 算法失败；
- `TokenDefaultDacl 1344` = Windows执行环境问题；
- 随机 seed QC FAIL = 可能只是 attempt failure；
- accepted output QC FAIL = delivery system failure。

---

# 四、独立99路径

新发现的优化方向如果需要新模型/内核/版本/架构或独立研究，不插回冻结主流程。

记录为：

```text
INDEPENDENT_99_PATH
```

以后独立重复四步。

---

# 五、99 定义

99 不是距离物理极限只差 1%。

确定性任务：

```text
固定 TASK
+ 当前硬件
+ T_PHY
+ REAL_STATE_OPTIMUM_RANGE
+ Virtual-99
+ Codex实测
+ Quality/Stability/Safety PASS
+ Final Certification
+ Remote Verify
= 当前稳定最优99
```

随机任务必须标明冻结层级：

```text
SINGLE_ATTEMPT_99
或
DELIVERY_SYSTEM_99
```

不得把 90% first-attempt pass 写成 100% single-attempt success。

可以在 accepted-delivery 层冻结：

```text
FINAL_ACCEPTED_QC = 100% in certification set
INVALID_OUTPUT_DELIVERED = 0
T_TFVR distribution certified
```

---

# 六、远端共同事实源

本地路径不是共同事实源。

固定流程：

```text
远端读取
-> 本机执行
-> 报告
-> Git commit
-> push
-> remote verify
```

任何阶段报告至少保存：

```text
TASK_ID
BRANCH
LAST_REMOTE_HEAD
COMPLETED_STEPS
DO_NOT_REPEAT
NEXT_ACTION
ARTIFACT_PATHS
```

---

# 七、自动控制面

v2.0 正式支持去除人工复制粘贴。

推荐角色：

```text
GPT = planner / judge / Virtual-99
Codex = deterministic executor
GitHub = shared truth workspace / event bus
AI Browser = ChatGPT transport
Capacity Router = Codex model availability failover
Workflow Orchestrator = state machine / checkpoint / idempotency
```

## 7.1 自动闭环

```text
GPT writes PLAN + COMMAND to GitHub
-> orchestrator detects READY_FOR_CODEX
-> Codex reads exact command from GitHub
-> Codex executes locally
-> Codex writes RESULT + STATE + evidence pointers
-> push + remote verify
-> orchestrator detects RETURN_TO_GPT
-> AI Browser opens/reuses ChatGPT conversation
-> sends only new result + exact artifact refs
-> GPT judges and writes next command
-> repeat until FREEZE or BLOCKED
```

用户保留：

```text
STOP
PAUSE
APPROVE_SENSITIVE_ACTION
CHANGE_TASK_CONTRACT
```

但不再负责纯文本搬运。

## 7.2 控制面安全规则

- 自动化不得绕过登录、验证码、支付、安全提示；
- capacity 切换不得重放已完成本地工作；
- 所有写操作必须幂等；
- 每个阶段必须有 `DO_NOT_REPEAT`；
- ChatGPT/Codex 回复必须经 GitHub 状态文件确认后再推进；
- 浏览器运输失败不等于业务失败。

详细规则见：

- `references/STOCHASTIC-VERIFIED-DELIVERY.md`
- `references/AUTOMATED-GPT-CODEX-CONTROL-PLANE.md`

---

# 八、H3-P0 成功案例

v2.0 的随机交付规则来自真实 H3-P0：

```text
20 formal delivery tasks
22 total attempts
first-attempt pass = 18/20 = 90%
mean attempts = 1.10
T_TFVR mean = 6.804s
P50 = 6.076s
P95 = 11.974s
max = 12.862s
final accepted QC = 20/20
invalid output delivered = 0
```

案例事实源：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-FINAL-99-FREEZE-v1.md`

---

# 九、最终一句话

> 固定任务后，以物理时间为终极参照，在 GPT 虚拟层吸收成熟方案并冻结状态机，让 Codex 只执行；对于随机系统，不要求每个随机候选一次成功，而用严格验证器拒绝坏候选，以最快路径重新采样，最小化首个有效交付结果的端到端时间。