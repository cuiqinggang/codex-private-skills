# H3-P0 v1.2 MATURE_PATH_FIRST（成熟路径优先）规则

状态：LEGACY_FREEZE_INPUT（旧档案冻结输入）。本文件只定义下一任务的复用顺序；本次旧任务 NO_NEW_GPU_BENCHMARK=YES（不再启动 GPU 测量）、NO_NEW_OPTIMIZATION_CANDIDATE=YES（不再启动候选）。

## 目标与适用边界

目标仍是 H3_P0_GENERATION_99（核心生成 99）与 H3_P0_PATH_99（系统路径 99）都达到 YES；第一版门槛不因当前结果慢而改。ACTIVE_HARDWARE_BOUNDARY（有效硬件边界）仅为本机实际单 RTX 2080 Ti 22GB/sm75；未来第二卡只有真实安装后才重新计算新 T_MACHINE_STAR。SOFTWARE_FRONTIER_GATE（软件前沿门禁）已有 v0.36.0 完整栈的本机 V9 A/B，结果回滚；HARDWARE_TOPOLOGY_GATE（硬件拓扑门禁）不得要求未安装的 GPU。

## 执行顺序

1. WORLD_KNOWN_BEST（世界已有成熟路径）：查官方稳定发布、上游代码、同硬件真实 A/B 与本机成熟技能。先读[旧档案](H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.md)、[机器数据](H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json)、[成熟矩阵](H3-P0-MATURE-HARVEST-MATRIX.md)、[失败索引](H3-P0-FAILURE-INDEX.md)，不全盘扫描 H3。
2. LOCAL_APPLICABILITY_FILTER（本机适用性过滤）：硬件 sm75/22GB、原生 INT8 ConvRot、固定 T2VA/32×32/5帧/1步、同一模型、MP4/QC 和计时边界逐项核对。公开大分辨率/多步收益不得直接折算本机绝对秒数。
3. MATURE_HARVEST（成熟收益收割）：每候选记录 SOURCE_LEVEL（证据等级）、HARDWARE_MATCH（硬件匹配）、TASK_MATCH（任务匹配）、MECHANISM（机制）、TARGET_BLOCK（目标时间块）、EXPECTED_ABS_GAIN_S（预期绝对收益秒数）、QUALITY_RISK（质量风险）、STABILITY_RISK（稳定风险）、INTEGRATION_COST（集成成本）、REVERSIBLE（可逆）、CURRENTLY_PRESENT（当前是否具备），并归入 ALREADY_HARVESTED（已收割）、HIGH_VALUE_TEST（高价值待测）、NOT_APPLICABLE（不适用）、PROVEN_BAD（当前证据否定）、LOW_PRIORITY（低优先级）。
4. 按有证据支持的绝对可减少秒数、任务适用性、来源强度、集成成本排序；UNKNOWN（未知）不得伪造为数字，也不能用外部百分比自动 KEEP。只选 1–3 个最高价值、可逆且安全的成熟候选。完整成熟栈有可靠重复验证时可直接作为同一候选本机 A/B，无需先重新拆解全部内部机制。
5. 本机 A/B：GPU_EXCLUSIVE=YES（GPU 独占）；固定任务合同、同 seed、1 条预热+3 条正式、原 CUDA Event+synchronize、PATH/总时间、完整 MP4/QC。更快且所有硬约束 PASS 才 KEEP（保留），否则 ROLLBACK（回滚）；每轮 checkpoint 并重算最大绝对 Gap。
6. 只有 HIGH_VALUE_MATURE_CANDIDATES_REMAINING=NO（无高价值成熟候选）以后才进入 RESIDUAL_GAP_PROFILE（残余差距诊断），再考虑 kernel、prefetch、offload、quant、attention 的定制攻击。诊断轮标 DIAGNOSTIC_ONLY（仅诊断），不能直接判 KEEP。
7. 双 99 首次满足后仍需 10 条有效稳态认证、质量/噪声/缓存核查、经验先验与失败索引更新、共同仓库远端核验，才可 FREEZE（冻结）。Target Revision Gate 仅在具体原始假设被真实证据推翻时启动。

## 1-step P0 的反例过滤

Turbo/PDD 通过减少原本多次的采样步数获益，本轮仅 1 step；T8、TeaCache、MotionCache 等依赖后续调用命中的方案不能只凭 4/8/20-step 的加速比例列高优先级。当前 V11 注意力 GPU 自耗时约 0.00126 秒，替换注意力本身的直接可消灭上界很小；大序列 SageAttention 比例不可外推。V7 所谓 VAE decoder call 含约 4.846GB 动态权重请求；不要提前断言纯数学 VAE 解码就是 17.825 秒。V10 H3 约 5.953GB 请求不等于真实 PCIe 传输时间。

## 经验先验与重复探索门禁

EMPIRICAL_PRIORS（经验先验）：本机 Torch2.9.1+cu130、INT8 ConvRot、DynamicVRAM/async offload 已有；V3 reserve1.0+禁用 pinned 是旧赢家；V4/V5/V8/V9 同配置已回滚；V6/V7/V10/V11 已诊断。重测必须说明任务、模型、硬件或实现机制哪项改变，并指向新证据。AI 会话报错不等于本地 GPU 失败；先查控制器、PID、8194、心跳、结果、QC 和锁。复杂 PowerShell 用独立 UTF-8 .ps1。

MATURE_PATH_FIRST_GATE（成熟路径门禁）：本旧档案已完成只读收割矩阵，但按最新用户冻结令不做新 A/B；因此旧任务不宣称该门禁为新 99 的 PASS。下一任务从矩阵开始，并对真正高价值候选做本机 A/B 后裁决。
