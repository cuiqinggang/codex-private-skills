# HARDWARE TOPOLOGY FRONTIER（硬件拓扑前沿门禁）

本规则属于 `first-principles-physical-limit-convergence v1.1.0`。

## 核心边界：只用当前真实可用硬件定义本轮 99

`T_MACHINE_STAR（本机稳定理论极限）` 与 `99（当前稳定最优）` 的硬件边界，必须冻结为：

```text
ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）
= 此刻已经真实安装 + 可正常使用 + 本任务允许使用的硬件
```

未来计划购买、尚未安装、当前不可用或尚未接入的硬件，不进入本轮 `T_MACHINE_STAR`，也不得成为本轮 `99=YES` 的阻断条件。

例如当前只有一张 22GB 主 GPU 可用于任务，而未来可能增加一张 8GB 辅 GPU：

```text
CURRENT ROUND（本轮）:
ACTIVE_HARDWARE_BOUNDARY = 单 22GB GPU
=> 先把当前单卡系统真实收敛到自己的 99

FUTURE ROUND（未来硬件改变后）:
ACTIVE_HARDWARE_BOUNDARY = 22GB + 8GB 双 GPU
=> 重新扫描硬件拓扑
=> 重新计算 T_MACHINE_STAR
=> 重新开启新的 Gap 收敛
```

这不是“旧 99 作废”，而是任务资源边界改变后产生新的版本化极限。

## 目标

在 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）` 内，`T_MACHINE_STAR（本机稳定理论极限）` 不只取决于单个 GPU 型号，也取决于整台机器实际存在的资源拓扑：

```text
实际安装的 GPU 数量与容量
PCIe 代际/通道宽度
显示器连接位置
主卡/辅卡职责
CPU / RAM / PCIe 共享路径
模型、VAE、文本编码器驻留位置
跨 GPU 数据传输
软件是否真正支持多 GPU
```

因此 99 前必须检查：在**当前真实存在的硬件**中，是否存在比当前分工更快、更稳定的硬件拓扑。

如果当前只有一张 GPU，则：

```text
HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）
= 单卡拓扑已冻结并验证
= PASS
```

不得为了不存在的第二张 GPU 延迟本轮 99。

## 双 GPU 三种正式候选

以下候选**只在第二张 GPU 已真实安装并可用时触发**。

### MODE A — DISPLAY OFFLOAD（显示卸载）

把显示器、桌面合成、浏览器/普通 UI 等尽量放到辅助 GPU；主 GPU 专用于目标任务。

适用于：
- 主 GPU VRAM 紧张；
- Windows 桌面/多屏占用可观；
- 固定任务本身只需要一张 GPU 完成核心计算。

必须真实记录主 GPU idle VRAM（空闲显存）、context（上下文）和正式 benchmark（基准测试）的变化。

### MODE B — FUNCTION SPLIT（功能拆分）

不同模型/阶段放不同 GPU，例如：

```text
PRIMARY GPU（主卡） = diffusion / sampler（扩散模型 / 采样器）
SECONDARY GPU（辅卡） = VAE / CLIP / preview / encode / auxiliary models（VAE / 文本编码 / 预览 / 编码 / 辅助模型）
```

前提：对应软件栈真正支持设备选择；任务结果完全相同；跨 GPU 传输成本低于释放主卡显存/减少换入换出的收益。

### MODE C — JOINT COMPUTE（联合计算）

两张 GPU 同时计算同一个核心模型，例如 tensor / sequence / pipeline / work-unit parallelism（张量 / 序列 / 流水线 / 工作单元并行）。

只有满足以下条件才进入正式候选：
- 当前软件有成熟实现；
- 两张 GPU 的 VRAM、算力、互联足够；
- 不因 PCIe 同步/拷贝抵消收益；
- 相同任务真实 benchmark 更快；
- 稳定性与结果一致性通过。

`MORE_GPUS != AUTOMATICALLY_FASTER（GPU 更多不自动等于更快）`。

## PCIe Gate（PCIe 门禁）

只有安装第二张 GPU 后才触发双卡 PCIe 对比。必须比较安装前后主 GPU：

```text
PCIE_GEN（PCIe代际）
PCIE_LINK_WIDTH（PCIe链路宽度）
```

如果主卡从例如 x16 降为 x8，必须把新增传输成本加入 `T_MACHINE_STAR` 和真实 benchmark。

对于存在 CPU↔GPU offload（卸载）的模型，PCIe 带宽下降可能抵消第二张卡带来的收益。

禁止只凭“多一张卡”宣布优化。

## 不同容量 GPU 的分工原则

不能把 VRAM 简单相加：

```text
22GB + 8GB != 一个透明的 30GB GPU
```

除非具体软件实现了模型切分，否则每块 GPU 都有独立 VRAM。

优先把能完整放进辅助卡、且与主 GPU 可清晰解耦的对象放到辅助卡。

例如某任务中：
- 20GB 模型不能放进 8GB 辅卡；
- 15GB 文本编码器不能放进 8GB 辅卡；
- 5GB VAE 可能成为 8GB 辅卡候选，但仍需考虑运行 workspace（工作区）和跨 GPU 传输。

## Benchmark Matrix（基准测试矩阵）

当双 GPU 已真实存在时，至少比较：

```text
A0 = 单主卡 / 当前连接
A1 = 双卡安装，但核心任务仍只用主卡
A2 = 双卡 + 显示器全部迁到辅卡
A3 = 双卡 + 显示迁移 + 功能拆分（若成熟支持）
A4 = 双卡联合计算（仅当成熟支持）
```

固定同一 TASK_CONTRACT（任务合同）、输入、seed 集合、计时边界与软件版本。

选择：

```text
BEST_HARDWARE_TOPOLOGY（最佳硬件拓扑）
= 在当前有效硬件边界内，所有硬约束通过时 T_EXEC 最小的配置
```

## 经验回灌：下一次重新计算必须使用本次真实数据

每次 99/FREEZE（99/冻结）后，应把真实分块数据、已证实有效/无效机制、Failure Index（失败索引）、稳定驻留点、模型切换成本、VAE/编码/传输成本等写入 `EMPIRICAL_PRIORS（经验先验）`。

当未来发生以下变化时：

```text
硬件增加/更换
关键软件栈重大升级
模型格式或推理后端改变
任务合同改变
```

重新计算 `T_MACHINE_STAR` 时，不得从零猜测；必须先继承最近一次兼容的真实经验：

```text
OLD VERIFIED 99（旧的已验证99）
+ EMPIRICAL_PRIORS（经验先验）
+ NEW HARDWARE/SOFTWARE FACTS（新的硬件/软件事实）
=> NEW T_MACHINE_STAR（新的本机稳定理论极限）
=> NEW ATTACK_ORDER（新的攻击顺序）
```

如果旧经验与新条件不兼容，则明确降级其置信度，而不是静默沿用。

## 99 Gate（99 门禁）

本轮门禁只针对 `ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）`。

```text
CURRENT_AVAILABLE_HARDWARE_AUDITED=YES（当前可用硬件已审计）
NO_UNTESTED_HIGH_VALUE_TOPOLOGY_WITHIN_ACTIVE_BOUNDARY=YES（当前边界内无未测试高价值拓扑）
=> HARDWARE_TOPOLOGY_GATE=PASS（硬件拓扑门禁通过）
```

未来硬件不参与本轮门禁。

门禁 PASS 不等于必须使用多 GPU；如果当前只有单 GPU，或者真实结果证明单 GPU 更快，单 GPU 可以成为正式 winner（胜出方案）。
