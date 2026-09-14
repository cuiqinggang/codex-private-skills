---
name: visual-art-engine-performance-ladder
description: 管理 Visual Art Engine 从 ComfyUI 控制路径到生产 H3 的 P0-P8 性能进化；用于固定 Benchmark Contract、调用第一性原理四列法 V4.0、记录真实端到端时间、阶段 99、FREEZE/REOPEN、ΔT_STAGE 和 PATH_ARCHITECTURE_ERROR。它不替代 visual-art-engine，也不在缺少证据时宣称性能通过。
metadata:
  version: "1.0.0"
  short-description: 通用高性能视觉作品生成引擎
---

# 通用高性能视觉作品生成引擎

这是 `visual-art-engine` 的性能进化管理层，不是替代实现。运行、测量、比较和冻结任何阶段前，必须直接加载正式技能 `mature-replication-four-column`，版本必须为 V4.0（metadata `4.0.0`）；不得另造四列法。依赖核验见 [METHODOLOGY-DEPENDENCY.md](references/METHODOLOGY-DEPENDENCY.md)。

## 固定方法

固定 TASK 后，唯一评分指标是 `TIME`，正式值为 `T_END_TO_END`。质量、成功、安全与稳定性只作为 `RESULT_VALIDITY_GATE`；任务合同变化所得时间一律 `INVALID_RESULT`。

四列固定为：

1. `CURRENT`
2. `EXTERNAL FRONTIER`
3. `FIRST-PRINCIPLES PHYSICAL TIME`（第一性原理物理时间，`T_PHY` 或 `T_PHY_RANGE`）
4. `ITERATIVE CONVERGENCE`

`T_PHY` 是唯一终极参照；外部成熟方案只是现实证据与路径库。99 仅表示当前硬件、软件、环境、固定 TASK 和已知可验证方法下的现实收敛，必须保留 `PHYSICAL_GAP = T_99 - T_PHY`。

## 工作流

1. 读取 [当前状态](state/CURRENT-STATE.md) 和 [阶段台账](state/STAGE-LEDGER.json)。
2. 只允许处理第一个未锁定阶段；上一阶段必须 `score_99=true` 且 `frozen=true`，下一阶段才可解锁。
3. 冻结或重开 TASK Contract；先完成前三列，第四列才可解锁。
4. 每次只测试一个局部假设，保留原始事件、输出校验、环境与计时证据。
5. 新阶段记录 `ΔT_STAGE = T_NEW_STAGE - T_PREVIOUS_STAGE`。出现明显数量级退化时先判 `PATH_ARCHITECTURE_ERROR`，检查路径、组件、模型、参数、offload、加载、依赖、软件栈、技能调用和调度结构；不得把崩塌接受为新 baseline。
6. 达到 99 后按 [FREEZE/REOPEN 规则](docs/FREEZE-REOPEN-RULES.md)冻结，并保留 previous stable、fallback 和 archive。

## P0 入口

P0 固定为 ComfyUI API 控制路径：`REQUEST -> QUEUE -> EXECUTE -> SAVE -> RESULT`。读取 [P0 Benchmark Contract](contracts/P0-BENCHMARK-CONTRACT.md) 后再使用：

```powershell
& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoLogo -NoProfile -File .\scripts\p0\prepare-p0.ps1
python .\scripts\p0\run-p0-control.py --dry-run
```

正式运行必须显式提供 `--execute --acknowledge-contract P0-CONTROL-V1`。默认协议为 3 次 warmup、20 次 measured。没有明确执行意图时只做 readiness，不提交 workload。

## 强制边界

- v1.0.0 仅表示方法、阶梯、版本、冻结系统、P0 Contract 和 P0 工具就绪；不表示 P0 已测或已优化。
- 本版本固定声明：`P0_BENCHMARK_EXECUTED=NO`、`PERFORMANCE_OPTIMIZATION_RUN=NO`、`H3_RUN=NO`。
- 初始状态固定为：`P0_CURRENT=PENDING`、`P0_EXTERNAL=PENDING`、`P0_T_PHY=PENDING`、`P0_ITERATIVE_CONVERGENCE=LOCKED`、`P0_99=NO`。
- 历史 Wan/FAST/COLD 数据只进入 `HISTORICAL_EVIDENCE`，不得作为 P0 CURRENT。
- 普通生产任务走 `RUNTIME_FAST_PATH`。只有规定触发条件才走 `CERTIFICATION_PATH`，详见 [运行与认证分离](docs/RUNTIME-VS-CERTIFICATION.md)。
- 不修改代理、网络、WSL、系统 CUDA/Torch、健康 ComfyUI、显存/offload/allocator/attention 设置；不安装 custom node 或新依赖。
- 不修改 `visual-art-engine`、`mature-replication-four-column`、莲花或烟花成熟技能。

## 失败复盘与证据

失败记录必须含阶段、固定 TASK、期望/实际时间、原始事件、输出有效性、是否 `PATH_ARCHITECTURE_ERROR`、回滚结果和冻结基线完整性。使用 [阶段证据模板](templates/STAGE-EVIDENCE-TEMPLATE.md)，写入台账所列 `evidence_path`。任何缺少真实证据的数字保持 `null` 或 `UNKNOWN`。
