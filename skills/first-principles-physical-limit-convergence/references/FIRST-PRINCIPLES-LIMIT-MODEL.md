# FIRST-PRINCIPLES LIMIT MODEL

## 1. 两个目标区间

### T_PHY

同一固定任务下，忽略历史实现和人为流程，只保留物理上不可避免的工作：

```text
T_PHY >= max(
  COMPUTE_FLOOR,
  MEMORY_TRAFFIC_FLOOR,
  MANDATORY_TRANSFER_FLOOR,
  SERIAL_DEPENDENCY_FLOOR,
  SYNCHRONIZATION_FLOOR,
  I/O_FLOOR,
  OTHER_IRREDUCIBLE_FLOOR
)
```

若多个不可避免步骤必须严格串行，则沿 critical path 求和；能真正重叠的只取重叠后的临界路径，不重复计账。

### T_MACHINE_STAR

将当前机器的真实资源、软件和稳定条件加入：

```text
T_MACHINE_STAR = F(
  T_PHY,
  hardware_capacity,
  sustainable_efficiency_range,
  memory_capacity,
  bandwidth,
  bus/transfer,
  software/runtime constraints,
  resource residency,
  scheduler/runtime overhead that is not safely eliminable,
  hard constraints
)
```

首选输出 `T_MACHINE_STAR=[LOW,HIGH]` 和 `CONFIDENCE=HIGH|MEDIUM|LOW`，不强制伪精确单点。

## 2. 先建 DAG，不先抄现有流程

候选节点标记：`PHYSICALLY_REQUIRED / CAUSALLY_REQUIRED / IMPLEMENTATION_REQUIRED_CURRENTLY / OPTIONAL / ARMOR_CANDIDATE`。

依赖标记：`SERIAL / PARALLELIZABLE / OVERLAPPABLE / PRECOMPUTABLE / CACHEABLE / PERSISTABLE / MOVE_AFTER_RESULT_READY`。

## 3. 不确定性不等于停止

对 kernel efficiency、memory bandwidth utilization、occupancy、cache hit、transfer overlap、model residency、allocator/scheduler jitter、thermal/power sustainable state 等建立 `ASSUMPTION_LEDGER`：LOW/BASE/HIGH/CONFIDENCE/SOURCE/SENSITIVITY。

低敏感未知量不允许触发大规模实测；高敏感未知量列入 V1 最低必要测量。

## 4. 现实结果用于验证模型，不用于定义物理规律

第一次运行后：

```text
MODEL_ERROR = MEASURED_V1 - PREDICTED_V1_RANGE
```

若偏差大，追踪假设错误、合同漂移、隐藏物理步骤、软件实现限制、测量错误或可并行性误判。

允许更新 `T_MACHINE_STAR`，但必须版本化记录 OLD_RANGE/NEW_RANGE/REASON/NEW_EVIDENCE/ASSUMPTION_INVALIDATED。禁止为了让当前结果接近 99 而移动目标。

## 5. 外部成熟方案

`EXTERNAL_REFERENCE = OPTIONAL_EVIDENCE`。只用于 sanity check、成熟实现复用和漏项检查。

## 6. 最短攻击路线

```text
DELTA_i = CURRENT_i - MACHINE_TARGET_i
NEXT_ATTACK = argmax_i(DELTA_i)
```

优先最大绝对可节省时间，而不是最大百分比。正确性、稳定性、质量、安全均为 hard constraints。
