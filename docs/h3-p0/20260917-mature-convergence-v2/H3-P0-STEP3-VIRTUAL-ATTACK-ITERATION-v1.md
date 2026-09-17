# H3-P0 STEP 3 — Virtual-99 成熟能力综合攻击迭代 v1

状态：`STEP3_COMPLETE=YES / VIRTUAL_ATTACK_COMPLETE / NO_NEW_GPU_RUN`

方法：`first-principles-physical-limit-convergence v1.8.0`

## 0. 输入边界

```text
T_PHY_TOTAL_REFERENCE = 0.23–0.57 s
REAL_STATE_OPTIMUM_RANGE = 4–14 s total P50
PROVEN_STABLE_V3 = 38.042308 s P50
CURRENT_MRE = 54.817736 s P50
NO_FREE_EXPLORATION=YES
```

所有外部速度数字只用于候选优先级和机制判断，不直接换算成本机 KEEP 秒数。本文件的数值投影是 Virtual-99 规划区间，不是实测结果。

---

# 1. 成熟能力矩阵

| ID | 成熟方案 | 本机/任务匹配 | 主要攻击块 | 成熟证据 | 风险 | Virtual 决策 |
|---|---|---|---|---|---|---|
| A0 | 当前 cu130 + comfy-kitchen INT8/ConvRot + DynamicVRAM + reserve-vram 1.0 + disable pinned | 精确 | 基础量化/驻留 | 本机 V1–V11 | 已收割 | KEEP BASE |
| A1 | Star7 Native FP16 Exact Loader | 高：明确面向 Turing sm75，支持原生 INT8/ConvRot | Generation manual-cast / dtype / overflow protection | star7code/minimax-h3-fp16-exact-star7 | 中 | HIGH_VALUE |
| A2 | Kijai/Comfy W4A8 FL2VA diffusion | 高：H3 原生量化路径；约 12.5GB FL2VA vs 当前 20.97GB | Generation + residency + H3↔VAE topology | Kijai experimental / comfy-kitchen W4A8 | 中：模型量化变化 | HIGH_VALUE |
| A3 | CLIPCached H3 conditioning | 条件高：固定 prompt，seed 不影响 cache key | Path / Qwen3-VL conditioning/load | Mu5hr00moO/ComfyUI-MiniMaxH3-CLIPCached | 低 | APPLICABILITY_FIRST |
| A4 | INT8 ConvRot Video VAE | 中高：官方/实验权重 2.81–3.17GB vs FP16 5.21GB | VAE decode + residency + Path | Comfy-Org/Kijai, public ~1.5–1.7x VAE reports | 高：2080Ti 有 black/NaN issue | STRICT_QC_HIGH_VALUE |
| R1 | W4A8 + smaller VAE 后重新做 H3/VAE co-residency/prefetch | 高，旧 V8 失败条件已改变 | Path residency transition | ComfyUI DynamicVRAM/prefetch + new capacity topology | 中 | RESIDUAL_HIGH_VALUE |
| R2 | H3 host-sync hoist / text_tags cache / sigma scalar sync reduction | 高机制匹配：本机 V11 大量未归属等待 | Generation host sync / Python control | Comfy-Org issue #15551 minimal patch mechanism | 中高：未合并完整解 | RESIDUAL_TARGETED |
| X1 | T8/PDD/Turbo/MotionCache | 低 | 多步跳 forward | 成熟但多步 | 违反 1-step 适用性 | NOT_APPLICABLE |
| X2 | Sparse/Sage/SLA 单独替换 | 低：P0 attention 本机约毫秒级 | attention | 同卡成熟大序列有收益 | 当前绝对上界极小 | EXCLUDE |
| X3 | ComfyUI 0.36 整栈升级 | 本机已测 | 全栈 | 本机 V9 | 已证慢 | PROVEN_BAD |
| X4 | pinned memory | 本机已测 | transfer | 本机 V5 | 已证慢 | PROVEN_BAD |
| X5 | 当前大模型条件下强制 VAE full load | 本机已测 | residency | 本机 V8 | 没有真正 full residency 且变慢 | PROVEN_BAD_OLD_TOPOLOGY |
| X6 | TRT VAE | 部分 | VAE decode | lihaoyun6 H3VAE_TRT up to 1.7x bare decode；T8 项目报告 end-to-end 可无收益 | 编译/shape/加载成本 | FALLBACK_ONLY |

关键外部来源：

- https://github.com/star7code/minimax-h3-fp16-exact-star7
- https://huggingface.co/Kijai/MiniMax-H3-experimental
- https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/vae
- https://github.com/Mu5hr00moO/ComfyUI-MiniMaxH3-CLIPCached
- https://github.com/Comfy-Org/ComfyUI/issues/15551
- https://github.com/IvenKooLab/minimax-h3-turing
- https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT

---

# 2. Virtual Attack 0 — 真实基线归一化

Virtual 规划锚点使用已证明稳定的 V3：

```text
G0 = 20.226 s
P0 = 17.970 s
T0 = 38.042 s
```

真实执行时绝不能拿这个旧时间直接裁决新候选；必须先在候选窗口跑 paired control。V3 只用于 Virtual 规划尺度。

---

# 3. Virtual Attack 1 — A1 Star7 FP16 Exact

机制：当前本机日志为 H3 weight BF16 / manual cast FP32，Turing sm75 没有原生 BF16 Tensor Core 路径。Star7 在 SM75 使用受保护 FP16，并对量化 checkpoint 保持 `force_cast_weights=false`，不主动展开原生 INT8/ConvRot。

Virtual 可消灭部分：

```text
TARGET = Generation dtype/manual-cast/dispatch overhead
EXPECTED_RELATIVE_GAIN_ON_GENERATION = 10%–30% planning band
EXPECTED_ABS_GAIN_FROM_V3 = ~2–6 s
```

投影：

```text
V1_PROJECTED_TOTAL = 32–36 s
```

这不是外部 benchmark 转换，而是基于本机 Generation 20.2 s 和明确机制做的有界规划。

若真实 A/B 未获益：ROLLBACK A1，但 A2/A3/A4 仍独立有效。

---

# 4. Virtual Attack 2 — A2 W4A8 diffusion

当前：

```text
DIFFUSION_CURRENT ≈ 20.97 GB
VIDEO_VAE_FP16 ≈ 5.21 GB
SUM ≈ 26.18 GB > 22.528 GB VRAM
```

W4A8 FL2VA 公开权重约：

```text
DIFFUSION_W4A8 ≈ 12.5 GB
```

仅模型大小关系变为：

```text
12.5 + 5.21 ≈ 17.71 GB
```

这第一次让“diffusion + FP16 VAE 权重名义同时容纳”从容量上成为可能，虽然 activation/workspace/text encoder/runtime 仍必须实测。

Virtual 作用：

- 减少 H3 权重驻留压力；
- 减少动态请求/切换；
- W4A8 CUDA/INT8 路径可能进一步改善 linear 执行；
- 与 Star7 量化感知 loader 可组合。

考虑 A1/A2 重叠后，不做简单加法；给予额外总时间有效收益规划：

```text
INCREMENTAL_NET_GAIN_AFTER_INTERACTION = ~6–12 s
V2_PROJECTED_TOTAL = 20–30 s
```

质量门禁必须真实比较，不允许仅凭模型更小 KEEP。

---

# 5. Virtual Attack 3 — A3 conditioning cache（条件分支）

固定 P0 prompt=`static frame`；seed、sampler、scheduler、steps 的变化本身不改变 CLIPCached conditioning key。公开实现只缓存 conditioning，不缓存最终视频、sampling 或 VAE。

但是 ComfyUI 自身有 node cache；因此先判断：

```text
IF current formal seed changes already produce native conditioning cache HIT:
    A3 = ALREADY_EFFECTIVELY_HARVESTED
    EXPECTED_GAIN = 0
ELSE:
    A3 = HIGH_VALUE
```

公开独立 benchmark 在另一硬件上报告 conditioning median 29.85s→1.12s；该数字禁止直接换算本机，只证明机制上可消灭重复 Qwen3-VL load/encode。

本机 Virtual 上界受 `Path≈17.97s` 限制。若当前确实重复 conditioning：

```text
PLANNING_ABS_GAIN = 4–10 s
V3_PROJECTED_TOTAL_IF_APPLICABLE = 12–26 s
```

如果 stock cache 已吃掉：保持 V2 投影，不因此继续折腾 cache。

---

# 6. Virtual Attack 4 — A4 INT8 ConvRot Video VAE

公开权重：

```text
FP16 VAE current = 5.21 GB
INT8 ConvRot VAE = 2.81–3.17 GB depending distribution
```

公开测试常见 VAE decode 约 1.5–1.7x，但本机 P0 V7 的 17.825 s decoder call 包含动态权重请求/等待，不是纯数学 decode，所以不能直接除 1.7。

在 A2 后容量关系进一步改善：

```text
W4A8 diffusion 12.5 GB + INT8 VAE 2.81–3.17 GB
≈ 15.31–15.67 GB nominal weights
```

名义留下约 6.86–7.22 GB VRAM 给 activation/workspace/runtime，资源拓扑发生本质变化。

Virtual 增量：

```text
PLANNING_NET_GAIN = 2–6 s
V4_PROJECTED_TOTAL_IF_QC_PASS = 9–22 s
```

但存在同 GPU RTX 2080 Ti 的公开 black/NaN/Inf issue。因此：

```text
ANY nonfinite / black / QC regression
→ ROLLBACK A4 IMMEDIATELY
→ NEVER relax QC
```

如果 A4 失败，最终方案继续使用 FP16 VAE，不阻断其他收益。

---

# 7. Residual Virtual Attack 1 — 新拓扑下 co-residency / prefetch

旧 V8 “强制 VAE full-load”是在当前 20.97GB diffusion + 5.21GB VAE 拓扑下失败，不能用来否定 A2/A4 后的新拓扑。

只有在 A2 KEEP，且 A4 KEEP 或至少 A2 让容量显著下降后，才允许建立新的 deterministic residency 验证：

```text
GOAL = keep/prepare H3 and VAE with minimum eviction during H3→VAE transition
NO reserve-vram sweep
NO free VRAM search
ONE predefined residency policy only
```

Virtual 预期：

```text
R1_NET_GAIN = 1–5 s depending actual misses
R1_PROJECTED_TOTAL = 7–16 s
```

如果新模型组合仍无法稳定共存，ROLLBACK residency policy，不回退 A2/A4 本身。

---

# 8. Residual Virtual Attack 2 — H3 host-sync targeted patch

ComfyUI 上游 issue #15551 已明确 H3 `_forward` 存在 per-step GPU→CPU scalar/readback 和 `text_tags.tolist()`；最小补丁可把表面 D2H sync 从三次减到一次，但完整 graph capture 仍需更深的 layout 重构。

本机 V11：

```text
GPU operator self total ≈ 1.46–1.62 s
Generation CUDA Event ≈ 22–25 s
```

二者巨大不闭合，使“host/control/sync + residency”成为真实残余候选。A1/A2 已先处理 dtype/驻留；如果更新后 Generation 仍明显高于 STEP2 的 2–5 s 带，则 R2 具有明确机制。

只允许采用预先审查的最小 patch：

- cache invariant `text_tags` list；
- reduce redundant sigma host pulls；
- 不改变数学任务、sampler、sigma 定义或输出合同；
- 不自行启用完整 torch.compile/CUDA graph 探索。

Virtual：

```text
R2_NET_GAIN = 0.5–3 s planning band
FINAL_WIDE_PROJECTED_TOTAL = 6–14 s
FINAL_CENTRAL_PROJECTED_TOTAL = 8–12 s
```

---

# 9. Virtual 综合赢家

Virtual 最终综合栈定义为条件组合，而不是一个插件：

```text
V99_COMPOSITE_STACK =
  BASE A0
  + A1 Star7 FP16 Exact           [if paired A/B KEEP]
  + A2 W4A8 FL2VA                 [if QC + paired A/B KEEP]
  + A3 exact conditioning cache   [only if native path truly repeats conditioning]
  + A4 INT8 ConvRot Video VAE     [only if 2080Ti strict QC PASS]
  + R1 new-topology residency     [only if measured transition remains major]
  + R2 minimal host-sync patch    [only if Generation residual remains major]
```

两个现实分支：

### STACK-A（全通过）

```text
PROJECTED_TOTAL_P50_WIDE = 6–14 s
PROJECTED_TOTAL_P50_CENTRAL = 8–12 s
```

已经进入 STEP2 `REAL_STATE_OPTIMUM_RANGE=4–14 s`。

### STACK-B（INT8 VAE 因 2080Ti QC 失败）

```text
USE FP16 VAE
KEEP A1/A2/A3/R1/R2 if individually valid
PROJECTED_TOTAL_P50 ≈ 9–16 s
```

若 STACK-B 上沿仍超过 14 s，只在实际最新数据证明有 ≥10% Total 的可归属大块时继续下一轮 GPT residual virtual convergence；不得由 Codex自行寻找。

---

# 10. Virtual 停止条件

本轮 Virtual 攻击已经推进到：

```text
CENTRAL_PROJECTED_TOTAL = 8–12 s
REAL_STATE_OPTIMUM_RANGE = 4–14 s
OVERLAP = YES
```

剩余已知方案中：

- 1-step 不适用的多步缓存已排除；
- P0 attention 绝对块太小；
- 整栈升级/pinned/current-topology full-load 已本机证伪；
- TRT VAE 只有作为 A4 失败后的低优先 fallback，且完整任务收益未稳定证明；
- 更深 CUDA graph/layout rewrite 超出当前“短、确定、成熟收益”边界。

因此当前 Virtual 层达到本轮停止点：

```text
STEP3_VIRTUAL_ATTACK_COMPLETE=YES
VIRTUAL_MATURE_PATH_COMPLETE=YES
PROJECTED_FINAL_OVERLAPS_REAL_STATE_OPTIMUM_RANGE=YES
READY_TO_WRITE_DETERMINISTIC_CODEX_TEST_PACK=YES
NEW_GPU_RUN=NO
```

真实结果若明显偏离这些投影，按母技能返回 GPT 重建 `REAL_STATE_MODEL`，而不是让 Codex继续探索。
