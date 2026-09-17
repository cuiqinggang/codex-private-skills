# H3-P0 T_MACHINE_STAR_REAL v2 — MRE 后真实态校准

状态：`CALIBRATED_PROVISIONAL / NOT_YET_CERTIFIED_99`

日期：2026-09-17

## 1. 结论先行

本次 MRE 已经足够把旧的 `T_MACHINE_STAR_V1 = 1.15–3.40 s total` 从“现实工程目标”降级为“旧假设产物”。它不能继续直接作为当前 99 门槛；但 `T_PHY` 仍保留为物理世界下界参照，不因一次慢跑而修改。

当前应同时保留三个层次：

1. `T_PHY`：物理下界参照。
2. `CERTIFIED_STABLE_UPPER_BOUND`：本机同合同已经真实达到过的稳定上界。
3. `T_MACHINE_STAR_REAL_V2`：由成熟候选继续收窄的真实本机稳定理论极限区间；当前只能发布“有证据约束的区间”，不能伪造一个单点。

## 2. 输入事实

固定任务：T2VA / 32×32 / 5 frames / 1 step / `static frame` / `res_multistep` / `beta` / 无输入音频 / 真实 MP4。

硬件边界：单 RTX 2080 Ti 22GB，Turing sm_75。

### 旧 V3 已证明稳定能力

- Generation P50/P95：20.226025 / 20.533857 s
- Path P50/P95：17.970201 / 18.007124 s
- Total P50/P95：38.042308 / 38.488666 s

### 新 MRE 当前真实态

- Generation P50/P95：24.467068 / 29.613326 s
- Path P50/P95：30.180904 / 30.333691 s
- Total P50/P95：54.817736 / 59.811207 s

相对旧 V3：

- Generation P50：+4.241043 s（约 +20.97%）
- Path P50：+12.210703 s（约 +67.95%）
- Total P50：+16.775428 s（约 +44.10%）

同一已记录硬件、任务合同、启动参数、ComfyUI commit、Python/Torch/CUDA 与模型文件大小下出现大幅漂移；原因未知。因此 MRE 的 54.818 s 是“当前运行态观测”，不是新的机器能力极限。

## 3. 旧 T_MACHINE_STAR_V1 为什么不能继续直接使用

旧 v1 把以下成本大部分视为可由软件消灭：

- Turing 上 BF16/manual-cast 路径；
- 小序列低利用率；
- DynamicVRAM/offload 调度；
- H3 与 VAE 之间的驻留切换；
- 动态权重请求与等待；
- 未归属调度时间。

V7/V10/V11 与 MRE 已经证明这些成本在真实系统里不是可以直接忽略的常数：

- VAE 调用块约 17.8 s，但不是纯数学 decode；内部含动态权重、切换和等待。
- H3 稳态 forward 约 155 次 residency miss、约 5.953GB requested；`REQUESTED != ACTUAL_TRANSFER`。
- V11 只归属到约 1.46–1.62 s 的部分 GPU 算子自耗时，而正式 CUDA Event 仍约 22–25 s，说明存在大量未归属等待/调度。

因此旧 1.15–3.40 s 不能再被当作“已经校准的本机现实 99 目标”。这不是宣布物理上永远达不到，而是撤销其现实工程认证。

## 4. T_PHY 保留

继续保留：

- `T_PHY_GENERATION = 0.05–0.12 s`
- `T_PHY_PATH = 0.18–0.45 s`
- `T_PHY_TOTAL = 0.23–0.57 s`

这些只代表第一性原理物理参考，不代表当前软件栈或当前成熟技术可以达到。

## 5. T_MACHINE_STAR_REAL_V2：当前可认证区间

### Generation

- 已证明稳定上界：`<= 20.226025 s P50`（旧 V3 已真实达到）。
- 经验下界线索：V11 已经看到部分 GPU 算子自耗时约 1.46–1.62 s，但该值不覆盖全部计算，且 profiler 有扰动。
- 因此当前只允许写：`1.62 s < T_MACHINE_STAR_REAL_GENERATION <= 20.226025 s`。

### Path

- 已证明稳定上界：`<= 17.970201 s P50`（旧 V3 已真实达到）。
- 物理/结构下界仍远低于该值，但当前没有足够同合同数据把真实可达下界压成可信单点。
- 因此当前只允许写：`0.45 s < T_MACHINE_STAR_REAL_PATH <= 17.970201 s`。

### Total

- 已证明稳定上界：`<= 38.042308 s P50`。
- 组合下界不能用简单相加伪装成现实目标；仅可保留物理参考与上述分量区间。
- `T_MACHINE_STAR_REAL_TOTAL` 当前状态：`BOUNDED_NOT_COLLAPSED`。

## 6. 为什么区间仍然很宽

当前正好存在三个足以改变整个资源拓扑的成熟候选，但还没有本机同合同 A/B：

1. **Star7 Native FP16 / Exact**：面向 Turing，使用受保护 FP16，同时保持原生 INT8/ConvRot 路径，不把量化权重展开为稠密 FP16。
2. **INT8 ConvRot Video VAE**：公开模型尺寸约 2.81–3.17GB，而当前 FP16 VAE 为 5.21GB；既可能缩短 VAE 计算，也可能降低 H3→VAE 切换压力。
3. **W4A8 diffusion**：公开 H3 W4A8 约 11.8GB，而当前 diffusion 为约 20.97GB。若质量门禁通过，它可能把“接近塞满 22GB VRAM”的状态改写成有明显余量的状态。

其中 W4A8 diffusion + INT8 VAE 单看权重约 14.6GB，理论上已经不再由“20.97GB H3 + 5.21GB VAE > 22GB”这一条简单容量关系强制决定二者不能同时驻留；但实际是否能共同驻留仍取决于激活、workspace、文本编码器卸载和 ComfyUI 运行态，必须实测，不能提前宣称。

## 7. 99 的正式定义（v2）

不再用旧 `Generation <=1.40 / Path <=2.00` 直接宣布 PASS。

`H3_P0_GENERATION_99=YES` 必须同时满足：

- 当前高价值 Generation 成熟候选全部得到 KEEP / ROLLBACK / NOT_APPLICABLE 裁决；
- 最终赢家经过 10 条有效稳态认证；
- 同合同质量/QC 全部通过；
- 残余虚拟收敛没有找到生命周期 ROI 为正、风险可接受、且预期收益高于测量噪声的可执行组合；
- 最终配置与证据远端冻结。

`H3_P0_PATH_99=YES` 使用同样规则作用于 Path。

因此 99 是“当前硬件、当前可验证成熟技术、质量/稳定硬约束下的稳定最优”，不是强迫达到旧 1.4/2.0 秒。

## 8. 当前现实状态模型

定义三个锚点：

- `REAL_STATE_NOW`：MRE Total P50 54.817736 s。
- `PROVEN_STABLE_ANCHOR`：V3 Total P50 38.042308 s。
- `PHYSICAL_REFERENCE`：0.23–0.57 s。

任何后续候选必须使用同会话、同 seed 的配对 A/B；不得把 MRE 与数天前外部比例直接比较并自动 KEEP。

当前性能漂移不需要先用数小时开放式 profiling 找根因。配对 A/B 本身就是控制漂移的实验设计；若 A/B 控制组在同一候选验证窗口内失稳，则该候选验证直接 `INVALID / STOP`，返回虚拟层重新设计。

## 9. 下一步

进入 `H3-P0-VIRTUAL-99-MATURE-PATH`，先完成完整虚拟铁路，再只让 Codex 做短、确定、可回滚的本机 A/B。不得恢复 V12 式自由探索。
