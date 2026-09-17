# H3-P0 成熟能力收割矩阵 v3 — Virtual-99 Batch 1

状态：`VIRTUAL_HARVEST_COMPLETE / NO_NEW_GPU_RUN`

方法规则：`first-principles-physical-limit-convergence v1.8.0`

固定任务：T2VA / 32×32 / 5f / 1 step / static frame / res_multistep / beta / real MP4 / RTX 2080 Ti 22GB sm75。

## 1. 排序原则

外部成熟方案只用于确认“这个机制已经真实存在、适合什么硬件、解决什么块、风险多大”；外部百分比和秒数不得直接换算成本机 32×32×5f×1step 的收益。

排序优先级：

```text
1. 直接攻击当前最大已知固定成本
2. 同 GPU / 同架构 / 同模型家族证据
3. 不改变任务合同
4. 可逆
5. 短验证即可裁决
6. 能同时改变模型驻留拓扑者优先
```

## 2. 第一批成熟候选

| ID | 成熟方案 | 主要优势 | H3-P0 目标块 | 本机适用性 | 风险 | 虚拟裁决 |
|---|---|---|---|---|---|---|
| M1 | Star7 MiniMax H3 Native FP16 Exact Loader | 专门面向 Turing/pre-BF16；FP16 activation compute + FP32 数值保护；保留 INT8/ConvRot/W4A8 原生量化调度 | Generation | 很高：明确支持 RTX20/sm75，且不改 sampler/sigma/latent/VAE/分辨率/帧数 | 中 | `FIRST_BATCH_PRIORITY_1` |
| M2 | MiniMax H3 W4A8 FL2VA diffusion | 将当前约20.97GB diffusion 降到约12.5GB；仍通过 INT8 GEMM 路径；同卡项目已真实使用 W4A8 | Generation + H3↔VAE residency / Path | 高：FL2VA 对应当前 T2VA；2080Ti 22G 有同卡成熟项目证明可运行 | 中 | `FIRST_BATCH_PRIORITY_2` |
| M3 | INT8 ConvRot Video VAE | 模型体积约3.2GB级，公开作者称 decode 约1.5×；可进一步释放 H3+VAE 共同驻留空间 | VAE / Path / residency | 中高：当前 ComfyUI 版本具备核心支持；但同卡高分辨率已有黑屏/NaN公开问题 | 中高 | `FIRST_BATCH_PRIORITY_3_WITH_STRICT_QC` |
| M4 | MiniMaxH3 CLIPCached / equivalent exact conditioning cache | 相同 prompt/reference 时跳过大型 Qwen3-VL 重编码和加载；不改 diffusion | Conditioning / Path / cold-to-warm stability | 条件适用：当前 prompt 固定；但 ComfyUI 原生 node cache 可能已经复用，必须先检查是否真的重算 | 低到中 | `CONDITIONAL_PRIORITY_4` |
| M5 | Star7 Activation Chunk / SM75 sparse attention modes | 长序列/显存峰值时减少激活峰值并可选注意力后端 | Generation memory pressure | 当前 P0 低：18–32 token 量级、1 step；本地 V11 attention 自耗时约1.26ms | 中 | `RESIDUAL_ONLY` |
| M6 | SageAttention | 大序列 attention 可加速 | Attention | 当前 P0 很低；同卡成熟项目报告 sm75 编译/原生管线失败，本地 attention 也不是大块 | 中高 | `EXCLUDE_BATCH_1` |
| M7 | T8 / PDD / Turbo / block cache | 多步场景跳 forward / 减步骤 | Generation | 不适用：当前固定 1 step；改变 step 数违反当前合同 | 中高 | `NOT_APPLICABLE` |
| M8 | ComfyUI v0.36 栈整体升级 | 上游新实现 | Path/Generation | 已本机同合同 V9 A/B 证伪，Total P50 +7.038s | 已证伪 | `PROVEN_BAD` |
| M9 | pinned-memory 开启 | CPU↔GPU transfer | Path | 已本机同合同 V5 证伪，Total P50 +5.303s | 已证伪 | `PROVEN_BAD` |
| M10 | VAE full-load 强制请求 | VAE residency | Path | V8 已本机证伪且没有真实 full residency 证明 | 已证伪 | `PROVEN_BAD` |

## 3. 成熟方案证据摘要

### M1 — Star7 Native FP16 Exact

成熟来源：

- https://github.com/star7code/minimax-h3-fp16-exact-star7
- https://github.com/Amduraznak/minimax-h3-fp16-fix

关键成熟能力：

- Turing/Volta 无原生 BF16 Tensor Core 时，避免默认 FP32/manual-cast 路径长期占用；
- condition_proj、残差流、SwiGLU、out_proj、fc2 设置受控 FP32/FP16 边界；
- 原生 `int8_tensorwise + ConvRot` 保留；
- `asym_w4a8_int8` 可保留原量化调度，但仍需本项目端到端验证；
- 不改变当前 1-step 任务数学合同。

本项目意义：当前历史日志明确记录 H3 weight dtype bfloat16 + manual cast float32，而 GPU 是 sm75；M1 与当前最大 Generation 固定成本的机制匹配度最高。

### M2 — W4A8 FL2VA diffusion

成熟来源：

- https://huggingface.co/Kijai/MiniMax-H3-experimental
- https://github.com/IvenKooLab/minimax-h3-turing
- https://github.com/starsFriday/ComfyUI-W4A8-Loader

关键事实：

```text
CURRENT_INT8_DIFFUSION_SIZE ≈ 20.97 GB
W4A8_FL2VA_SIZE ≈ 12.5 GB
WEIGHT_REDUCTION ≈ 8.47 GB
```

当前 FP16 VAE 约5.21GB：

```text
20.97 + 5.21 > 22.528 GB
12.5 + 5.21 < 22.528 GB
```

这不等于“必然全驻留”，因为 runtime/activation/workspace 仍需显存；但它第一次把“H3 + VAE 权重体积本身就必然超过 VRAM”这一硬关系改写为“理论上可能共同驻留”。因此 M2 不只是量化计算候选，也是 Path 拓扑候选。

同卡成熟证据：IvenKooLab 在 RTX 2080 Ti 22GB / sm75 / Torch2.9.1+cu130 使用 W4A8 mixed H3 路线真实运行，但其任务为更大分辨率、多帧、多步，不能把加速比例外推到本 P0。

### M3 — INT8 ConvRot Video VAE

成熟来源：

- https://huggingface.co/Kijai/MiniMax-H3-experimental
- ComfyUI core 已合并 H3 INT8 ConvRot VAE 支持

公开作者给出约1.5× decode 加速，并将视频 VAE 压缩到约3.2GB级。

组合体积粗略关系：

```text
W4A8 diffusion ~12.5 GB
+ INT8 VAE ~3.2 GB
= ~15.7 GB weights
```

相对 22.528GB VRAM 留出约6.8GB名义空间给 activation/runtime/workspace，显著优于当前 26.18GB 的 diffusion+FP16-VAE 权重和。

风险：ComfyUI 公开 issue #15524 报告 RTX 2080 Ti 在高分辨率长视频上 INT8 VAE 出现 black / NaN/Inf。故 M3 必须严格同 seed QC；任何非有限像素/黑帧/异常立即回滚，不能把外部“1.5×”当 KEEP 证据。

### M4 — Conditioning Cache

成熟来源：

- https://github.com/Mu5hr00moO/ComfyUI-MiniMaxH3-CLIPCached
- https://github.com/linjian-ufo/comfyui-speed-minimaxH3

CLIPCached 在另一硬件上的受控 benchmark：相同 conditioning 的 cache HIT 将 conditioning 中位时间约29.85s降到1.12s，并避免载入 Qwen3-VL；但这只是机制证据，不是本机预计收益。

当前任务 prompt 固定、seed 改变不应改变 conditioning，因此 M4 合同上允许；但 ComfyUI 自身 node cache 可能已经使正式暖态运行不重新编码。故先做无侵入适用性检查：如果当前三条正式 run 的 conditioning 已经是 native cache hit，则 M4 标记 `ALREADY_EFFECTIVELY_HARVESTED / NO_GPU_TEST`。

## 4. 第一批组合逻辑

不是把四个候选一次性全装上。虚拟组合顺序：

```text
BASELINE_CONTROL
→ M1 Star7 FP16 Exact on current INT8 checkpoint
→ RETURN GPT
→ M2 W4A8 on current winner loader path
→ RETURN GPT
→ M3 INT8 VAE on M2 winner
→ RETURN GPT
→ M4 conditioning-cache applicability
→ if applicable: bounded A/B
→ RETURN GPT
→ MATURE_BATCH_1_COMPLETE
```

原因：

1. M1 改 compute dtype/保护机制，最接近当前 Generation 大块；
2. M2 改 diffusion 体积和驻留拓扑，可能同时影响 Generation/Path；
3. M3 在新 diffusion 赢家上继续压 VAE 与切换；
4. M4 先判是否已有原生缓存，避免重复加一层 cache。

每个实际候选必须独立返回 GPT 后再进入下一项；本文件只预先完成虚拟铁路，不授权 Codex 连续自主执行。

## 5. 明确排除重复探索

第一批不再测试：

```text
reserve-vram 3.5/2/1/0.5 粗搜索
pinned-memory 开启
VAE full-load request
ComfyUI 0.36 整栈复刻
SageAttention standalone
T8/PDD/Turbo/MotionCache
开放式 profiler
随机 kernel/参数搜索
```

除非 GPT 以后拿到新机制、新版本或新硬件证据并重新建立完整验证铁路。
