# H3-P0 质量稳定性99：最小数值边界诊断命令 v1

状态：`READY_TO_EXECUTE / QUALITY_STABILITY_PATH_ONLY`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎 v1.9.0）`

依据：`H3-P0-QUALITY-STABILITY-99-VIRTUAL-PLAN-v1.md`

## 1. 目标

仅回答：

> Star7 FP16 快速路径在失败 seed `930103` 上，和原始 UNETLoader 相比，第一次明确数值分叉发生在哪一个已定义边界？

不是性能优化，不允许自由探索。

## 2. 固定任务

保持现有 H3-P0 固定任务、模型、VAE、text encoder、sampler、scheduler、flags、计时合同不变。

仅比较 loader：

```text
FAST = MiniMaxH3FP16LoaderStar7
REF  = 原始 UNETLoader
```

固定 seed：

```text
FAIL_SEED = 930103
PASS_SEED = 930100
```

## 3. 最大运行

最多 4 条 GPU 运行：

```text
1. 930103 FAST
2. 930103 REF
3. 930100 FAST
4. 930100 REF
```

不得增加第5条。

如果第1条 `930103 FAST` 不再复现内容 QC FAIL：

```text
FAILURE_NOT_REPRODUCED=YES
→ 保存证据
→ 不再提交第2-4条
→ STOP
→ RETURN GPT
```

## 4. 允许的临时诊断

只允许在候选副本/可恢复插桩中记录以下统计摘要：

```text
dtype
finite
min
max
mean
std
absmax
```

禁止保存完整 tensor。

边界：

```text
A. condition_proj 输出
B. t_emb 与 AdaLN shift / scale / gate
C. block 0 / 10 / 20 / 30 / 40 / 49：
   1) norm+mod 后 h
   2) Q/K RMSNorm+RoPE 后 q/k
   3) attention 输出：out_proj 前 / 后
   4) MLP：fc1、SwiGLU activated、fc2
   5) block residual x
D. FinalLayer：输入、调制后、最终输出
E. VAE 前 video latent
```

诊断运行不做正式性能裁决；时间只记录，不作为优化 KEEP 条件。

## 5. 插桩约束

- 修改前备份源码并记录 SHA256；
- 只允许读取/统计，不改变 tensor 数值；
- 不允许 clamp、cast 修复、缩放调整、参数变化；
- 不允许 profiler（性能剖析）、kernel trace（内核追踪）；
- 不允许版本升级、模型替换、参数 sweep；
- 结束后必须恢复源码，并回读 SHA256 与原值一致。

如果无法做到“只观测、不改变数学结果”，停止返回 GPT。

## 6. QC

每条仍执行原 H3-P0 内容 QC：

- MP4 32×32×5；
- ffmpeg 可解码；
- finite；
- 非黑/非平坦；
- 每帧 range≥8；
- 每帧 std≥1.5；
- 保存 SHA256。

不得降低门槛。

## 7. 分叉判定

将同 seed FAST 与 REF 的每个边界统计对齐比较。

只允许输出：

```text
FIRST_DIVERGENCE =
  ADALN
  / QK_ROPE_ATTENTION
  / OUT_PROJ_MLP
  / FINAL_LAYER
  / PRE_VAE_LATENT
  / NOT_IDENTIFIED
```

并写明：

- 第一个出现异常尺度/塌缩/饱和的边界；
- 前一个仍正常的边界；
- FAST 与 REF 的关键统计差；
- PASS seed 是否存在同类分叉；
- 置信度 HIGH/MEDIUM/LOW。

不得自行提出并执行修复。

## 8. 结果文件

生成：

```text
H3-P0-QUALITY-STABILITY-DIAGNOSTIC-RESULT.md
H3-P0-QUALITY-STABILITY-DIAGNOSTIC-RESULT.json
```

至少包含：

- 4条以内运行结果；
- 各边界统计摘要；
- FIRST_DIVERGENCE；
- QC；
- 插桩前后源码 SHA256；
- 是否复现失败；
- 诊断置信度；
- `NEXT_ACTION=RETURN_TO_GPT`。

完成：

```text
commit → push → remote verify → STOP → RETURN GPT
```

Codex 不得继续进入任何修复实验。
