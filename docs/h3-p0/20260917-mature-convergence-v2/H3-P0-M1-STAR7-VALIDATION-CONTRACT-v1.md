# H3-P0 M1 — Star7 Native FP16 Exact 完整验证合同 v1

状态：`GPT_RAILROAD_READY / NOT_EXECUTED`

此文件是下一条允许 Codex 执行的第一成熟候选合同。它只验证 M1；任何 M2/M3/M4、profiling、参数搜索或附加实验都不属于本轮授权。

## 0. 身份与环境门禁

```text
SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_SKILL_VERSION=1.8.0
CANONICAL_SKILL_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
CANONICAL_IDENTITY_GATE=PASS required
NO_FREE_EXPLORATION=YES
PROJECT_WORKSPACE_BRANCH=codex/h3-p0-mature-convergence-v2
PROJECT_PATH=docs/h3-p0/20260917-mature-convergence-v2
GPU_EXCLUSIVE=YES
GPU_BENCHMARK_SERIAL=YES
PORT=8194
```

本机 runtime 技能若不是 v1.8.0：本轮直接 `BLOCKED / NO GPU RUN / RETURN GPT`。

不得修改网络代理、系统代理或其他无关系统设置。

## OBJECTIVE

验证成熟 `MiniMax H3 Native FP16 Loader - Star7` 是否能在 RTX 2080 Ti sm75 上，在保留当前 INT8 ConvRot checkpoint 和固定 P0 合同的情况下，显著降低 Generation 和 Total，同时保持完整 MP4/QC。

## CURRENT_STATE

控制组固定：

```text
DIFFUSION=minimax_h3_fl2va_pruned_int8_convrot.safetensors
TEXT_ENCODER=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VIDEO_VAE=minimax_h3_video_vae_fp16.safetensors
FLAGS=--fast-disk --reserve-vram 1.0 --disable-pinned-memory
MODE=T2VA
32x32 / 5f / 1step / static frame
res_multistep / beta
NO_INPUT_AUDIO
REAL_MP4
```

历史 V3 只作 sanity anchor；真实裁决使用本轮 same-window control。

## ALLOWED_CHANGE

唯一性能变量：

```text
STANDARD H3 DIFFUSION LOADER
→ MiniMax H3 Native FP16 Loader - Star7
```

允许安装官方/上游 Star7 节点包并最小修改 P0 workflow 以替换 loader。

必须确认 Star7 诊断：

```text
GPU_ARCH=sm75/Turing
FP16_PROTECTED_PATH_ACTIVE=YES
QUANTIZED_CHECKPOINT_DETECTED=YES
FORCE_CAST_WEIGHTS=false (or equivalent proof quantized path preserved)
INT8/ConvRot scheduling preserved=YES
```

若实际插件字段名称不同，允许记录其真实等价日志，但不得自行发明其他优化。

## ALLOWED_FILES_OR_COMPONENTS

允许触碰：

- `C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-fp16-exact-star7`（安装/更新本候选）；
- 当前 P0 workflow 的候选副本；
- M1 本轮临时控制/候选工作文件；
- M1 证据目录；
- 本项目本轮正式报告/JSON。

禁止：

- 修改原 diffusion / text encoder / VAE 权重；
- 同时换 W4A8；
- 同时换 INT8 VAE；
- 加 conditioning cache；
- 加 Activation Chunk / Sage / SLA / Sol；
- 改 steps/sampler/scheduler/seed/resolution/frames；
- 开 profiler、kernel trace、参数 sweep；
- 改代理或系统设置。

## BASELINE

同一验证窗口先跑 `M1_CONTROL`：当前原 loader + 当前模型。

历史：

```text
V3_P50_TOTAL=38.042308 s
MRE_P50_TOTAL=54.817736 s
```

二者不直接作为 KEEP 基线，只用于识别异常漂移。

## SEEDS_AND_RUN_COUNT

```text
CONTROL_WARMUP=910002
CONTROL_FORMAL=910100,910102,910103
CANDIDATE_WARMUP=910002
CANDIDATE_FORMAL=910100,910102,910103
MAX_GPU_RUNS=8
```

每条只执行一次。不得因某条慢而自动追加重复样本。

## TIMING_BOUNDARY

沿用已有权威定义：

```text
T_GENERATION=KSAMPLER.sample 内 sampler_function 前后 CUDA Event + synchronize
T_TOTAL=POST /prompt 前 → history complete AND real MP4 exists
T_PATH=T_TOTAL-T_GENERATION
QC=RESULT_READY 后执行，不计入 Total
```

## QC_GATE

每个正式 seed：

```text
history complete
real MP4 exists
ffprobe=32x32x5
ffmpeg decode PASS
finite pixels
non-black
non-flat
frame range >= 8
frame std >= 1.5
MP4 SHA256 recorded
```

3/3 candidate formal QC 必须 PASS。

## EXPECTED_BOUNDED_OUTCOME

允许的虚拟预期只有方向，不伪造本机秒数：

```text
EXPECTED_DIRECTION=Generation lower if Turing manual-cast/FP32 path is a major cause
EXPECTED_ABS_GAIN_S=UNKNOWN_UNTIL_LOCAL_PAIRED_AB
T_PHY_TOTAL_REFERENCE=0.23–0.57 s (comparison only)
```

外部 V100 ~11× 结果不得换算成本机预计值。

## SUCCESS_RULE

M1 进入 GPT 的 `KEEP_CANDIDATE` 必须：

1. candidate QC 3/3 PASS；
2. 三个同 seed `CONTROL_G-CANDIDATE_G` paired median > 0；
3. 至少 2/3 Generation paired delta > 0；
4. Total paired median > 0；
5. 收益高于本窗口噪声，不以单条 fastest run 判定；
6. Star7 量化路径保护证据成立；
7. 无新的稳定性错误/NaN/黑帧；
8. task contract 完全不变。

Codex 只能报告 `SUCCESS_RULE_MET=YES/NO`；正式 `KEEP` 由 GPT 决定。

## FAILURE_RULE

任一：

```text
plugin incompatible
quantized checkpoint expanded incorrectly
QC fail
NaN/Inf
black/flat frame
candidate paired median Generation <= control
candidate Total materially slower
task contract drift
source/workflow cannot be restored
```

=> 按预定义 rollback，记录 `M1_FAILURE`，停止。

## INCONCLUSIVE_RULE

若：

- control 窗口发生异常漂移；
- paired seeds 方向严重分裂；
- 收益与测量噪声同量级；
- 插件诊断无法证明走了预期 quantized+FP16 protected path；

则：

```text
M1_RESULT=INCONCLUSIVE
NO_EXTRA_RUNS=YES
STOP=YES
RETURN_TO_GPT=YES
```

## ROLLBACK

候选结束后无论成功/失败：

- 原始权重不变；
- 原始 P0 workflow 保留；
- 若 M1 未经 GPT KEEP，不把候选 workflow 设为新默认；
- 源码若有临时插桩必须恢复并哈希回读；
- 8194 服务退出；
- 确认无第二 H3 实例。

Star7 节点包本身若只是独立安装且未污染原 workflow，可保留为候选资产；不得自动启用到生产默认。

## STOP_POINT

本轮完成以下收口后立即停止：

```text
control results complete
candidate results complete or predefined failure
QC complete
paired deltas computed
M1 report + JSON written
formal project files committed/pushed
REMOTE_VERIFY=PASS
STOP
RETURN RESULT TO GPT
```

不得自动执行 M2。

## MAX_GPU_RUNS

```text
MAX_GPU_RUNS=8
NO_AUTOMATIC_EXTRA_RUNS=YES
```

## TIME_BUDGET

```text
GPU_VALIDATION_WINDOW_BUDGET=15 minutes target ceiling
OPEN_ENDED_DEBUG_BUDGET=0
```

若因启动/安装/环境问题明显超出铁路边界，且没有预定义修复：安全停止，不把超时变成新探索。

## CODEX_BUDGET

```text
ONE_CANDIDATE_ONLY=M1
AUTONOMOUS_NEXT_CANDIDATE=NO
AUTONOMOUS_PROFILING=NO
AUTONOMOUS_FIX_SEARCH=NO
```

## NEXT_ACTION_AFTER_EACH_OUTCOME

```text
SUCCESS_RULE_MET
→ write evidence
→ rollback to controlled safe state unless GPT explicitly designated candidate persistence
→ remote verify
→ STOP
→ GPT decides KEEP and whether M2 uses Star7 path

FAILURE_RULE_MET
→ rollback
→ write failure evidence
→ remote verify
→ STOP
→ GPT decides M2 route

INCONCLUSIVE
→ safe restore
→ write evidence
→ remote verify
→ STOP
→ GPT redesigns M1 only
```

本合同到此结束。
