# 增强 Pi 长流程持续交付与故障恢复 V1.26

这是供 Gemini 网页端及其他执行者查阅的公开阅读版。先读 [SKILL.md](SKILL.md)，再按当前故障选读对应参考。历史运行标识、私有证据地址和宿主身份已脱敏，实测指标和操作约束保留。

| 需要处理的事 | 阅读入口 |
| --- | --- |
| 正式派发、接续和独立验收 | [正式派发及验收流程](references/formal-run.md) |
| 长任务中断、供应商回执缺失或写入结果未知 | [原单停滞后的接管与签收](references/stalled-order-recovery.md) |
| Temporal 原生接入与状态读回 | [Temporal 原生派发](references/temporal-native-submit.md) |
| 选用调度器、核对部署和实测边界 | [路线](references/routes.md) · [部署及演练手册](references/runbook.md) |
| 已验的本机处置与双签 | [Windows 配方](references/windows-proven-recipes.md) · [双签与实机验收](references/final-closure-v243-r2.md) |

## 执行脚本

- [admission_gate.py](scripts/admission_gate.py)
- [durable_pi_runtime.py](scripts/durable_pi_runtime.py)
- [pi_durable.py](scripts/pi_durable.py)

运行 Windows 示例时，用 `DURABLE_PI_TEMPORAL_CLI_PATH` 指向已安装的 Temporal CLI，用 `DURABLE_PI_TEMPORAL_SDK_PATH` 指向已验的 SDK 目录。默认文件位置相对于当前用户的 `Documents/DurablePi`。正式订单沿用各项目的冻结合同、原业务键和实际入口。
