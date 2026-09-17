# H3-P0 MRE 真实态报告 01

状态：MRE_COMPLETE=YES；NO_NEW_OPTIMIZATION=YES；NO_STAR7_TEST=YES；NO_VIRTUAL_99_EXECUTION=YES；RETURN_TO_GPT=YES。

## STATIC_FACTS（静态事实）

- 合同：T2VA，32×32，5 帧，1 step，static frame，res_multistep / beta，无外部音频，真实 MP4。
- 固定配置：--fast-disk --reserve-vram 1.0 --disable-pinned-memory；端口 8194。冷态 seed 910001，预热 910002，正式 seed 910100/910102/910103。
- 冻结 runner SHA256：EA3B3FB4FA70DFE05448B138E90FFDC6A22121033F936D764A8CD03A82B574E4；权威 workflow SHA256：89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5。
- T_PHY 仅供参照：Generation 0.05–0.12 s，Path 0.18–0.45 s，Total 0.23–0.57 s。

## LEGACY_PRIORS（旧任务经验先验）

- V3_RESERVE1 的 Generation P50/P95：20.226025/20.533857 s；Path：17.970201/18.007124 s；Total：38.042308/38.488666 s。
- 旧证据：C:\AI\H3-P0-Acceptance\fp-convergence\20260916-run-01\summary-V3_RESERVE1.json 及 runs\V3_RESERVE1 内三条同 seed JSON。

## NEW_MRE_OBSERVATIONS（新极简真实运行观测）

原 runner 顺序完成冷态、预热、三条正式任务。Generation 是 CUDA Event 时间；Path = Total − Generation；QC 在结果就绪后执行。单位为秒。

| 阶段 / seed | Generation CUDA | Generation wall | Path | Total | QC |
| --- | ---: | ---: | ---: | ---: | --- |
| 冷态 910001 | 77.521852 | 77.538135 | 130.792081 | 208.313933 | PASS |
| 预热 910002 | 23.545457 | 23.549550 | 26.060469 | 49.605926 | PASS |
| 正式 910100 | 24.467068 | 24.468701 | 30.350668 | 54.817736 | PASS |
| 正式 910102 | 30.185133 | 30.188591 | 30.180904 | 60.366037 | PASS |
| 正式 910103 | 20.316711 | 20.321628 | 26.962981 | 47.279692 | PASS |

| 正式统计 | P50 | P95 |
| --- | ---: | ---: |
| Generation | 24.467068 | 29.613326 |
| Path | 30.180904 | 30.333691 |
| Total | 54.817736 | 59.811207 |

三条正式结果均为 task_completed=true、history_completed_and_mp4_exists；原 runner 的 ffprobe、ffmpeg、非黑/非平坦帧 QC 为 3/3 PASS。五个 MP4 已回读确认存在，SHA256 与逐条结果一致。逐条 MP4 路径、SHA、帧统计和时间边界在机器报告与原始证据中。

同 seed 新值减旧 V3（正值表示变慢）：

| seed | Generation Δ s | Path Δ s | Total Δ s |
| --- | ---: | ---: | ---: |
| 910100 | +3.899008 | +12.380467 | +16.279475 |
| 910102 | +10.154051 | +12.169678 | +22.323729 |
| 910103 | +0.090686 | +9.170009 | +9.260694 |

- P50 漂移：Generation +4.241043 s，Path +12.210703 s，Total +16.775428 s。
- P95 漂移：Generation +9.079469 s，Path +12.326568 s，Total +21.322541 s。
- 冷态 Total 比正式 P50 多 153.496197 s；预热 Total 比正式 P50 少 5.211810 s；两者不进入正式统计。

## CONFLICTS（新旧冲突）

- 相同的任务合同、启动参数、已记录软硬件版本和三个模型文件大小下，本轮正式时间比旧 V3 慢；原因尚未确定。
- 三个同 seed 视频的帧均值、范围、标准差与旧 V3 一致，MP4 SHA256 不同；帧统计一致不能证明逐像素相同。

## REAL_STATE_FACTS（当前可确认真实态事实）

- NVIDIA GeForce RTX 2080 Ti, 22528 MiB, 21007 MiB, 591.74；Python 3.11.15，Torch 2.9.1+cu130，CUDA 13.0，ComfyUI 8a33128f2f8c5585c57486c07de481241e70a39c，comfy-kitchen 0.2.31，comfy-aimdo 0.4.15。
- 三个模型路径和字节数与旧 V3 一致；本轮未重新哈希大型模型。8194/8195 运行前空闲，结束后无监听，没有第二个 H3 实例。
- samplers.py 已恢复，SHA before = SHA after = 2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE；runner 退出码 0，锁已释放。
- 原始证据：C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-mre-01。关键文件：preflight.json、pid.json、heartbeat.json、server-MRE_REAL_STATE_01.log、runs/、summary-MRE_REAL_STATE_01.json、instrumentation-restore-proof.json。

## UNKNOWN_REMAINDER（仍未知部分）

- 性能漂移原因与未归属的生成/路径等待时间；本轮没有做性能剖析。
- T_MACHINE_STAR_REAL 由后续 GPT 校准；本轮不修订理论目标，不进入新优化。
