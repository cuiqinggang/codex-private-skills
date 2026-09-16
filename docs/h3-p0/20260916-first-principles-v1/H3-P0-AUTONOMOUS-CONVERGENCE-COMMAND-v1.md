# H3-P0 V1 → 双 99 自动收敛命令包 v1

> 交给 Codex 的正式执行合同。所有英文键后均带中文含义；程序兼容字段保留英文。

```text
COMMAND_STATUS=RELEASED（已发布）
COMMAND_REVIEW=PASS（命令审核通过）
METHOD=first-principles-physical-limit-convergence v1.0.0
TARGET=H3-P0
GOAL=V1 -> ITERATIVE CONVERGENCE（迭代收敛） -> DUAL 99（双99）
```

---

## A. 总任务

调用已经本机部署并索引的：

```text
C:\Users\A\.codex\skills\first-principles-physical-limit-convergence\SKILL.md
```

并同时按需读取：

```text
C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\SKILL.md
```

共同事实源：

```text
REPO=cuiqinggang/codex-private-skills
LOCAL_REPO=C:\Users\A\Documents\Codex\codex-private-skills
METHOD_BRANCH=codex/first-principles-physical-limit-convergence-v1.0.0
METHOD_HEAD=449575b16db9394e91bcfa618e88b55ea1f3d382
PREFLIGHT_BRANCH=codex/h3-p0-local-preflight
PREFLIGHT_HEAD=c88c150962d677bae555d85834e03c796e5e46fc
EXECUTION_BRANCH=codex/h3-p0-fp-limit-v1
```

先读取本分支：

```text
docs/h3-p0/20260916-first-principles-v1/H3-P0-STEP1-PHYSICAL-LIMIT-v1.md
```

不要重新全盘扫描 `C:\AI`，不要重新从零研究 H3。

本命令不是“只跑 V1 然后停止”。它必须：

```text
建立 V1
-> 获得第一组权威数据
-> 自动计算 Gap（距离本机理论极限的可消灭时间）
-> 攻击最大 Gap
-> KEEP（保留）/ROLLBACK（回滚）
-> 再测
-> 再攻击
-> 直到两个 99 都 PASS
-> FINAL FREEZE（最终冻结）
```

如果真实证据证明目标模型有错误，可以按 Skill 的 Target Revision Gate（目标修订门禁）发布新目标版本；禁止为了“过 99”直接放宽目标。

---

# B. 固定任务合同

```text
TASK_ID=H3-P0-MINIMUM-TECHNICAL-GENERATION

WIDTH=32
HEIGHT=32
FRAMES=5
STEPS=1
PROMPT=static frame
INPUT_MODE=T2VA（纯文本生成；不使用首尾参考图）
AUDIO_INPUT=NO（无外部音频）
SAMPLER=res_multistep
SCHEDULER=beta

TASK_COMPLETED=
API accepted（接口接受）
+ real H3 sampler executed（真实H3采样器已执行）
+ 32×32
+ 5 frames（5帧）
+ 1 step（1步）
+ VAE decode PASS（VAE解码通过）
+ finite pixels（有效有限像素）
+ not corrupted（结果不损坏）
+ minimal video artifact readable（最小视频产物可读取）
```

只研究 warm steady state（服务就绪稳态）的两个 99。

Cold Start（冷启动）只记录，不参与两个 99。

两个正式 99：

```text
H3_P0_PATH_99（系统路径99）
H3_P0_GENERATION_99（图/视频核心生成99）
```

兼容旧名：

```text
H3_P0_GPU_CORE_99 == H3_P0_GENERATION_99
```

禁止创建第三个 TOTAL_99（总时间99）。

---

# C. STEP 1 目标区间

使用已经发布的 v1 目标：

```text
T_PHY_GENERATION（核心生成物理极限）=0.05~0.12 s
T_PHY_PATH（路径物理极限）=0.18~0.45 s
T_PHY_TOTAL（总物理参照）=0.23~0.57 s

T_MACHINE_STAR_GENERATION（本机核心生成稳定理论极限）=0.45~1.40 s
T_MACHINE_STAR_PATH（本机路径稳定理论极限）=0.70~2.00 s
T_MACHINE_STAR_TOTAL（本机总时间理论区间）=1.15~3.40 s
```

首版 99 门槛：

```text
GENERATION_99:
P50_CUDA <= 1.40 s
P95_CUDA <= 1.70 s

PATH_99:
P50_PATH <= 2.00 s
P95_PATH <= 2.40 s
```

并且必须：

```text
TASK_COMPLETED=PASS
HARD_CONSTRAINTS=PASS
NO_HIGH_VALUE_REMAINING_GAP=YES
SHARED_REPO_SYNC=PASS
```

---

# D. 多智能体执行方式

正式模式：

```text
AGENT_MODE=SUPPORT_PARALLEL（辅助并行）
MAX_SUPPORT_AGENTS=3（最多3个辅助智能体）
MAIN_EXECUTOR=1（主执行器1个）
GPU_EXCLUSIVE=YES（GPU独占）
GPU_BENCHMARK_SERIAL=YES（GPU正式测试串行）
CONCURRENT_GPU_HEAVY_AGENTS=0（并发GPU重任务为0）
```

如果当前 Codex/调度器支持子智能体，则并行使用：

```text
AGENT-A=PHYSICS_GAP_AUDITOR（物理/Gap审计，只读）
AGENT-B=CODE_TIMING_AUDITOR（代码/计时审计，只读）
AGENT-C=EVIDENCE_GIT_AUDITOR（证据/Git审计，只读）
```

主执行器唯一负责：

```text
GPU run（GPU运行）
文件修改
launcher 修改
instrumentation（计时插桩）
KEEP/ROLLBACK 落地
Git 写入
```

如果子智能体能力不可用，不阻断任务；主执行器按同样三个审计角色串行完成。

严禁多个 H3/ComfyUI GPU 进程同时 benchmark（基准测试）。

---

# E. Git / 工作区安全

先：

```text
git fetch origin
```

保护陌生 dirty changes（未提交修改）。

禁止：

```text
git add .
git reset --hard
force push
覆盖其他任务修改
删除未知成果
```

如果当前工作树不适合直接承载本轮，建立安全分支/worktree（工作树），但不得破坏现有工作。

所有运行时修改必须可逆。

---

# F. 建立 V1：第一最小正确执行版本

Canonical workflow（权威母版）：

```text
C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json
SHA256=89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5
```

只复制，不修改 canonical（权威母版）。

创建：

```text
H3-P0-V1-workflow.json
```

从母版受控减法：

1. `width=32`；
2. `height=32`；
3. `length=5`；
4. `steps=1`；
5. prompt=`static frame`；
6. 保留 `res_multistep / beta`；
7. 断开 first_frame / last_frame（首尾图）输入；
8. 删除不再有依赖的 LoadImage（载图）路径；
9. 不提供外部 audio（音频）；
10. stock 8194 首先不用 TE-Speed 8195；
11. 保留 `VAEDecode -> CreateVideo -> SaveVideo` 最小产物链；
12. `ffprobe / PyAV / black-frame QC / evidence logging` 等验证移到 `RESULT_READY（结果就绪）` 之后，不计入 T_TOTAL；
13. 不缓存最终视频结果。

如果 32×32/1step 在 schema（模式）接受后发生模型内部硬约束失败：

```text
禁止盲目 32->64->128->256 搜索。
```

先读错误与对应源码，只允许把**被源码/错误明确证明非法的字段**提升到最近合法值，并发布：

```text
TASK_CONTRACT_REVISION_V2（任务合同修订v2）
```

记录原因后继续。

---

# G. 权威计时插桩

文件：

```text
C:\AI\MiniMax-H3\ComfyUI\comfy\samplers.py
```

修改前：

```text
SAMPLERS_SHA_BEFORE=<sha256>
BACKUP=YES（已备份）
```

仅在 `KSAMPLER.sample`：

```text
before samples = self.sampler_function(...)
```

记录：

```text
cuda_start = torch.cuda.Event(enable_timing=True)
cuda_end   = torch.cuda.Event(enable_timing=True)
cuda_start.record()
```

执行原 sampler_function，不改变参数/算法。

返回后：

```text
cuda_end.record()
cuda_end.synchronize()
GENERATION_CUDA_MS=cuda_start.elapsed_time(cuda_end)
```

同时保存 wall cross-check（墙钟交叉检查）：

```text
GENERATION_WALL_MS
```

正式核心生成时间：

```text
T_GENERATION = GENERATION_CUDA_MS / 1000
```

Submitter（提交器）计时：

```text
T_TOTAL_START=POST /prompt 之前的 perf_counter
T_TOTAL_END=SaveVideo 最小产物真正 RESULT_READY 时
T_TOTAL=T_TOTAL_END-T_TOTAL_START
T_PATH=T_TOTAL-T_GENERATION
```

避免 WebSocket + HTTP 单连接池死锁；旧 Failure Index（失败索引）FI-02 的教训必须复用。

---

# H. 运行前资源门禁

启动前要求：

```text
8194_LISTENER=NO
8195_LISTENER=NO
NO_OTHER_H3_COMFYUI=YES
NO_OTHER_CUDA_COMPUTE_WORKLOAD=YES
```

桌面显示占用不自动判失败；其他 CUDA compute（CUDA计算）任务会污染正式数据，不能并发。

不要修改：

```text
网络代理
系统代理
FlClash
系统级安全设置
GPU power limit（功耗上限）
GPU overclock（超频）
```

记录 GPU idle（空闲）VRAM / 温度 / 时钟 / 功耗即可。

---

# I. V1 首轮数据

使用正式 8194 launcher（启动器）当前配置先运行：

```text
C:\Users\A\Desktop\Start-MiniMax-H3-8194-Manual.cmd
```

先做 1 次：

```text
COLD_OBSERVATION（冷态观察）
```

只记录，不进入 99。

随后做 1 次 warmup（预热），再用不同 seed 做 3 次正式 V1 warm measurements（稳态测量）：

```text
V1_WARM_RUNS=3
PROMPT_FIXED=YES
SEED_UNIQUE=YES
FINAL_OUTPUT_CACHE=NO
```

得到：

```text
V1_GENERATION_P50_CUDA
V1_GENERATION_P95_CUDA
V1_PATH_P50
V1_PATH_P95
V1_TOTAL_P50
V1_TOTAL_P95
```

技术 QC（质量检查）在 RESULT_READY 后完成；任何无效 run 不进入统计。

---

# J. 自动迭代总算法

从 V1 开始，每轮：

```text
GENERATION_GAP = CURRENT_GENERATION_P50 - TARGET_GENERATION
PATH_GAP       = CURRENT_PATH_P50 - TARGET_PATH
```

其中 TARGET（目标）优先取 `T_MACHINE_STAR` 高置信可达区间内的当前目标。

选择**绝对可消灭时间最大**的一块，不按百分比排序。

```text
NEXT_ATTACK = argmax(ABSOLUTE_REDUCIBLE_TIME)
```

每次只改变一个可解释机制，或不可拆分的同一机制组。

每个候选：

```text
备份
-> 修改
-> 1 次预热
-> 3 次不同 seed 正式 warm run
-> QC
-> 与上一 KEEP 版本比较
```

判定：

```text
IF TASK_COMPLETED=PASS
AND HARD_CONSTRAINTS=PASS
AND gain > measurement_noise（收益高于测量噪声）
THEN KEEP（保留）
ELSE ROLLBACK（回滚）
```

每次 KEEP 后重新计算 Gap，不允许机械把候选列表全部跑完。

---

# K. 首轮候选池（不是固定顺序，按 Gap 重排）

## K1 MODEL RESIDENCY（模型驻留）

当前：

```text
--reserve-vram 3.5
```

这是首要高价值候选。

采用 adaptive search（自适应搜索），不是暴力全扫：

```text
3.5 -> 2.0 -> 1.0 -> 0.5 GiB
```

一旦 OOM（显存不足）/不稳定，立即回滚到最后稳定值，并只在稳定值与失败值之间按 0.25 GiB 粒度做最多两次定点逼近。

目标：最大化 sampler（采样器）期间模型常驻比例，同时保留稳定 workspace（工作区）。

## K2 PINNED MEMORY（锁页内存）/ TRANSFER（传输）

在最佳稳定 reserve-vram 基础上，对比：

```text
保留 --disable-pinned-memory
vs
移除 --disable-pinned-memory
```

其余条件不变。

更快且稳定才 KEEP。

## K3 CONDITIONING CACHE（条件缓存）

固定 prompt 的文本 embedding（嵌入）属于同一固定任务可复用条件。

确保 seed 改变只重跑 noise/sampler（噪声/采样）和必要后处理，不重复 Qwen3-VL 文本编码。

优先使用 ComfyUI 已有 node cache（节点缓存）。

禁止缓存 sampler 最终输出。

## K4 H3↔VAE TRANSITION（H3与VAE切换）

当 PATH 仍为最大 Gap 时，定点分析：

```text
sampler end
-> H3 weight release/offload（H3权重释放/卸载）
-> VAE load/prefetch（VAE加载/预取）
-> decode
```

只采用当前 ComfyUI 已有安全机制或可逆小补丁；测试 pinned transfer / prefetch overlap（锁页传输/预取重叠）。

## K5 RESULT PATH（结果路径）

保持最小视频产物，但把：

```text
history polling（历史轮询）
重复 fetch/copy（抓取/复制）
ffprobe
PyAV decode
black-frame QC
日志/报告/Git
```

全部移到 `RESULT_READY` 后。

正确性仍然要检查，只是不进入生成完成时间。

## K6 PYTHON/KERNEL OVERHEAD（Python/内核开销）

只有前面候选收敛后仍有明显 GENERATION_GAP 才测试：

```text
torch.compile（PyTorch编译）
kernel fusion（内核融合）
CUDA Graph（CUDA图）
现有 model_prefetch（模型预取）参数/机制
```

先读当前源码和现有能力，禁止为了测试随意安装大型新环境。

## 默认低优先级/不跑

```text
Sparse Attention（稀疏注意力）：最小约20 token，收益理论很小
TE-Speed 8195：固定 prompt 缓存后不是主矛盾；历史也并非所有规格都更快
进一步降低精度/新量化：可能改变质量合同
多 GPU-heavy agent：污染单 GPU benchmark
系统超频/功耗修改：不进入本轮
```

---

# L. 新候选发现规则

允许在真实 profiling（性能剖析）中发现 K1~K6 之外的新候选，但必须先由审计角色回答：

```text
WHY_REQUIRED（为什么需要）
EXPECTED_ABSOLUTE_GAIN（预计绝对收益）
TASK_CONTRACT_RISK（任务合同风险）
REVERSIBLE（是否可逆）
RESOURCE_CONFLICT（资源冲突）
```

预计绝对收益不明显，禁止为了“可能快一点”增加实验。

---

# M. 99 判定与最终认证

当候选版首次满足目标后，不立即宣布 99。

做 Final Certification（最终认证）：

```text
VALID_WARM_RUNS=10
UNIQUE_SEEDS=YES
PROMPT_FIXED=YES
FINAL_OUTPUT_CACHE=NO
GPU_EXCLUSIVE=YES
```

要求：

```text
H3_P0_GENERATION_99=YES
当且仅当：
P50_CUDA <= 当前目标高界
P95_CUDA <= 当前P95门槛
TASK_COMPLETED=PASS
NO_HIGH_VALUE_GENERATION_GAP=YES

H3_P0_PATH_99=YES
当且仅当：
P50_PATH <= 当前目标高界
P95_PATH <= 当前P95门槛
TASK_COMPLETED=PASS
NO_HIGH_VALUE_PATH_GAP=YES
```

如果测得比 `T_PHY（物理极限）` 还快，不能直接庆祝；必须优先检查任务合同、计时边界、缓存、输出身份和物理模型。

---

# N. Target Revision Gate（目标修订门禁）

只有真实新证据证明 STEP 1 的某一假设错误时允许修订：

```text
TARGET_VERSION=v2+
OLD_RANGE=
NEW_RANGE=
INVALIDATED_ASSUMPTION（被推翻假设）=
NEW_EVIDENCE（新证据）=
REASON（理由）=
```

禁止：

```text
CURRENT_TOO_SLOW -> MOVE_TARGET_UP
```

---

# O. 自动停止条件

成功停止：

```text
PATH_99=YES
AND GENERATION_99=YES
AND FINAL_CERTIFICATION=PASS
AND SHARED_REPO_SYNC=PASS
```

安全停止而非无限盲跑：

```text
MAX_KEEP_ITERATIONS=12
MAX_TOTAL_CANDIDATE_RUNS=24
```

如果仍未 99，但已经没有高置信、高收益、安全候选：

```text
FINAL=PARTIAL_NOT_99
```

必须给出剩余 Gap 和物理原因，禁止伪造 99。

若未知 CUDA 负载、文件冲突、无法恢复 instrumentation、Git 冲突或任务合同无法保持：安全停止并报告 BLOCKED。

---

# P. Evidence（证据）与 GitHub 收口

本机：

```text
C:\AI\H3-P0-Acceptance\fp-convergence\<timestamp>\
```

至少：

```text
H3-P0-STEP1-TARGET.json
H3-P0-V1-workflow.json
H3-P0-runner.ps1 或等价最小 runner
H3-P0-ITERATIONS.csv
H3-P0-GAP-MATRIX.csv
H3-P0-FINAL.md
H3-P0-FINAL.json
instrumentation.patch
instrumentation-restore-proof.txt
runs\V1\
runs\V2...\
certification\
```

共同仓库正式同步：

```text
docs/h3-p0/<final timestamp>/
```

保存小型正式事实：STEP1 target、V1、每轮 KEEP/ROLLBACK 摘要、最终时间、目标修订、最终认证、SHA、下一步。

大型视频/模型/cache 不提交。

精确 stage（暂存）本轮文件，commit、push、remote verify（远端验证）。

最终必须：

```text
LOCAL_HEAD == ORIGIN_HEAD
SHARED_REPO_SYNC=PASS
REMOTE_VERIFY=PASS
```

---

# Q. 环境恢复

最终无论 PASS / PARTIAL / BLOCKED：

1. 恢复 `samplers.py`；
2. 证明 `SAMPLERS_SHA_AFTER == SAMPLERS_SHA_BEFORE`；
3. 对被 ROLLBACK 的 launcher/配置恢复；
4. 只保留最终 KEEP 版的正式可复现入口；
5. 不留下临时并发 GPU 进程。

如果 instrumentation（插桩）恢复失败：

```text
FINAL != PASS
```

---

# R. 最终只回传这一份结果

```text
H3_P0_FINAL=PASS|PARTIAL_NOT_99|BLOCKED

TASK_CONTRACT_FINAL=
TARGET_VERSION=

T_PHY_GENERATION=
T_MACHINE_STAR_GENERATION=
FINAL_GENERATION_P50_CUDA=
FINAL_GENERATION_P95_CUDA=
H3_P0_GENERATION_99=YES|NO

T_PHY_PATH=
T_MACHINE_STAR_PATH=
FINAL_PATH_P50=
FINAL_PATH_P95=
H3_P0_PATH_99=YES|NO

FINAL_TOTAL_P50=
FINAL_TOTAL_P95=

V1_GENERATION_P50=
V1_PATH_P50=
V1_TOTAL_P50=

TOTAL_KEEP_GAIN=
KEEP_ITERATIONS=
ROLLBACK_ITERATIONS=

WINNING_CHANGES（最终保留优化）=
REJECTED_CHANGES（回滚优化）=
REMAINING_GAPS（剩余差距）=

MULTI_AGENT_MODE=
GPU_EXCLUSIVE=

SAMPLERS_SHA_BEFORE=
SAMPLERS_SHA_AFTER=
INSTRUMENTATION_RESTORE=

EVIDENCE_PATH=
GIT_BRANCH=
GIT_COMMIT=
LOCAL_HEAD=
ORIGIN_HEAD=
SHARED_REPO_SYNC=
REMOTE_VERIFY=
```

任务结束后停止，不继续自动进入 H3-P1 或完整视频质量优化。

---

# S. 发布前审核结果

```text
TASK_CONTRACT_FIXED=PASS（任务合同固定）
TWO_99_ONLY=PASS（只有两个99）
GENERATION_99_EXPLICIT=PASS（图/视频核心生成99明确）
PHYSICS_TARGETS_BOUND=PASS（物理目标已绑定）
V1_IS_DEARMORED=PASS（V1已按去重甲设计）
FULL_ITERATION_LOOP_INCLUDED=PASS（包含完整迭代闭环）
KEEP_ROLLBACK_INCLUDED=PASS（保留/回滚完整）
TARGET_REVISION_GATED=PASS（目标修订有门禁）
MULTI_AGENT_RESOURCE_AWARE=PASS（多智能体考虑资源冲突）
GPU_RUN_SERIAL=PASS（GPU正式运行串行）
AUTHORITATIVE_CUDA_TIMER=PASS（权威CUDA计时）
OUTPUT_RESULT_REQUIRED=PASS（要求真实视频结果）
QC_OUTSIDE_TIMED_PATH=PASS（质量检查移出计时关键路径）
REVERSIBLE_INSTRUMENTATION=PASS（插桩可恢复）
GIT_SAFETY=PASS（Git安全）
SHARED_FACT_SOURCE_CLOSURE=PASS（共同事实源收口）
NO_PROXY_CHANGE=PASS（不改代理）
NO_OVERCLOCK=PASS（不超频）
NO_BLIND_LONG_RUN=PASS（禁止无限盲跑）

COMMAND_REVIEW=PASS
READY_TO_EXECUTE=YES
```
