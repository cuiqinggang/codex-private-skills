# H3-P0 成熟收益收割矩阵

状态：READ_ONLY_HARVEST（只读收割）；NO_NEW_GPU_BENCHMARK=YES（禁止新 GPU 基准测试）。本矩阵供下一任务排序，不自动产生 KEEP（保留）。任务合同固定为 32×32、5 帧、1 步，当前硬件边界是单张 RTX 2080 Ti 22GB / sm_75。

SOURCE_LEVEL（证据等级）：L1 本机同合同 A/B；E1 外部同卡实测；O1 官方代码或版本；H1 机制推断。EXPECTED_ABS_GAIN_S（预期绝对收益秒数）无同合同证据则记 UNKNOWN（未知），不得用外部加速比例换算。

| 候选/类别 | 来源/硬件/任务匹配 | 机制与目标块 | 绝对收益秒数 | 质量/稳定风险 | 集成成本/可逆/当前具备 |
| --- | --- | --- | --- | --- | --- |
| V3 reserve-vram 1.0 GiB；ALREADY_HARVESTED（已获得） | L1/精确/精确 | 显存驻留；Generation（核心生成）和 Path（系统路径） | 相对 V1 Total P50 快 2.965 秒 | QC 3/3，通过 | 已完成/YES/YES |
| Torch 2.9.1+cu130、INT8 ConvRot、DynamicVRAM、async offload、--disable-pinned-memory；ALREADY_HARVESTED | L1/精确/精确 | 当前完整 V3 栈 | 已包含在 V3，不重复计收益 | 已通过 QC | 已完成/YES/YES |
| ComfyUI v0.36.0+kitchen 0.2.34+aimdo 0.5.3；PROVEN_BAD（当前组合已证伪） | L1+O1/精确/精确 | H3/VAE、prefetch；Path/Total | V9 Total P50 慢 7.038 秒 | QC 过；首次缺依赖后修复 | 已完成/YES/已测且回滚 |
| pinned-memory 开启；PROVEN_BAD | L1/精确/精确 | CPU/GPU 搬运 | V5 Total P50 慢 5.303 秒 | QC 过/低 | 已完成/YES/已回滚 |
| 强制 VAE full-load 请求；PROVEN_BAD | L1/精确/精确 | VAE 驻留 | V8 Total P50 慢 10.533 秒，完全装载事件 0 | QC 过/中 | 已完成/YES/已回滚 |
| Star7 FP16 Exact sm75 实现；HIGH_VALUE_TEST（高价值待测） | O1/高/部分 | 受保护 FP16 H3 forward；Generation | UNKNOWN | 中/中，须同 seed 帧级 QC | 中/YES/NO |
| 后续官方成熟完整栈或可定向移植的 H3 VAE fusion/prefetch；HIGH_VALUE_TEST | O1+V9 反例/需验证/高 | VAE 阶段；Path | UNKNOWN | 中/中 | 中高/YES/NO；旧 v0.36 组合已否定 |
| IvenKooLab 同卡 W4A8、INT8、TE-Speed；LOW_PRIORITY（低优先级） | E1/高/部分，公开为多步长视频 | 量化与编码；Generation | UNKNOWN | 中高/中 | 中高/YES/部分已有 INT8 |
| T8/PDD 减步；NOT_APPLICABLE（当前 P0 不适用） | E1/高/低 | 跳后续采样步；1-step 无后续步 | 直接跳步收益 0 | 改步数违反合同/中 | 中/YES/NO |
| 多步 block cache/MotionCache；NOT_APPLICABLE | O1/部分/低 | 跨步缓存；Generation | 单步收益未证实 | 中高/中 | 中/YES/NO |
| SageAttention；LOW_PRIORITY | 外部不同序列+V11/需验证/低 | Attention（注意力） | V11 本机注意力仅约 1.26 ms | 中/中 | 中/YES/NO |
| 公开 VAE TensorRT 静态 engine；NOT_APPLICABLE | O1/需编译/低，公开 latent 16/32 与本 P0 不同 | VAE 计算；Path | UNKNOWN | 中/高 | 高/YES/NO |
| 未来第二张 8GB GPU；NOT_APPLICABLE（本轮边界外） | 无本机证据/不存在/不属合同 | 双 GPU 驻留 | UNKNOWN | 未测/未测 | 硬件变化/N/A/NO |

上述各行依次记录 SOURCE_LEVEL（证据等级）、HARDWARE_MATCH（硬件匹配）、TASK_MATCH（任务匹配）、MECHANISM（机制）、TARGET_BLOCK（目标块）、EXPECTED_ABS_GAIN_S（预期绝对收益秒数）、QUALITY_RISK（质量风险）、STABILITY_RISK（稳定风险）、INTEGRATION_COST（集成成本）、REVERSIBLE（可逆）和 CURRENTLY_PRESENT（当前是否具备）。下一任务按可消灭绝对秒数、适用性、证据强度、集成成本选 1～3 个成熟候选做同合同 A/B；外部结果只决定优先级。只有 HIGH_VALUE_MATURE_CANDIDATES_REMAINING=NO（高价值成熟候选已测尽）后才恢复自研残余 Gap（差距）诊断。

一手资料：[ComfyUI v0.36.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.36.0)、[H3 VAE PR 16187](https://github.com/Comfy-Org/ComfyUI/pull/16187)、[低显存 PR 16332](https://github.com/Comfy-Org/ComfyUI/pull/16332)、[kitchen PR 167](https://github.com/Comfy-Org/comfy-kitchen/pull/167)、[MiniMax 官方](https://github.com/MiniMax-AI/MiniMax-H3)、[IvenKooLab 同卡 benchmark](https://github.com/IvenKooLab/minimax-h3-turing/blob/main/docs/en/10-benchmarks.md)、[Star7 FP16 Exact](https://github.com/star7code/minimax-h3-fp16-exact-star7)、[VAE TRT 源码](https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/main/compile.py)、[MotionCache](https://github.com/Mozer/ComfyUI-MiniMax-H3-MotionCache-FastVAE)。
