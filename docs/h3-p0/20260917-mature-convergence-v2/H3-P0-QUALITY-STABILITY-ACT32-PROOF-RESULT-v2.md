# H3-P0 ACT32 候选实证结果 v2

```text
CANDIDATE=STAR7_ACT32_INT8_CONVROT
ACT32_PROOF=FAIL_QUALITY
GPU_RUNS_EXECUTED=3
READY_FOR_FINAL_QUALITY_STABILITY_CERTIFICATION=NO
FINAL_QUALITY_STABILITY_99=NO
```

依据：`H3-P0-QUALITY-STABILITY-ACT32-SOURCE-IDENTITY-CORRECTION-v1.md` 与 `H3-P0-QUALITY-STABILITY-ACT32-PROOF-COMMAND-v2.md`。本轮只实施该命令包的唯一 ACT32 候选；在第一条正式样本 `930103` 失败后立即停止 GPU。此前 v1 阻断证据保持原样。

## 源码身份与候选

| 文件 | 操作前及恢复后 SHA256 | 冻结值 |
|---|---|---|
| Star7 自定义节点 `C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-fp16-exact-star7\nodes.py` | `8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B` | MATCH |
| ComfyUI 根 `C:\AI\MiniMax-H3\ComfyUI\nodes.py` | `5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7` | MATCH |
| MiniMax `C:\AI\MiniMax-H3\ComfyUI\comfy\ldm\minimax\model.py` | `3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A` | MATCH |

ComfyUI 提交 `8a33128f2f8c5585c57486c07de481241e70a39c`；RTX 2080 Ti 22GB / sm75。候选临时源码 SHA256 为 `1C0A0D9B3FE514D172FE22909ED7F79C66F808D69644220AB1019CD708590AE6`，实际修改见 `H3-P0-QUALITY-STABILITY-ACT32-PATCH-v2.diff`。只改 Star7 的 FP32 激活边界与日志标识；`K_OUT_PROJ=64.0`、`K_FC2=256.0`、`set_model_compute_dtype(torch.float16)`、condition_proj 保护及模型/采样任务均未改动。候选语法检查、启动标识检查通过。

## 后端门禁

首条预热载入时的日志：

```text
[Star7 H3 ACT32] Enabled v2.0.14 | mode=loader-quantized | backend=int8_tensorwise+convrot:200 | force-cast=False | weight-patches=0 | blocks=50
```

因此 INT8/ConvRot 后端、量化模块数 200、`force_cast_weights=False` 均保持；没有检测到 dense weight fallback。运行日志没有执行异常或 fallback 标记，ComfyUI `comfy.ops` 的量化分支条件仍由 `layout_type`、`force_cast_weights` 和 weight patches 控制。本轮遵守禁止 kernel trace 的规则；“无 dense fallback”依据上述日志和未变更的量化代码路径，不是逐 kernel 跟踪结论。

## GPU 运行与 QC

运行输出满足 history completed、真实 MP4 存在、ffprobe `32×32×5`、ffmpeg 完整解码、像素有限、非黑。逐帧 range 和 std 按冻结门槛 `range>=8` 且 `std>=1.5` 判定。

| 顺序 | 阶段 | Seed | Total s | Generation CUDA s | Path s | QC | 关键逐帧数值 |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | 预热 | 940098 | 186.3754 | 89.9951 | 96.3803 | PASS | 最小 range=80，最小 std=26.1024 |
| 2 | 预热 | 940099 | 19.4245 | 15.9498 | 3.4746 | FAIL（不计正式质量） | 第 1 帧 range=6，std=2.2657 |
| 3 | 正式 | 930103 | 5.0537 | 2.0936 | 2.9600 | **FAIL_QUALITY** | 第 1 帧 range=2，std=0.7454；其余帧 range=28/43/48/51 |
| — | 正式 | 920108 | — | — | — | 未执行 | 第一条正式失败，按停止规则跳过 |
| — | 正式 | 930100 | — | — | — | 未执行 | 同上 |
| — | 正式 | 930101 | — | — | — | 未执行 | 同上 |

预热 940098 MP4 SHA256：`9D33049BC179CE885D885FBF57855F4D50285643836A75974AAE382010B03A3B`。

预热 940099 MP4 SHA256：`2B9DEA8F1B357C8663E810039501A28F2B695298777D00435C8C8A7C0C357AD2`。

正式 930103 MP4 SHA256：`EA7F3C1B3B99048FCD2E4A1C662E6E721617FB42638C93EEB82F44A16BECD65B`。三个文件的 SHA256 均从生成文件重新核对为一致。

## 配对时间与裁决

| Seed | 历史 Star7 Total s | ACT32 Total s | 差值 s | 比值 | 变化 |
|---:|---:|---:|---:|---:|---:|
| 930103 | 6.1379 | 5.0537 | -1.0842 | 0.8234 | -17.66% |
| 930100 | 6.8896 | 未执行 | — | — | — |
| 930101 | 8.6514 | 未执行 | — | — | — |

三条配对样本未集齐，因此不计算 paired median，也不作性能通过/失败裁决。`930103_REPAIRED=NO`；`920108_REPAIRED`、`930100_REMAINS_PASS`、`930101_REMAINS_PASS` 均为未验证。`ACT32_PROOF=FAIL_QUALITY`，不是 `FAIL_PERFORMANCE` 或 `FAIL_BACKEND_MUTATION`。没有设计或测试第二候选，没有追加运行。

## 恢复与原始证据

GPU 提交账本只有 `940098`、`940099`、`930103` 三条。Star7 `nodes.py` 已按字节备份恢复，恢复后 SHA256 为 `8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B`。临时计时插入的 `comfy/samplers.py` 亦已恢复，SHA256 为 `2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE`。原始运行 JSON、工作流、日志、账本、备份与 MP4 路径保存在 `C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-act32-proof-v2-01`。本仓库的 v2 JSON 保存裁决和逐条摘要。

Git 证据提交为 `3a5886bc36502cf39b08762b4ee8c61d9f248ee3`。推送后执行 `git ls-remote origin refs/heads/codex/h3-p0-mature-convergence-v2`，回读的远端 HEAD 与该提交一致。本段补记另行提交；最终远端 HEAD 以返回 GPT 时的再次回读为准。
