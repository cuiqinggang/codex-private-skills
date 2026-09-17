# H3-P0 最终 99 认证结果（失败，未冻结）

方法：first-principles-physical-limit-convergence v1.9.0；canonical branch：codex/first-principles-physical-limit-convergence-v1.9.0。
执行文件：H3-P0-SIMPLE-FINAL-COMMAND-v1.md；远端项目基线 HEAD：ea96ebbf75fe0b2918147186b8064fc595a0424e。

## 裁决

FINAL_CERTIFICATION=FAIL
H3_P0_GENERATION_99=NO
H3_P0_PATH_99=NO
FINAL_99=NO
FREEZE=NO
NEXT_ACTION=STOP_RETURN_TO_GPT

种子 920108 的历史与 MP4 已到 RESULT_READY，但固定 QC 检测到全部五帧均不满足 range≥8、std≥1.5；最后四帧为纯白常量帧。执行器立即停止，920109 未提交。总 GPU 运行数为 10：预热 1、正式 9；无自动重试或追加运行。因门禁失败，禁止宣称 10/10 或 99 冻结。

## 固定任务与运行栈

Star7 loader=MiniMaxH3FP16LoaderStar7；diffusion=minimax_h3_fl2va_pruned_int8_convrot.safetensors；text encoder=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors；video VAE=minimax_h3_video_vae_fp16.safetensors。启动参数：--fast-disk --reserve-vram 1.0 --disable-pinned-memory。任务：T2VA、32×32、5 帧、1 步、prompt=static frame、sampler=res_multistep、scheduler=beta、无输入音频、真实 MP4。模板 SHA256：66834FD34C192188DAE55F0CB6A7C4064D3AECC50EE4A9FEB00A8CE0C18E2632。

Generation 为 sampler_function 前后 CUDA Event + synchronize；Total 为 POST /prompt 前至 history complete 且 MP4 存在；Path=Total−Generation。QC 在 RESULT_READY 后执行，不计入 Total。预热 seed 920099：Generation 80.1943 s，Path 95.3096 s，Total 175.5039 s，不计统计。

## 十条正式 seed

单位：秒。920108 的 Total/Path 因 QC 抛错未写入结果文件，不用服务器的粗粒度执行时间代替冻结计时；920109 未运行。

| Seed | 状态 | Generation | Path | Total |
| --- | --- | ---: | ---: | ---: |
| 920100 | QC_PASS | 16.0761 | 3.9180 | 19.9941 |
| 920101 | QC_PASS | 2.7736 | 3.3286 | 6.1022 |
| 920102 | QC_PASS | 2.0216 | 3.5449 | 5.5665 |
| 920103 | QC_PASS | 2.1523 | 3.3839 | 5.5362 |
| 920104 | QC_PASS | 2.0785 | 3.8799 | 5.9584 |
| 920105 | QC_PASS | 2.0808 | 3.4643 | 5.5451 |
| 920106 | QC_PASS | 2.1931 | 3.6925 | 5.8856 |
| 920107 | QC_PASS | 2.1652 | 3.2697 | 5.4350 |
| 920108 | QC_FAIL_FLAT_WHITE | 2.1033 | UNKNOWN | UNKNOWN |
| 920109 | NOT_SUBMITTED_AFTER_QC_FAILURE | UNKNOWN | UNKNOWN | UNKNOWN |

正式有效=8/10；QC通过=8/10；正式已提交=9/10。920100–920107 每条均 history complete、真实 MP4 存在、ffprobe 为 32×32×5、ffmpeg 可解码、rgb24 像素有限、非黑非平坦、每帧 range≥8/std≥1.5，MP4 SHA256 已保存在证据目录的逐条 run JSON。

920108 MP4 SHA256=A27B423156BCC56ACD187EBDDDBF6F333EAA36AE6FB692C15BB9CF59FDE9B871，3205 bytes；ffprobe 为 32×32×5，ffmpeg 完整解码 15360 bytes，rgb24 有限像素。每帧均值=[254.83333333333334,255,255,255,255]；range=[2,0,0,0,0]；std=[0.5527707983925775,0,0,0,0]。runner 原始错误：flat frame: ranges=[2, 0, 0, 0, 0], stds=[0.5527707983925775, 0.0, 0.0, 0.0, 0.0]。证据：C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-final-99-01\driver.log、failed-920108-ffprobe.json、failed-920108-frame-stats.json、failed-920108-ffmpeg-decode.log、失败 MP4。

## 统计与稳定性

以下统计仅基于通过 QC 的 8 条正式运行，采用 E1 的 (n−1) 线性插值 P95。它们不是合同要求的 10 条最终认证统计。

| 指标 | n | P50 s | P95 s | Min s | Max s |
| --- | ---: | ---: | ---: | ---: | ---: |
| Generation | 8 | 2.1588 | 11.4202 | 2.0216 | 16.0761 |
| Path | 8 | 3.5046 | 3.9047 | 3.2697 | 3.9180 |
| Total | 8 | 5.7260 | 15.1320 | 5.4350 | 19.9941 |

完整 10 条稳定性认证=FAIL（样本与 QC 均不满足 10/10）。描述性 8 条子集还显示 P95 Total=15.1320 s > 2×P50=11.4521 s；最大 Total=19.9941 s > 2.5×P50=14.3151 s。前 3 条已完成 Total 中位数 6.1022 s，后 3 条已完成中位数 5.5451 s；它不是冻结合同定义的完整后 3 条验证。ComfyUI 未见进程崩溃，失败来自 QC；无自动重试。

## 上游事实与物理参照

E1 裁决 KEEP：Star7 Total P50=10.562 s、P95=14.510 s、最快有效 6.484 s。最后一轮末端收益虚拟攻击结论 COMPLETE，当前主路径无剩余成熟正收益候选；这不等于全局优化穷尽。T_PHY_TOTAL_REFERENCE=0.23–0.57 s；REAL_STATE_OPTIMUM_RANGE=4–14 s。E2R 与 E2P 只作为历史证据，W4A8 等其他方向保持独立路径或暂缓，未在本轮运行。

## 固定文件身份

| 文件 | SHA256 |
| --- | --- |
| C:\AI\MiniMax-H3\ComfyUI\models\diffusion_models\minimax_h3_fl2va_pruned_int8_convrot.safetensors (20970379616 bytes) | E889202C41DAFB67B10D67B97F0D8541508036A6090AF23425A5C2615D03C47A |
| C:\AI\MiniMax-H3\ComfyUI\models\text_encoders\qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (15687142551 bytes) | 35A88D51044231FE332301D7A62AA81E3F2CBA62FEBEB446E2C1E3E0EF76F2C6 |
| C:\AI\MiniMax-H3\ComfyUI\models\vae\minimax_h3_video_vae_fp16.safetensors (5207808496 bytes) | 7C1F131492E7EDDACAAC9069A61B81BDD39DE5CC96561E677C5EAB1CDCE5E522 |
| Star7 nodes.py | 8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B |
| ComfyUI samplers.py（已恢复） | 2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE |
| 最终认证执行器 | 649CAA234C67E5F1646440950356B349B22327A0587BD83B47D1CB02259B6E05 |
| 冻结工作流模板 | 66834FD34C192188DAE55F0CB6A7C4064D3AECC50EE4A9FEB00A8CE0C18E2632 |

ComfyUI commit=8a33128f2f8c5585c57486c07de481241e70a39c；Star7 commit=dc8ea63b51439ffd767eead53faaed23b550c504。samplers.py 运行前后 SHA 相同，恢复证明见 evidence root/instrumentation-restore-proof.json；8194 端口已关闭。

## Failure Index / 经验事实

FI-H3-P0-FINAL-920108-FLAT-WHITE：固定 Star7 KEEP 栈在本次连续认证的第 9 条正式 seed 输出可解码但接近全白的 MP4，违反逐帧质量门槛。现有证据只能确定产物失败，根因 UNKNOWN；不得用此结果自行改模型、参数、版本或添加测试。第 1 条正式运行的慢尾使已完成 8 条子集的 P95/Max 比例超过阈值，持续性根因 UNKNOWN。

Git 证据提交：PENDING。远端回读核验：PENDING。按失败规则保存证据、停止并返回 GPT；不冻结 99。

