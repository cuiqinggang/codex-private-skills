# H3-P0 全量探索回归与旧基线冻结档案

状态：FROZEN（远端已核验）；本档案与机器可读 JSON、[证据索引](H3-P0-LEGACY-EVIDENCE-INDEX.md)、[失败索引](H3-P0-FAILURE-INDEX.md)、[成熟路径规则 v1.2](H3-P0-MATURE-PATH-FIRST-v1.2.md)构成下一任务的直接入口。完成精确提交、推送和远端 HEAD 核验后，才可宣告 H3_P0_LEGACY_RETROSPECTIVE=FROZEN（旧探索档案冻结）。本档案冻结历史事实，不宣称双 99 已完成。

## 1. 目标、固定任务合同与计时

H3-P0 要在本机真实硬件、固定最小有效视频合同下，把核心生成与系统路径分别收敛到本机稳定理论极限的 99。ACTIVE_HARDWARE_BOUNDARY（当前有效硬件边界）是实际安装的单张 RTX 2080 Ti，22528 MiB，Turing sm75。未来第二张 8GB GPU 未安装，不属于本轮理论目标或硬件拓扑必测条件；安装后应继承本档案并重算新边界。

TASK_CONTRACT（任务合同）：T2VA；32×32 像素、5 帧、1 step（一步）；提示词 static frame；sampler 为 res_multistep、scheduler 为 beta；无输入音频；保留 H3 sampler → H3 VAE decode → CreateVideo → SaveVideo 的真实 MP4 产物链；不缓存最终输出。权威母版工作流位于 C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json，SHA256 为 89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5。由母版受控减法形成的 P0 冻结工作流在证据根内，SHA256 为 2CA2B4D4E9EED6FA40FBB018534E78B2A8DD41AF03001B27BCCD793C09E7A146；这两个哈希不能混称。

每轮先做一条 seed 910002 预热，不计统计，再用固定正式 seed 910100、910102、910103 各测一次；P95 采用 n−1 线性插值。TASK_COMPLETED（任务完成）至少要求 history 完成、MP4 存在；正式 QC 还要求 ffprobe 识别 32×32×5、ffmpeg 解码出 15360 字节像素、每帧有限非黑，range≥8、标准差≥1.5，并保存产物 SHA256。QC 在 RESULT_READY（结果就绪）之后运行，不进入正式总时间。

T_GENERATION（核心生成）是 KSAMPLER.sample 中 sampler_function 前后的 CUDA Event elapsed_time，结束事件 synchronize（同步）；墙钟只作交叉检查。T_TOTAL（总时间）从 POST /prompt 前到 history 完成且 MP4 真正存在；T_PATH（系统路径）= T_TOTAL−T_GENERATION。一个 GPU 正式实例独占运行，8194 服务串行。结果文件中分块诊断的 wall/epoch 标记不得替代正式 CUDA Event。

## 2. 理论第一版：原样保留与实测校正

[STEP1 理论报告](H3-P0-STEP1-PHYSICAL-LIMIT-v1.md)和[原始 JSON](H3-P0-STEP1-RESULTS.json)是理论第一版的权威来源。T_PHY（物理极限）初始区间：Generation 0.05–0.12 秒、Path 0.18–0.45 秒、Total 0.23–0.57 秒。T_MACHINE_STAR_V1（本机稳定理论极限第一版）：Generation 0.45–1.40 秒、Path 0.70–2.00 秒、Total 1.15–3.40 秒。99 门槛为 Generation P50≤1.40、P95≤1.70；Path P50≤2.00、P95≤2.40；通过后还需 10 条有效稳态样本、无高价值残余 Gap、共同仓库同步。

原计算把 H3 关键权重估在约 20B 参数、packed tokens 估在约 18–32，以约 0.72–1.28 TFLOP 的一次 dense forward、FP32 峰值 14.2 TFLOPS 和 616 GB/s 显存带宽推下界；又以 H3 19.53 GiB 与 VAE 4.85 GiB 无法同时放入 22GB VRAM，承认必须有驻留切换。它把小序列矩阵效率、Turing BF16/manual cast、动态权重从文件/RAM 到 GPU 的调度和模型切换成本视作软件可消灭项，因此给出上述机器目标。当时这是显式假设，不是实测保证。

现实证据修正了优先级：V3 核心生成 P50 20.226 秒、Path P50 17.970 秒；V7 证明所谓 VAE decode 17.825 秒的调用内部还有动态权重请求，不能称为纯数学 VAE 计算；V10 稳态 H3 一次 forward 记录 155 次驻留未命中、约 5.953GB 请求，而预热为约 19.45GB，说明预热与稳态机制不同。V11 算子剖析中 GPU 算子自耗时仅约 1.46–1.62 秒，与 22–25 秒正式 CUDA Event 不闭合，提示大量未归属等待/调度；剖析本身有扰动，不能据此计算新的物理下界。约 5.953GB REQUESTED（请求字节）不等于实际 PCIe 传输字节，更不等于传输耗时。当前证据尚不足以按 Target Revision Gate（目标修订门禁）发布新目标；未因慢而放宽第一版门槛。

LAST_GOOD（最近保留版本）V3 与冻结门槛的剩余绝对 Gap：Generation P50 18.826025、P95 18.833857 秒；Path P50 15.970201、P95 15.607124 秒。H3_P0_GENERATION_99=NO（核心生成未达 99），H3_P0_PATH_99=NO（系统路径未达 99）。未启动最终 10 次稳态认证。

## 3. 本轮真实环境

| 项目 | 本机旧基线事实 |
| --- | --- |
| 硬件与系统 | 单 RTX 2080 Ti，22528 MiB，sm75；RAM 33498504 KiB；Windows 10 Pro 10.0.19045；驱动 591.74 |
| 运行时 | Python 3.11.15；Torch 2.9.1+cu130；CUDA 13.0；cuDNN 91200 |
| 原 ComfyUI | v0.34.0-16-g8a33128f；commit 8a33128f2f8c5585c57486c07de481241e70a39c |
| 原依赖 | comfy-kitchen 0.2.31；comfy-aimdo 0.4.15；cudaMallocAsync；DynamicVRAM；2 streams 的 async weight offload；PyTorch efficient attention；原生 MixedPrecisionOps INT8 tensorwise / asym_w4a8_int8 / convrot_w4a4 |
| V3 启动 | --fast-disk、--reserve-vram 1.0、--disable-pinned-memory；日志显示 H3 model weight dtype bfloat16、manual cast float32 |
| H3 diffusion | C:\AI\MiniMax-H3\ComfyUI\models\diffusion_models\minimax_h3_fl2va_pruned_int8_convrot.safetensors；20970379616 bytes |
| Qwen3-VL text encoder | C:\AI\MiniMax-H3\ComfyUI\models\text_encoders\qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors；15687142551 bytes |
| H3 video VAE | C:\AI\MiniMax-H3\ComfyUI\models\vae\minimax_h3_video_vae_fp16.safetensors；5207808496 bytes |

本轮权威证据只给上述三个模型的路径和字节数，没有已验证的内容 SHA256；为回归报告没有重新读取数十 GB 生成新模型哈希。母版与 P0 工作流哈希、各次 MP4 哈希和源码插桩恢复哈希均另有证据，不得借它们代替模型哈希。

## 4. V1–V11 完整时间线

下表单位为秒，G=GENERATION（核心生成），P=PATH（系统路径），T=TOTAL（总时间）；各列分别给 P50/P95。每个 V1_QC–V11 阶段均有 1 条 seed 910002 预热、3 条固定正式 seed 910100/910102/910103、3/3 正式 MP4 QC PASS（质量检查通过）；原始 V1 的不充分 QC 另述。完整精度、每条 run 与 MP4 哈希在[机器档案](H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json)和[证据索引](H3-P0-LEGACY-EVIDENCE-INDEX.md)。

| PHASE（阶段） | G P50/P95 | P P50/P95 | T P50/P95 | DECISION（裁决） |
| --- | ---: | ---: | ---: | --- |
| V1_QC | 21.758 / 23.707 | 18.162 / 19.141 | 41.007 / 41.945 | 权威首版 |
| V2_RESERVE2 | 20.503 / 21.996 | 18.239 / 19.301 | 39.910 / 40.351 | KEEP（保留） |
| V3_RESERVE1 | 20.226 / 20.534 | 17.970 / 18.007 | 38.042 / 38.489 | KEEP；LAST_GOOD |
| V4_RESERVE0_5 | 20.472 / 22.836 | 18.182 / 18.340 | 38.471 / 41.157 | ROLLBACK（回滚） |
| V5_PINNED | 19.561 / 22.490 | 23.784 / 28.113 | 43.345 / 46.758 | ROLLBACK |
| V6_PATH_PROFILE | 21.113 / 21.120 | 19.275 / 24.867 | 40.380 / 45.986 | DIAGNOSTIC_ONLY（仅诊断） |
| V7_VAE_STAGE | 24.165 / 25.790 | 19.628 / 21.568 | 45.599 / 45.913 | DIAGNOSTIC_ONLY |
| V8_VAE_FULL_SINGLE | 20.658 / 24.861 | 23.248 / 28.046 | 48.575 / 49.171 | ROLLBACK |
| V9_SOFTWARE_036 | 24.861 / 26.995 | 18.307 / 26.182 | 45.080 / 51.234 | ROLLBACK |
| V10_GENERATION_PROFILE | 22.836 / 24.784 | 20.752 / 21.496 | 44.149 / 45.197 | DIAGNOSTIC_ONLY |
| V11_OP_PROFILE | 22.303 / 25.041 | 31.386 / 35.870 | 53.689 / 60.911 | DIAGNOSTIC_ONLY |

V1：PURPOSE（目的）是建立首个真实最小执行版本；ONE_CHANGE（单项改变）是对权威母版受控减法，reserve-vram 3.5 GiB、禁用 pinned。最初 V1 原始 summary 记 T P50 41.665 秒，seed 910101 产物五帧均值约 251.9–254.3，近乎全白，旧 run JSON 无 range/std，虽然 task_completed=true 但不足以通过升级后的非平坦 QC。补测的 V1_QC 用三个有效 seed 建立表中权威 V1；旧记录保留作误判证据。REUSABLE_FACT（可复用事实）：任务完成标志不等于视频内容 QC。

V2：PURPOSE 是释放过量预留显存；唯一机制是 reserve-vram 3.5→2.0 GiB，基线 V1_QC。G P50 快 1.255 秒，P P50 却慢约 0.076 秒，端到端 T P50 仍快 1.097 秒，因此曾 KEEP。无独立 V2 decision JSON；裁决来源是本轮用户确认及连续阶段记录，数值来源为正式 summary/run，不能伪装为独立裁决文件。

V3：同一自适应搜索把 reserve-vram 2.0→1.0 GiB，基线 V2；G、P、T P50 均改进，T P50 成 38.042 秒。相对权威 V1，T P50 减少 2.964632 秒，约 7.23%；G 减少 1.531727 秒、P 减少 0.192138 秒。last-good.json 明确记录 KEEP 与 V3_RESERVE1；没有独立 V3 decision JSON。后续全部候选均以此为固定保留基准。

V4：只把 reserve-vram 1.0→0.5 GiB；T P50 比 V3 慢 0.428 秒，三组同 seed 有两组变慢，配对中位收益 −0.452 秒，QC 仍全过，正式 ROLLBACK。LESSON（经验）：剩余显存不能越少越好，禁止重做 3.5/2/1/0.5 GiB 粗搜索，除非硬件、模型或软件驻留机制改变。

V5：在 V3 的 1.0 GiB 上单独启用 pinned memory（移除 disable-pinned-memory）；T P50 43.345 秒，比 V3 慢 5.303 秒，三条同 seed 总时间 42.271/43.345/47.137 秒且全部变慢，QC 全过，ROLLBACK。PINNED_MEMORY_CURRENT_ROUTE=PROVEN_BAD（仅当前软件、参数与合同下的锁页内存路线已证伪），不扩展为一切 pinned transfer 无效。

V6：PURPOSE 是诊断 PATH，配置仍为 V3；可逆插桩分别测生成前、H3 装载、H3 卸载、VAE 装载、VAE decode、视频创建/写入、结果就绪。T_VAE_DECODE_STAGE P50=17.823566、P95=23.381317 秒，是最大系统路径块；三条 PATH 为 25.488/19.268/19.275 秒，显示明显波动。该阶段包含模型切换、动态权重/计算/输出搬运，不能直接当纯 VAE 数学时间。五个源码文件的插桩前后 SHA256 相等；仅诊断，不改 V3。

V7：在 V6 的 VAE 大块内只再拆一层，T_VAE_PREPARE P50≈0、T_VAE_LOAD_GPU P50=0.127308、T_VAE_ACTUAL_DECODE 调用 P50=17.825251、T_VAE_OUTPUT_TRANSFER≈0.001 秒。所谓 ACTUAL_DECODE 实为 decoder 调用边界，内部每条正式 run 有 146 次动态驻留未命中、4846446592 bytes 请求和同数文件直读请求，不能称为纯数学 kernel。全部 QC 和五源码 SHA 恢复 PASS；DIAGNOSTIC_ONLY。

V8：在旧软件、单卡、V3 配置下提出可逆 force_full_load 请求。T P50 48.575 秒，比 V3 慢 10.533 秒；三条配对总收益均负；QC 与 sd.py SHA 恢复 PASS，ROLLBACK。日志中 loaded completely 事件为 0；本轮只能证明“这次请求无收益”，不能证明 VAE 完整驻留机制已实现，更不能证明驻留概念无效。

V9：软件前沿从原 ComfyUI v0.34.0-16 commit 8a33128f 到官方 v0.36.0 commit ee71d5c（前进 121 commits），隔离 git worktree 与 python-overlay 使用 comfy-kitchen 0.2.34、comfy-aimdo 0.5.3，原 .venv 和原 ComfyUI 工作树不变。差异覆盖 H3/VAE、model_management、model_prefetch、ops、sd，官方包含 H3 VAE 优化。首次启动缺 comfy_aimdo.malloc_graph，没有正式 prompt，属于 MISSING_COMFY_AIMDO（依赖启动失败），不是性能失败；补齐隔离依赖后从 V9 检查点恢复。最终三条正式 QC PASS，T P50 45.080，比 V3 慢 7.038 秒，三组配对均慢，完整组合 ROLLBACK；不能因此否定组合中每项单独优化。

V10：回到 V3 做核心生成可逆诊断。50 个 DiT block 是主时间块；五组各 10 层 P50 约 3.932/4.114/4.312/4.541/5.021 秒。稳态每个 H3 forward 约 155 次 residency miss、5952846848 bytes 权重请求；预热为 255 次、约 19.45GB，不能混合统计。请求字节不等于实际 PCIe 字节或耗时。三条 QC PASS，model.py/ops.py 修改前备份和恢复 SHA256 均相等，DIAGNOSTIC_ONLY；诊断计时不能与无插桩 V3 做 KEEP 比较。

V11：在方法转向前已启动的算子剖析自然完成，随后冻结新 GPU 候选。三条正式 QC PASS，DIAGNOSTIC_ONLY；算子 GPU 自耗时约 1.46–1.62 秒，其中 HtoD 约 0.95–1.03 秒、attention 约 0.00126 秒，而权威核心生成约 22–25 秒。算子自耗时不能相加当作正式生成时间，未归属区间需后续任务再判断；profiler 使 PATH 明显增大。仅 samplers 临时插桩，最新全局恢复 proof 为 SHA_before=SHA_after=2850B400E0C07DDB73429F35E5DA3DE01952E7EE58F4C050124EA948CBDA53AE；该全局文件每轮覆盖，不能当逐阶段历史 proof。

## 5. Local Resumable Controller（本地可恢复控制器）的演进

最初 Codex 出现 Selected model is at capacity 时，本地 1.0 GiB 候选可能仍在运行；形成 AI_SESSION_FAILURE != LOCAL_EXPERIMENT_FAILURE（AI 会话失败不等于本地实验失败）。恢复必须先只读检查 PID、8194、nvidia-smi、server log、result/QC/state，不因模型容量或浏览器关闭终止进程，更不能重新启动第二个 H3。CPU Guardian 的 cpu-guardian.py 进程不属于 H3，不得终止。

[控制器源码](H3-P0-controller.py)实现独立于对话生命周期的 state.json（状态）、pid.json（进程身份）、heartbeat.json（心跳）、iteration.json（当前阶段与检查点）、last-good.json（最近保留版）、controller.lock（单实例锁）；每轮完成立即 checkpoint（保存检查点），完成阶段重复调用直接复用结果，支持 --resume（恢复）、--status（只读查看）、--stop-safe（检查点安全停止）。状态机：IDLE（空闲）→ STARTING（启动）→ WARMUP（预热）→ MEASURING（正式测量）→ QC（质量检查）→ DECIDING（裁决）→ KEEP/ROLLBACK（保留/回滚）→ CHECKPOINTED（已保存）→ NEXT_ITERATION（下一轮）；满足条件后才有 CERTIFICATION（最终认证）与 DONE（完成）。当前 IDLE、index=8、LAST_GOOD=V3、无锁、8194 无监听；99 未到，故没有认证/DONE。

RUNNER_START_PID_WINDOW（运行器启动至 PID 落盘窗口）防护：spawn 前原子保存 STARTING、launch_id、controller PID/起始时间、计划命令哈希、runner_pid=null；spawn 后立即补 runner PID/起始时间及同一 launch_id。恢复时先按身份、命令行、启动时间、8194 与证据找旧子进程，不能见 null 就重启。PREMATURE_LOCK_RELEASE（过早释放锁）防护：异常退出保留锁；只有 owner 和 runner 均已失效、心跳过期、8194 不属于旧实例且结果无新进展，才可认定 STALE_LOCK（失活锁）。已完成轮次的旧锁则通过 QC/SHA 证明走 COMPLETED_LOCK_RECOVERY（已完成锁恢复），V6 有归档证据。Windows 原子写使用 PID/线程唯一临时名加有界重试；进程扫描捕获 psutil.NoSuchProcess 的 TOCTOU（检查与使用竞态）。

## 6. Failure Index（失败索引）与证据等级

[扩充后的失败索引](H3-P0-FAILURE-INDEX.md)保存可执行触发、处理与禁令。AI_MODEL_CAPACITY：先查本地实验状态，不因对话失败重跑。WINDOWS_ATOMIC_REPLACE：controller-launch.stderr.log 有 os.replace(pid.json.tmp,pid.json) 的 WinError 5；已改唯一临时名与最多 20 次短重试，尚无专门并发压力回归证明彻底根治。RUNNER_START_PID_WINDOW、PREMATURE_LOCK_RELEASE 是真实实施的防护；未发现它们曾造成双 runner/过早释放事故的原始日志，不能冒充已发生事故。PSUTIL_NOSUCHPROCESS_POSTRUN：V6 收尾进程扫描抛异常，但三条结果/QC/SHA 完整；以已完成锁接管，绝不重跑 V6。MISSING_COMFY_AIMDO：V9 首次只启动失败，隔离补依赖后重试同阶段。DIAGNOSTIC_PROFILE_IS_NOT_KEEP_EVIDENCE：插桩轮只用于归因，不能拿更慢的诊断数判候选。

NESTED_POWERSHELL_EXPANSION（嵌套 PowerShell 展开）：本轮用户已确认 .CommandLine、$_、$r、.seed 等在多层双引号中被外层污染；成熟处理是复杂逻辑写独立临时 .ps1 并由 PowerShell 7 -File 执行。本地证据目录未保留原始错误日志，来源标 USER_REPORTED（用户叙述）。TEMP_SCRIPT_NULL_BYTES（临时脚本空字节）：用户要求纳入，但在指定证据根与仓库文档未找到原始日志；只能标 EVIDENCE_GAP（原始证据缺口），通用恢复方式是重建明确 UTF-8 文本并先做语法检查，不能声称本轮已有可审计 traceback。V1_WHITE_FRAME_QC_GAP（V1 近白帧误判）由原始 run JSON 与修正 V1_QC 证明；见失败索引。

## 7. 方法论三代演进

初始 v1：FIRST PRINCIPLES（第一性原理）→ V1 → MAX_ABSOLUTE_GAP（最大绝对差距）→ CUSTOM_ATTACK（定制攻击）。好处是合同、物理假设和计时可解释；在复杂 H3 栈中，先深挖源码容易重新发明已有成熟优化，使 T_CONVERGENCE（收敛工程时间）过长。

v1.1：增加 SOFTWARE_FRONTIER_GATE（软件前沿门禁），真实比较官方成熟新栈；V9 完整 v0.36.0 组合已正式 A/B 并回滚。明确 ACTIVE_HARDWARE_BOUNDARY 为当前实际单卡；未来新增 GPU 时继承经验后重新计算 T_MACHINE_STAR，不因未来硬件缺席阻止当前边界的目标判断。

v1.2：[MATURE_PATH_FIRST（成熟路径优先）](H3-P0-MATURE-PATH-FIRST-v1.2.md)：WORLD_KNOWN_BEST（世界已有成熟方案）→ LOCAL_APPLICABILITY_FILTER（按 sm75、22GB、32×32/5帧/1步过滤）→ MATURE_HARVEST（成熟收益收割）→ 本机同合同 A/B → RESIDUAL_GAP（残余差距）→ 必要时 CUSTOM_ATTACK。外部比例只给优先级，不给 KEEP；1-step 无后续模型调用，Turbo/PDD 减步与多步 block cache 不能照搬。当前用户冻结 NO_NEW_GPU_BENCHMARK=YES、NO_NEW_OPTIMIZATION_CANDIDATE=YES；[成熟收割矩阵](H3-P0-MATURE-HARVEST-MATRIX.md)只作为下一任务输入。

## 8. 成熟外部参考：来源与本机验证必须分开

ComfyUI 官方 v0.36.0 与 [MiniMax-H3 VAE 优化 PR #16187](https://github.com/Comfy-Org/ComfyUI/pull/16187)含 VAE 融合/更低内存路径；[comfy-kitchen PR #167](https://github.com/Comfy-Org/comfy-kitchen/pull/167) 的加速测量来自 RTX 5090、1344×768、362 帧，不能外推到本机 P0。v0.36 的 model_prefetch、DynamicVRAM、async offload、H3 DiT prefetch queue 与 VAE kernel fusion 相关改动均在本轮软件前沿评估范围；本机 LOCAL_VERIFIED（本机验证）仅能说完整 V9 组合更慢，不能断言每个 PR 无效。[官方发布页](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.36.0)。

[IvenKooLab/minimax-h3-turing 同硬件项目](https://github.com/IvenKooLab/minimax-h3-turing/blob/main/docs/en/10-benchmarks.md)用 RTX 2080 Ti 22GB/sm75，有 W4A8/INT8、Torch 2.9.1+cu130、comfy-kitchen、T8、PDD、TE-Speed、SageAttention、reserve-vram/pinned-memory 等真实探索。但公开 A/B 是 640×352、124 帧、4/8 步，且模型/文本编码路线不同；T8/PDD 主要跳过后续步，本轮固定 1 步无可跳过调用。其数据属于 EXTERNAL_EVIDENCE（外部证据），不是本轮 LOCAL_VERIFIED。

[Star7 FP16 Exact](https://github.com/star7code/minimax-h3-fp16-exact-star7) 为 sm75 提供受保护 FP16 原生 H3 loader，声明保留 MixedPrecisionOps INT8/ConvRot；与 V3 日志 BF16 权重、manual cast FP32 的机制相符，但本轮未做同合同 A/B，收益 UNKNOWN（未知）、质量未认证。[Star7 大序列注意力基准](https://github.com/star7code/minimax-h3-chunk-star7/blob/main/BENCHMARKS.md)不能外推到本轮短序列；V11 本机 attention 算子约 1.26 毫秒。[H3 VAE TensorRT 项目](https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/main/compile.py)公开引擎固定 latent 16×16/32×32，本轮 32×32 产物的 latent 约 2×2，现成引擎不能当作已适用候选。详见成熟收割矩阵。

## 9. 已获资产与禁止重复支付试错成本

| 类别 | 已冻结事实与适用边界 |
| --- | --- |
| KEEP（保留） | V2 曾改善端到端；V3 1.0 GiB 是最终 LAST_GOOD，较 V1 T P50 少 2.965 秒。当前 Torch2.9.1+cu130、原生 INT8 ConvRot、DynamicVRAM/async offload 已在 V3，不能重新当新收益。 |
| ROLLBACK（回滚） | V4 0.5 GiB、V5 当前 pinned、V8 单卡 full-load 请求、V9 精确 v0.36.0 组合；各结论只适用于当时硬件/软件/任务。 |
| DIAGNOSTIC_FACT（诊断事实） | V6 PATH 最大块是 VAE stage；V7 decoder call 含 146 次/4.846GB 动态请求；V10 H3 稳态 155 次/5.953GB 请求；V11 attention 约 1.26ms、算子自耗时与总事件不闭合。 |
| FAILURE_SOLUTION（故障方案） | 容量错误先只读状态；唯一临时名+重试；STARTING launch_id；异常保锁；完成锁单独接管；NoSuchProcess 竞态按结果复核；复杂 PowerShell 用独立 .ps1。 |
| SOFTWARE_FRONTIER（软件前沿） | 官方 v0.36.0 的 H3/VAE/kitchen/aimdo 改动真实存在，完整本机 V9 已回滚；未来新版本或单项隔离需新任务按 v1.2 过滤。 |
| EMPIRICAL_PRIORS（经验先验） | 冻结合同和 CUDA Event；先看同硬件但严格筛 1-step；标清请求量与实际传输；诊断轮不判 KEEP；外部 A/B 不代替本机 QC；单卡 99 不等待未来第二 GPU。 |

DO_NOT_REPEAT（禁止重复探索）：不要再跑原 V1、reserve 3.5→2→1→0.5 粗搜索、V5 当前 pinned 路线、V8 同一 full-load 请求、V9 同一完整组合、V6/V7/V10/V11 同一诊断；不要因 AI 容量、V6 NoSuchProcess 或 V9 无 prompt 的启动失败重跑已完成 GPU 轮次；不要使用多层 PowerShell 双引号内的 .CommandLine/$_ 查询。重新测试门槛分别是：任务合同/硬件/模型/相关软件机制有可证实变化；或原结果证明不完整；或新成熟方案明确不同机制。具体边界和证据在[成熟矩阵](H3-P0-MATURE-HARVEST-MATRIX.md)、[失败索引](H3-P0-FAILURE-INDEX.md)和[证据索引](H3-P0-LEGACY-EVIDENCE-INDEX.md)。

## 10. NEXT-TASK INHERITANCE CONTRACT（新任务继承合同）

下一 H3-P0 任务只需先读本档案、同名 JSON、证据索引、失败索引、成熟路径 v1.2 规则。它们给出 V3 基准、所有 KEEP/ROLLBACK、完整控制器恢复规则、当前硬件与软件边界、外部成熟候选和剩余精确 Gap；无需重新阅读旧对话。先做成熟候选的本机适用性过滤，再独占 GPU 串行 A/B；外部 benchmark 仅排优先级。当前旧任务保持 NO_NEW_GPU_BENCHMARK=YES 与 NO_NEW_OPTIMIZATION_CANDIDATE=YES，直到新任务明确启动。

待解决：双 99 未达，T_MACHINE_STAR_V1 未修订；未做最终 10 次认证。模型文件内容 SHA 未在旧证据中找到；V1_QC/V2/V3 无独立 decision JSON（V3 的 last-good 文件明确）；TEMP_SCRIPT_NULL_BYTES 无原始日志；samplers 恢复证明是每轮覆盖的全局文件。上述缺口在 JSON 标明来源与限度，不得后填猜测。
