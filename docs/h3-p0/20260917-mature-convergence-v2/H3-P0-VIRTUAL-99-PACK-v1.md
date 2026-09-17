# H3-P0 Virtual-99 Pack v1 — 第1部分完整入口

状态：`PHASE_1_VIRTUAL_WORK_COMPLETE=YES`

本包是在**不启动新 GPU 优化实验**的前提下，把 H3-P0 从当前真实态一直虚拟推演到 99 所能提前完成的工作全部完成。

## 1. Canonical 方法

```text
SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_VERSION=1.8.0
CANONICAL_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
```

H3 项目分支中的历史 v1.0.0 skill 快照不是当前运行规则源。

## 2. 当前固定事实

```text
TASK=T2VA / 32x32 / 5f / 1step / static frame / res_multistep / beta / real MP4
GPU=RTX 2080 Ti 22528MiB sm75
CURRENT_MRE_TOTAL_P50=54.817736 s
PROVEN_STABLE_V3_TOTAL_P50=38.042308 s
T_PHY_TOTAL_REFERENCE=0.23–0.57 s
```

## 3. 本包文件

1. `H3-P0-T-PHY-TOTAL-REFERENCE-v1.8.md`
   - 唯一正式第一性原理物理极限：`0.23–0.57 s`；
   - 历史 Generation/Path/T_MACHINE_STAR 仅作为内部/历史证据，不再并列成极限板。

2. `H3-P0-MATURE-HARVEST-MATRIX-v3.md`
   - 搜索并筛选世界成熟方案；
   - 首批优先级：Star7 FP16 Exact → W4A8 diffusion → INT8 VAE → conditional conditioning cache；
   - 明确排除已证伪/1-step 不适用/低收益路线。

3. `H3-P0-VIRTUAL-99-RAILROAD-v1.md`
   - M1–M4 完整虚拟执行顺序；
   - paired A/B、QC、KEEP/ROLLBACK/INCONCLUSIVE、失败门禁；
   - 第一批完成后的 10% 大块切换规则；
   - residual virtual convergence；
   - portfolio lifetime ROI；
   - Final Certification 入口。

4. `H3-P0-VIRTUAL-99-STATE-v1.json`
   - 机器可读当前状态；
   - 下一授权动作固定为 GPT 发布 M1 完整验证铁路；
   - Codex 不得自动进入 M2。

5. `H3-P0-M1-STAR7-VALIDATION-CONTRACT-v1.md`
   - 下一条真正可执行的第一成熟候选验证合同；
   - 只验证 M1，不允许顺带测试 W4A8/VAE/cache。

## 4. 第一批成熟大头

```text
M1 Star7 Native FP16 Exact
  目标：Turing Generation 固定成本

M2 W4A8 FL2VA diffusion
  目标：Generation + H3↔VAE residency

M3 INT8 ConvRot Video VAE
  目标：VAE decode + Path + residency

M4 exact conditioning cache (conditional)
  目标：仅当当前正式运行仍重复 Qwen3-VL conditioning 时消除该块
```

这里不是“只选一个最好方案”。不同成熟方案攻击不同物理/工程块，允许在 QC 和真实 A/B 通过后组合成最终成熟栈。

## 5. 虚拟运行逻辑

```text
CURRENT REAL STATE
→ M1 virtual + bounded A/B contract
→ GPT裁决
→ M2 virtual + bounded A/B contract
→ GPT裁决
→ M3 virtual + strict QC A/B contract
→ GPT裁决
→ M4 applicability / bounded A/B
→ GPT裁决
→ MATURE_BATCH_1_COMPLETE
→ REBUILD REAL_STATE_MODEL
```

如果最新赢家仍有某个**已测量现实大块 ≥ Total 10%**，并且存在机制明确、ROI 为正、能做短验证的方案：继续建立 Batch 2 / targeted attack。

如果大头已经吃完：进入 `RESIDUAL_VIRTUAL_CONVERGENCE`，把剩余小收益作为组合统一推演；不是交给 Codex 一点点自由试。

最终没有 ROI 为正且高于噪声、可短验证的剩余组合后，才进入 Final Certification。

## 6. 当前阶段已完成 / 未完成

```text
CANONICAL_SKILL_IDENTITY=PASS
SINGLE_T_PHY_TOTAL_REFERENCE=PASS
MRE_REAL_STATE=PASS
MATURE_SEARCH_AND_FILTER=PASS
MATURE_BATCH_1_VIRTUAL_DESIGN=PASS
FULL_CONDITIONAL_RAILROAD=PASS
RESIDUAL_REPLAN_RULE=PASS
PORTFOLIO_ROI_STOP=PASS
FINAL_CERTIFICATION_ENTRY=PASS
NEW_GPU_OPTIMIZATION_RUN=NO
M1_REAL_AB=NOT_STARTED
FINAL_99=NO
```

因此“第1部分”的虚拟设计工作已经完整到可以直接发布第一条实机验证铁路的程度。
