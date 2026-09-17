# H3-P0 STEP 4 — Codex 确定性实测命令包 v1

状态：`STEP4_COMPLETE=YES / COMMAND_PACK_REVIEWED / NOT_EXECUTED`

依据：

- `first-principles-physical-limit-convergence v1.8.0`
- `H3-P0-STEP1-PHYSICAL-LIMIT-FINAL-v1.8.md`
- `H3-P0-STEP2-REAL-STATE-OPTIMUM-RANGE-v1.md`
- `H3-P0-STEP3-VIRTUAL-ATTACK-ITERATION-v1.md`

本命令包已经把 Virtual-99 转成 Codex 只能机械执行的验证铁路。Codex 不得从结果自行派生新实验。

---

# A. 最高门禁

```text
SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_SKILL_VERSION=1.8.0
CANONICAL_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
PROJECT_REMOTE=cuiqinggang/codex-private-skills
PROJECT_BRANCH=codex/h3-p0-mature-convergence-v2
PROJECT_PATH=docs/h3-p0/20260917-mature-convergence-v2
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
GPU_EXCLUSIVE=YES
GPU_BENCHMARK_SERIAL=YES
PORT=8194
```

## A1. Canonical skill runtime gate

执行任何 GPU 任务前：

1. 从 canonical branch 远端读取 `skills/first-principles-physical-limit-convergence/VERSION` 和 `SKILL.md`；
2. 必须确认远端 `VERSION=1.8.0`；
3. 检查本机 `C:\Users\A\.codex\skills\first-principles-physical-limit-convergence`；
4. 若本机不存在或版本不是 1.8.0：先备份现有目录，再从 canonical branch 安装/同步 v1.8.0，回读 VERSION/SKILL.md 验证；
5. 不得把 H3 项目分支中历史 `VERSION=1.0.0` 快照当运行规则源。

失败：

```text
CANONICAL_IDENTITY_GATE=BLOCKED
→ NO GPU RUN
→ NO INSTALL OF CANDIDATES
→ REPORT
→ STOP
```

## A2. 项目远端门禁

必须先 fetch 并远端回读以下文件：

```text
H3-P0-REMOTE-WORKSPACE-DECLARATION.md
H3-P0-STEP1-PHYSICAL-LIMIT-FINAL-v1.8.md
H3-P0-STEP2-REAL-STATE-OPTIMUM-RANGE-v1.md
H3-P0-STEP3-VIRTUAL-ATTACK-ITERATION-v1.md
H3-P0-STEP4-CODEX-TEST-COMMAND-PACK-v1.md
```

本地 clone 只是 `LOCAL_EXECUTION_CHECKOUT`，不是共同事实源。

## A3. 环境硬限制

```text
DO_NOT_CHANGE_PROXY=YES
DO_NOT_CHANGE_SYSTEM_NETWORK=YES
DO_NOT_CHANGE_UNRELATED_SYSTEM_SETTINGS=YES
BACKUP_BEFORE_MODIFY=YES
READBACK_AFTER_MODIFY=YES
NO_SECOND_H3_INSTANCE=YES
NO_PROFILER_UNLESS_STAGE_EXPLICITLY_AUTHORIZES=YES
NO_PARAMETER_SWEEP=YES
NO_AUTOMATIC_EXTRA_RUNS=YES
```

---

# B. 固定任务与计时/QC

```text
MODE=T2VA
WIDTH=32
HEIGHT=32
FRAMES=5
STEPS=1
PROMPT="static frame"
SAMPLER=res_multistep
SCHEDULER=beta
INPUT_AUDIO=NONE
FINAL_OUTPUT=REAL_MP4
```

固定 seeds：

```text
WARMUP=910002
FORMAL=910100,910102,910103
```

每个普通 A/B stage 最多：

```text
CONTROL  = 1 warmup + 3 formal
CANDIDATE= 1 warmup + 3 formal
MAX_GPU_RUNS=8
```

不得自动添加重复样本。

计时：

```text
T_GENERATION = CUDA Event around sampler_function + synchronize
T_TOTAL = before POST /prompt → history complete AND real MP4 exists
T_PATH = T_TOTAL - T_GENERATION
QC executes after RESULT_READY and is not included in T_TOTAL
```

QC：

- history complete；
- MP4 exists；
- ffprobe = 32×32×5；
- ffmpeg decode succeeds；
- finite pixels；
- non-black/non-flat；
- every frame range >= 8；
- every frame std >= 1.5；
- artifact SHA256 saved。

任何质量异常：候选失败，不允许降低 QC。

---

# C. 统一 paired A/B 裁决

每个候选使用本阶段同窗口 control，不直接用数日前 V3/MRE 判 KEEP。

定义每个 formal seed：

```text
GAIN_TOTAL(seed) = CONTROL_TOTAL(seed) - CANDIDATE_TOTAL(seed)
GAIN_GEN(seed)   = CONTROL_GEN(seed)   - CANDIDATE_GEN(seed)
GAIN_PATH(seed)  = CONTROL_PATH(seed)  - CANDIDATE_PATH(seed)
```

默认 KEEP 规则：

```text
ALL_QC_PASS=YES
P50_TOTAL_GAIN > max(0.5 s, 3% of control P50)
PAIRED_MEDIAN_TOTAL_GAIN > 0
AT_LEAST_2_OF_3_FORMAL_SEEDS_FASTER=YES
NO_NEW_STABILITY_FAILURE=YES
```

如果候选只攻击 Generation 或 Path，可同时报告对应主块；但总时间不能显著退化。

ROLLBACK：

```text
QC_FAIL
OR paired median <= 0
OR total P50 regression > 0.5 s
OR required mechanism not actually active
OR new stability/runtime failure
```

INCONCLUSIVE：

```text
control window unstable
OR server/environment drift invalidates pairing
OR evidence incomplete
```

INCONCLUSIVE 时不得追加运行：保存证据、恢复、停止、返回 GPT。

---

# D. 已冻结的完整执行铁路

## E0 — SAME-WINDOW CONTROL

OBJECTIVE：建立本轮实时控制组并验证性能漂移是否可比较。

ALLOWED_CHANGE：无性能变化，只运行当前 last-good 合同。

EXPECTED_BOUNDED_OUTCOME：Total P50 可能落在历史 38s 到当前 MRE 55s 一带；任何值都不自动改目标。

FAIL/INCONCLUSIVE：3 formal 无法 QC 3/3 或时间极端漂移且控制不稳定。

STOP_POINT：控制组完整后进入 E1；E0 与 E1 必须同一验证窗口。

---

## E1 — A1 Star7 Native FP16 Exact

OBJECTIVE：验证 Turing FP16 protected loader 是否真实降低 Generation/Total。

ALLOWED_CHANGE：唯一性能变量为 standard H3 diffusion loader → `MiniMax H3 Native FP16 Loader - Star7`。

必须证明：

```text
GPU_ARCH=sm75
PROTECTED_FP16_PATH_ACTIVE=YES
QUANTIZED_CHECKPOINT_DETECTED=YES
force_cast_weights=false or exact equivalent
INT8/ConvRot preserved=YES
```

ALLOWED_FILES：Star7 custom node、候选 workflow 副本、本轮证据、项目报告。

禁止：同时换 W4A8/VAE/cache/residency policy/attention/profiler。

EXPECTED_BOUNDED_OUTCOME：Virtual 规划 Total 可能净降约 2–6s；不是成功保证。

MAX_GPU_RUNS=8；GPU_RUNTIME_BUDGET<=15min；WALL_STAGE_BUDGET<=45min；CODEX_BUDGET=ONE_STAGE_ONLY。

NEXT：写 `E1-RESULT.md/json` → restore/KEEP by rule → push → remote verify → STOP → RETURN GPT。

**即使 E1 PASS，也不得自动执行 E2。**

---

## E2 — A2 W4A8 FL2VA diffusion（必须 GPT 解锁）

PRECONDITION：E1 已远端收口；GPT 明确 `UNLOCK_E2=YES`。

OBJECTIVE：验证约 12.5GB W4A8 FL2VA 是否降低 Generation 和驻留/Path。

BASELINE：最新 KEEP winner，不固定要求 Star7；若 E1 rollback，则用 E0 winner。

ALLOWED_CHANGE：只替换 diffusion checkpoint/其必要原生 loader 配置；其他合同不变。

必须保存 candidate 模型文件名、大小、来源、SHA256（若正式纳入候选下载完成后生成）。

QC：除普通 QC 外，保存同 seed 基础帧统计；任何明显质量塌陷直接 rollback。

EXPECTED_BOUNDED_OUTCOME：Virtual 额外净收益约 6–12s，但实际以 paired A/B 为唯一裁决。

MAX_GPU_RUNS=8；同统一预算；STOP 后返回 GPT，不自动 E3。

---

## E3 — A3 Conditioning Cache Applicability（必须 GPT 解锁）

PRECONDITION：GPT `UNLOCK_E3=YES`。

先做只读/零性能改变检查：确认 current formal seed changes 是否实际重新执行 Qwen3-VL conditioning。

如果 native Comfy cache 已复用：

```text
A3=ALREADY_EFFECTIVELY_HARVESTED
GPU_RUNS=0 additional
STOP/REPORT
```

如果确实重复 conditioning：才允许安装/验证 `ComfyUI-MiniMaxH3-CLIPCached`，只缓存 conditioning，不缓存 final latent/sampling/VAE/output。

必须先 MISS 建立 cache，再以相同 prompt + 不同正式 seed 测 HIT；cache key 必须证明 seed 不参与 invalidation。

EXPECTED_BOUNDED_OUTCOME：Virtual 规划本机 Path 可能下降 4–10s；外部 5080 数字不得用于本机裁决。

STOP 后返回 GPT，不自动 E4。

---

## E4 — A4 INT8 ConvRot Video VAE（必须 GPT 解锁）

PRECONDITION：GPT `UNLOCK_E4=YES`。

OBJECTIVE：验证 smaller INT8 ConvRot VAE 是否降低 Path 且不产生 2080Ti black/NaN/Inf。

ALLOWED_CHANGE：Video VAE checkpoint only + 必需的已知兼容 loader support；diffusion/text encoder/sampler 等冻结。

STRICT_QC：

```text
all decoded tensors finite
all frames non-black/non-flat
range/std thresholds PASS
ffmpeg/ffprobe PASS
same task dimensions PASS
```

任一 NaN/Inf/black：立即候选失败；无需跑完剩余 candidate seeds；安全回滚并保存失败证据。这里允许早停，不能为满足“8 runs”继续浪费 GPU。

EXPECTED_BOUNDED_OUTCOME：Virtual 额外净收益约 2–6s；公开 1.5–1.7x 只为机制先验。

STOP 后返回 GPT。

---

## E5 — R1 New-topology co-residency/prefetch（条件 + GPT 解锁）

PRECONDITION：A2 已 KEEP；最新模型容量关系显著改变；最新实测 Path 中 residency transition 仍 >=10% Total；GPT `UNLOCK_E5=YES`。

OBJECTIVE：在新容量拓扑下只测试一个预定义 H3→VAE 最小 eviction/residency policy。

禁止 reserve-vram sweep、自动 VRAM search、多策略比较。

ALLOWED_CHANGE：GPT 当轮会在解锁命令中填入唯一 policy；若未填：`VALIDATION_PLAN_NOT_MATURE=YES → STOP`。

MAX_GPU_RUNS=8；STOP 后返回 GPT。

---

## E6 — R2 minimal H3 host-sync patch（条件 + GPT 解锁）

PRECONDITION：成熟大头收割后，最新 Generation residual 仍 >=10% Total 或明显高于 STEP2 Generation 2–5s 目标带；GPT `UNLOCK_E6=YES`。

OBJECTIVE：只验证已审查的最小 host-sync 减法。

允许：

- invariant `text_tags` Python list cache；
- 将重复 sigma host scalar reads 合并到预定义的最小次数；
- 保持数学 sigma/time-shift 完全等价。

禁止：完整 torch.compile/CUDA Graph 改造、layout 重构、kernel search、profiler sweep。

修改前后必须备份源码并记录 SHA256；结束无论 KEEP/ROLLBACK 均验证源码/候选状态清楚。

EXPECTED_BOUNDED_OUTCOME：Virtual 规划 0.5–3s；实际 paired A/B 裁决。

STOP 后返回 GPT。

---

# E. 结果返回格式

每个 stage 必须生成远端正式：

```text
H3-P0-E<n>-RESULT.md
H3-P0-E<n>-RESULT.json
```

至少含：

```text
CANONICAL_SKILL_VERSION
REMOTE_PROJECT_HEAD_BEFORE
CONTROL_CONFIG
CANDIDATE_CONFIG
EXACT_ONE_CHANGE
MECHANISM_ACTIVE_PROOF
RUNS[]
P50/P95 Generation/Path/Total
PAIRED_GAINS[]
QC[]
KEEP_ROLLBACK_INCONCLUSIVE
ROLLBACK_PROOF
SOURCE_SHA_BEFORE_AFTER
EVIDENCE_ROOT
REMOTE_COMMIT
REMOTE_VERIFY
NEXT_ACTION=RETURN_TO_GPT
```

只有 push + remote verify 后：

```text
SHARED_FACT_CONFIRMED=YES
```

---

# F. Final Certification 入口

只有 GPT 根据最新数据确认：

```text
HIGH_VALUE_MATURE_CANDIDATES_REMAINING=NO
RESIDUAL_VIRTUAL_CONVERGENCE_COMPLETE=YES
PORTFOLIO_ROI_EVALUATED=YES
NO_SHORT_POSITIVE_ROI_ATTACK_REMAINS=YES
```

才允许发 Final Certification 解锁。

Final：10 条有效 warm runs、变化 seed、任务合同固定、完整 QC，最终配置/Failure Index/Empirical Priors/证据全部远端冻结。

---

# G. 给 Codex 的当前可直接粘贴启动命令

```text
执行 H3-P0 STEP 4 确定性验证任务。

唯一方法源：first-principles-physical-limit-convergence v1.8.0。
远端共同工作区：cuiqinggang/codex-private-skills，分支 codex/h3-p0-mature-convergence-v2，路径 docs/h3-p0/20260917-mature-convergence-v2。

先远端回读并严格遵守：
1) H3-P0-REMOTE-WORKSPACE-DECLARATION.md
2) H3-P0-STEP1-PHYSICAL-LIMIT-FINAL-v1.8.md
3) H3-P0-STEP2-REAL-STATE-OPTIMUM-RANGE-v1.md
4) H3-P0-STEP3-VIRTUAL-ATTACK-ITERATION-v1.md
5) H3-P0-STEP4-CODEX-TEST-COMMAND-PACK-v1.md

先通过 canonical identity/runtime gate：远端 canonical branch 必须是 codex/first-principles-physical-limit-convergence-v1.8.0；本机 runtime skill 必须回读为 VERSION=1.8.0。若本机不是 v1.8.0，先备份后同步安装并回读验证。H3 项目分支中的历史 v1.0.0 skill 快照不得作为运行规则源。

NO_FREE_EXPLORATION=YES。禁止自行发现候选、修改顺序、增加运行、做 profiler、参数 sweep、版本 sweep、VRAM sweep、改变代理/网络/系统设置。

本次只授权 E0 SAME-WINDOW CONTROL + E1 Star7 Native FP16 Exact paired A/B。严格使用命令包内固定任务、seeds、计时、QC、MAX_GPU_RUNS、KEEP/ROLLBACK/INCONCLUSIVE 规则。E1 完成后写正式 md/json、push 到项目远端分支并 remote verify，然后停止并返回全部结果。即使 E1 PASS，也绝对不得自动进入 E2。

若任何门禁缺项、环境异常、控制组失稳或出现未定义情况：保存证据、安全恢复、停止、返回，不得自行补计划。
```

## STEP 4 结论

```text
STEP4_COMPLETE=YES
COMMAND_PACK_REVIEWED=YES
CURRENT_AUTHORIZATION=E0+E1_ONLY
E2_TO_E6=PREWRITTEN_BUT_LOCKED
CODEX_FREE_EXPLORATION=NO
ACTUAL_GPU_EXECUTION=NOT_STARTED
```
