# H3-P0 四步 99 完整包 v1

状态：`FOUR_STEP_DESIGN_COMPLETE=YES / READY_FOR_DETERMINISTIC_E0_E1_EXECUTION`

当前方法源：`first-principles-physical-limit-convergence v1.8.0`

## 四步结构

### STEP 1 — 第一性原理物理极限

文件：`H3-P0-STEP1-PHYSICAL-LIMIT-FINAL-v1.8.md`

唯一正式物理参照：

```text
T_PHY_TOTAL_REFERENCE = 0.23–0.57 s
```

这是纯物理终极参照，不是机器 benchmark，也不是直接 99 门槛。

### STEP 2 — 本机真实状态极限区间

文件：`H3-P0-STEP2-REAL-STATE-OPTIMUM-RANGE-v1.md`

基于 V1–V11、V3、MRE、V7/V10/V11 诊断和本机硬件/驻留约束，冻结当前现实工程目标带：

```text
REAL_STATE_GENERATION_OPTIMUM_RANGE = 2–5 s
REAL_STATE_PATH_OPTIMUM_RANGE       = 2–9 s
REAL_STATE_OPTIMUM_RANGE            = 4–14 s total P50
CONFIDENCE = MEDIUM_LOW
```

辅助严格证据外包络：

```text
2.07 s < T_REAL_OPTIMUM <= 38.042308 s
```

4–14 s 是 Virtual-99 的 reality-calibrated attack target；不是第二块物理极限板。

### STEP 3 — 成熟方案矩阵 + Virtual-99 综合攻击

文件：`H3-P0-STEP3-VIRTUAL-ATTACK-ITERATION-v1.md`

成熟/残余组合：

```text
A0 current cu130/INT8/ConvRot/reserve1 baseline
→ A1 Star7 Native FP16 Exact
→ A2 W4A8 FL2VA diffusion
→ A3 exact conditioning cache if applicable
→ A4 INT8 ConvRot Video VAE if strict QC passes
→ R1 new-topology H3/VAE co-residency/prefetch if residual remains major
→ R2 minimal H3 host-sync reduction if Generation residual remains major
```

Virtual 综合最终：

```text
FINAL_WIDE_PROJECTED_TOTAL    = 6–14 s
FINAL_CENTRAL_PROJECTED_TOTAL = 8–12 s
REAL_STATE_OPTIMUM_RANGE      = 4–14 s
OVERLAP = YES
```

因此 Virtual 层已经达到本轮停止点：继续添加多步 cache、attention、开放式 profiler、版本扫描等路线的预期 ROI/适用性不足。

### STEP 4 — Codex 实机确定性命令包

文件：`H3-P0-STEP4-CODEX-TEST-COMMAND-PACK-v1.md`

完整 E0–E6 铁路已经预写；但遵守 v1.8 母技能，每一个实测结果必须返回 GPT 裁决。

当前唯一解锁：

```text
E0 SAME-WINDOW CONTROL
+
E1 Star7 Native FP16 Exact paired A/B
```

E1 后无论 PASS/FAIL/INCONCLUSIVE：

```text
WRITE REPORT
→ PUSH
→ REMOTE VERIFY
→ STOP
→ RETURN TO GPT
```

E2–E6 只是在命令包中预先冻结，未获得自动执行授权。

---

## 两个核心数字

```text
1) PHYSICAL:
T_PHY_TOTAL_REFERENCE = 0.23–0.57 s

2) REAL MACHINE PLANNING:
REAL_STATE_OPTIMUM_RANGE = 4–14 s
```

后续所有实测结果同时回答两个问题：

```text
距离纯物理极限还有多远？
距离本机现实最优带还有多远？
```

99 不等于强迫达到 0.57 s，也不等于机械达到 4 s；99 仍要求高价值成熟候选裁决、残余虚拟收敛、组合 ROI 停止、10-run certification 和远端冻结。

---

## 当前状态

```text
CANONICAL_SKILL=v1.8.0
STEP1_COMPLETE=YES
STEP2_COMPLETE=YES
STEP3_COMPLETE=YES
STEP4_COMPLETE=YES
T_PHY_TOTAL_REFERENCE=0.23–0.57 s
REAL_STATE_OPTIMUM_RANGE=4–14 s
VIRTUAL_FINAL_CENTRAL=8–12 s
VIRTUAL_FINAL_WIDE=6–14 s
VIRTUAL_ATTACK_STOP=PASS
CODEX_COMMAND_PACK_REVIEWED=YES
CURRENT_EXECUTION_UNLOCK=E0+E1
NEW_GPU_RUN_FROM_GPT_PHASE=NO
FINAL_99=NO
```

`FINAL_99=NO` 的唯一原因不是虚拟设计未完成，而是 STEP 4 尚未由本机 Codex 真实执行、裁决和最终认证。

---

## 下一次恢复的最短读取顺序

1. canonical `first-principles-physical-limit-convergence v1.8.0` `SKILL.md`
2. `H3-P0-FOUR-STEP-99-PACK-v1.md`
3. `H3-P0-STEP4-CODEX-TEST-COMMAND-PACK-v1.md`
4. 最新 `H3-P0-E<n>-RESULT.md/json`（一旦产生）

不要重新扫描旧 V1–V11，除非最新结果触发明确冲突审计。
