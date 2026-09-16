# H3-P0 Mature Convergence v2 — 新任务完整执行文件

状态：READY_TO_START（可启动）

本文件定义一个新的 H3-P0 收敛任务。它不是旧任务 V1→V11 的延续编号，也不是重新从零做 H3-P0；它以旧任务冻结档案为事实根，以 `MATURE_PATH_FIRST（成熟路径优先）` 为新的主执行方法，目标是在最短工程时间内达到当前真实硬件边界下的 `H3_P0_GENERATION_99（核心生成99）` 和 `H3_P0_PATH_99（系统路径99）`。

旧任务冻结提交：

`654a47489cb68a958f689484a07bcaa5c659f8e2`

旧任务冻结状态：

```text
H3_P0_LEGACY_RETROSPECTIVE=FROZEN
LAST_GOOD=V3_RESERVE1
H3_P0_GENERATION_99=NO
H3_P0_PATH_99=NO
FINAL_10_RUN_CERTIFICATION=NOT_RUN
```

新任务工作分支：

`codex/h3-p0-mature-convergence-v2`

---

## 1. 新任务总目标

在完整继承旧任务全部已验证事实、失败、坑、控制器能力和经验先验的前提下：

```text
WORLD_KNOWN_BEST（世界成熟已知方案）
→ LOCAL_APPLICABILITY_FILTER（本机适用性筛选）
→ MATURE_HARVEST（成熟收益收割）
→ LOCAL_FIXED-CONTRACT_A/B（本机固定合同A/B）
→ KEEP / ROLLBACK（保留 / 回滚）
→ RESIDUAL_GAP（剩余差距）
→ CUSTOM_ATTACK（定制攻击）
→ GENERATION_99 + PATH_99
→ FINAL CERTIFICATION（最终认证）
→ EXPERIENCE FREEZE（经验冻结）
```

优化两个目标：

```text
PRIMARY_OBJECTIVE = MINIMIZE T_END_TO_END
（最小化真实端到端时间）

SECONDARY_ENGINEERING_OBJECTIVE = MINIMIZE T_CONVERGENCE
（最小化达到稳定最优所需的工程时间）
```

也就是说：不仅要让任务运行得快，还要让“找到稳定最优解”的过程本身尽量走捷径，不重复世界上已经付过的试错成本。

---

## 2. 必须先读取的旧任务事实源

启动新任务后，第一步只读以下文件，不启动 GPU：

1. `docs/h3-p0/20260916-first-principles-v1/H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.md`
2. `docs/h3-p0/20260916-first-principles-v1/H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.json`
3. `docs/h3-p0/20260916-first-principles-v1/H3-P0-LEGACY-EVIDENCE-INDEX.md`
4. `docs/h3-p0/20260916-first-principles-v1/H3-P0-FAILURE-INDEX.md`
5. `docs/h3-p0/20260916-first-principles-v1/H3-P0-EMPIRICAL-PRIORS.md`
6. `docs/h3-p0/20260916-first-principles-v1/H3-P0-MATURE-HARVEST-MATRIX.md`
7. `docs/h3-p0/20260916-first-principles-v1/H3-P0-MATURE-PATH-FIRST-v1.2.md`
8. `docs/h3-p0/20260916-first-principles-v1/H3-P0-STEP1-PHYSICAL-LIMIT-v1.md`
9. `docs/h3-p0/20260916-first-principles-v1/H3-P0-STEP1-RESULTS.json`

不得要求重新阅读旧聊天才能恢复上下文。

旧任务档案是本任务的事实根。若本文件与旧档案具体历史数据冲突，以旧档案与机器可读 JSON 为准，并在新任务中记录冲突，不得自行覆盖历史。

---

## 3. 必须继承的固定任务合同

```text
MODE = T2VA
WIDTH = 32
HEIGHT = 32
FRAMES = 5
STEPS = 1
PROMPT = "static frame"
SAMPLER = res_multistep
SCHEDULER = beta
INPUT_AUDIO = NONE
FINAL_OUTPUT = REAL MP4
```

真实结果链必须保留：

```text
H3 sampler
→ H3 VAE decode
→ CreateVideo
→ SaveVideo
→ real MP4 exists
```

禁止通过缓存最终输出、跳过解码、伪造 result-ready 或改变合同来换取时间。

正式固定 seed：

```text
WARMUP = 910002（不计统计）
FORMAL = 910100, 910102, 910103
```

正式 QC 至少要求：

- history 完成；
- MP4 存在；
- ffprobe 识别 32×32×5；
- ffmpeg 可解码；
- 像素有限、非黑、非平坦；
- range ≥ 8；
- std ≥ 1.5；
- 保存产物 SHA256。

QC 在 RESULT_READY 之后执行，不进入正式总时间。

---

## 4. 权威计时定义

`T_GENERATION（核心生成）`：

- 在 `KSAMPLER.sample` 中围绕 `sampler_function` 的 CUDA Event；
- 结束事件必须 synchronize；
- wall clock 只作交叉检查。

`T_TOTAL（总时间）`：

- 从 POST `/prompt` 之前；
- 到 history 完成且真实 MP4 已存在。

`T_PATH（系统路径）`：

```text
T_PATH = T_TOTAL - T_GENERATION
```

正式 GPU benchmark 必须：

```text
GPU_EXCLUSIVE=YES
GPU_BENCHMARK_SERIAL=YES
PORT=8194
```

任何 profiler、wall 分块、日志时间都不能替代正式 CUDA Event 和正式端到端计时。

---

## 5. 当前真实硬件边界

```text
ACTIVE_HARDWARE_BOUNDARY
= 单 RTX 2080 Ti / 22528 MiB / Turing sm_75
```

RAM：约 32GB。

未来第二张 8GB GPU 当前未安装，因此：

```text
FUTURE_SECOND_GPU_REQUIRED_FOR_CURRENT_99=NO
```

不得让未来硬件阻止当前单卡 99。

未来硬件真实安装后，应继承本任务最终档案重新计算新的 `T_MACHINE_STAR（本机稳定理论极限）`，而不是推翻旧 99。

---

## 6. 当前软件/模型旧基线

旧任务稳定基线环境至少包括：

```text
Windows 10 Pro 22H2 / 10.0.19045
Python 3.11.15
Torch 2.9.1+cu130
CUDA 13.0
Driver 591.74
ComfyUI v0.34.0-16-g8a33128f
comfy-kitchen 0.2.31
comfy-aimdo 0.4.15
DynamicVRAM
async weight offload = 2 streams
PyTorch efficient attention
```

核心模型：

```text
H3 diffusion:
minimax_h3_fl2va_pruned_int8_convrot.safetensors
20970379616 bytes

Text Encoder:
qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
15687142551 bytes

VAE:
minimax_h3_video_vae_fp16.safetensors
5207808496 bytes
```

三个大模型旧任务没有已验证内容 SHA256，这是已知证据缺口；新任务如无必要不要为了补档案扫描几十 GB 文件。若未来模型文件本身要更换或正式冻结最终生产栈，则届时可生成 SHA256。

---

## 7. 当前稳定基准与旧任务成绩

当前权威 `LAST_GOOD（最近保留版本）`：

```text
V3_RESERVE1
reserve-vram = 1.0 GiB
--fast-disk
--disable-pinned-memory
```

正式基准：

```text
GENERATION P50 = 20.226025 s
PATH       P50 = 17.970201 s
TOTAL      P50 = 38.042308 s
```

旧任务从权威 V1 到 V3 已获得：

```text
V1_QC TOTAL P50 = 41.007 s
V3    TOTAL P50 = 38.042 s

收益 ≈ 2.965 s
≈ 7.23%
```

这部分收益已经属于历史资产，不得为了重新展示提升幅度而故意退回慢版本。

---

## 8. 旧任务必须继承的阶段结论

### 8.1 已 KEEP

```text
V2_RESERVE2
reserve-vram 3.5 → 2.0 GiB
TOTAL P50 ≈ 39.910 s
KEEP
```

```text
V3_RESERVE1
reserve-vram 2.0 → 1.0 GiB
TOTAL P50 = 38.042 s
KEEP
LAST_GOOD
```

### 8.2 已 ROLLBACK / 禁止无理由重复

`V4_RESERVE0_5`：

- reserve-vram 1.0 → 0.5 GiB；
- TOTAL P50 ≈ 38.471 s；
- ROLLBACK。

结论：同软件/同模型/同硬件下，不重复 3.5→2→1→0.5 GiB 粗搜索；只有驻留机制、模型或硬件明显改变时才允许重测。

`V5_PINNED`：

- 开启 pinned-memory 路线；
- TOTAL P50 ≈ 43.345 s；
- 相对 V3 慢约 5.303 s；
- ROLLBACK。

限定：只否定旧栈和旧合同下这一路线，不推广为“所有 pinned memory 永远无效”。

`V8_VAE_FULL_SINGLE`：

- 强制 VAE full-load 请求；
- TOTAL P50 ≈ 48.575 s；
- 比 V3 慢约 10.533 s；
- 三组 same-seed 都变慢；
- ROLLBACK。

限定：只证明该旧单卡软件栈下的这次强制完整装载请求没有收益，不否定一切 VAE residency 思路。

`V9_SOFTWARE_036`：

- ComfyUI v0.36.0 + comfy-kitchen 0.2.34 + comfy-aimdo 0.5.3；
- 正式 TOTAL P50 ≈ 45.080 s；
- 比 V3 慢约 7.038 s；
- ROLLBACK。

限定：不能因为“最新版”就自动 KEEP。未来新版本或定向移植必须有具体机制变化并重新 A/B。

### 8.3 诊断事实

`V6_PATH_PROFILE`：

- PATH 大块集中在 VAE stage；
- `T_VAE_DECODE_STAGE P50 ≈ 17.824 s`；
- 但该值不是纯数学 decode 时间，包含模型切换/装载/驻留/输出等可能成本。

`V7_VAE_STAGE`：

- 进一步证明 VAE 调用内部仍存在动态权重请求；
- 禁止把 VAE stage 粗暴解释成纯 GPU 计算时间。

`V10_GENERATION_PROFILE`：

- 50 层 DiT 是核心生成主时间块；
- 稳态一次 H3 forward 约 155 次 residency miss；
- 累计约 5.953GB requested weights；
- `REQUESTED != ACTUAL_TRANSFER`；
- 禁止用 5.953GB 直接估 PCIe 时间。

`V11_OP_PROFILE`：

- profiler 中部分 GPU 算子自耗时约 1.46–1.62 s；
- 正式 CUDA Event 却仍约 22–25 s；
- 时间不闭合说明存在 profiler 扰动、等待或未归属调度；
- profiler 时间不得替代正式计时，也不能直接用来修订物理极限。

---

## 9. 已知旧理论目标与 Target Revision 纪律

旧任务第一版理论：

```text
T_PHY_GENERATION = 0.05–0.12 s
T_PHY_PATH       = 0.18–0.45 s
T_PHY_TOTAL      = 0.23–0.57 s

T_MACHINE_STAR_V1_GENERATION = 0.45–1.40 s
T_MACHINE_STAR_V1_PATH       = 0.70–2.00 s
T_MACHINE_STAR_V1_TOTAL      = 1.15–3.40 s
```

旧 99 门槛：

```text
GENERATION P50 <= 1.40 s
GENERATION P95 <= 1.70 s
PATH P50       <= 2.00 s
PATH P95       <= 2.40 s
```

这些第一版目标当前尚未被正式修订。

新任务不得因为现实结果慢而直接放宽门槛。

只有当成熟路径收割与真实本机证据证明旧假设失效时，才能执行：

`TARGET_REVISION_GATE（目标修订门禁）`

修订必须记录：

```text
OLD_TARGET
NEW_TARGET
INVALIDATED_ASSUMPTION
NEW_EVIDENCE
WHY_THE_OLD_MODEL_FAILED
CONFIDENCE
```

修订是模型被证据纠正，不是为了让当前结果“看起来达到99”。

---

## 10. 必须继承的 Failure Index（失败索引）

新任务启动前必须读取完整 `H3-P0-FAILURE-INDEX.md`。

至少继承：

1. `AI_MODEL_CAPACITY`：Codex/AI 模型容量不足 ≠ 本地 GPU 任务死亡；先查 PID、8194、heartbeat、result、checkpoint。
2. `WINDOWS_ATOMIC_REPLACE`：状态文件采用唯一临时文件名 + bounded retry。
3. `RUNNER_START_PID_WINDOW`：spawn 前先写 `STARTING + launch_id`；恢复时先查已有进程。
4. `PREMATURE_LOCK_RELEASE`：异常退出不能立即删锁；必须确认 owner/runner/heartbeat/8194/结果状态。
5. `PSUTIL_NOSUCHPROCESS`：进程扫描竞态时视为 PID 已退出，重新核对结果，不因此重跑 GPU。
6. `NESTED_POWERSHELL_EXPANSION`：复杂 `$r`、`$_`、`.CommandLine`、`.seed` 逻辑写临时 `.ps1`，不要继续堆外层双引号。
7. `TEMP_SCRIPT_NULL_BYTES`：优先检查脚本生成编码，明确 UTF-8，不调试业务逻辑。

以后同一故障优先走已验证最短恢复路径，禁止重新从零探索。

---

## 11. 必须继承的本地可恢复控制器

旧任务已经形成可复用 controller/runner 体系。

新任务必须优先复用，而不是重写长任务调度。

要求：

```text
state.json
pid.json
heartbeat.json
lock
launch_id
checkpoint
last-good.json
resume
status
stop-safe
```

AI 会话中断时，本地实验必须尽量继续。

恢复时：

```text
先只读检查
→ PID
→ 8194
→ heartbeat
→ runs/results
→ QC
→ checkpoint
→ 再决定是否 resume
```

禁止看到会话错误就重复启动同一 GPU 阶段。

---

## 12. 新方法：MATURE_PATH_FIRST（成熟路径优先）

这是本任务与旧任务最重要的区别。

旧任务已经证明：对于复杂大模型，如果继续从零拆每个 kernel、prefetch、offload、内存和调度机制，会重复支付大量外部世界已经支付过的试错成本。

因此新任务的默认顺序改为：

```text
1. EXTERNAL MATURE SCAN（外部成熟方案扫描）
2. APPLICABILITY FILTER（适用性筛选）
3. MATURE HARVEST MATRIX（成熟收益收割矩阵）
4. TOP CANDIDATE SELECTION（最高价值候选选择）
5. LOCAL A/B（本机真实A/B）
6. KEEP / ROLLBACK
7. RE-MEASURE（重新测量）
8. ONLY THEN CUSTOM ATTACK（之后才定制攻击）
```

这不是放弃第一性原理。

第一性原理负责：

- 固定合同；
- 定义物理边界；
- 定义 99；
- 识别剩余 Gap；
- 防止伪优化。

成熟方案负责：

- 提供已经被别人验证的快捷道路；
- 降低 T_CONVERGENCE。

---

## 13. 外部成熟证据分级

```text
L0 = 官方稳定版 / 官方性能提交 / 官方模型与硬件建议
L1 = 同 GPU 架构、同 VRAM 档、同模型的真实 A/B
L2 = 相邻 GPU 架构或相近硬件的高质量 benchmark
L3 = 大量社区重复验证、机制清楚但硬件差异较大
L4 = 单一经验帖或未复现 claim
```

默认优先 L0–L2。

外部 benchmark 只决定“先测什么”，不自动决定 KEEP。

最终 KEEP 只能由本机固定合同 A/B 产生。

---

## 14. 第一阶段：只读 Mature Harvest（成熟收割）

第一阶段不要立即跑新 GPU 候选。

先更新现有：

`H3-P0-MATURE-HARVEST-MATRIX.md`

至少覆盖：

### 14.1 官方来源

- MiniMax H3 官方仓库/模型卡；
- ComfyUI 当前稳定版与 H3 相关性能提交；
- comfy-kitchen；
- comfy-aimdo；
- model-management / DynamicVRAM / async offload；
- H3 VAE 优化；
- quantization / ConvRot / attention / compiler / prefetch。

### 14.2 同硬件来源

重点：

`IvenKooLab/minimax-h3-turing`

因为它直接覆盖：

- RTX 2080 Ti；
- 22GB；
- Turing / sm_75；
- MiniMax H3；
- 实际生产 A/B。

其结论必须拆成“机制”和“适用条件”，不能整包盲抄。

### 14.3 其他成熟来源

搜索：

- Turing / sm_75 H3；
- 2080 Ti；
- W4A8 / INT8；
- Star7 FP16 Exact；
- H3 VAE 优化；
- 成熟模型格式；
- 低显存/动态驻留；
- 经过真实 A/B 的 ComfyUI H3 加速。

---

## 15. Mature Harvest Matrix 必须包含的字段

每个候选记录：

```text
CANDIDATE
SOURCE_LEVEL
SOURCE_URL_OR_COMMIT
HARDWARE_MATCH
TASK_MATCH
SOFTWARE_MATCH
MECHANISM
TARGET_BLOCK
EXPECTED_ABS_GAIN_S
APPLICABILITY_CONFIDENCE
EVIDENCE_CONFIDENCE
QUALITY_RISK
STABILITY_RISK
INTEGRATION_COST
REVERSIBILITY
CURRENTLY_PRESENT
LOCAL_STATUS
```

分类：

```text
ALREADY_HARVESTED
HIGH_VALUE_TEST
NOT_APPLICABLE
PROVEN_BAD
LOW_PRIORITY
UNKNOWN
```

排序方向：

```text
EXPECTED_ABS_GAIN
× APPLICABILITY
× EVIDENCE_STRENGTH
÷ INTEGRATION_COST
```

不追求伪精确分数。

目标是：大收益、强证据、同硬件、低集成成本优先。

---

## 16. 当前已知 Mature Harvest 初始矩阵事实

旧任务已经形成以下初始结论，新任务先继承再更新：

### ALREADY_HARVESTED

- Torch 2.9.1 + CUDA 13.0；
- INT8 ConvRot H3；
- DynamicVRAM；
- async offload；
- `--disable-pinned-memory`；
- reserve-vram 已粗搜到 1.0 GiB winner。

### PROVEN_BAD（当前合同/当前已测实现）

- pinned-memory 当前开启路线；
- force-full-load VAE 当前实现；
- 完整 v0.36.0+kitchen0.2.34+aimdo0.5.3 当前组合。

### HIGH_VALUE_TEST

至少包括：

- `Star7 FP16 Exact sm75` 实现；
- 后续官方成熟 H3/VAE 定向优化或可定向移植机制；
- 与当前 Turing/1-step 合同真正吻合的成熟实现。

### NOT_APPLICABLE / LOW PRIORITY

- Turbo / PDD 主要减少采样步数；当前 P0 已是 1 step，不能凭外部加速比进入高优先级；
- T8 / BlockCache / MotionCache 主要利用多步或多 block 重复，当前单步收益必须先证明；
- SageAttention 当前本机旧 profiler 显示 attention 不是主大块，且 Turing 兼容性版本敏感；
- 未来第二张 GPU 当前不存在，不进入本轮 99。

---

## 17. 第一批正式测试规则

成熟矩阵完成后，只选择最高价值的 1–3 个候选。

不要同时把十几个成熟方案都跑一遍。

一个候选原则上只改变一个可归因机制。

例外：如果外部成熟方案本身是经过大量验证的不可拆完整栈，可以先作为完整 stack A/B；若整体胜出，再做消融只用于理解和进一步优化，不要求先拆散才允许 KEEP。

每个正式候选：

```text
1 warmup
3 fixed formal seeds
full QC
P50 / P95
paired-seed delta
source/instrumentation restore proof
```

裁决：

```text
FASTER + HARD_CONSTRAINTS_PASS + STABLE
=> KEEP

ELSE
=> ROLLBACK
```

每次 KEEP 后必须更新 `LAST_GOOD`，重新测量并重排候选，不机械跑完整候选列表。

---

## 18. 什么时候才允许进入自研深度优化

只有满足以下任一：

```text
A. HIGH_VALUE_MATURE_CANDIDATES_REMAINING=NO
B. 成熟方案与当前最大 Gap 不匹配
C. 成熟收益已吃完，但仍有显著绝对 Gap
D. 当前任务/硬件组合没有成熟方案覆盖
```

才允许进入：

```text
RESIDUAL_GAP_PROFILE
→ kernel
→ prefetch
→ offload
→ quant/dequant
→ attention
→ compiler
→ CUDA graph
→ custom model management
```

并且仍然永远攻击“最大绝对可减少秒数”，而不是百分比最大的块。

---

## 19. 软件前沿门禁

最终 99 前必须通过：

`SOFTWARE_FRONTIER_GATE=PASS`

必须确认：

- 当前安装版；
- 官方最新稳定版；
- 与 H3 关键路径相关的成熟优化版；
- 与本机 Turing/sm75 相容性；
- 本机同合同 A/B。

最新版不自动等于最优版。

旧任务已经证明 v0.36.0 完整栈在当前条件下比 V3 慢，因此未来不能机械重测同一组合；只有版本、机制或定向移植发生实质变化时才进入新候选。

---

## 20. 硬件拓扑门禁

当前：

```text
HARDWARE_TOPOLOGY_GATE
= 单卡真实边界核验
```

当前只有一张实际可用 RTX 2080 Ti 22GB，因此单卡拓扑核验后即可 PASS。

未来第二张 8GB 卡不属于当前任务。

---

## 21. 多智能体使用规则

允许：

```text
AGENT_MODE=SUPPORT_PARALLEL
```

适合并行：

- 官方成熟方案搜索；
- 同硬件案例搜索；
- 版本/兼容性核验；
- benchmark 证据审计；
- Git/报告整理。

禁止多个 GPU-heavy agent 并行正式 benchmark。

```text
MAIN_EXECUTOR=1
GPU_HEAVY_CONCURRENCY=1
GPU_FORMAL_BENCHMARK_SERIAL=YES
```

多智能体优化的是工程收敛时间，不自动优化单次 H3 执行时间。

---

## 22. 安全与环境限制

必须遵守：

- 不改变网络代理；
- 不修改 FlClash 工作方式；
- 不随意改系统设置；
- 不改 GPU 电源限制/超频；
- 不改 BIOS；
- 系统级 driver/CUDA 候选只有高收益强证据、隔离方案和可回滚路径时才允许进入；
- 不破坏现有稳定 H3 环境；
- 软件候选优先使用独立 worktree/copy/venv/overlay；
- 所有源码插桩必须备份并验证 SHA 恢复。

复杂 PowerShell 使用临时 `.ps1`，避免旧任务已知的嵌套展开坑。

---

## 23. Git 与共同工作区规则

共同事实源：

`cuiqinggang/codex-private-skills`

当前新任务分支：

`codex/h3-p0-mature-convergence-v2`

本任务产生的新工程事实必须：

```text
LOCAL RESULT
→ FORMAL REPORT
→ SHARED REPOSITORY
→ EXACT STAGE
→ COMMIT
→ PUSH
→ REMOTE VERIFY
```

禁止：

```text
git add .
force push
git reset --hard
```

不得覆盖旧任务冻结提交。

旧任务分支/提交是只读历史基线。

---

## 24. 本任务必须持续保存的文件

建议新任务目录：

`docs/h3-p0/20260917-mature-convergence-v2/`

至少持续维护：

1. `H3-P0-MATURE-CONVERGENCE-TASK.md` — 本文件，任务合同。
2. `H3-P0-MATURE-HARVEST-MATRIX-v2.md` — 更新后的成熟收益矩阵。
3. `H3-P0-EXTERNAL-SOURCE-MAP.md` — 外部成熟来源、commit、PR、版本、适用性。
4. `H3-P0-LOCAL-BASELINE-v2.json` — 新任务起点基线。
5. `H3-P0-ITERATION-LEDGER.md` — 每轮候选、数据、KEEP/ROLLBACK。
6. `H3-P0-DECISION-LOG.json` — 机器可读裁决。
7. `H3-P0-FAILURE-INDEX-v2.md` — 仅新增新故障；旧故障通过链接继承。
8. `H3-P0-EMPIRICAL-PRIORS-v2.md` — 新任务新经验先验。
9. `H3-P0-TARGET-REVISION.md` — 仅在目标修订门禁触发时生成/更新。
10. `H3-P0-FINAL-CERTIFICATION.md` — 双99完成后的最终认证。
11. `H3-P0-FINAL-SKILL-HARVEST.md` — 最终把成熟路径、最短路径、失败索引压缩回母技能。

如果某文件尚无内容，不必预先制造空文件；在第一次产生相关事实时创建。

---

## 25. 每轮正式候选必须保存的证据

每轮至少保存：

```text
phase / candidate id
purpose
source/evidence level
single changed mechanism
full command/runtime flags
software version matrix
hardware snapshot
warmup result
3 formal runs
P50/P95
paired seed deltas
QC
artifact hashes
instrumentation before/after SHA
KEEP/ROLLBACK decision
reason
rollback proof
last-good update
```

如果使用外部完整成熟栈，还要保存：

```text
source URL / repo / commit / release
which parts were copied
which parts were changed locally
compatibility deviations
```

---

## 26. 证据不足时的纪律

禁止：

- 因为外部项目“说更快”就自动 KEEP；
- 因为新版发布就自动升级生产基线；
- 把 profiler 自耗时当成正式端到端时间；
- 把累计请求字节当成实际 PCIe 传输；
- 为了达到99而放宽目标；
- 为了补历史档案重跑已经完成且有充分证据的旧阶段；
- 把未来硬件当成当前必须条件；
- 同时修改多个未知机制导致结果不可归因。

允许：

- 用外部成熟 benchmark 决定测试优先级；
- 用同硬件成熟案例跳过明显死路；
- 用完整成熟栈做第一次 A/B；
- 如果成熟栈直接胜出，先 KEEP，再在需要时做消融。

---

## 27. 当前新任务第一阶段的具体执行顺序

启动后严格按以下顺序：

### Phase A — Inherit（继承）

- 读取旧回归档案、JSON、证据索引、Failure Index、经验先验；
- 确认旧冻结 commit；
- 建立新任务 baseline snapshot；
- 不运行 GPU。

### Phase B — World Scan（世界成熟扫描）

- 官方 H3/ComfyUI/comfy-kitchen；
- Turing/sm75；
- 2080 Ti 22GB；
- 同模型/同量化；
- 有 A/B 数据的成熟优化。

### Phase C — Applicability Filter（适用性筛选）

筛掉：

- 只对多步采样有效；
- 只对 Ampere/Ada/Blackwell 有效；
- 改变任务合同；
- 质量/稳定风险无法接受；
- 已经被本机证伪且机制未变化。

### Phase D — Rank（排序）

输出最高价值 1–3 个候选。

### Phase E — Local A/B（本机A/B）

逐一运行，不并发。

### Phase F — Re-measure（重新测量）

每次 KEEP 后更新 LAST_GOOD、矩阵、Gap。

### Phase G — Residual Custom Attack（剩余定制攻击）

只有成熟高价值候选耗尽后进入。

### Phase H — 99 Certification（99认证）

达到正式门槛后执行最终 10 条有效稳态认证，并核对 P50/P95、QC、稳定性、软件前沿、硬件门禁和共同仓库同步。

---

## 28. 99 定义

99 不是数学绝对极限，也不是“比旧版本快很多”。

必须同时满足：

1. TASK_COMPLETED=TRUE；
2. QC PASS；
3. 正式 CUDA/端到端计时稳定；
4. 当前结果进入或贴近经过证据校准后的 `T_MACHINE_STAR`；
5. 无明显大块重甲；
6. 无高置信、高收益成熟候选遗漏；
7. Mature Path First Gate PASS；
8. Software Frontier Gate PASS；
9. Hardware Topology Gate PASS；
10. 最终 10 次认证 PASS；
11. Shared Repo Sync PASS；
12. Failure/rollback/last-good 证据完整。

最终只能声明两个 99：

```text
H3_P0_GENERATION_99
H3_P0_PATH_99
```

不建立 TOTAL_99。

---

## 29. 最终完成后必须保存什么

达到双99后必须生成最终收口资产：

### 29.1 Final Winner（最终赢家）

完整记录：

- hardware boundary；
- software stack；
- exact versions/commits；
- model files；
- launch flags；
- workflow SHA；
- controller/runner；
- final P50/P95；
- 10-run raw results；
- QC；
- final artifact hashes。

### 29.2 Mature Harvest Summary（成熟收割总结）

明确：

- 哪些收益直接来自成熟外部方案；
- 哪些成熟方案本机无效；
- 哪些外部结论因任务不匹配而跳过；
- 哪些剩余收益来自自研定制攻击。

### 29.3 Do Not Repeat（禁止重复支付试错成本）

每个死路记录：

- 机制；
- 证据；
- 适用边界；
- 什么条件变化才允许重测。

### 29.4 EMPIRICAL_PRIORS v2（经验先验2）

把最终真实数据压缩成下一次任务可以直接继承的先验。

### 29.5 Mother Skill Upgrade（母技能升级）

把这次验证后的最短成熟路径、Failure Index、新控制器经验和“成熟路径优先”真实案例回写：

`first-principles-physical-limit-convergence`

要求：

```text
经验完整保留
执行路径极简
默认先读 FAST PATH
故障时再读 FAILURE INDEX
```

---

## 30. 本任务最终 Git 收口

只有：

```text
LOCAL_RESULT=PASS
AND GENERATION_99=YES
AND PATH_99=YES
AND FINAL_10_RUN_CERTIFICATION=PASS
AND MATURE_PATH_FIRST_GATE=PASS
AND SOFTWARE_FRONTIER_GATE=PASS
AND HARDWARE_TOPOLOGY_GATE=PASS
AND SHARED_REPO_SYNC=PASS
AND REMOTE_VERIFY=PASS
```

才允许：

```text
H3_P0_MATURE_CONVERGENCE_V2=FROZEN
FINAL=PASS
```

完成后必须回报：

- 最终 branch；
- final commit SHA；
- remote HEAD；
- 最终 winner；
- Generation P50/P95；
- Path P50/P95；
- 10-run certification；
- 成熟方案收割结果；
- 剩余自研攻击结果；
- Failure Index 新增项；
- 母技能更新状态。

---

# 一句话执行原则

> **先完整继承旧任务已经付出的全部试错成本，再系统收割世界上已经成熟验证、且与当前 RTX 2080 Ti / Turing / H3-P0 真正匹配的大收益方案；只有成熟收益吃完以后，才对剩余绝对 Gap 做定制攻击，最终以本机真实 A/B、双99和10次认证冻结结果。**
