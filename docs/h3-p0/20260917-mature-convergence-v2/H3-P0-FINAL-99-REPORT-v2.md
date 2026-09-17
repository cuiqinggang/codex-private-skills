# H3-P0 最终 99 认证重试报告 v2

状态：**FINAL_CERTIFICATION=FAIL / STAR7_QUALITY_FAIL=YES / STOP / RETURN_TO_GPT**。

方法源：`first-principles-physical-limit-convergence v1.9.0`。已从项目分支远端回读 `H3-P0-FINAL-CERTIFICATION-RETRY-COMMAND-v1.md` 与 `H3-P0-FINAL-CERTIFICATION-REPAIR-v1.md`，并回读本机母技能 `VERSION=1.9.0`。

## 固定合同

Star7 KEEP：`MiniMaxH3FP16LoaderStar7`；diffusion=`minimax_h3_fl2va_pruned_int8_convrot.safetensors`；text encoder=`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`；VAE=`minimax_h3_video_vae_fp16.safetensors`。启动参数：`--fast-disk --reserve-vram 1.0 --disable-pinned-memory`。任务：T2VA / 32×32 / 5 帧 / 1 步 / `static frame` / `res_multistep` / `beta` / 无输入音频 / 真实 MP4。Generation 为 sampler_function 前后 CUDA Event + synchronize；Total 为 POST /prompt 前至 history complete 且 MP4 存在；Path = Total − Generation；QC 在 RESULT_READY 后。

## 两次预热（不计正式统计）

| seed | Generation s | Path s | Total s | 技术输出链 | 内容 QC |
|---:|---:|---:|---:|---|---|
| 930098 | 87.2793 | 121.6911 | 208.9704 | history complete；MP4 32×32×5 可解码、finite | FAIL（合同仅要求技术输出链） |
| 930099 | 20.0394 | 3.4767 | 23.5160 | history complete；MP4 32×32×5 可解码、finite | PASS |

## 正式运行

| 顺序 | seed | Generation s | Path s | Total s | QC | 结论 |
|---:|---:|---:|---:|---:|---|---|
| 1 | 930100 | 3.3969 | 3.4926 | 6.8896 | PASS | 有效正式样本 |
| 2 | 930101 | 4.5420 | 4.1094 | 8.6514 | PASS | 有效正式样本 |
| 3 | 930102 | 2.2790 | 4.3253 | 6.6044 | PASS | 有效正式样本 |
| 4 | 930103 | 2.2551 | 3.8828 | 6.1379 | FAIL | 首帧近乎全白/平坦；同 seed 对照后停止 |
| 5–10 | 930104–930109 | — | — | — | 未运行 | 按合同停止 |

有效正式样本 **3/10**；正式 QC **3/10**。930103 Star7 的 history、MP4、32×32×5、完整解码与 finite 检查均通过，但首帧 mean=254.0000、range=3、std=1.4142，违反每帧 range≥8、std≥1.5。MP4 SHA256：`F26429ECAAFEE7ED05E22DC36693148FB38E3237F4582DB9E128AA3F944F446D`。

## 同 seed 原始 Loader 对照

仅对 930103 提交 1 次标准 `UNETLoader` 对照；diffusion、text encoder、VAE、flags、任务与 seed 不变。该对照仅作 QC 归因，不计性能统计。输出 history complete、MP4 32×32×5 可解码、finite，**QC PASS**；首帧 mean=251.6644、range=9、std=2.8792，所有帧都满足 QC。MP4 SHA256：`7B9D056A87F510C23BD253FA23BE2FB5A489CEF5C1B81BC115366A00DB33227F`。

依命令包裁决：`STAR7_QUALITY_FAIL=YES`，`FINAL_CERTIFICATION=FAIL`。930103 不属于 reference 证实的无效 seed；未使用 930110/930111，**没有 seed 替换**。更深根因 `UNKNOWN`，未开展探索。

## 描述性统计与稳定性

以下仅来自 930100–930102 这 **3 条** QC PASS 的正式 Star7 运行。P95 使用线性插值；不是 10 条认证统计。

| 指标 | P50 s | P95 s | Min s | Max s |
|---|---:|---:|---:|---:|
| Generation | 3.3969 | 4.4275 | 2.2790 | 4.5420 |
| Path | 4.1094 | 4.3037 | 3.4926 | 4.3253 |
| Total | 6.8896 | 8.4752 | 6.6044 | 8.6514 |

10 条有效正式运行和 10/10 QC 未达成；10 条 P50/P95、Total 比值及 last3/first3 稳定性认证均未成立。已提交任务无崩溃，无自动重试。总 GPU 提交 **7/16**：2 预热 + 4 Star7 正式 + 1 同 seed reference。930104–930109 和备用 seed 均未运行。

## 执行证据与安全恢复

首段执行脚本把内容归因错误限于“全部 5 帧平坦”，在 930103 首帧 QC 失败后安全停止。回读逐帧原始 QC 后，只恢复同一个中断认证，按命令包运行该 seed 一次 reference。没有重复已完成 prompt 或预热。服务已停止，计时插桩恢复前后 `comfy/samplers.py` SHA256 一致：`2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE`。

原始证据：`C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-final-cert-retry-01`，包括 `runs.jsonl`、`submissions.jsonl`、两段 driver/server 日志、`execution-recovery.json`、两段 runner outcome、两份插桩恢复证明。所有 MP4 路径、SHA256 和逐帧 QC 在 `runs.jsonl` 中。

## 最终裁决

```text
VALID_FORMAL_RUNS=3/10
QC_PASS=3/10
NO_CRASH=YES
NO_AUTO_RETRY=YES
STAR7_QUALITY_FAIL=YES
FINAL_CERTIFICATION=FAIL
H3_P0_GENERATION_99=NO
H3_P0_PATH_99=NO
FINAL_99=NO
FREEZE=NO
STOP
RETURN_TO_GPT
```

远端核验：PASS。已从远端回读提交 `e301bf8557d3f88199ca749333d87ac5c165457c`，MD/JSON 的远端 Git blob 与本地一致；本段核验回执随下一提交推送。
