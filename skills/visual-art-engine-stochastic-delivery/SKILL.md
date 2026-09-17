---
name: visual-art-engine-stochastic-delivery
description: Visual Art Engine 的随机生成交付子技能。用于图像/视频/粒子/生成式视觉任务中，将随机候选生成与最终交付质量分离：最快生成路径 -> 严格 QC -> 失败候选拒绝 -> 新随机 seed 重采样 -> 首个合格结果交付。优化 Time To First Valid Result，而不是强迫每个随机 seed 单次成功。exact-seed、参考复刻、精确编辑等语义依赖固定输入的任务不得默认自动换种。
metadata:
  version: "1.0.0"
  parent: "visual-art-engine-performance-ladder"
  method_dependency: "first-principles-physical-limit-convergence@2.0.0"
---

# Visual Art Engine — Stochastic Verified Delivery v1.0.0

## 1. 目标

对于本质随机的视觉生成，正式优化目标是：

```text
在最终质量硬约束成立时
最小化 Time To First Valid Result（T_TFVR）
```

不是：

```text
每一个随机 seed 第一次都必须成功
```

## 2. 默认生产状态机

仅在 seed 不属于用户语义时使用：

```text
NEW_RANDOM_SEED
-> FAST_GENERATION
-> QC
-> PASS: ACCEPT
-> FAIL: REJECT + NEW_RANDOM_SEED
```

质量失败没有“为了方便而降低 QC”的权限。

## 3. QC 独立于生成器

生成器只负责 proposal；QC/verifier 负责决定是否交付。

视觉 QC 可按任务包含：

- 文件存在与可解码；
- 尺寸/帧数/时长；
- finite / 非黑 / 非平坦；
- 结构、区域、颜色、动态范围；
- 参考图/参考视频相似度；
- 用户指定视觉约束；
- 作品完整性与安全门禁。

任何 QC FAIL：

```text
INVALID_OUTPUT_DELIVERED=NO
```

## 4. 什么时候允许自动换 seed

允许：

- 自由创作图像/视频；
- 用户只要求“得到一个合格作品”；
- seed 只是内部随机状态；
- verifier 可以可靠判定合格/不合格。

不允许默认换种：

- 用户要求 exact seed；
- benchmark 要求同 seed A/B；
- 参考复刻中 seed 是固定证据变量；
- 精确编辑要求同输入状态对照；
- 故障定位需要复现同一失败；
- retry 会改变用户语义。

## 5. 正式指标

每个 production/certification batch 至少记录：

```text
FIRST_ATTEMPT_PASS_RATE
ATTEMPT_PASS_RATE
MEAN_ATTEMPTS_PER_TASK
ATTEMPTS_P50/P95/MAX
T_TFVR Mean/P50/P95/Max
INVALID_OUTPUTS_REJECTED
INVALID_OUTPUT_DELIVERED
```

普通视觉生产默认以 `T_TFVR` 作为端到端时间。

## 6. 与 Performance Ladder 的关系

`visual-art-engine-performance-ladder` 负责性能阶段、Benchmark Contract、99/FREEZE。

本技能只改变**随机视觉任务的完成语义和计时边界**：

```text
ATTEMPT_RUNTIME != USER_DELIVERY_TIME
```

当随机重采样启用时：

```text
T_END_TO_END = T_TFVR
```

而不是单次 attempt runtime。

## 7. 失败优先级

当某些随机样本失败时，优先判断：

```text
A. random-sample failure?
B. algorithm failure?
C. verifier/QC error?
D. execution/control-plane failure?
```

只有 A 且 seed 非用户语义时，才进入 reseed。

不要因为少量随机失败让 100% task 全部降级到明显更慢路径。

## 8. H3-P0 成功案例

固定 T2VA 32x32 / 5 frames / 1 step：

```text
20 formal delivery tasks
22 attempts
first-attempt PASS=18/20=90%
mean attempts=1.10
T_TFVR mean=6.804s
P50=6.076s
P95=11.974s
max=12.862s
final accepted QC=20/20
invalid delivered=0
```

关键失败经验：

- 固定 seed 10/10 认证失败；
- ACT32 质量修复失败；
- same-seed 原始 Loader fallback 对部分 seed 仍失败且很慢；
- 新随机 seed 的同一最快 Star7 1-step 路径恢复成功；
- 最终 20-task 系统认证通过。

事实源：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-FINAL-99-FREEZE-v1.md`

## 9. 最终原则

> 视觉随机生成应把“产生候选”和“交付作品”分开：用最快成熟路径提出候选，用严格 QC 验证；坏候选立即丢弃，仅在语义允许时重新随机采样，直到得到首个合格作品。