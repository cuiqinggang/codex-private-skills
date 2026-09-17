# H3-P0 质量稳定性最后一次定向定位结果 v1

状态：`FINAL_LOCALIZATION_EXECUTED / STOP / RETURN_TO_GPT`

依据：`H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-COMMAND-v1.md`、同名 `PLAN-v1.md` 及上一轮 v2 诊断结果。只执行固定四条 GPU 运行；未改精度策略、Star7 算法、模型、seed、sampler、scheduler 或参数，未执行修复、profiler、kernel trace、版本/参数搜索。

## 四条运行与内容 QC

| # | Seed | Loader | QC | 首帧 mean / range / std | 全帧 range | MP4 SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 930103 | MiniMaxH3FP16LoaderStar7 | FAIL：首帧近白/平坦 | 254.0000 / 3 / 1.4142 | 3, 26, 40, 46, 50 | `954DBEB2A2AB3879164255F6B017A8DCD62B1EB5B7AC9FF4A6D4A01111F8E8C5` |
| 2 | 930103 | 原始 UNETLoader | PASS | 251.6644 / 9 / 2.8792 | 9, 18, 29, 39, 50 | `857CA588F2F69605A20753C78FC5F95366B528B3574CF9B7D84B45CCD3338D8D` |
| 3 | 930100 | MiniMaxH3FP16LoaderStar7 | PASS | 61.4069 / 163 / 61.0207 | 163, 148, 133, 126, 129 | `2BAB51DE7A8F2A42E3409E1C1537D081E12664A6D8BC734DA63880F64298C49B` |
| 4 | 930100 | 原始 UNETLoader | PASS | 43.3945 / 107 / 35.9963 | 107, 105, 90, 84, 85 | `9E58838520BE371BFA66D5DE3069942274BDAD17E85D581A37E8129992849B3E` |

四个 MP4 均为 32×32×5、可解码、像素 finite、非黑；按原门槛逐帧检查 range≥8 与 std≥1.5。第 1 条只因首帧低于两项门槛而失败。

## 采样与配对

每条运行取得 **204 个**边界样本：`condition_proj` 1 个、50 个 DiT block 各 4 个、FinalLayer 输入与 video 输出及 Pre-VAE video latent 各 1 个。每个 tensor 先转 FP32、flatten，再按整数公式取最多 1024 个确定性等距索引；同 seed 两条路径的 shape、元素数与索引 SHA256 全部对齐。所有已采样元素 finite；只在本地临时保存小样本，未保存完整 tensor。

逐边界计算 relative L2 error、cosine similarity、max/median absolute difference、sign flip rate、std ratio、normalized mean shift。`error growth ratio` 用当前边界与上一层**同类边界**的 relative L2 比值；跨不同分支的比值只作为描述，不作为因果跳变判据。全部 50 层、两 seed、四类 block 边界的逐项指标见 `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-STATE-v1.json`。

### 残差链误差曲线摘要

下表是各 block **最终 residual 输出**的 relative L2；`F/P` 分别为失败 seed `930103` 和通过 seed `930100`。两条曲线在早期均很低，中后段均跨多层增长，并非只有失败 seed 出现深层误差。

| Block | F | P | Block | F | P |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.007682 | 0.007845 | 25 | 0.010618 | 0.006670 |
| 5 | 0.005601 | 0.005705 | 30 | 0.018628 | 0.014115 |
| 10 | 0.004993 | 0.005417 | 34 | 0.036467 | 0.031431 |
| 13 | 0.004667 | 0.005090 | 35 | 0.036203 | 0.042511 |
| 14 | 0.005131 | 0.005144 | 38 | 0.049990 | 0.065819 |
| 15 | 0.006968 | 0.005165 | 40 | 0.060268 | 0.074529 |
| 20 | 0.009719 | 0.006015 | 45 | 0.085239 | 0.081047 |
| 24 | 0.010343 | 0.006503 | 47 | 0.116503 | 0.084934 |
|  |  |  | 48 | 0.114195 | 0.127694 |
|  |  |  | 49 | 0.079755 | 0.084150 |

### 最大误差增长边界与局部候选

| 边界 | 930103 增长 / relative L2 | 930100 同处 | 裁决 |
| --- | --- | --- | --- |
| block 14 MLP 分支 | 13.30× / 0.10700 | 5.42× / 0.02952 | 失败 seed 明显偏高；cosine 0.996060 对 0.999568，sign flip 1.76% 对 0.88% |
| block 14 Attention 分支 | 1.91× / 0.04282 | 0.95× / 0.01941 | 同层支持局部误差增强 |
| block 15 最终 residual | 1.36× / 0.006968 | 1.00× / 0.005165 | 有后续传播迹象；block 14 最终 residual 仍为 0.005131 对 0.005144 |
| block 31 最终 residual | 1.32× / 0.024569 | 1.25× / 0.017650 | 两 seed 均增长 |
| block 38 最终 residual | 1.34× / 0.049990 | 1.49× / 0.065819 | 通过 seed 增长更大 |
| block 47 最终 residual | 1.25× / 0.116503 | 0.90× / 0.084934 | 失败 seed 局部再次偏高，但下一层反转 |

block 14 是最强局部候选，但**不能裁决为首次致病突变**：该层最终 residual 的误差与通过 seed 几乎相同；到 block 35、38 和 48，通过 seed 的最终 residual 误差反而更大。失败 seed 的 FinalLayer 输入 relative L2 为 0.079755，通过 seed 为 0.084150；FinalLayer video 输出为 0.171939 对 0.303235，Pre-VAE latent 为 0.205930 对 0.431663。通过 seed 在输出端的相对误差更大却仍 QC PASS。block 14 的误差没有作为失败 seed 独有增幅持续到终端，归一化均值漂移也未显示可靠的持续正向亮度偏移。因此不满足冻结命令的五项单点定位条件。

早期 `condition_proj` 的两 seed relative L2 均为约 0.000075、cosine 约 1.0。中段 residual 从 block 15 左右开始出现失败 seed 较大的区间性偏离；block 27–48 的多层增长在通过 seed 也存在，最终两条曲线交错。对这组固定小样本，整体形态更符合分布式传播和累积误差，而不是一个足以解释 QC 失败的持续单点跳变。

## 最终裁决

`ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION`

`FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE`

`CONFIDENCE=MEDIUM`

`LIKELY_MECHANISM=FP16 快速路径与原始精度路径的有限值误差经多层 Attention/MLP 与 residual 传播累积；930103 的画面本已接近白色量化上限，终端差异可使首帧跨过平坦 QC 阈值。block 14 有局部误差峰值，但未满足持续、失败独有及输出方向三项定位条件。`

此结论限于固定两 seed、四次 GPU 运行及每个 tensor 最多 1024 个等距样本；没有把误差幅度本身当作 QC 失败的充分条件。按计划停止寻找“某一个坏算子”，不派生 v4/v5 诊断链；下一步由 GPT 做最小精度保护组合的 Virtual-99 设计。

## 源码恢复与交付

仅临时插入只读采样代码。两处源码在四条运行结束后恢复，前后 SHA256 完全一致：

- `C:\AI\MiniMax-H3\ComfyUI\comfy\ldm\minimax\model.py`：`3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A`
- `C:\AI\MiniMax-H3\ComfyUI\nodes.py`：`5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7`

`GPU_RUNS_EXECUTED=4`

`REPAIR_EXPERIMENTS_EXECUTED=0`

Git commit 与 remote verify 的核验记录将在结果提交推送后回填；最终远端 HEAD 见交付返回。

`NEXT_ACTION=STOP_RETURN_TO_GPT_VIRTUAL_99`
