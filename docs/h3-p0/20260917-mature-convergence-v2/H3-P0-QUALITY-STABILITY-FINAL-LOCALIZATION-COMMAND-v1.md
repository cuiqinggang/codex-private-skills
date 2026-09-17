# H3-P0 质量稳定性99 — 最后一次定向定位命令 v1

状态：`READY_TO_EXECUTE / MAX_GPU_RUNS=4 / NO_REPAIR`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎 v1.9.0）`

必须先读取：

- `H3-P0-QUALITY-STABILITY-DIAGNOSTIC-RESULT-v2.md`
- `H3-P0-QUALITY-STABILITY-DIAGNOSTIC-STATE-v2.json`
- `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-PLAN-v1.md`

## 唯一目标

判断 930103 的 Star7 质量失败是：

- `LOCALIZED_JUMP（局部数值突变）`；还是
- `DISTRIBUTED_ACCUMULATION（分布式累积误差）`。

不得做修复。

## 最高约束

`NO_FREE_EXPLORATION=YES`

Codex 仅允许解决执行层问题，不允许改变测试内容。

允许：
- 等价 PowerShell / Python 脚本写法；
- 临时只读 instrumentation（插桩）；
- 本地临时保存固定小样本用于配对计算；
- 任务结束后恢复源码并核验 SHA256。

禁止：
- 改 Star7 数值算法；
- 改 FP16/FP32 策略；
- 改模型、seed、参数；
- profiler、kernel trace；
- 参数扫描、版本扫描；
- 自动修复；
- 第 5 条 GPU 运行；
- 派生下一轮诊断。

## 固定任务

与最终认证完全相同：

- T2VA
- 32×32
- 5帧
- 1 step
- prompt=`static frame`
- sampler=`res_multistep`
- scheduler=`beta`
- 无输入音频
- 真实 MP4
- flags=`--fast-disk --reserve-vram 1.0 --disable-pinned-memory`

模型保持：

- diffusion=`minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- text encoder=`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
- VAE=`minimax_h3_video_vae_fp16.safetensors`

## 四条 GPU 运行

1. `930103 + MiniMaxH3FP16LoaderStar7`
2. `930103 + 原始 UNETLoader`
3. `930100 + MiniMaxH3FP16LoaderStar7`
4. `930100 + 原始 UNETLoader`

`MAX_GPU_RUNS=4`

## 数值采样规则

每个指定 tensor：

1. 转 FP32；
2. flatten；
3. 使用确定性等距索引；
4. 最多采 1024 个元素；
5. Star7/reference 必须使用相同索引；
6. 不保存完整 tensor。

必须覆盖：

### 早期边界
- `condition_proj` 输出；

### 50 个 DiT block：0–49 全部
每层记录：
- block 输入 residual；
- attention 分支输出（进入 residual gate 前）；
- MLP 分支输出（进入 residual gate 前）；
- block 最终 residual 输出。

### 输出边界
- FinalLayer 输入；
- FinalLayer video 输出；
- Pre-VAE video latent。

## 配对误差指标

同 seed 的 Star7/reference 配对后逐层计算：

- relative L2 error（相对L2误差）；
- cosine similarity（余弦相似度）；
- max absolute difference（最大绝对差）；
- median absolute difference（绝对差中位数）；
- sign flip rate（符号翻转率）；
- std ratio（标准差比）；
- normalized mean shift（均值漂移/参考std）；
- error growth ratio（相对上一边界的误差增长率）。

同时对比：

`930103失败seed的误差曲线`
vs
`930100通过seed的误差曲线`

## FIRST_DIVERGENCE 规则

只有同时满足以下条件才允许定位：

1. 930103 某边界相对前一边界误差显著跃升；
2. 930100 同边界没有相近跃升；
3. 后续误差持续保持或扩大；
4. 至少两个误差指标同时支持；
5. 与最终近白/平坦输出方向相符。

否则不得强行定位。

## 最终裁决

### 若找到局部突变

输出：

`ERROR_TOPOLOGY=LOCALIZED_JUMP`

`FIRST_DIVERGENCE=<具体block/边界>`

`CONFIDENCE=HIGH/MEDIUM`

`LIKELY_MECHANISM=<中文机制说明>`

### 若没有单点突变而是平滑累积

输出：

`ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION`

`FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE`

`CONFIDENCE=HIGH/MEDIUM`

并明确误差从哪些层开始持续扩大。

### 只有测试本身不完整才允许

`ERROR_TOPOLOGY=INCONCLUSIVE`

## 证据输出

生成：

- `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-RESULT-v1.md`
- `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-STATE-v1.json`

必须包含：
- 4 条运行与 QC；
- 930103/930100 的逐层误差曲线摘要；
- 最大误差增长的 top 边界；
- ERROR_TOPOLOGY；
- FIRST_DIVERGENCE；
- LIKELY_MECHANISM；
- CONFIDENCE；
- instrumentation 前后源码 SHA256；
- 恢复证明；
- GPU_RUNS_EXECUTED；
- Git commit；
- remote verify。

完成后：

`STOP → RETURN_TO_GPT`

无论定位成功还是判为分布式累积，都不得自行进入修复。