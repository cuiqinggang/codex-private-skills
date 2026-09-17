# H3-P0 ACT32 候选实证结果 v1

状态：`BLOCKED_SOURCE_IDENTITY / STOP / RETURN_TO_GPT`

依据：远端 `9973756` 的 `H3-P0-QUALITY-STABILITY-ACT32-PROOF-COMMAND-v1.md` 第 3 节。该节要求在临时修改前核对 Star7 `nodes.py` 和 ComfyUI `model.py` 的 SHA256；真实值与冻结值不一致时，不覆盖源码并立即停止。

## 源码身份门禁

| 文件 | 本机 SHA256 | 命令包标称 SHA256 | 结果 |
|---|---|---|---|
| `C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-fp16-exact-star7\nodes.py` | `8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B` | `5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7` | MISMATCH |
| `C:\AI\MiniMax-H3\ComfyUI\nodes.py` | `5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7` | 未列为本轮允许修改的 Star7 文件 | 标称值实际对应此文件 |
| `C:\AI\MiniMax-H3\ComfyUI\comfy\ldm\minimax\model.py` | `3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A` | `3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A` | MATCH |

命令包中的 `nodes.py` 冻结值对应 ComfyUI 根目录文件，并不对应本轮允许临时修改的 Star7 自定义节点文件。按照明文停止规则，没有制作 ACT32 补丁，没有修改或覆盖任何源码，没有启动 ComfyUI 或 GPU 运行。

## 执行与裁决

```text
CANDIDATE=STAR7_ACT32_INT8_CONVROT
SOURCE_IDENTITY_GATE=FAIL
ACT32_PROOF=NOT_RUN_SOURCE_IDENTITY_MISMATCH
GPU_RUNS_EXECUTED=0
WARMUPS_EXECUTED=0
FORMAL_RUNS_EXECUTED=0
ACT32_DIFF=NOT_GENERATED
READY_FOR_FINAL_QUALITY_STABILITY_CERTIFICATION=NO
FINAL_QUALITY_STABILITY_99=NO
```

两次预热、四条正式 QC、backend/force_cast/dense fallback 运行证明及三条 paired Total 均未产生；不能据此裁决候选质量或性能。Star7 `nodes.py` 未修改，结束时 SHA256 仍为 `8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B`。无 ACT32 修改，因此没有实际 ACT32 diff 文件。

停止点：等待 GPT 修正或确认命令包的 Star7 源码冻结 SHA256；本轮不自行改动冻结命令或补做 GPU 实验。

## Git 证据

- 阻断证据提交：`8550416e05918fc0b937733922ef9b7e60fcfa70`。
- 首次推送后通过 `git ls-remote origin refs/heads/codex/h3-p0-mature-convergence-v2` 回读，远端 HEAD 与上述提交一致。
- 本节补记在后续提交中；最终远端 HEAD 以任务返回的再次回读结果为准。
