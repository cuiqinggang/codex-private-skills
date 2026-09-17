# FIRST-PRINCIPLES LIMIT MODEL — v1.8.0

## 1. 唯一正式物理极限标准

同一固定任务下，忽略历史实现和人为流程，只保留物理上不可避免的工作。正式对外只发布：

```text
T_PHY_TOTAL_REFERENCE=<一个端到端时间数字或区间>
```

其内部推导可以使用：

```text
COMPUTE_FLOOR
MEMORY_TRAFFIC_FLOOR
MANDATORY_TRANSFER_FLOOR
SERIAL_DEPENDENCY_FLOOR
SYNCHRONIZATION_FLOOR
I/O_FLOOR
OTHER_IRREDUCIBLE_FLOOR
```

若多个不可避免步骤必须严格串行，则沿 critical path 求和；能真正重叠的只计算重叠后的临界路径，不重复计账。

这些分量、公式、DAG、假设和置信度都是**推导工作底稿**，不得与 `T_PHY_TOTAL_REFERENCE` 并列形成多指标“物理极限板”。

## 2. 当前机器现实能力不是第二个物理极限标准

历史文档曾使用 `T_MACHINE_STAR` / `T_MACHINE_STAR_REAL`。从 v1.7.0 起，它们不再作为正式并列物理极限目标。

当前软件栈、硬件利用率、驻留、调度、缓存、offload、框架限制等现实条件统一进入：

```text
REAL_STATE_MODEL
```

必要时 GPT 可以在内部形成现实可达时间区间或经验边界，但它属于工程判断/候选排序证据，不得形成第二个与 `T_PHY_TOTAL_REFERENCE` 平级的“终极参照”。

历史项目报告中的 `T_MACHINE_STAR*` 字段可以作为历史证据保留，不得自动推广为新任务的正式标准。

## 3. 先建物理 DAG，不先抄现有流程

候选节点标记：

```text
PHYSICALLY_REQUIRED
CAUSALLY_REQUIRED
IMPLEMENTATION_REQUIRED_CURRENTLY
OPTIONAL
ARMOR_CANDIDATE
```

依赖标记：

```text
SERIAL
PARALLELIZABLE
OVERLAPPABLE
PRECOMPUTABLE
CACHEABLE
PERSISTABLE
MOVE_AFTER_RESULT_READY
```

DAG 的用途是推导单一 `T_PHY_TOTAL_REFERENCE` 和解释现实 Gap，不是制造额外 KPI。

## 4. 不确定性不等于停止，也不允许伪精确

对 kernel efficiency、memory bandwidth utilization、occupancy、cache hit、transfer overlap、model residency、allocator/scheduler jitter、thermal/power sustainable state 等建立内部 `ASSUMPTION_LEDGER`：

```text
LOW
BASE
HIGH
CONFIDENCE
SOURCE
SENSITIVITY
```

高不确定性时扩大 `T_PHY_TOTAL_REFERENCE` 区间并说明置信度；不能为了“只有一个数字”而伪造精确单点。

低敏感未知量不允许触发大规模实测；高敏感未知量只有在 GPT 完整铁路预定义后才允许进入最小必要验证。

## 5. 现实结果用于校准假设，不用于移动物理极限讨好当前结果

MRE / 后续验证若与预测差异大，应检查：

- 假设错误；
- 任务合同漂移；
- 隐藏的物理步骤；
- 软件实现限制；
- 测量错误；
- 并行/重叠判断错误。

只有新证据证明原物理模型的某个假设错误时，才允许版本化修订 `T_PHY_TOTAL_REFERENCE`：

```text
OLD_T_PHY_TOTAL_REFERENCE
NEW_T_PHY_TOTAL_REFERENCE
REASON
NEW_EVIDENCE
ASSUMPTION_INVALIDATED
```

禁止为了让当前实测更接近“99”而放宽物理极限参照。

## 6. 外部成熟方案

```text
EXTERNAL_REFERENCE=OPTIONAL_EVIDENCE
```

只用于 sanity check、成熟实现复用、候选排序和漏项检查；成熟方案本身不是物理极限。

## 7. 优化方向

统一比较：

```text
CURRENT / CANDIDATE / FINAL
↔ T_PHY_TOTAL_REFERENCE
```

真正要攻击哪个现实时间块，由 GPT 基于 `REAL_STATE_MODEL`、成熟证据、绝对可消灭时间、风险、验证成本和组合生命周期 ROI 决定。

Codex 不得从这个模型自行推导并执行下一实验；所有实验必须来自 GPT 的完整验证铁路。
