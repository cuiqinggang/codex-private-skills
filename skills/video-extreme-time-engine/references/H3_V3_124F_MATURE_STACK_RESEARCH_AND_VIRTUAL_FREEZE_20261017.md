# 高品质极限时间引擎V3｜124帧、1024×576成熟路径全链检索与虚拟成熟｜2026-10-17

## 0 规范及结论
合同：单机RTX2080Ti改显存22GB/32GB RAM，MiniMax H3、124帧、1024×576、完整音画（若要求）与同等可接受人脸、衣纹、动作、时序、声音品质。必须区分20步严格合同与允许成熟蒸馏4/8步的“同画质不限步数”合同；后者质量未验不可替代前者。目标最小完整T_VALID，非采样单节点、单帧平均时间。此次只读文献与已有源码、既有实验，新增GPU生成=0。
**当前本机124帧/1024×576/20步同质有效T_VALID=UNKNOWN，不能从已有5帧203.797s、124帧640×352/4步49.707s线性外推。全球算法无穷多，不能证明绝对物理极限。以下给条件下界和明确的实际参照；物理模型缺吞吐及VRAM/PCIe细账。**

## 1 多源真实性排行榜（绝对秒不能跨硬件直接排同质量冠军）
- NVIDIA Sol Engine：https://nvlabs.github.io/Sana/Sol-Engine/H3/ ：8×GB200、1344×768、124帧、50步、热态；无优化27.205s→Kernel fusion/CUDA graph/VAE19.514s→+Sol-Attn17.744s→+FirstBlockCache6.883s，总3.95×。近无损质量需注意：质量保守cache-only 3.16×；全稀疏3.95×感知偏移较大。不可单GPU照搬multi-GPU吞吐或torch bf16核；学习按方案家族独立筛选＋整体集成的成熟方法。
- duckyshell FirstBlockCache：https://github.com/duckyshell/ComfyUI-MiniMaxH3-FirstBlockCache/blob/main/benchmark/BENCHMARK.md ：RTX5090、960×544、124帧、20步、T2V、pruned INT8 ConvRot；Sage2.2.0热态no-cache58.389/复验57.527s，Safe46.371s(6/20缓存)、Fast40.261s(8/20)、Aggressive37.277s(10/20)；Native热态no-cache90.644s/Fast60.819s。Safe与no-cache SSIM0.8216、PSNR25.80dB，激进阈值轨迹差异更大；非同质量自动PASS。
- Icyoung TeaCache：https://github.com/Icyoung/ComfyUI-MiniMaxH3-TeaCache ：CMP170HX SM80/64GB，fl2va、1024×576、124帧、20步，完整306.22s→102.08s，采样246→87s，作者A/B主观质量一致；多提示词、VBench质量门未完成，当前可视为单次成熟实测，不能冒充跨场景质量认证。source里的calibration仍待完成，缓存生命周期/音视频联合输出需实审。
- star7code SM75：https://github.com/star7code/minimax-h3-chunk-star7/blob/main/BENCHMARKS.md ：同款RTX2080Ti mod 22GB但1MP/约243帧/4步Turbo合同，CK INT8 119.50s/步；SLA QK8 PV16 96.68s/步；SLA All-INT8 60.83s/步、完整325.51s；Sol All-INT8 88.71s/步；SM75 Sage190.50s/步。此路线直接适用的仅为注意力实现和兼容性线索，不是本合同的实测秒数；旧版All INT8存在质量/音频错误，后续修正单样本成功但非全面质量门。
- 本机V1 R5：640×352、124帧、Turbo4，首次490.504s、热态49.707s，采样热态30.949s，VAE13.734s，音画与R4不同、最终同质未认证。R4同规格热态172.128s。
- 本机V3 FBC Safe：1024×576、**5帧**、20步，整套203.797s、采样106.297s、缓存11/20、原尺寸画质本样本PASS。不可将11命中套在124帧，5帧与124帧不是线性独立图。
- 反例：loading-awesome/MiniMax-H3-Swift Apple M3 Ultra MLX 864×480 124帧20步，跨步缓存1.79×，但稀疏attention在cache后收益小且有时间闪烁；Prefix-2局部刷新损害语音关键字0/5；AdaLN批处理/融合/重排优化通常仅1–3%。GPU不同，这些为风险证据不是SM75速度测量。https://github.com/loading-awesome/MiniMax-H3-Swift/blob/main/docs/PERFORMANCE_GUIDE.md
- 较严谨公共多样本质量资料：https://bluepointdigital.github.io/minimax-h3-benchmarks/benchmarks.html，362帧15.084s另一合同，Standard 611.380s、PDD+Sage8步375.042s、低清预览+3D upscaler+4步修复285.765s；不能照搬到124帧目标，但提示真正少步/层级精修可降低**同质量业务**运算路径，必须用同数据完整验证。

## 2 本机算法第一性原理计算（有假设的下界而非目标预测）
原生H3源码 MiniMaxH3Model:50个DiTBlock，hidden5376、56 heads×128=7168内维、MLP14336、patch(1,2,2)，视频latent[B,24,T,H/16,W/16]。124帧的时间latent T=((124-5)/17)×5+2=37，视频token S_video=37×(576/32)×(1024/32)=21312；**实际全序列S_total大于21312**（文本、图像、音频条件）。
固定原生满密集S_video的单层主矩阵粗计：F_block≈2S(4hd+3hm)+4S²d≈29.45 TFLOPs；50层×20步≈29.45 PFLOPs。只有“所有主矩阵在215.2 TOPS的INT8理论峰值计算、不计其他精度及额外Tokens和传输”的不真实乐观模型才得约136.9秒。对于固定S_video密集计算和FirstBlock缓存6/20的假设：(14×50+6)/1000≈70.6%，则主矩阵粗计约20.79PF、峰值折算约96.6秒；8/20→(12×50+8)/1000=60.8%、约83.2秒；11/20→(9×50+11)/1000=46.1%、约63.1秒。这**不是总时间**，也不是跨所有算法的物理下界；有不同FLOPs的稀疏Attention/蒸馏技术可以低于它。真实执行混合FP16/FP32，现实吞吐通常更低；需加文本/音频、Qwen条件、VAE及PCIe传输。
Roofline逐算子：t_j≥max(F_j/P_j,B_j/W_j)，结合真实依赖/资源占用最短调度；不能用所有算子统一INT8 TOPS；不能删除采样得到物理极限。硬件峰值和已实现时间只能建立相应算法上下界，真正质量约束全局极限未知。
由他人40s/102s与本机不同架构不能得出“100倍可追差距”，尤其每帧平均不是视频DiT独立前向推理成本。124帧比5帧video tokens18.5倍，密集attention S²项变化更大；并不能按总帧数乘20或作线性外推。

## 3 成熟方案族与冲突矩阵
族1 跳算：FirstBlockCache Safe/Fast/Aggressive（源码、日志、质量保护）；TeaCache整步输出复用（单独候选，不能与FBC同时加）；Turbo4/PDD少步（改模型/步数需质量重新验）。优先已验证FirstBlock Safe，不同frame/运动会改变命中。
族2 Attention：CK原INT8（GOOD），SLA SM75 QK8/PV16（较保守）；SLA all INT8、Sol all INT8（速度优先，但质量/音频guard需验证）。只选其一，检查是否可独立应用，不叠R5 activation chunk以冒充加速；不要按RTX5090性能默认启用SM75 Sage。
族3 数值无损优化：已有融合Norm/RoPE/QKV、operator fusion、CUDA Graph的受支持子集、权重常驻/预计算、重用匹配静态conditioning与single decode。按端到端净收益挑选，吞吐/编译预热及显存失败成本必须计入。CUDA Graph/torch.compile在本机动态卸载/VRAM边界下可能负收益，不可当默认。
源模型联合图像音频，质量不仅单帧清晰度，也包括运动连续、音频（若合同需要）及时间稳定。外部Apple研究的sparse flicker/语音丢失作为强反例，阻止盲目叠加。

## 4 至多三条可交付组合与虚拟成熟结论
A 稳健可复用：原生INT8/CK + FirstBlockCache Safe + 现有官方动态显存和精确合法缓存 + 原VAE，完整20步同质量，面向124帧的首选兼容性审查基线。五帧203.797s不迁移作124帧预期；此组124帧总时间UNKNOWN。
B 质量约束性能挑战：A + 单独SM75 SLA QK8/PV16（如收益不足再考虑已有实测All INT8，但须单独音视频质量QA）；B是否和FBC补丁不冲突、缓存命中数、额外显存峰值须先检查本地源码。参考同卡4步不同合同CK→SLA倍率1.24×，不能乘到当前124帧20步完整时间。
C 算法路径挑战：对124帧完整音视频质量合同，引入成熟经实测的PDD/少步Turbo/分层latent upscale+refine算法路径；需完全同画质比较，和固定20步路径不同，不得在无证明时宣布等价。对于纯20步限制，C退化为独立TeaCache（必须修复生命周期/音频输出语义），不与FBC叠加。

**虚拟迭代与停止**：
- 第一最大潜在净收益是跳过昂贵H3完整前向；A源码和5帧现实例支持方向，但124帧命中不可直接继承；
- 第二候选仅在本机SM75质量/显存/音频保护可保留时采用attention优化；若源代码冲突或预期收益抵不过变更风险，则STOP并选A；
- 第三种少步重建可能更快但更易改变质量，缺同规格视觉QA则不得替代A；
- 不再试探未成熟的自研CUDA核/改写H3模型大结构；NVIDIA 8GPU Sol全栈视为可复用模块清单而不是单卡可照搬脚本；
- 迭代后下一动作仅做**无生成**本机接口兼容审核/必要的只读模型profiling，锁定单一124帧候选，Freeze后按授权 exactly-once 的Reality。不可逐点GPU试验。

## 5 可计算的极限区间与当前缺口
已确实算出一个**固定S_video密集主矩阵/INT8峰值的理想算力折算数**：零跳算~137s、假设6命中~97s、8命中~83s、11命中~63s；这些都不含不可省的条件Token、其他精度、访存和非采样节点，而且稀疏/蒸馏会改变计算总量，故**不能称这些数字为真正本机同质量全任务物理极限、可实现区间或预测**。
要给有证据的单卡工程可达秒数区间，缺同卡同精度124帧：1)每步S_total和缓存命中；2)算子FP16/INT8混合吞吐和SLA稀疏实际密度；3)模型offload及PCIe内存搬运实测；4)条件编码/VAE/音频全链首单/热态时间；5)124帧quality/VRAM PASS。没有这些数据则不能有依据宣布“目标124帧要X秒”或“下界X秒”；先有计算约束才进行Reality。
STATUS: MATURE_EXTERNAL_RESEARCH=PASS; COMPOSITION_VIRTUAL_REVIEW=COMPLETE_AT_SOURCE_LEVEL; 124F_STATIC_RUNTIME_COMPAT=PENDING; 124F_T_VALID_REAL=UNKNOWN; FULL_PHYSICAL_MINIMUM=UNKNOWN; NEW_GPU_RUNS=0.
