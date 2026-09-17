# H3-P0 Virtual-99 Railroad v1 — GPT 完整虚拟运行铁路

状态：`VIRTUAL_99_RAILROAD_COMPLETE=YES / EXECUTION_NOT_STARTED`

方法：`first-principles-physical-limit-convergence v1.8.0`

本文件完成“先把第1部分能虚拟完成的全部完成”：单一物理极限、成熟候选组合、执行顺序、每一候选的验证合同、分支、停止点、残余收敛和 Final-99 入口。它**不授权 Codex 自行连续执行**。

---

## 0. 固定输入

```text
T_PHY_TOTAL_REFERENCE=0.23–0.57 s
CURRENT_MRE_TOTAL_P50=54.817736 s
CURRENT_MRE_TOTAL_P95=59.811207 s
PROVEN_STABLE_V3_TOTAL_P50=38.042308 s
PROVEN_STABLE_V3_TOTAL_P95=38.488666 s
ACTIVE_HARDWARE=RTX_2080_Ti_22528MiB_sm75
CURRENT_DIFFUSION=minimax_h3_fl2va_pruned_int8_convrot.safetensors (~20.97GB)
CURRENT_TEXT_ENCODER=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (~15.69GB)
CURRENT_VAE=minimax_h3_video_vae_fp16.safetensors (~5.21GB)
CURRENT_FLAGS=--fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

当前 MRE 与历史 V3 存在明显漂移，所以任何新候选都不能只和数天前 V3 数字比较。正式裁决必须使用**同验证窗口、同 seed、同任务合同的当前控制组**。

---

# 1. 统一 A/B 验证模板

任何候选 M1–M4 实际执行前，GPT 必须发出这一模板的具体实例。

```text
OBJECTIVE=<candidate objective>
CURRENT_STATE=<latest remote confirmed winner>
ALLOWED_CHANGE=<exact single candidate change>
ALLOWED_FILES_OR_COMPONENTS=<explicit list>
BASELINE=CURRENT_CONTROL
WARMUP_SEED=910002
FORMAL_SEEDS=910100,910102,910103
CONTROL_RUNS=1 warmup + 3 formal
CANDIDATE_RUNS=1 warmup + 3 formal
MAX_GPU_RUNS=8
TIMING_BOUNDARY=existing authoritative CUDA Generation + POST/prompt→history+real MP4 Total
QC_GATE=existing 32x32x5 ffprobe/ffmpeg/finite/nonblack/nonflat/range/std/SHA rules
ROLLBACK=restore exact pre-candidate workflow/config/source/model selection
STOP_POINT=after candidate report + remote sync
NEXT_ACTION=RETURN_TO_GPT
```

## 1.1 漂移控制

```text
PAIR_BY_SEED=YES
CONTROL_AND_CANDIDATE_SAME_SESSION_WINDOW=YES
HISTORICAL_V3_ONLY_SANITY_ANCHOR=YES
```

候选收益以三组 paired delta 为主：

```text
DELTA_TOTAL(seed)=CONTROL_TOTAL-CANDIDATE_TOTAL
DELTA_GENERATION(seed)=CONTROL_G-CANDIDATE_G
DELTA_PATH(seed)=CONTROL_PATH-CANDIDATE_PATH
```

## 1.2 KEEP 规则

候选只有同时满足才允许进入 GPT 的 KEEP 候选：

1. `TASK_COMPLETED=PASS`；
2. 正式 QC 3/3 PASS；
3. 没有 NaN/Inf/黑帧/平坦输出；
4. targeted block 的 paired median gain > 0；
5. Total paired median gain > 0，或目标是明确为后续组合释放驻留且 Total 不出现实质回退；
6. 至少 2/3 paired seeds 方向一致；
7. 收益大于当前窗口的测量噪声，而不是单条偶然最快值；
8. 没有违反任务合同。

最终 `KEEP / ROLLBACK / INCONCLUSIVE` 由 GPT 裁决，Codex 不得自行决定下一候选。

## 1.3 INVALID / STOP

任何以下情况：

```text
CONTROL_WINDOW_UNSTABLE
TASK_CONTRACT_DRIFT
QC_FAIL
UNEXPECTED_MODEL_FORMAT
OOM_WITHOUT_PREDEFINED_FALLBACK
NAN_INF
BLACK_OR_FLAT_VIDEO
BUDGET_DRIFT
GIT_REMOTE_CHANGED_UNEXPECTEDLY
SKILL_VERSION_MISMATCH
```

=> 保存证据、恢复预定义状态、远端写回失败事实、`STOP + RETURN_TO_GPT`。

---

# 2. M1 — Star7 Native FP16 Exact / Turing

## 2.1 目的

```text
OBJECTIVE=消除/降低 Turing sm75 上 H3 BF16→FP32/manual-cast 造成的 Generation 固定成本
TARGET_BLOCK=Generation
```

## 2.2 允许变化

只允许：

- 安装/启用 `minimax-h3-fp16-exact-star7`；
- 将当前 diffusion loader 替换为 Star7 Native FP16 Loader；
- 保持当前 INT8 ConvRot checkpoint；
- 保持 sampler、scheduler、step、seed、latent、VAE、resolution、frames、attention backend 不变。

禁止同时更换 W4A8/VAE/cache，确保 M1 单独可裁决。

## 2.3 预期有界结果

不使用 V100 的11×外部比例换算本机。只接受方向性预测：

```text
EXPECTED_DIRECTION=Generation materially lower if current manual-cast path is dominant
EXPECTED_ABS_GAIN=UNVERIFIED_UNTIL_LOCAL_AB
QUALITY_EXPECTATION=no contract change; numeric output may not be bit-identical
```

## 2.4 分支

```text
M1_KEEP
→ CURRENT_WINNER=M1
→ virtual next=M2 using Star7-compatible W4A8 path

M1_ROLLBACK
→ CURRENT_WINNER=CONTROL
→ virtual next=M2 standard compatible W4A8 loader

M1_INCONCLUSIVE
→ STOP; GPT redesigns only M1 evidence plan; no M2 execution yet
```

---

# 3. M2 — W4A8 FL2VA diffusion

## 3.1 目的

```text
OBJECTIVE=缩小 diffusion 权重、降低/消除 H3↔VAE residency pressure，并测试 W4A8 compute path
TARGET_BLOCK=Generation + Path residency
```

关键虚拟拓扑：

```text
CURRENT_DIFFUSION ~20.97GB
CURRENT_FP16_VAE ~5.21GB
SUM ~26.18GB > 22.528GB VRAM

W4A8_DIFFUSION ~12.5GB
+ CURRENT_FP16_VAE ~5.21GB
SUM ~17.71GB < 22.528GB VRAM
```

这不证明 runtime 全驻留，但足以把“权重本身必然超 VRAM”变成“有可能在保留 runtime/activation 余量后减少模型切换”。

## 3.2 允许变化

只允许：

- 使用成熟 FL2VA W4A8 checkpoint；
- 使用与该格式匹配的 ComfyUI/comfy-kitchen loader；
- 若 M1 KEEP，则优先使用已证明支持 `asym_w4a8_int8` 调度的 Star7 loader 路线；
- VAE 保持当前 FP16；
- text encoder 保持当前；
- task contract 不变。

## 3.3 成功判定重点

除了统一 KEEP 规则，再观察：

```text
WEIGHT_LOAD_MODE
QUANT_BACKEND
FORCE_CAST_WEIGHTS
RESIDENCY/OFFLOAD EVENTS if already available without profiler
GENERATION_DELTA
PATH_DELTA
TOTAL_DELTA
```

禁止为了确认机制开启开放式 profiler。

## 3.4 分支

```text
M2_KEEP
→ CURRENT_WINNER=M2(or M1+M2)
→ virtual next=M3 INT8 VAE

M2_ROLLBACK
→ restore previous winner
→ virtual next=M3 may still test VAE on previous winner

M2_INCONCLUSIVE
→ STOP / GPT redesign
```

---

# 4. M3 — INT8 ConvRot Video VAE

## 4.1 目的

```text
OBJECTIVE=降低 VAE decode 成本和 VAE 权重体积，进一步减少 H3→VAE 切换压力
TARGET_BLOCK=Path / VAE / residency
```

若 M2 KEEP，虚拟组合体积约：

```text
W4A8_DIFFUSION ~12.5GB
+ INT8_VAE ~3.2GB
= ~15.7GB
NOMINAL_HEADROOM ≈ 6.8GB before runtime/activation/workspace
```

## 4.2 风险门禁

公开资料存在 RTX 2080 Ti + INT8 VAE 黑视频/NaN 报告，因此：

```text
M3_QUALITY_RISK=HIGHER_THAN_M1_M2
STRICT_FINITE_CHECK=YES
STRICT_BLACK_FLAT_CHECK=YES
IMMEDIATE_ROLLBACK_ON_ANY_QC_FAIL=YES
```

不允许因公开作者“~1.5× decode”直接 KEEP。

## 4.3 允许变化

仅替换 Video VAE 为成熟 INT8 ConvRot VAE；其他赢家配置保持不变。

## 4.4 分支

```text
M3_KEEP
→ CURRENT_WINNER=M3_COMBINED
→ virtual next=M4 applicability

M3_ROLLBACK
→ restore M2/M1/control winner
→ virtual next=M4 applicability

M3_INCONCLUSIVE
→ STOP / GPT redesign
```

---

# 5. M4 — Conditioning cache applicability

## 5.1 先做零/低成本适用性裁决

当前固定 prompt=`static frame`，正式 seed 改变不应改变 conditioning。但 ComfyUI 原生 node cache 可能已经复用 conditioning。

在不新增 GPU 性能实验前先确认现有日志/执行图：

```text
IF conditioning node is not re-executed on formal seed changes
→ M4_STATUS=ALREADY_EFFECTIVELY_HARVESTED
→ NO_M4_GPU_AB

IF Qwen3-VL is reloaded/re-encoded for each formal run
→ M4_STATUS=APPLICABLE_HIGH_VALUE
→ build M4 bounded A/B
```

## 5.2 若适用，允许变化

只允许使用成熟 exact conditioning cache（例如 MiniMaxH3 CLIPCached 或等价方案）替换 stock conditioning 重编码；不得缓存 sampler 输出、latent final result、VAE output 或 MP4。

必须保证 cache key 至少绑定 prompt/reference/encoder/config，seed 改变可以复用 conditioning。

## 5.3 分支

```text
M4_ALREADY_HARVESTED
→ MATURE_BATCH_1_COMPLETE

M4_KEEP
→ CURRENT_WINNER=M4_COMBINED
→ MATURE_BATCH_1_COMPLETE

M4_ROLLBACK / INCONCLUSIVE
→ restore previous winner
→ MATURE_BATCH_1_COMPLETE or STOP if evidence invalid
```

---

# 6. 第一批成熟收益后的虚拟再计算

M1–M4 实际裁决完成后，GPT 必须重新读取远端事实，生成：

```text
WINNER_TOTAL_P50/P95
WINNER_GENERATION_P50/P95
WINNER_PATH_P50/P95
T_PHY_TOTAL_REFERENCE=0.23–0.57 s
PHYSICAL_HEADROOM=WINNER_TOTAL_P50-0.57
```

然后把剩余现实时间按**已测量块**重建，不继续沿用旧 V7/V10/V11 占比。

## 6.1 >10% 大块规则

用户指定的“先吃绝大部分成熟收益，再处理10%以内残余”在本项目转换为：

```text
MAJOR_RESIDUAL_BLOCK=任何一个已测量现实时间块
且 BLOCK_TIME / WINNER_TOTAL_P50 >= 10%
且存在机制明确、ROI为正、可短验证的成熟/定向方案
```

若存在 `MAJOR_RESIDUAL_BLOCK=YES`：

```text
DO_NOT_FINAL_CERTIFY
→ GPT builds MATURE_BATCH_2 or TARGETED_ATTACK_BATCH
→ Codex仍只执行下一条完整铁路
```

若所有剩余可执行块均 <10% Total，或没有成熟短验证路径：

```text
ENTER_RESIDUAL_VIRTUAL_CONVERGENCE=YES
```

注意：10%只是从“大头收割”切换到“残余组合收敛”的工作分界，不是 99 的数学门槛。

---

# 7. Residual Virtual Convergence（残余虚拟收敛）

GPT 在最新赢家上重新推演：

```text
CURRENT_WINNER
→ measured residual blocks
→ remaining mature candidates
→ interactions
→ exact mechanism
→ expected reducible time interval
→ validation cost
→ quality/stability risk
→ reversibility
→ lifetime benefit
→ portfolio cost
```

优先残余攻击方向只在最新数据证明仍为大块时激活：

1. 新 W4A8/VAE 拓扑下的真实 offload/prefetch/residency；
2. M1/M2 组合后的 dtype/quant loader 边界；
3. conditioning persistence；
4. VAE/runtime 调度；
5. Python/kernel launch 固定成本；
6. attention 只有在最新测量成为显著块时才重新进入。

禁止恢复“发现一点→试一点”的自由探索。

## 7.1 组合 ROI 停止

```text
EXPECTED_LIFETIME_BENEFIT_PORTFOLIO
vs
PORTFOLIO_COST
```

若不存在同时满足以下条件的剩余组合：

```text
MECHANISM_DEFINED=YES
EXPECTED_GAIN_ABOVE_NOISE=YES
SHORT_BOUNDED_VALIDATION=YES
QUALITY_STABILITY_RISK_ACCEPTABLE=YES
EXPECTED_LIFETIME_BENEFIT > PORTFOLIO_COST
```

则：

```text
PORTFOLIO_ECONOMIC_STOP=YES
READY_FOR_FINAL_CERTIFICATION=YES
```

---

# 8. Final Certification 入口

只有 GPT 裁决进入 Final Certification 后才执行：

- 最终赢家固定配置；
- 10 条有效 warm runs；
- seed 变化、prompt/规格固定；
- authoritative Generation CUDA event + Total + Path；
- 全部真实 MP4/QC；
- cache 只能缓存固定 conditioning，不能缓存最终结果；
- Failure Index / empirical priors / final config / model identity / remote report 冻结；
- remote verify PASS。

最终：

```text
H3_P0_GENERATION_99=<GPT decision>
H3_P0_PATH_99=<GPT decision>
FINAL_99_FREEZE=<GPT decision>
```

`T_PHY_TOTAL_REFERENCE=0.23–0.57 s` 只作终极对照，不直接强迫最终赢家达到该区间。

---

# 9. 当前虚拟结论

```text
VIRTUAL_99_RAILROAD_COMPLETE=YES
MATURE_BATCH_1_DEFINED=YES
M1_STAR7_FP16_DEFINED=YES
M2_W4A8_DEFINED=YES
M3_INT8_VAE_DEFINED=YES
M4_CONDITION_CACHE_DEFINED=YES
RESIDUAL_REPLAN_RULE_DEFINED=YES
TEN_PERCENT_TRANSITION_RULE_DEFINED=YES
PORTFOLIO_ROI_STOP_DEFINED=YES
FINAL_CERTIFICATION_ENTRY_DEFINED=YES
NO_NEW_GPU_RUN=YES
RETURN_TO_GPT_FOR_FIRST_EXECUTION_COMMAND=YES
```
