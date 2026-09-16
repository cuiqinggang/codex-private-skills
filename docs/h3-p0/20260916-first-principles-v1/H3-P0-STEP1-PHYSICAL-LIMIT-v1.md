# H3-P0 STEP 1：第一性原理物理极限计算 v1

```text
METHOD=first-principles-physical-limit-convergence v1.0.0
MODE=CALCULATE（计算）
NEW_H3_RUN=NO（本阶段没有新增 H3 运行）
BASE_SKILL_COMMIT=449575b16db9394e91bcfa618e88b55ea1f3d382
PREFLIGHT_EVIDENCE_COMMIT=c88c150962d677bae555d85834e03c796e5e46fc
```

## 1. 固定任务合同

本轮研究对象不是完整高画质作品，而是 H3 的**最小技术正确生成单位**：

```text
WIDTH=32
HEIGHT=32
FRAMES=5
STEPS=1
PROMPT="static frame"
INPUT_MODE=T2VA（纯文本到音视频潜变量；不要求首尾参考图）
SAMPLER=res_multistep
SCHEDULER=beta
AUDIO_INPUT=NO（不提供外部音频）
OUTPUT=5 帧有效解码视频 + 最小视频产物
SERVICE_STATE=WARM / READY（服务已就绪的稳态）
```

Cold Start（冷启动）单独记录，不进入本轮两个 99 的核心目标。

TASK_COMPLETED（任务完成）要求：API 接受、真实 H3 sampler 执行、5 帧、32×32、1 step、VAE 解码成功、像素有限且不损坏、最小视频产物可读取。

## 2. 两个 99

只保留两个正式 99：

```text
H3_P0_PATH_99（系统路径99）
= 除 sampler 核心生成之外的关键路径时间收敛

H3_P0_GENERATION_99（图/视频核心生成99）
= sampler_function 内真实 H3 去噪生成时间收敛
= 兼容旧名 H3_P0_GPU_CORE_99
```

没有第三个 TOTAL_99（总时间99）。总时间只做组合观测：

```text
T_TOTAL = T_PATH + T_GENERATION
```

## 3. 已冻结的本机事实

来自 H3-P0 PRE-FLIGHT：

- GPU：RTX 2080 Ti，实际报告 22528 MiB VRAM；
- H3 主模型：20,970,379,616 bytes（约 19.53 GiB）；
- Qwen3-VL text encoder（文本编码器）：15,687,142,551 bytes；
- H3 VAE：5,207,808,496 bytes（约 4.85 GiB）；
- 当前 launcher（启动器）：`--reserve-vram 3.5 --disable-pinned-memory --fast-disk`；
- H3 模型 INT8/convrot；当前运行链存在 manual cast（手动类型转换）和 async offload（异步卸载）；
- GPU core（GPU核心）边界：`KSAMPLER.sample` 内 `sampler_function(...)` 前后；
- 权威核心计时：CUDA Event（CUDA事件）+ synchronize（同步）；
- 32×32 / 5f / 1 step 是 schema（模式约束）最低候选；5 帧已被源码和历史成功证据确认，32×32 与 1 step 尚待 V1 实跑验证。

H3 官方公开结构：33B dense Transformer（330亿稠密 Transformer），约 13B AdaLN 参数可以预计算/缓存；50 层，hidden size 5376，56 heads（注意力头），head dim 128，FFN 14336。当前本机约 20.97GB 的裁剪 INT8 权重与“推理关键权重约 20B 量级”一致。

RTX 2080 Ti Turing 官方峰值参考：FP32 约 14.2 TFLOPS、FP16 约 28.5 TFLOPS、Tensor FP16 约 113.8 TFLOPS、显存带宽 616 GB/s。这里只把峰值用于物理下界，不把峰值当现实持续性能。

## 4. 最小 token（标记）规模

H3 5 帧时：

```text
video_latent_t=2
latent_h=32/16=2
latent_w=32/16=2
patch=1×2×2
video_tokens=2×1×1=2
```

音频潜变量即使没有外部音频输入仍存在联合 AV latent（音视频潜变量）：

```text
audio_t=round((5/24)×40)=8
audio_tokens=2 stereo × 8 = 16
```

`static frame` 为极短文本。考虑 tokenizer（分词器）和实现差异，本次把 packed sequence（打包序列）工作区间按约 18~32 tokens 建模，而不是假装知道一个未经本机实测的精确 token 数。

## 5. T_PHY（物理极限）推导

### 5.1 核心生成物理下界

推理关键权重约 20B 量级。对 18~32 个 packed tokens，一个 dense forward（稠密前向）仅线性层粗略计算量级约：

```text
FLOPs ≈ 2 × 20B × tokens
      ≈ 0.72 ~ 1.28 TFLOP
```

在当前卡峰值能力上：

```text
FP32_compute_floor ≈ 0.051 ~ 0.090 s
```

同时完整读取 20.97GB 权重的显存带宽硬下界：

```text
20.97 GB / 616 GB/s ≈ 0.034 s
```

Attention（注意力）在如此短序列上不是主要项；真正下界由线性计算、权重读取、类型转换和同步共同决定。

因此首版：

```text
T_PHY_GENERATION = 0.05 ~ 0.12 s
CONFIDENCE（置信度）= MEDIUM-HIGH（中高）
```

这里不是声称当前 PyTorch 已能达到 0.05 秒，而是同一硬件、同一数学任务在理想实现下不应低于的量级区间。

### 5.2 系统路径物理下界

主 H3 权重约 19.53 GiB，VAE 约 4.85 GiB，两者合计约 24.38 GiB，已经超过 22 GiB 级 VRAM，且还没计算 runtime/workspace（运行时/工作区）。因此即使最理想实现，也存在不可消灭的 residency transition（驻留切换）/ PCIe transfer（PCIe传输）。

PCIe 3.0 x16 理论有效上限约 15.75 GB/s 量级；仅从容量差看就至少有数 GiB 数据不能同时常驻。再加最小 VAE decode（VAE解码）、请求/调度和最小视频封装，得到：

```text
T_PHY_PATH = 0.18 ~ 0.45 s
CONFIDENCE（置信度）= MEDIUM（中）
```

### 5.3 总物理参照

```text
T_PHY_TOTAL
= T_PHY_PATH + T_PHY_GENERATION
= 0.23 ~ 0.57 s
```

它只作为终极参照，不作为直接 PASS 门槛。

## 6. T_MACHINE_STAR（本机稳定理论极限）

当前真实软件栈需要考虑：

- Turing 对当前 H3 quant/manual-cast（量化/手动转换）路径不能持续达到峰值；
- 小 token GEMM（小批矩阵乘）利用率低于大序列；
- 模型接近 VRAM 容量，存在 offload/prefetch（卸载/预取）；
- 当前 `reserve-vram 3.5` 使有效驻留空间进一步下降；
- 当前 `disable-pinned-memory` 可能降低主机到 GPU 传输效率；
- H3/VAE 不能完全同时常驻；
- Windows / PyTorch / ComfyUI 调度与 allocator（内存分配器）存在稳定开销。

结合物理下界、现有 H3 12~14 秒/step 的大序列历史、当前显存容量和可消除 offload 机制，首版现实目标区间定义为：

```text
T_MACHINE_STAR_GENERATION = 0.45 ~ 1.40 s
CONFIDENCE（置信度）= MEDIUM（中）

T_MACHINE_STAR_PATH = 0.70 ~ 2.00 s
CONFIDENCE（置信度）= MEDIUM-LOW（中低）

T_MACHINE_STAR_TOTAL = 1.15 ~ 3.40 s
```

这些是 **v1 理论区间**，不是已经跑出来的 benchmark（基准测试）。V1 实测如果系统性落在区间之外，必须找出被新证据推翻的假设后才能版本化修订目标；禁止因为结果慢就直接把目标往上抬。

## 7. 为什么当前历史 12~14 秒/step 不等于本机极限

已有 1344×768/5f/20step 的 TE-Speed sampler（采样器）约 257.781 秒，即约 12.89 秒/step；864×480/22f/10step 历史约 13.86 秒/step。两个规格 token 数相差明显，但 per-step（每步）时间接近，说明当前实现中存在较大的固定成本/驻留/卸载/转换成分，不是纯 token 计算量主导。

这正是本轮最值得攻击的对象：最小 32×32/5f/1step 把 activation（激活）计算压到极低后，固定成本会直接暴露出来。

## 8. 最短攻击顺序 v1

```text
ATTACK-0（第0刀）= V1 去重甲最小图
- 32×32 / 5f / 1step
- 非空极短 prompt
- 不用首尾参考图
- 不用外部音频
- 保留 VAE decode 和最小视频产物
- ffprobe/PyAV/日志/证据校验全部移到 RESULT_READY（结果就绪）之后

ATTACK-1（第1刀）= MODEL RESIDENCY（模型驻留）
- 重点测试 reserve-vram 3.5 是否导致不必要的 H3 权重 offload
- 在安全余量内逐级降低 reserve-vram
- 目标：最大化 H3 sampler 时的模型常驻比例

ATTACK-2（第2刀）= HOST↔GPU TRANSFER（主机↔GPU传输）
- 对比保留/移除 --disable-pinned-memory
- 保持 async offload/prefetch 可用
- 只保留能真实降低 wall/CUDA time 且稳定的配置

ATTACK-3（第3刀）= CONDITIONING CACHE（条件缓存）
- 固定 prompt 的 Qwen3-VL embedding（嵌入）允许在稳态任务中复用
- seed 改变不得触发重复文本编码
- 不允许缓存最终生成结果

ATTACK-4（第4刀）= H3↔VAE RESIDENCY TRANSITION（H3与VAE驻留切换）
- 优化 sampler 结束到 VAE decode 的换入换出
- 利用 pinned transfer / prefetch / 最小必要驻留

ATTACK-5（第5刀）= PYTHON/KERNEL OVERHEAD（Python/内核开销）
- 只有前四刀后仍存在明显 Gap 才测试 compile/fusion/CUDA Graph 等
- 任何候选必须真实更快，否则 ROLLBACK（回滚）
```

Sparse Attention（稀疏注意力）在约 20 个 token 的最小任务上理论收益很小，不列入首轮高优先级。进一步量化若改变数学/质量合同，也不进入首轮。

## 9. 多智能体结论

```text
AGENT_MODE=SUPPORT_PARALLEL（辅助并行）
GPU_BENCHMARK_SERIAL=YES（GPU正式测试串行）
GPU_EXCLUSIVE=YES（GPU独占）
CONCURRENT_GPU_HEAVY_AGENTS=0（并发GPU重任务为0）
```

推荐最多 3 个辅助智能体并行：

1. Physics/Gap Auditor（物理/差距审计）：只读计算 Gap、检查目标假设；
2. Code/Timing Auditor（代码/计时审计）：只读检查计时边界、缓存、offload；
3. Evidence/Git Auditor（证据/Git审计）：只读检查结果、回滚和共同仓库收口。

主 Executor（执行器）唯一拥有 GPU 正式运行和敏感写操作。多智能体优化的是 T_CONVERGENCE（收敛工程时间），不能污染 T_EXEC（任务实际运行时间）。

## 10. 99 首版门槛

首版目标，不是永久不可修改阈值：

```text
GENERATION_99_TARGET_V1:
P50_CUDA <= 1.40 s
P95_CUDA <= 1.70 s
TASK_COMPLETED=PASS
NO_HIGH_VALUE_GENERATION_GAP=YES

PATH_99_TARGET_V1:
P50_PATH <= 2.00 s
P95_PATH <= 2.40 s
TASK_COMPLETED=PASS
NO_HIGH_VALUE_PATH_GAP=YES
```

Final Certification（最终认证）至少 10 次有效 warm runs（稳态运行），seed 变化，prompt/规格固定；任何缓存只能缓存固定条件，不能缓存最终输出。

如果出现新证据证明 v1 区间假设错误，允许发布 `TARGET_V2（目标v2）`，但必须记录被推翻的假设、新证据和修订理由。

## 11. STEP 1 结论

```text
T_PHY_DEFINED=PASS
T_MACHINE_STAR_DEFINED=PASS
ATTACK_ORDER_DEFINED=PASS
MULTI_AGENT_MODE_DEFINED=PASS
READY_FOR_V1_AND_AUTONOMOUS_CONVERGENCE_COMMAND=YES

H3_P0_PATH_99=NO
H3_P0_GENERATION_99=NO
```

### 主要来源

- H3 本机 PRE-FLIGHT：commit `c88c150962d677bae555d85834e03c796e5e46fc`
- MiniMax H3 官方仓库/模型卡：33B dense、约13B AdaLN可预计算、H3-VAE f16t4d24、full-attention 初始开源实现
- MiniMax H3 `transformer/config.json`：50 layers / hidden 5376 / heads 56 / head dim 128 / FFN 14336
- NVIDIA Turing Architecture Whitepaper：RTX 2080 Ti 峰值算力和显存带宽
