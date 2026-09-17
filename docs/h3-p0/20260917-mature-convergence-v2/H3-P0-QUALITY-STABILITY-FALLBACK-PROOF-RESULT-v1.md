# H3-P0 Verified Fast Path 兜底证明结果 v1

```text
SYSTEM_CANDIDATE=VERIFIED_FAST_PATH_V1
VERIFIED_FAST_PATH_PROOF=FAIL_REFERENCE_QUALITY
FINAL_ACCEPTED_QC=1/2
INVALID_OUTPUT_DELIVERED=NO
CONTROLLED_FAIL=YES
NO_SEED_CHANGE=YES
NO_MANUAL_INTERVENTION=YES
GPU_RUNS_EXECUTED=4
READY_FOR_SYSTEM_TIME_ROI_RECALC=NO
FINAL_99=NO
```

依据：`H3-P0-QUALITY-STABILITY-FALLBACK-VIRTUAL-99-v1.md` 与 `H3-P0-QUALITY-STABILITY-FALLBACK-PROOF-COMMAND-v1.md`。只执行 `930103`、`920108` 两个固定 seed；各自 Star7 QC 失败后，自动运行同 seed 标准 `UNETLoader`。第二个 seed 的 reference 仍失败，系统判定 CONTROLLED_FAIL，没有交付该无效输出。没有第三层 retry 或额外 GPU 运行。

## 源码与任务身份

Star7 自定义节点 `nodes.py` 操作前后 SHA256：`8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B`。ComfyUI 根 `nodes.py`：`5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7`；MiniMax `model.py`：`3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A`，均前后不变。`comfy/samplers.py` 也未修改，SHA256 `2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE`。

ComfyUI 提交 `8a33128f2f8c5585c57486c07de481241e70a39c`，GPU RTX 2080 Ti 22GB / sm75。四份实际提交的工作流均使用 `minimax_h3_fl2va_pruned_int8_convrot.safetensors`、`static frame`、`res_multistep`、`beta`、1 step，且每对 Star7/reference 保持同 seed。服务启动 flags 为 `--fast-disk --reserve-vram 1.0 --disable-pinned-memory`。Reference 工作流节点确认为标准 `UNETLoader`。未编辑任何源码。

## 完整生产链与实际交付时间

`DELIVERY_TOTAL` 使用同一运行器的单调时钟，从该 seed 首次 Star7 `POST /prompt` 前，到最终 QC 后作出 ACCEPT 或 CONTROLLED_FAIL。包括首次运行和 QC、切换到原始 Loader、第二次运行和 QC；没有用历史时间拼接。

| Seed | Star7 Total s | Star7 QC s | Star7 QC | Fallback | Reference Total s | Reference QC s | Reference QC | DELIVERY_TOTAL s | 最终裁决 |
|---:|---:|---:|---|---|---:|---:|---|---:|---|
| 930103 | 180.3624 | 3.3344 | FAIL | 是，同 seed | 91.0023 | 0.5017 | PASS | **275.2157** | ACCEPT / UNETLoader |
| 920108 | 92.3179 | 0.4779 | FAIL | 是，同 seed | 105.1330 | 1.0097 | FAIL | **198.9567** | CONTROLLED_FAIL / 不交付 |

每个阶段的 `history` 均 completed，生成真实 MP4，通过 ffprobe `32×32×5` 结构检查和 ffmpeg 解码；像素统计有限、非黑。冻结 QC 仍要求**每帧** `range>=8` 且 `std>=1.5`。

- `930103` Star7：首帧 `range=3`、`std=1.4142`，FAIL；MP4 SHA256 `20A833E11F5D8E7103B61B95E8C5C8C04477CC031CE8C9AD9DCC5754519E1FAB`。
- `930103` reference：最小帧 `range=9`、`std=2.8792`，全帧 PASS；MP4 SHA256 `91DB737B1E9A2AC9F013F3CBB6F5E2E5663370D2648B9129D268BEFD694475D0`。
- `920108` Star7：后四帧 `range=0`、`std=0`，FAIL；MP4 SHA256 `99B36AF38CA2DD577A1B597A16438E7A24FD43FF378C68C28B557CAB4BC87B28`。
- `920108` reference：后四帧仍为 `range=0`、`std=0`，FAIL；MP4 SHA256 `CFD9F1B4CFFAEA3AE3A6480692657105BFDB7A6F36BD58C2042939CE3D9A4D65`。

以上四个 MP4 的 SHA256 均从生成文件再次核对，与运行记录一致。`930103` 只交付通过 QC 的 reference 输出；`920108` 的两份输出均未 ACCEPT。

## GPU 账本与结论

| 提交序号 | Seed | 路径 |
|---:|---:|---|
| 0 | 930103 | Star7 |
| 1 | 930103 | 原始 UNETLoader |
| 2 | 920108 | Star7 |
| 3 | 920108 | 原始 UNETLoader |

`GPU_RUNS_EXECUTED=4`，等于命令包上限。`930103` 得到最终有效输出，`920108` 的 reference 也白/平坦，故 `FINAL_ACCEPTED_QC=1/2`，未达到 2/2 通过条件。正式裁决 `VERIFIED_FAST_PATH_PROOF=FAIL_REFERENCE_QUALITY`；该 seed 在生产链内被受控拒绝。不能据此宣告最终 99，也不进入本轮系统时间收益复算。

原始运行记录、逐帧 QC、四份工作流、日志和提交账本保存在 `C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260918-fallback-proof-v1-01`。同目录 `runner-state.json` 的完整数据已保存为本仓库对应的 `...FALLBACK-PROOF-STATE-v1.json`。

Git 证据提交与远端回读将在提交后补记；最终远端 HEAD 以返回 GPT 时的回读为准。
