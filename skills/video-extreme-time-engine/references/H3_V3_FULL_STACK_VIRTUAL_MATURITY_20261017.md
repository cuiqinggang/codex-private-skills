# 《高清视频第3版》全链路第一性原理与成熟方案整体虚拟成熟｜2026-10-17
执行：三人行V3 / C通道 / 不新增GPU推理。合同不变：1024×576、5张、20步、seed3013、参考图与提示词、原生INT8、原VAE；不得把Turbo4或124帧成绩混入本合同。
## 一、真实基线
R2 463.266秒=采样332.610+条件50.422+加载34.813+解码38+其余7.421。R3 W4A8 555.985秒；R5高清分块总452.188秒但采样339.344（比R2慢6.734），整体快11.078秒由条件/加载变化混杂，绝不将R5认定采样加速。
5帧是20次联合时空潜变量推理，不是5次独立单帧生成。本机H3原生源码有50个DiTBlock以及TokenRefiner、时间调制、联合图音频attention；同一张输出图不等于后续去噪步骤具有相同输入。精确复用只适用于完全相同的输入/权重/条件/设备等状态；TeaCache/FirstBlockCache改变数值轨迹，是允许质量容差下的近似复用而非无损保存所有步骤。
## 二、成熟外部路线覆盖
- NVIDIA Sol Engine: https://nvlabs.github.io/Sana/Sol-Engine/H3/；https://nvlabs.github.io/Sana/Sol-Engine/Sol-H3/：跨步残差缓存+稀疏attention+融合Norm/RoPE/MLP+编译/图捕获+AdaLN预计算+VAE与驻留协同，公开3.95倍为8×GB200不同合同，不能投影为本机实际速度。
- FirstBlockCache: https://github.com/duckyshell/ComfyUI-MiniMaxH3-FirstBlockCache ; 20步 H3 Fast缓存8步，后续49/50块跳过，RTX5090上cache-only约30.5-32.9% wall-time减少；Safe较保守。原作者明确数值轨迹不同、不能叠加其他double_block cache。
- TeaCache: https://github.com/Icyoung/ComfyUI-MiniMaxH3-TeaCache ; 20步124帧+64GB sm80的采样246→87秒，整个306.22→102.08；该收益受命中率/场景/模型输入及硬件影响，不能简单平移5帧SM75。其包装器直接复用前一次模型结果并更新状态，需核实联合图音频两输出的语义兼容。
- TE-Speed独立成熟来源 https://github.com/HELPMEEADICE/TE-Speed-MiniMaxH3-OSS ; 公开跨步块缓存；第三方报告https://github.com/soren-labs/minimax-h3-colab/blob/main/docs/te-speed-compatibility.md记录8 full+12 cache /20，和其他包装器叠加报错，禁止无证据叠层。
- SageAttention、Sol/SLA/VSA SM75：本机已装minimax-h3-chunk-star7显示existing/comfy_kitchen_int8/sol_sm75_all_int8/sla_sm75等运行时可选，但可选不等于本机此工作流有真实精度/提速证据。稀疏注意力与量化都可能失真。
- 低步蒸馏/轻量LoRA/低分辨率生成+超分/细化路线虽公开极快，实际改变20步参考画质合同，另立合同才可讨论，不进入当前最小高清等质测试。
- 权重驻留/内存分配/异步卸载/缓存键合法复用/图捕获/torch.compile/融合内核/预计算AdaLN/VAE并行均纳入全链比较。单GPU22GB显存和约32GB RAM造成压力，不能简单把8GPU融合通信或无卸载结果按算力比缩放。
## 三、虚拟候选A/B/C
A 原生INT8 R2，参数完全不变，可靠对照；R5分块已测无采样收益，淘汰速度晋级。
B 最强稳健候选：在原R2图上单独插入成熟FirstBlockCache Safe（0.08、保护10–95%、最多连续两次缓存），不叠R5分块、不改attention、不改分辨率步数。优先代码级验证与当前ComfyUI0.34、SM75、模型joint audio/visual返回、50块接口、内存额外残差成本。不是保证一定命中，也不是画质等价。只有完整兼容/风险边界合格才冻结下一次现实测试。
C 激进性能对照：TeaCache或成熟TE-Speed单独使用，不与B或R5叠加；TeaCache全模型近似重用可能导致音视频联合输出语义问题；TE-Speed需审查其patch的模型结构路径，二者择一后也要先质量门。没有证据时不能定为赢家。
融合原则：同等质量硬条件下，从复用最大净收益采样→同架构SM75算子/访存减少→AdaLN与条件缓存合法化→加载/卸载热冷分账→VAE/保存；每一步完成模型层整体虚拟刷新，不逐点真实试验；不得把互斥加速的宣传倍率相乘。
## 四、时间界限的正确口径
当前实际最快一次全程452.188秒，但非统计稳定最优；默认可靠R2 463.266秒。物理理论下界尚无法给出：必须观测每步真实CUDA kernels、GPU活动、HBM/PCIe流量、CUDA memcpy/page-fault/offload、当前模型计算FLOPs、真实缓存命中率。硬件理论峰值单独无法推出T_min。
R2模型敏感性：假设采样耗时减少20%/35%/50%/65%，其他130.656秒不变且不计新缓存开销，则全程分别396.744/346.353/296.961/247.570秒。均非预测、非可认证物理下界。实际还需加缓存维护/模型卸载副作用，质量有可能下降。特别是5帧可能缓存不命中，不能借用124帧8/20命中。
## 五、成熟停止门与下一个唯一动作
当前可据证据冻结的最优方向是B的**只读兼容/数值策略审查**，不是立即宣称性能赢家；C作为最强挑战者，备选而非双缓存融合。先验证原作者代码版本固定、节点注册与图引用、原H3联合输出、每步缓存失效规则（seed/context/尺寸/sigma）、显存缓存开销、失败回退、安全守护及对脸/手/衣纹/时序的独立质量标准。仍无合格候选则STOP并保留R2。
冻结后的一个现实验收批次（如果获得下一次授权）仍为5张、1024×576、20步、seed3013，保证端到端计时和RAM/VRAM时间序列，分别给实际跳过步数、采样时间与总时间；真实可视质量不退化才晋级。当前无新Reality。
