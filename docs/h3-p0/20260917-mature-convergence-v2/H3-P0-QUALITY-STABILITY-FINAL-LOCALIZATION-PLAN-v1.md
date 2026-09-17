# H3-P0 质量稳定性99 — 最后一次定向定位计划 v1

状态：`FINAL_LOCALIZATION_PLAN / BOUNDED / NO_REPAIR`

## 目标

在不修改 Star7 数值算法、不搜索参数、不做性能优化的前提下，判断 930103 的质量失败究竟是：

1. 某个明确局部边界出现异常误差突增；或
2. 50 层 FP16 路径的分布式小误差逐层累积，最终把接近白色阈值的样本推过 QC 边界。

本计划是质量稳定性99的**最后一次定位诊断**。若仍无法定位局部突变，禁止继续产生 v4/v5 诊断链，直接进入“分布式累积误差”虚拟修复设计。

## 已有 v2 事实

- 930103：Star7 QC FAIL；原始 UNETLoader QC PASS。
- 930100：两条路径均 PASS。
- v2 未发现 t_emb、已采样 AdaLN、Q/K+RoPE、主干 residual、FinalLayer、Pre-VAE 上失败 seed 独有的明显尺度塌缩。
- 所有已采摘要均 finite，无 NaN/Inf。
- v2 覆盖缺口：condition_proj 未采；block 只抽样 0/10/20/30/40/49；使用聚合统计，不能观察逐层元素误差增长。

## 核心方法

只对相同 seed、相同任务的 Star7 与 reference 路径做固定位置的小样本比较。

每个被比较 tensor：

- 转 FP32；
- flatten；
- 使用完全确定的等距索引，最多采 1024 个元素；
- 不保存完整 tensor；
- reference 与 Star7 使用完全相同索引。

配对后计算：

- `relative_l2_error = ||fast-ref|| / max(||ref||, eps)`；
- cosine similarity（余弦相似度）；
- max absolute difference（最大绝对差）；
- median absolute difference（绝对差中位数）；
- sign flip rate（符号翻转比例）；
- std ratio；
- mean shift normalized by reference std；
- 每层相对上一层的 error growth ratio（误差增长率）。

## 固定边界

必须覆盖：

1. `condition_proj` 输出；
2. 每一个 DiT block（0–49）的：
   - block 输入 residual；
   - attention 分支输出进入 residual gate 前；
   - MLP 分支输出进入 residual gate 前；
   - block 最终 residual 输出；
3. FinalLayer 输入；
4. FinalLayer video 输出；
5. Pre-VAE video latent。

不再采 profiler、kernel trace 或无关模块。

## 四条固定运行

1. 930103 + Star7
2. 930103 + 原始 UNETLoader
3. 930100 + Star7
4. 930100 + 原始 UNETLoader

`MAX_GPU_RUNS=4`

## 局部突变判据

不能因为 FP16 与 reference 有差异就判故障。只有同时满足以下条件，才允许声明局部 FIRST_DIVERGENCE：

1. 930103 在某层/边界的配对误差较前一边界出现显著跃升；
2. 930100 同位置没有相近幅度的跃升；
3. 930103 之后误差持续保持或扩大；
4. 数值变化与最终近白/平坦输出方向一致；
5. 至少两个误差指标同时支持（例如 relative L2 + cosine / sign flip / normalized mean shift）。

否则不得强行定位。

## 最终仅允许两个大类结论

### A. 局部突变

`ERROR_TOPOLOGY=LOCALIZED_JUMP`

输出：
- `FIRST_DIVERGENCE=<具体 block/边界>`
- `CONFIDENCE=HIGH/MEDIUM`
- `LIKELY_MECHANISM=<中文说明>`

### B. 分布式累积

若从 condition_proj 到 FinalLayer 都只见平滑误差增长，没有失败 seed 独有局部突变：

`ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION`

`FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE`

这将成为正式技术结论；停止继续定位，下一步由 GPT 虚拟设计最小精度保护组合。

### C. 仍不充分

只有采样/执行本身不完整时才允许：

`ERROR_TOPOLOGY=INCONCLUSIVE`

不得用 INCONCLUSIVE 开启自由探索。

## 禁止

- 修改 FP16/FP32 策略；
- 修改 K_OUT_PROJ/K_FC2；
- 修改模型、seed、sampler、scheduler；
- 性能剖析；
- 参数/版本搜索；
- 自动修复；
- GPU 超过 4 次；
- 派生新诊断版本。

## 下一步

本诊断结束后无论 LOCALIZED_JUMP 或 DISTRIBUTED_ACCUMULATION，都必须 STOP → RETURN GPT。GPT 再做质量稳定性 Virtual-99 修复设计。