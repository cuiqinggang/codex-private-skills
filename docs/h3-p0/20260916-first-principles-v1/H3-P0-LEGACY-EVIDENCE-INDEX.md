# H3-P0 旧探索证据索引

本索引指向 C 盘正式证据，不复制大型模型、输出视频或软件环境。根目录 E = C:\AI\H3-P0-Acceptance\fp-convergence\20260916-run-01；仓库目录 R = docs/h3-p0/20260916-first-principles-v1。每个正式阶段有 E\summary-<PHASE>.json、E\runs\<PHASE>\run-*.json 和相应 E\server-<PHASE>.log；完整字段、样本与出处也保存在 R\H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json。SOURCE=LOCAL_FORMAL_EVIDENCE（本机正式证据）。V1 初版已由 V1_QC 取代，但保留 E\summary-V1.json 作为误判历史。

| 关键结论 | 主要原始证据 | 辅助证据和边界 |
| --- | --- | --- |
| 固定任务合同、初始理论与目标 | R\H3-P0-STEP1-PHYSICAL-LIMIT-v1.md；R\H3-P0-STEP1-RESULTS.json；R\H3-P0-AUTONOMOUS-CONVERGENCE-COMMAND-v1.md | 原始 v1 理论保留，后续偏差不抹掉模型 |
| V1_QC 正式基线，G/P/T P50=21.758/18.162/41.007 秒 | E\summary-V1_QC.json；E\runs\V1_QC\run-*.json | E\server-V1_QC.log；E\summary-V1.json 是旧 QC 误判证据 |
| V2 reserve=2.0 GiB，KEEP（保留） | E\summary-V2_RESERVE2.json；E\runs\V2_RESERVE2\run-*.json | E\server-V2_RESERVE2.log；无独立 decision JSON，裁决由历史确认和后续 last-good 链还原 |
| V3 reserve=1.0 GiB，LAST_GOOD（最近保留版） | E\summary-V3_RESERVE1.json；E\runs\V3_RESERVE1\run-*.json；E\last-good.json | E\server-V3_RESERVE1.log；无独立 decision JSON |
| V4 reserve=0.5 GiB 回滚 | E\summary-V4_RESERVE0_5.json；E\decision-V4_RESERVE0_5.json | E\runs\V4_RESERVE0_5\run-*.json |
| V5 pinned-memory 回滚 | E\summary-V5_PINNED.json；E\decision-V5_PINNED.json | E\runs\V5_PINNED\run-*.json；E\server-V5_PINNED.log |
| V6 PATH 分块，仅诊断；VAE 阶段 P50=17.824 秒 | E\summary-V6_PATH_PROFILE.json；E\path-profile-V6_PATH_PROFILE.json；E\decision-V6_PATH_PROFILE.json | E\runs\V6_PATH_PROFILE\run-*.json；E\instrumentation-restore-proof.json；该阶段不是纯数学 decode |
| V7 VAE 深拆，仅诊断；VAE load GPU 约 0.127 秒 | E\summary-V7_VAE_STAGE.json；E\decision-V7_VAE_STAGE.json；E\vae-stage-proof.json | E\runs\V7_VAE_STAGE\run-*.json；解码函数包含按需权重请求；请求字节不等于实际 PCIe 传输 |
| V8 full-load 请求回滚；完全装载事件 0 | E\summary-V8_VAE_FULL_SINGLE.json；E\decision-V8_VAE_FULL_SINGLE.json；E\v8-candidate-proof.json | E\runs\V8_VAE_FULL_SINGLE\run-*.json；只否定本次实现 |
| V9 v0.36.0 完整软件栈回滚 | E\summary-V9_SOFTWARE_036.json；E\decision-V9_SOFTWARE_036.json；E\server-V9_SOFTWARE_036.log | E\server-V9-startup-failure.log 记录首次缺 comfy-aimdo，首次无正式 prompt；隔离 worktree/overlay 位于 E\software-frontier |
| V10 生成分块，仅诊断；50 层 DiT 与请求量 | E\summary-V10_GENERATION_PROFILE.json；E\generation-profile-V10_GENERATION_PROFILE.json；E\decision-V10_GENERATION_PROFILE.json | E\generation-profile-proof.json；E\generation-profile-manifest.json；E\runs\V10_GENERATION_PROFILE\run-*.json |
| V11 算子剖析，仅诊断；算子自耗时≠ CUDA 事件时间 | E\summary-V11_OP_PROFILE.json；E\op-profile-V11_OP_PROFILE.json；E\decision-V11_OP_PROFILE.json | E\runs\V11_OP_PROFILE\run-*.json；全局 E\instrumentation-restore-proof.json 最后记录仅能证明最终源文件恢复 |
| 长任务控制、恢复与故障 | E\state.json；E\last-good.json；E\lock-recovery-1789575692.json；E\controller-v6-host.err；R\H3-P0-controller.py | controller 记录和 R\H3-P0-FAILURE-INDEX.md；旧锁恢复证据不得当作 GPU 性能证据 |
| 软件和模型版本 | E\server-V3_RESERVE1.log；E\server-V9_SOFTWARE_036.log；R\H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json | 模型路径及文件长度有证据；无现成三大模型内容 SHA256，不推测 |
| 外部成熟路径 | R\H3-P0-MATURE-HARVEST-MATRIX.md | 外部官方/GitHub 原始链接在矩阵；EXTERNAL_EVIDENCE（外部证据）绝不写成 LOCAL_VERIFIED（本机已验证） |
| Git 起点和收口 | 起点分支 codex/h3-p0-fp-limit-v1，原 HEAD 85d21793753a0ca271208f0d099950ec081a9223 | 最终封存提交及远端 HEAD 以 Git 远端核验和最终报告为准 |

QC（质量检查）真值以逐条 run JSON 与阶段 summary 为准。阶段文件缺少独立 QC JSON 时，不虚构文件；机器版逐轮嵌入从 run JSON 恢复的 QC 值并标注源。插桩恢复证明区分 V6/V7/V8/V10 的专门 proof 与覆盖式全局 proof。没有相应原始记录的 PowerShell/null-byte 故障只标 USER_REPORTED（用户报告），不伪造日志或发生时间。
