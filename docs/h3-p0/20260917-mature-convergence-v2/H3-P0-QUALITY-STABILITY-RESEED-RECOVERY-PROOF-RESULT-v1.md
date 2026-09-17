# H3-P0 Star7 随机换种恢复证明结果 v1

```text
CANDIDATE=STAR7_RESEED_UNTIL_PASS_V1
RESEED_RECOVERY_PROOF=PASS
FINAL_ACCEPTED_QC=2/2
INVALID_OUTPUTS_REJECTED=2
INVALID_OUTPUT_DELIVERED=NO
EVERY_RETRY_USED_NEW_RANDOM_SEED=YES
NO_MANUAL_SEED_SELECTION=YES
MODEL_AND_RUNTIME_UNCHANGED=YES
STEP_REMAINS_1=YES
STAR7_ONLY=YES
QUALITY_RETRY_LIMIT=NONE
GPU_RUNS_EXECUTED=4
READY_FOR_FINAL_RESEED_SYSTEM_CERTIFICATION=YES
FINAL_QUALITY_STABILITY_99=NO
```

依据：`H3-P0-QUALITY-STABILITY-RESEED-UNTIL-PASS-VIRTUAL-99-v1.md` 与 `H3-P0-QUALITY-STABILITY-RESEED-RECOVERY-PROOF-COMMAND-v1.md`。未执行 Adaptive-Step、ACT32、原始 Loader fallback 或其他候选。Task A/B 均从固定失败 seed 起步，首次 QC FAIL 后自动使用操作系统随机源 `secrets.randbits(63)` 抽取未用过的新 seed；各自在第 2 次 attempt 首次 QC PASS 并停止。没有固定质量 retry 次数上限。

## 身份与后端

ComfyUI 提交 `8a33128f2f8c5585c57486c07de481241e70a39c`，GPU RTX 2080 Ti 22GB / sm75。源码操作前后 SHA256 一致：Star7 `nodes.py`=`8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B`，ComfyUI 根 `nodes.py`=`5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7`，MiniMax `model.py`=`3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A`，`comfy/samplers.py`=`2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE`。未修改任何上述源码。

启动 flags 为 `--fast-disk --reserve-vram 1.0 --disable-pinned-memory`。四份提交工作流均为 `MiniMaxH3FP16LoaderStar7`、`minimax_h3_fl2va_pruned_int8_convrot.safetensors`、`static frame`、32×32、5 帧、1 step、`res_multistep`、`beta`。日志证明 `backend=int8_tensorwise+convrot:200 | force-cast=False | weight-patches=0 | blocks=50`。

## 全部 attempts

每条均有 completed history、真实 MP4、ffprobe `32×32×5`、ffmpeg 解码、有限像素、非黑结果与 MP4 SHA256。冻结 QC 要求**每帧** `range>=8` 且 `std>=1.5`。完整逐帧 range/std、文件路径与计时原值见同名 JSON。

| Task | attempt | Seed | 来源 | Total s | Generation wall s | Path wall proxy s | QC s | 最小帧 range / std | QC |
|---|---:|---:|---|---:|---:|---:|---:|---|---|
| A | 1 | 930103 | 固定失败起点 | 168.8476 | 79.23 | 89.6176 | 0.7383 | 3 / 1.4142 | FAIL / 拒绝 |
| A | 2 | 4462651218371415901 | OS 随机新 seed | 19.1144 | 15.31 | 3.8044 | 0.3025 | 19 / 5.4816 | PASS / ACCEPT |
| B | 1 | 920108 | 固定失败起点 | 5.5506 | 2.16 | 3.3906 | 0.1300 | 0 / 0 | FAIL / 拒绝 |
| B | 2 | 1350105258942230860 | OS 随机新 seed | 5.7018 | 2.33 | 3.3718 | 0.1332 | 110 / 44.2951 | PASS / ACCEPT |

随机 seed 抽取账本记录 Task A 的 `4462651218371415901` 与 Task B 的 `1350105258942230860`，两次均非重复、均由 `secrets.randbits(63)` 生成。两个固定初始 seed 和两个随机 seed 在整个任务内互不重复；没有人工挑选历史 PASS seed。

四份 MP4 SHA256：

| Task / attempt | SHA256 |
|---|---|
| A1 FAIL | `5433E769C2A72BA1752296942F9A1E2B4305E8922A9B9E73547ADF252A031685` |
| A2 ACCEPT | `631E8284829025B5B52F8A3BE46FD42955CB1D45CFBCE553BD218528B908A6DE` |
| B1 FAIL | `6C53B6F8BCE6B49BA27EDF8BE9E067BC13FF30954229AAC552149E0A12ECF6AE` |
| B2 ACCEPT | `6FAD79527DF6A3FE876D29931AF75CF7DD2030F3E5CC27B9BEC95630967B58BB` |

上述 SHA256 均从生成文件重新核对为一致。A1 首帧平坦；B1 后四帧 `range=0、std=0`。A2 五帧 range 为 `19/38/40/40/33`；B2 为 `110/144/149/151/155`，全部通过 QC。

## DELIVERY_TOTAL 与计时边界

同一运行器使用单调时钟，从各 Task 首次 Star7 `POST /prompt` 前到第一个 QC PASS 被 ACCEPT；失败 attempt、QC、随机抽种与成功 attempt 均计入。

| Task | ATTEMPTS_TO_SUCCESS | 接受 seed | DELIVERY_TOTAL s | 最终 QC |
|---|---:|---:|---:|---|
| A | 2 | 4462651218371415901 | **189.5088** | PASS |
| B | 2 | 1350105258942230860 | **11.5405** | PASS |

**计时证据限制：**命令包要求每条 `Generation CUDA` / CUDA 口径 `Path`，同时禁止源码修改、profiler 与 kernel trace；冻结源码没有内置 CUDA 分段计时。因此本轮未取得可核验的 CUDA event 分段，JSON 将 `generation_cuda_s` 与 `path_cuda_s` 明确记为 `null`。表中的 Generation 是 ComfyUI 进度日志的单步 **wall time**，Path 是 `Total - Generation wall` 的代理值，均不冒充 CUDA 时间。`Total`、QC time 和 `DELIVERY_TOTAL` 是实测，不受此限制。此项影响分段性能分析的完整性，不改变按冻结 QC 与系统通过条件得到的恢复机制裁决。

## 结论与原始证据

两个初始失败输出均被拒绝，两个新随机 seed 的首个合格输出均被 ACCEPT。`ATTEMPTS_TO_SUCCESS=2/2`，`FINAL_ACCEPTED_QC=2/2`，`RESEED_RECOVERY_PROOF=PASS`，可交 GPT 决定是否进入独立最终系统认证；本轮不宣告 FINAL_99。

原始逐 attempt JSON、工作流、运行日志、seed 抽取账本、GPU 提交账本和 MP4 保存在 `C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260918-reseed-recovery-proof-v1-01`。本仓库的同名 JSON 保存完整运行状态。

Git 提交与远端回读将在证据提交后补记；最终远端 HEAD 以返回 GPT 时的再次回读为准。
