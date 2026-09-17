# H3-P0 STEP 2 — 本机真实状态极限区间 v1

状态：`STEP2_COMPLETE=YES / REAL_STATE_CALIBRATED`

方法：`first-principles-physical-limit-convergence v1.8.0`

> 本文件给出第 2 个正式项目数据：不是第二个“物理极限板”，而是由本机真实运行、诊断和硬件约束收缩出来的 `REAL_STATE_OPTIMUM_RANGE`。STEP 3 的 Virtual-99 必须攻击这个现实目标带。

## 1. 输入真实事实

固定任务同 STEP 1。

### 已证明稳定上界

```text
V3 Generation P50/P95 = 20.226025 / 20.533857 s
V3 Path       P50/P95 = 17.970201 / 18.007124 s
V3 Total      P50/P95 = 38.042308 / 38.488666 s
```

因此任何“本机最优”一定满足：

```text
T_REAL_OPTIMUM <= 38.042308 s P50
```

因为这台机器已经真实、稳定做到过。

### 当前 MRE 真实态

```text
MRE Generation P50/P95 = 24.467068 / 29.613326 s
MRE Path       P50/P95 = 30.180904 / 30.333691 s
MRE Total      P50/P95 = 54.817736 / 59.811207 s
```

MRE 比 V3 慢，不代表机器能力退化到 54.8 s；它证明当前运行态存在显著漂移/调度成本，所以以后所有候选必须使用同窗口 paired A/B。

### 已测诊断事实

```text
V11 torch.profiler GPU operator self total ≈ 1.46–1.62 s
formal Generation CUDA Event ≈ 22–25 s
```

说明当前 Generation 中绝大部分时间不是“纯 GPU 算子数学时间”，而是驻留、量化调度、同步、Python/host 控制、等待或 profiler 未归属成本。

```text
V7 VAE actual decoder call P50 ≈ 17.825251 s
V7 VAE requested bytes/run ≈ 4.846 GB
V10 H3 steady resident misses/run = 155
V10 H3 requested bytes/run ≈ 5.953 GB
```

`requested bytes != measured PCIe bytes`，因此不能拿这些数直接除 PCIe 带宽伪造传输时间；它们只证明驻留/调度压力真实存在。

## 2. 严格证据外包络

如果只接受“已直接观察到”的绝对约束：

```text
Generation practical optimum > 1.62 s
Path physical/structural optimum > 0.45 s
Stable achieved total <= 38.042308 s
```

因此最保守证据外包络为：

```text
2.07 s < T_REAL_OPTIMUM <= 38.042308 s
```

这个区间真实但过宽，不能有效指导 Virtual-99，因此需要用实际运行结构进一步收缩成工程目标带。

## 3. Generation 本机现实最优带

已观察到的 1.46–1.62 s GPU operator self total 是下界线索，而不是完整 Generation；必须给未归属的必要 launch/sync/dequant/quant-dispatch/模型管理留现实余量。

不再采用旧版“0.45–1.40 s”过度理想化估计。以 1.62 s 为本机已测 GPU 工作尺度，给必要运行时成本约 1.25×–3.0× 的现实余量：

```text
1.62 × 1.25 ≈ 2.03 s
1.62 × 3.0  ≈ 4.86 s

REAL_STATE_GENERATION_OPTIMUM_RANGE = 2–5 s
CONFIDENCE = MEDIUM_LOW
```

这个倍率不是硬件常数，而是现实工程安全带；后续真实 A/B 会继续收窄。

## 4. Path 本机现实最优带

Path 必须保留：

- conditioning/latent 准备；
- 必要模型驻留切换；
- H3→VAE 交接；
- 5 帧真实 Video VAE decode；
- CreateVideo/SaveVideo；
- history 完成且 MP4 真正存在。

当前 V3 Path 已经是 17.97 s，但 V7/V10 证明里面存在大量动态权重请求与驻留 miss；P0 只有 32×32×5，纯输出计算规模极小，因此 17.97 s 不应被视作不可消灭下界。

结合：

- T_PHY Path 上沿约 0.45 s；
- 当前 VAE/驻留请求量级；
- 固定 prompt/conditioning 可复用；
- 真实 MP4 和 QC 不可删除；
- Windows/ComfyUI/Python 调度与动态 VRAM 必须留现实余量；

给出当前本机工程规划带：

```text
REAL_STATE_PATH_OPTIMUM_RANGE = 2–9 s
CONFIDENCE = MEDIUM_LOW
```

下沿代表主要驻留/conditioning 等待已被成熟机制消灭；上沿代表仍保留部分动态切换但已去除当前大块等待。

## 5. 第 2 个项目正式数据

组合 Generation 与 Path：

```text
REAL_STATE_OPTIMUM_RANGE
= REAL_STATE_GENERATION_OPTIMUM_RANGE
+ REAL_STATE_PATH_OPTIMUM_RANGE
= 4–14 s total P50 planning range

CONFIDENCE = MEDIUM_LOW
ROLE = REALITY_CALIBRATED_ATTACK_TARGET
```

这就是 STEP 3 的现实攻击目标带。

它和 STEP 1 的关系：

```text
T_PHY_TOTAL_REFERENCE = 0.23–0.57 s        # 纯物理终极参照
REAL_STATE_OPTIMUM_RANGE = 4–14 s          # 本机现实工程极限目标带
PROVEN_STABLE_V3 = 38.042308 s             # 已证明稳定锚点
REAL_STATE_NOW_MRE = 54.817736 s            # 当前运行态观测
```

## 6. 为什么不是旧的 1.15–3.40 s

旧 `T_MACHINE_STAR_V1=1.15–3.40 s` 把 Turing manual-cast、动态 offload、驻留切换和 host/control 成本大部分当作可以接近完全消灭。V7/V10/V11/MRE 已证明这个假设不足，因此旧区间降级为历史假设，不再参与当前决策。

## 7. STEP 2 输出

```text
STEP2_COMPLETE=YES
REAL_STATE_OPTIMUM_RANGE=4–14 s
REAL_STATE_GENERATION_OPTIMUM_RANGE=2–5 s
REAL_STATE_PATH_OPTIMUM_RANGE=2–9 s
CONFIDENCE=MEDIUM_LOW
NEXT=STEP3_VIRTUAL_ATTACK_ITERATION
```

后续真实验证如果系统性推翻该区间，必须记录具体被推翻的现实假设并发布 v2；不能静默移动目标。
