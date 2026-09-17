# H3-P0 E1 — Star7 Native FP16 Exact 确定性验证结果

状态：KEEP。当前只执行 E0 + E1；NEXT_ACTION=RETURN_TO_GPT；E2_UNLOCKED=NO。

## 门禁与固定合同

- Canonical skill：first-principles-physical-limit-convergence v1.8.0；canonical branch：codex/first-principles-physical-limit-convergence-v1.8.0。本机 VERSION 与 SKILL.md 已回读。
- 项目远端执行前 HEAD：a94ea765cbae7fa56199dc4e3e35924bb19c7c03。
- GPU：RTX 2080 Ti / sm75。任务：T2VA、32×32、5 帧、1 step、prompt 为 static frame、sampler 为 res_multistep、scheduler 为 beta、无输入音频、真实 MP4。
- Diffusion checkpoint、text encoder、Video VAE 与启动 flags 完全相同；E1 唯一性能变量是 workflow 节点 1 的 diffusion loader：UNETLoader → MiniMaxH3FP16LoaderStar7。
- E0/E1 各 1 次 warmup（910002）和 3 次 formal（910100、910102、910103），共 8 次 GPU 运行。各条 T_TOTAL 合计 487.694 s，首条提交到末条 RESULT_READY 为约 561.625 s；均低于冻结预算。

## 计时与配对

| 指标 | E0 control P50 / P95 | E1 Star7 P50 / P95 |
| --- | ---: | ---: |
| Generation CUDA Event | 20.102 / 23.707 s | 3.102 / 10.677 s |
| Path = Total − Generation | 18.654 / 18.905 s | 3.430 / 7.626 s |
| Total POST→history complete + MP4 | 38.816 / 41.993 s | 10.562 / 14.510 s |

| Seed | E0 Total s | E1 Total s | Paired Total gain s | Generation gain s | Path gain s |
| --- | ---: | ---: | ---: | ---: | ---: |
| 910100 | 42.346 | 14.949 | 27.397 | 12.589 | 14.808 |
| 910102 | 38.816 | 6.484 | 32.332 | 16.781 | 15.550 |
| 910103 | 38.756 | 10.562 | 28.194 | 17.632 | 10.562 |

P50 Total gain 为 28.254 s；paired median Total gain 为 28.194 s；KEEP 下限为 1.164 s；3/3 同 seed 更快。E1 formal Total 为 6.484–14.949 s，Path 为 3.382–8.092 s；记录波动，不追加样本。

## 机制、QC 与恢复

Star7 日志证明：Loading at creation-time FP16 | device=sm75；Enabled v2.0.14 | mode=loader-quantized | backend=int8_tensorwise+convrot:200 | force-cast=False | weight-patches=0 | blocks=50。上游提交为 dc8ea63b51439ffd767eead53faaed23b550c504。

8/8 条在 RESULT_READY 后通过真实 MP4 的 ffprobe 32×32×5、ffmpeg 解码、非黑非平、逐帧 range≥8、std≥1.5，所有产物 SHA-256 见同名 JSON 的 RUNS[].qc。Generation 使用 sampler_function 前后 CUDA Event 加同步；Total 截止 history complete 且 MP4 存在；QC 不计入 Total。

samplers.py 前后 SHA-256 均为 2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE；原始 P0 workflow 前后 SHA-256 均为 89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5；8194 服务已退出。Star7 与候选 workflow 作为 KEEP 资产保留，原始 P0 workflow 未替换为候选。其余源码哈希和每条运行、QC、配对值见同名 JSON。

本机证据：C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-e0-e1-01。

## 远端收口

REMOTE_COMMIT=PENDING_FIRST_PUSH；REMOTE_VERIFY=PENDING_FIRST_PUSH。推送后更新为实际提交并再次远端核验。随后停止，返回 GPT；不得自动执行 E2。
