# Changelog

## Unreleased / Measurement Protocol V2 UNDER_VALIDATION - 2026-09-15

- 引入同期 interleaved paired A/B、A/A calibration、order equivalence、environment drift 与 confirmation 规则；历史固定 baseline 不再裁决微优化。
- 增加 null Type-I calibration：同时报告正向 false KEEP 与任意方向 rejection；null PASS 前 `FINAL_MDE_MS=UNKNOWN`。
- MDE 改为在正式 KEEP 管线与 block 依赖结构下计算完整 effect-size→power curve。
- Bracket 固定以完整 cluster/block 为重采样单位；共享 A 不得拆成 IID observations。
- history 必须保存无损原文及 SHA-256；统计实现变化必须产生新 runner SHA 并重新 A/A。
- 旧 A/A 与候选证据保留，但受审计取代的批次不得参与正式裁决。

## 1.0.1 - 2026-09-14

- 修复正式 ComfyUI 启动器使用 data/input、data/output 而旧 readiness/runner 假定 ComfyUI/input 的 PATH_ARCHITECTURE_ERROR。
- P0 runner 改用正式 /upload/image API 注入冻结的 256x256 黑色 PNG，不安装 custom node、不改变冻结 workflow。
- readiness 明确报告 FORMAL_LAUNCHER_LAYOUT；在正式实测前仍保持 P0_CURRENT=PENDING。
- 兼容 PowerShell 7 将大型 /object_info 返回为字符串的行为，避免把真实存在的 built-in 节点误报为缺失。

## 1.0.0 - 2026-09-14

- 建立母技能、V4.0 方法依赖、P0-P8 性能阶梯、99/FREEZE/REOPEN 与版本制度。
- 冻结 P0 ComfyUI Control Benchmark Contract。
- 提供 P0 只读准备脚本与默认 dry-run runner。
- 初始化 P0 为 `READY_TO_MEASURE`，P1-P8 为 `LOCKED_BY_PREVIOUS_STAGE`。
- 明确未执行 P0 benchmark、性能优化或 H3。
