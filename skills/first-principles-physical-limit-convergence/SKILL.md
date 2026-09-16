---
name: first-principles-physical-limit-convergence
description: 在固定任务和硬约束下，以时间为唯一优化目标；先冻结 ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界），计算 T_PHY（物理极限）和 T_MACHINE_STAR（当前有效硬件 + 最佳成熟软件栈下的稳定理论极限），再从去重甲 V1 开始按最大绝对 Gap（差距）迭代，并在 99 前强制通过 Software Frontier Gate（软件前沿门禁）与当前硬件边界内的 Hardware Topology Gate（硬件拓扑门禁）。
metadata:
  version: "1.1.0"
  short-description: 第一性原理物理极限收敛引擎·软件/硬件边界版
  lineage: first-principles-physical-limit-convergence@1.0.0 <- absolute-time-fireworks-optimization@2.0.1
---

# 第一性原理物理极限收敛引擎 v1.1.0

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END（最小化真实端到端时间）

SUBJECT TO（硬约束）:
TASK_COMPLETED == TRUE（任务真实完成）
CORRECTNESS == PASS（正确性通过）
QUALITY >= FIXED_THRESHOLD（质量达到固定阈值）
STABILITY >= FIXED_THRESHOLD（稳定性达到固定阈值）
SAFETY == PASS（安全通过）
TASK_CONTRACT == IDENTICAL（任务合同保持一致）
```

本版继承 v1.0.0 的两步法、去重甲、KEEP/ROLLBACK（保留/回滚）、多智能体资源约束、Shared Fact Source（共同事实源）和 99/FREEZE（99/冻结），新增两条硬规则：

> **软件规则：本机极限不由“当前已安装软件”定义，而由当前可获得、成熟、兼容、可验证的最佳软件栈定义。**

> **硬件规则：本轮 99 只由 ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）定义；未来计划增加但当前不存在的硬件，不得阻断当前 99。**

“最新版”只是候选；“最优化版”必须通过同任务真实 benchmark（基准测试）证明更快后才获得正式地位。

---

## STEP 1 — CALCULATE（第一步：计算）

先冻结：

```text
TASK_CONTRACT（任务合同）
ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
```

其中：

```text
ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
= 此刻已经真实安装 + 可正常使用 + 本任务允许使用的硬件
```

尚未安装、未来计划购买或当前不可用的硬件不进入本轮目标。

然后计算：

```text
T_PHY（物理极限）
= 同一固定任务在已冻结硬件边界、物理规律和不可避免工作约束下的绝对下界区间

T_MACHINE_STAR（本机稳定理论极限）
= 同一固定任务在 ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
  + 当前边界内最佳硬件拓扑
  + 当前可获得最佳成熟兼容软件栈
  + 已验证 EMPIRICAL_PRIORS（经验先验）下，
  正确、稳定、可持续运行的理论极限区间
```

硬不变量：

```text
T_MACHINE_STAR >= T_PHY
```

### STEP 1 必须继承 Empirical Priors（经验先验）

如果存在以前兼容的真实 99、阶段测试或失败复盘，禁止从零猜测。必须优先继承：

- VERIFIED_99（已验证99）；
- 分块 P50/P95；
- 已证实有效的 KEEP（保留）机制；
- 已证伪的 ROLLBACK（回滚）机制；
- Failure Index（失败索引）；
- 模型加载、卸载、VAE、编码、传输等真实成本；
- 稳定 VRAM（显存）边界与资源竞争事实。

当硬件/软件条件改变时，以：

```text
OLD VERIFIED FACTS（旧验证事实）
+ EMPIRICAL_PRIORS（经验先验）
+ NEW HARDWARE/SOFTWARE FACTS（新硬件/软件事实）
=> NEW T_MACHINE_STAR（新的本机稳定理论极限）
```

不兼容的旧经验降低置信度，而不是静默沿用。

### STEP 1 必须包含 Software Frontier Scan（软件前沿扫描）

在计算 `T_MACHINE_STAR` 时，不得只读取当前已安装版本。必须检查与关键路径相关的软件层：

- GPU driver（显卡驱动）；
- CUDA / PyTorch（CUDA / PyTorch运行时）；
- ComfyUI / inference runtime（ComfyUI / 推理运行时）；
- model kernels / quant ops（模型内核 / 量化算子）；
- attention backend（注意力后端）；
- compiler / graph capture（编译器 / 图捕获）；
- memory allocator / prefetch / offload（内存分配 / 预取 / 卸载）；
- model format / quantization（模型格式 / 量化实现）；
- VAE / codec / output path（VAE / 编码器 / 输出路径）；
- 与固定任务关键路径直接相关的成熟第三方优化。

每个候选分类：

```text
CURRENT（当前已安装）
LATEST_STABLE（官方最新稳定版）
MATURE_OPTIMIZED（成熟优化版）
EXPERIMENTAL（实验版）
```

只有前 3 类可进入正式 99 候选；`EXPERIMENTAL（实验版）` 默认只做研究，不直接进入最终冻结。

### 最佳软件栈定义

```text
BEST_SOFTWARE_STACK（最佳软件栈）
= argmin_stack T_EXEC（任务实际执行时间）
```

但必须同时满足：

```text
TASK_CONTRACT_IDENTICAL=YES（任务一致）
HARD_CONSTRAINTS_PASS=YES（硬约束通过）
STABILITY_PASS=YES（稳定通过）
COMPATIBILITY_PASS=YES（兼容通过）
REPRODUCIBLE=YES（可复现）
```

因此：

```text
LATEST != AUTOMATIC_WINNER
（最新版不自动等于最优版）
```

### Hardware Topology Scan（硬件拓扑扫描）

只扫描 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）` 内真实存在的硬件。

如果当前只有一张 GPU，则单卡就是本轮硬件边界；未来第二张 GPU 不进入本轮 `T_MACHINE_STAR` 和 99 门禁。

如果未来第二张 GPU 实际安装，资源边界发生变化，则重新计算新的 `T_MACHINE_STAR`，旧 99 作为经验先验继续继承。

详细规则见 `references/HARDWARE-TOPOLOGY-GATE.md`。

### 第一步必须产出

- `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`；
- `T_PHY=[LOW,HIGH]（物理极限区间）`；
- `T_MACHINE_STAR=[LOW,HIGH]（本机稳定理论极限区间）`；
- `EMPIRICAL_PRIORS（经验先验）`；
- `CURRENT_STACK（当前软件栈）`；
- `SOFTWARE_FRONTIER_CANDIDATES（软件前沿候选）`；
- `BEST_KNOWN_STACK_ASSUMPTION（当前最佳栈假设）`；
- `PHYSICAL_DAG（物理因果图）`；
- `ASSUMPTION_LEDGER（假设账本）`；
- `ATTACK_ORDER（攻击顺序）`；
- 多智能体模式。

未知效率优先写成区间，不因缺少一次新实测而取消第一性原理计算。

---

## STEP 2 — CONVERGE（第二步：收敛）

先继承兼容的冻结 99，不为展示提升百分比故意退回慢版本。

建立：

```text
V1 = FIRST MINIMUM VIABLE EXECUTION（第一最小正确执行版本）
```

V1 是去重甲后的第一个可测版本，不要求已经使用最终最佳软件栈。

每轮：

```text
DELTA_T_REDUCIBLE_i（可消灭时间差）
= T_CURRENT_BLOCK_i - T_MACHINE_TARGET_BLOCK_i

NEXT_ATTACK（下一攻击）
= argmax_i(DELTA_T_REDUCIBLE_i)
```

真实修改后：

```text
FASTER + HARD_CONSTRAINTS_PASS => KEEP（保留）
ELSE => ROLLBACK（回滚）
```

持续：

```text
V1 -> V2 -> V3 -> ...
```

但**在任何 99 / FREEZE 之前，必须通过 Software Frontier Gate（软件前沿门禁），以及当前有效硬件边界内的 Hardware Topology Gate（硬件拓扑门禁）**。

---

# SOFTWARE FRONTIER GATE（软件前沿门禁）

## 触发时机

以下任一发生时必须执行：

1. STEP 1 初次计算 `T_MACHINE_STAR`；
2. 当前候选已经接近旧目标区间；
3. 准备声明 `99=YES`；
4. 距上次前沿扫描期间出现相关软件重大新版本；
5. 新 release / commit 明确修改了当前任务关键路径相关代码。

## 候选优先级

优先测试预计高收益、低风险候选：

```text
Tier A（A档）= 运行时/框架/内核/内存管理/编译器更新
Tier B（B档）= 模型格式、量化、注意力、VAE、codec 等成熟替代实现
Tier C（C档）= driver / CUDA / 系统级更新
```

Tier C 系统级候选只有在有明确收益证据和安全回滚路径时才进入；不得为了追“最新”随意破坏稳定环境。

## 测试方式

软件前沿候选必须在隔离 branch/worktree/compat-lab（分支/工作树/兼容实验区）中测试：

```text
CURRENT_BEST（当前最佳）
vs
SOFTWARE_CANDIDATE（软件候选）
```

固定：

```text
TASK_CONTRACT（任务合同）
INPUT（输入）
SEEDS（随机种子集合）
TIMING_BOUNDARY（计时边界）
RESOURCE_STATE（资源状态）
QUALITY_GATE（质量门禁）
```

只有真实更快且稳定：

```text
SOFTWARE_CANDIDATE_WINS=YES（软件候选胜出）
=> KEEP（保留）
=> 更新 BEST_SOFTWARE_STACK（最佳软件栈）
=> 必要时重新计算 T_MACHINE_STAR（本机稳定理论极限）
```

否则：

```text
ROLLBACK（回滚）
```

## 软件前沿与物理极限的关系

软件升级不能改变已冻结硬件边界下正确的 `T_PHY（物理极限）`，但可以显著降低软件造成的效率损失，使现实结果更接近 `T_PHY`。

因此：

```text
T_PHY（物理极限）
= 当前有效硬件边界 + 物理规律参照

T_MACHINE_STAR（本机稳定理论极限）
= 当前有效硬件边界 + 当前边界内最佳硬件拓扑 + 当前最佳成熟软件栈 + 经验先验参照

T_CURRENT（当前实测）
= 当前实际实现
```

软件进步时，`T_MACHINE_STAR` 可以因为新证据而下修；硬件边界改变时，应建立新的版本化 `T_MACHINE_STAR`。必须记录：

```text
OLD_BOUNDARY（旧硬件边界）
NEW_BOUNDARY（新硬件边界，如有）
OLD_STACK（旧软件栈）
NEW_STACK（新软件栈）
OLD_TARGET（旧目标）
NEW_TARGET（新目标）
BENCHMARK_EVIDENCE（基准证据）
REASON（修订原因）
```

禁止因为当前结果慢而把目标往上放宽。

---

## 多智能体

多智能体优化 `T_CONVERGENCE（收敛工程时间）`，不自动优化单次 `T_EXEC（任务执行时间）`。

```text
AGENT_MODE = OFF | SUPPORT_PARALLEL | RESOURCE_PARTITIONED
```

对单 GPU 正式 benchmark：

```text
GPU_BENCHMARK_SERIAL=YES（GPU正式基准串行）
GPU_EXCLUSIVE=YES（GPU独占）
```

软件前沿扫描适合并行拆分：官方最新版、成熟第三方优化、兼容性/风险、benchmark 审计可由不同只读智能体并行完成。

---

## 继承的成熟纪律

继续继承：TASK_COMPLETED（任务完成边界）、De-Armoring（去重甲）、真实端到端计时、CUDA Event（CUDA事件）、KEEP/ROLLBACK（保留/回滚）、99/FREEZE（99/冻结）、可逆 instrumentation（插桩）、已有事实优先、Failure Index（失败索引）、dirty worktree（工作树保护）、Shared Fact Source（共同事实源）、精确 stage（精确暂存）、禁止 `git add .` / force push / `reset --hard`、remote verify（远端验证）。

---

## SHARED FACT SOURCE CLOSURE GATE（共同事实源收口门禁）

```text
SHARED_FACT_SOURCE=cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SHARED_REPO_SYNC_REQUIRED=YES
```

产生新工程事实时：

```text
LOCAL RESULT（本机结果）
-> FORMAL REPORT（正式报告）
-> SHARED REPOSITORY（共同仓库）
-> EXACT STAGE（精确暂存）
-> COMMIT（提交）
-> PUSH（推送）
-> REMOTE VERIFY（远端验证）
```

只有：

```text
LOCAL_TASK_RESULT=PASS（本机任务通过）
AND SHARED_REPO_SYNC=PASS（共同仓库同步通过）
AND SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）
AND HARDWARE_TOPOLOGY_GATE=PASS（当前硬件拓扑门禁通过）
```

才允许最终：

```text
99=YES
FREEZE=YES
FINAL=PASS
```

---

## 99 / FREEZE（99 / 冻结）

99 不是数学绝对极限，也不是固定 1% 阈值。

必须同时满足：

1. 固定任务真实完成；
2. hard constraints（硬约束）全部通过；
3. 权威计时稳定；
4. 当前结果进入或贴近高置信 `T_MACHINE_STAR`；
5. 没有明显大块重甲；
6. 没有高置信高收益剩余 Gap；
7. `SOFTWARE_FRONTIER_GATE=PASS（软件前沿门禁通过）`；
8. 已比较当前版本、最新稳定版和主要成熟优化候选；
9. 最终采用栈已真实 benchmark 证明是当前最佳已知可复现方案；
10. `HARDWARE_TOPOLOGY_GATE=PASS（当前硬件拓扑门禁通过）`；
11. `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）` 已明确冻结，未来不存在的硬件不参与本轮门禁；
12. Shared Fact Source closure（共同事实源收口）PASS。

因此：

> **99 = 当前真实可用硬件边界 + 当前边界内最佳硬件拓扑 + 当前最佳成熟兼容软件栈 + 当前已知可验证方法下的稳定最优。**

当未来增加硬件或关键软件发生重大变化时：

```text
旧 99 不直接冒充新 99
旧 99 也不作废
```

而是：

```text
OLD 99（旧99）
+ EMPIRICAL_PRIORS（经验先验）
+ NEW FACTS（新事实）
=> NEW T_MACHINE_STAR（新本机稳定理论极限）
=> 新一轮收敛
```

---

## 默认最短读取路径

正常任务读取：

1. `SKILL.md`
2. `references/FAST-PATH.md`

按需读取：

- `references/FIRST-PRINCIPLES-LIMIT-MODEL.md`
- `references/SOFTWARE-FRONTIER-GATE.md`
- `references/HARDWARE-TOPOLOGY-GATE.md`
- `references/MULTI-AGENT-PARALLELISM.md`
- `references/EXECUTION-BRIDGE.md`
- `references/EXECUTION-CLOSURE-CONTRACT.md`
- `references/FAILURE-INDEX.md`

## 状态

```text
SKILL_VERSION=1.1.0
TWO_STEP_METHOD=PASS（两步法通过）
ACTIVE_HARDWARE_BOUNDARY_DEFINED=PASS（当前有效硬件边界已定义）
EMPIRICAL_PRIOR_REUSE_DEFINED=PASS（经验先验复用已定义）
SOFTWARE_FRONTIER_GATE_DEFINED=PASS（软件前沿门禁已定义）
HARDWARE_TOPOLOGY_GATE_DEFINED=PASS（硬件拓扑门禁已定义）
BEST_SOFTWARE_STACK_REQUIRED_FOR_99=YES（99必须验证最佳软件栈）
FUTURE_UNAVAILABLE_HARDWARE_BLOCKS_CURRENT_99=NO（未来不可用硬件不阻断当前99）
LEGACY_INHERITANCE_REVIEW=PASS（继承审查通过）
MULTI_AGENT_POLICY_DEFINED=PASS（多智能体策略已定义）
```
