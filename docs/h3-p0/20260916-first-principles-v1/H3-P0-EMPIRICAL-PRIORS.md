# H3-P0 旧任务经验先验

本文件供下一任务继承，来源为[完整回归档案](H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.md)、[机器档案](H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json)和[证据索引](H3-P0-LEGACY-EVIDENCE-INDEX.md)。这是已发生事实与适用边界，不是新任务的自动 KEEP（保留）裁决。

| 经验先验 | 本机证据 | 继承条件 |
| --- | --- | --- |
| V3_RESERVE1 是单卡旧基线，TOTAL P50=38.042308 秒、GENERATION P50=20.226025 秒、PATH P50=17.970201 秒 | summary-V3_RESERVE1.json、last-good.json | 同 32×32/5 帧/1 步、同模型和硬件时用作本机对照；变化后重新建立可比基线 |
| reserve-vram 3.5→2.0→1.0 GiB 得到收益，0.5 GiB 回退 | V1_QC、V2、V3、V4 正式 summary；V4 decision | 不重复同软件的粗搜索；仅当驻留机制、模型或硬件改变时重测 |
| 当前 pinned-memory 开启路线较 V3 慢 5.303 秒 P50 | V5 summary/decision、三条同 seed QC | 仅否定旧软件、旧参数、旧合同的实现 |
| VAE 阶段是 PATH 大块，但 17.824 秒不是纯数学解码 | V6/V7 profile、proof 与 run | 分清模型切换、文件直读、权重请求、实际 GPU 计算 |
| 当前 force_full_load 请求未带来完整装载且慢 10.533 秒 P50 | V8 proof/decision | 不把失败推广为一切 VAE 驻留方案无效 |
| 完整 ComfyUI v0.36.0/kitchen0.2.34/aimdo0.5.3 组合比 V3 慢 7.038 秒 P50 | V9 summary/decision | 未来版本须有具体机制变化且本机 A/B，不能只凭版本新 |
| H3 一次稳态 forward 有约 155 次驻留未命中与 5.953GB 请求 | V10 profile/decision | REQUESTED（请求量）≠ ACTUAL_TRANSFER（真实传输量）；勿用请求量计算 PCIe 时间 |
| V11 的注意力约 1.26ms，算子自耗时与正式 CUDA Event 不闭合 | V11 op profile/summary | 诊断开销与未归属等待需要区别；不能用 profiler 时间取代正式计时 |
| 外部同卡多步/长视频加速比不能套用 1-step P0 | IvenKooLab 一手 benchmark、固定 TASK_CONTRACT | 外部证据只排序；T8/PDD 跳后续步在当前 1 步没有直接收益 |
| AI 会话故障不能认定本地实验故障 | state/pid/heartbeat、V6 lock recovery、Failure Index | 先查进程、8194、结果、QC、SHA；完整则 checkpoint 并不重跑 |
| 当前 99 门槛不因未来第二张显卡而改写 | STEP1、命令包和本轮硬件边界 | 新硬件真正安装后继承历史、重建新 T_MACHINE_STAR（本机稳定理论极限） |

下一任务的行动顺序见[成熟路径 v1.2](H3-P0-MATURE-PATH-FIRST-v1.2.md)与[成熟收割矩阵](H3-P0-MATURE-HARVEST-MATRIX.md)。旧任务的 H3_P0_GENERATION_99（核心生成 99）与 H3_P0_PATH_99（系统路径 99）均为 NO（未达），没有最终 10 次认证。旧任务 NO_NEW_GPU_BENCHMARK=YES（禁止新 GPU 测试）。
