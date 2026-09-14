# Architecture

## 定位

`visual-art-engine-performance-ladder` 是性能治理与证据层。`visual-art-engine` 继续拥有视觉作品生成能力，前者不复制、替代或覆盖后者。

## 层次

- 方法层：只引用 `mature-replication-four-column` V4.0。
- 合同层：固定每个阶段的 TASK、起止点和 `RESULT_VALIDITY_GATE`。
- 阶梯层：P0-P8 只能按前一阶段 99 + FREEZE 顺序解锁。
- 执行层：生产使用 `RUNTIME_FAST_PATH`；必要变更才进入 `CERTIFICATION_PATH`。
- 证据层：原始事件、时间、输出验证、环境、外部证据和 T_PHY 推导分开保存。
- 状态层：`STAGE-LEDGER.json` 是机器可读状态；阶段 Markdown 是人类可审计合同。

## 状态流

`LOCKED_BY_PREVIOUS_STAGE -> READY_TO_MEASURE -> MEASURED -> CONVERGING -> 99 -> FROZEN`

`FROZEN` 只可在明确 REOPEN 条件触发后进入 `REOPENED`。任何 TASK 变化进入 `INVALID_RESULT`，数量级退化优先进入 `PATH_ARCHITECTURE_ERROR` 调查。

## v1.0.0 能力声明

`METHODOLOGY_INTEGRATION=READY`、`PERFORMANCE_LADDER=READY`、`VERSIONING_SYSTEM=READY`、`FREEZE_SYSTEM=READY`、`P0_CONTRACT=READY`、`P0_TOOLING=READY`。

这些均为静态系统就绪，不是性能结果。
