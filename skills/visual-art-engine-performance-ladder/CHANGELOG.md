# V3.0.0 — 2026-10-31

保存成熟9环节返工路径、A—G批量安排、R9完整报告、20项实跑脚本、配置/来源/资源与恢复证据。完成15秒人工审核候选，不代签最终艺术批准；不改变P0/P8或通用控制认证。保留旧版正文和失败记录。

# Changelog

## 1.3.0 - 2026-10-11（来源真实性与重复违规硬门禁）

- 主文件 `SKILL.md` 从 v1.2.1 升至 v1.3.0，`VERSION` 从滞后的 1.0.1 对齐 1.3.0；版本不一致不得声明升级完成。
- 新增 `references/IMAGE-SOURCE-ANTI-CHEAT-V3.md`：执行前锁定 ComfyUI 生成后端和 T2I/图生图/条件生成/编辑四类合同；明确禁止 ChatGPT image_gen 代替 ComfyUI 正式结果。
- 新增 `references/INCIDENT-KREA-REPEAT-IMAGEGEN-20261011.md`：记录重复调用 image_gen 修图及其生成式“原图/修正后”海报，裁决 INVALID，不凭视觉相似或 gen_id 冒充 ComfyUI。
- 新增 `scripts/quality/verify_comfy_provenance.py`：原生 ComfyUI history、工作流图、prompt_id、SaveImage 原图及 SHA 只读交叉核对；缺证据 fail closed。该脚本不是生图器、调度器或平台级工具禁令。
- 新增 `tests/test_comfy_source_guard.py`：模拟测试 7/7 PASS，覆盖真历史匹配、只有预检、ChatGPT gen_id、错误图像输入链、历史漂移、PNG 替换、工作流哈希篡改。测试不是 Windows 生产出图认证。
- 对条件生成与图生图，源图 SHA 仍需人工审计；对局部 Inpaint 暂不自动认证；G3 高品质、真实左右像素拼接、工具路由回归仍未完成生产跨会话实测。`FINAL_VALID` 在这些门没有满足前只能保持 NO。

## Unreleased / Measurement Protocol V2 UNDER_VALIDATION - 2026-09-15

- 引入同期 interleaved paired A/B、A/A calibration、order equivalence、environment drift 与 confirmation 规则；历史固定 baseline 不再裁决微优化。
- 增加 null Type-I calibration：同时报告正向 false KEEP 与任意方向 rejection；null PASS 前 `FINAL_MDE_MS=UNKNOWN`。
- MDE 改为在正式 KEEP 管线与 block 依赖结构下计算完整 effect-size→power curve。
- Bracket 固定以完整 cluster/block 为重采样单位；共享 A 不得拆成 IID observations。
- history 必须保存无损原文及 SHA-256；统计实现变化必须产生新 runner SHA 并重新 A/A。
- 旧 A/A 与候选证据保留，但受审计取代的批次不得参与正式裁决。
- 新 runner `fcdae8b8...` 的统计 selftest 与 null calibration 通过；40-block 权威 A/A 因同实现 formal CI 全正而 FAIL，技能继续 `UNDER_VALIDATION`，候选锁不解除。
- 定位旧 A/A 的 arm-label leakage：A/B 标签进入 workflow `filename_prefix`、HTTP 输出身份及计时内 evidence 路径；服务端 execution block effect=0，客户端控制路径主导假差异。
- 新 runner `c43875c3...` 改用预分配 label-blind opaque token，增加 normalized workflow SHA 等价与 timed/workflow/HTTP leak=0 自测；统计函数重放保持 null/CI/MDE 原值。新权威 A/A 因本机 listener 权限拒绝尚未运行，候选锁继续开启。
- 建立双重 benchmark 身份：`8f5c3a59...` 保留为 `SUPERSEDED_LABEL_BLIND_RUNNER`，`c43875c3...` 为 `CURRENT_LABEL_BLIND_RUNNER`；当前 `HARNESS_MANIFEST_SHA=81974d60e1aa54bac03e0d5c27556d87b4ff4e52e742d9e36156998de4b807bf`，覆盖 runner、两层启动器、decision rules、bracket summary、workflow 与 fixture。
- 完成 160/160 label-blind 权威 A/A：formal effect `2.8688 ms`、CI `[-0.847625,6.585225]`、noise floor `3.7609 ms`；旧 CI 全正假效应消失，标签修复得到 runtime 因果确认。order-effect CI `[-3.081325,22.327025]` 仍不足以证明等价，故 `AA_CALIBRATION=INCONCLUSIVE / CANDIDATE_LOCK=ON`。
- 将 Windows deepest evidence path 实际创建加入 preflight；首次长路径失败未提交 workload，随后使用短、中性 `aa-lb-v3` 证据根完成相同冻结批次。
- 完成新的独立 `a4` 160/160 A/A；formal CI 跨 0，但 environment drift gate FAIL，故候选锁保持 ON。
- SEARCH_ONLY 依次实测 R1、local-file V2、R4 与 R6；R6 在两个独立 confirmation 中 paired CI 均全正，但 pooled P50/P95=`41.5258/58.000845 ms`，未优于历史参考，故 `P0_99=NO / P0_FREEZE=NO`。
- 固化“过早并发会争用 output/history 发布”“不可挑 smoke/单批最好值”“相对收益不等于绝对 99”三条失败经验。

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

