# H3-P0 质量稳定性数值边界诊断结果 v2

状态：`DIAGNOSTIC_EXECUTED / RETURN_TO_GPT`

依据：冻结的 `H3-P0-QUALITY-STABILITY-DIAGNOSTIC-COMMAND-v1.md` 与 `H3-P0-QUALITY-STABILITY-99-VIRTUAL-PLAN-v1.md`。此前 v1 的 `BLOCKED_EXECUTION_ENVIRONMENT / GPU_RUNS_EXECUTED=0` 仅为环境阻断记录，不参与本次技术裁决。

## 固定运行与 QC

按指定顺序完成恰好四条 GPU 运行。诊断运行的耗时不用于性能裁决，未执行第五条、修复试验或参数搜索。

| # | Seed | Loader | QC | 首帧 mean / range / std | 全帧 range | MP4 SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 930103 | MiniMaxH3FP16LoaderStar7 | FAIL：首帧平坦/近白 | 254.0000 / 3 / 1.4142 | 3, 26, 40, 46, 50 | `B291D9AAEAA2051950423808B683D183B7D1F8021BA45344351E7697DD7D5B4E` |
| 2 | 930103 | 原始 UNETLoader | PASS | 251.6644 / 9 / 2.8792 | 9, 18, 29, 39, 50 | `F67039071E820243BC753FD7B73A185B935943CB103DABFB7DFABB52512D3788` |
| 3 | 930100 | MiniMaxH3FP16LoaderStar7 | PASS | 61.4069 / 163 / 61.0207 | 163, 148, 133, 126, 129 | `445C81D4937570830E2D19475786115FC93CE0FF88E00AA0A02255E1FB5167AF` |
| 4 | 930100 | 原始 UNETLoader | PASS | 43.3945 / 107 / 35.9963 | 107, 105, 90, 84, 85 | `3F88471156AC1067449E8CC59325057FA52B2E118F9EA780D5AEF8A083C2CBDC` |

四个 MP4 均为 32×32×5、可解码、像素 finite、非黑；逐帧 std 和 range 均按原门槛检查。第 1 条重现既知首帧 QC FAIL，故按命令包继续第 2–4 条。各运行的完整逐帧 QC、文件路径、SHA256 和边界摘要保存在 `H3-P0-QUALITY-STABILITY-DIAGNOSTIC-STATE-v2.json`。

## 已观测的数值边界

每条运行记录 `dtype / shape / finite / NaN / Inf / min / max / mean / std / absmax / p01 / p50 / p99 / rms / abs_ge_60000` 摘要；不保存完整 tensor。采样 block 为 0、10、20、30、40、49。Star7 每条 125 条摘要，原始 Loader 每条 113 条；所有已记录摘要的 NaN 和 Inf 均为 0。

| 边界（930103） | Star7 | 原始 Loader | 对照含义 |
| --- | --- | --- | --- |
| `t_emb`，block 0 | FP32，std 0.17139，absmax 0.46788 | FP32，完全相同 | 未见时间嵌入分叉 |
| `adaln_shift_msa`，block 0 | FP32，std 0.17808，absmax 1.03182 | FP32，完全相同 | 已采样 AdaLN shift/scale/gate 摘要一致 |
| norm+mod 后 h，block 0 | FP16，std 0.29241，absmax 9.10938 | FP32，std 0.29241，absmax 9.11290 | 精度路径不同；整体尺度接近 |
| Q after RMSNorm+RoPE，block 0 | FP16，std 1.11398，absmax 9.52344 | FP32，std 1.11398，absmax 9.52425 | 整体尺度接近 |
| K after RMSNorm+RoPE，block 0 | FP16，std 1.12941，absmax 10.29688 | FP32，std 1.12941，absmax 10.30350 | 整体尺度接近 |
| Attention out_proj 前，block 0 | FP16，std 1.68705，absmax 36.03125 | FP32，std 1.68698，absmax 36.02332 | 整体尺度接近 |
| Attention out_proj 后，block 49 | FP32，std 355.34485，absmax 11288.0 | FP32，std 354.19189，absmax 11815.44922 | 深层差异存在，未构成独有塌缩证据 |
| block 49 residual / FinalLayer 输入 | FP32，std 8231.79297，absmax 1497124.375 | FP32，std 8288.41113，absmax 1499582.125 | 整体尺度接近，均 finite |
| FinalLayer video 调制后 | FP32，std 0.12476，absmax 2.58494 | FP32，std 0.12011，absmax 2.44648 | 差异存在，但非突发塌缩 |
| FinalLayer video 输出 | FP32，std 1.42203，absmax 3.74878 | FP32，std 1.29150，absmax 3.64301 | Star7 std 高约 10.1% |
| Pre-VAE video latent | FP32，shape `[1,24,2,2,2]`，std 1.18931，absmax 2.37811 | 同 shape，std 1.07891，absmax 2.28639 | Star7 std 高约 10.2%，均 finite |

通过 seed `930100` 的 FinalLayer video 输出 std 也为 Star7 1.64279、原始 Loader 1.43327（约高 14.6%）；Pre-VAE latent std 为 1.31850 对 1.00690（约高 30.9%），但两条路径均 QC PASS。因此单凭这些摘要差异不能把 FinalLayer 或 Pre-VAE 判为失败 seed 的首次异常边界。

### 覆盖限制

- `condition_proj` 在模型 `_forward` 之前执行；本次钩子在 `_forward` 起点安装，四条运行均未取得其输出摘要。不能排除该更早边界的元素级差异。
- 原始 Loader 的 `fc2` 使用融合运算，没有独立 `fc2` 输入/输出钩子记录；已记录 `fc1`、只读重算的 SwiGLU 摘要及 MLP 输出。Star7 的 `fc2` 有独立摘要。
- 所有比较仅用聚合统计，未保存完整 tensor，也未做元素逐点对照。采样 block 之间可能存在未捕获的首次分叉。

## 裁决

`FAILURE_NOT_REPRODUCED=NO`

`FIRST_DIVERGENCE=NOT_LOCALIZED`

`CONFIDENCE=LOW`

`LIKELY_MECHANISM=Star7 的 FP16 路径与原始 Loader 的默认精度路径产生有限值差异；失败 seed 的首帧已贴近 8-bit 白色上限，差异经最终输出与 VAE 映射后跨过逐帧平坦阈值。现有聚合摘要不能证明具体首次触发算子。`

可确认的前一边界是相同的 `t_emb` 与已采样 AdaLN 调制摘要；未能确认“第一个异常尺度/塌缩/饱和的内部边界”。这是一项本轮真实运行后的有限技术结论，不能使用 v1 的环境阻断记录补足缺失边界。没有设计或执行修复。

## 恢复与收口

只在运行期间临时插入只读统计钩子；`comfy/ldm/minimax/model.py` 与 `nodes.py` 已在 `finally` 恢复。前后 SHA256 分别一致：

- `model.py`：`3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A`
- `nodes.py`：`5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7`

`GPU_RUNS_EXECUTED=4`

`NEXT_ACTION=RETURN_TO_GPT`
