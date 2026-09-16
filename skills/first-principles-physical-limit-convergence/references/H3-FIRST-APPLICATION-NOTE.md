# H3-P0 — 首个计划验证案例（尚未执行）

H3-P0 将作为 v1.0 两步法首个正式验证案例。本文件只固定方法入口，不预填未经计算的极限数字。

优先读取 `h3-high-fidelity-local-video-recreation`、H3-P0 PRE-FLIGHT 正式报告和 shared repository 现有事实；禁止重新全盘扫描 H3 环境。

STEP 1 预期输出：

```text
H3_P0_T_PHY_PATH=[LOW,HIGH]
H3_P0_T_PHY_GPU_CORE=[LOW,HIGH]
H3_P0_T_PHY_TOTAL=[LOW,HIGH]
H3_P0_T_MACHINE_STAR_PATH=[LOW,HIGH]
H3_P0_T_MACHINE_STAR_GPU_CORE=[LOW,HIGH]
H3_P0_T_MACHINE_STAR_TOTAL=[LOW,HIGH]
ASSUMPTION_LEDGER=
ATTACK_ORDER=
AGENT_MODE=
```

H3 已有逻辑保持：`T_TOTAL = T_PATH + T_GPU_CORE`；只有 `H3_P0_PATH_99` 与 `H3_P0_GPU_CORE_99`，不建立 TOTAL_99。

STEP 2 不再要求 raw stock B0。第一份命令包应是 `H3-P0 V1 / FIRST MINIMUM VIABLE EXECUTION`：基于 STEP 1 去掉确定重甲、保持固定合同、经独立审计、单 GPU 正式运行串行、使用权威 CUDA 计时、产生 V1 时间块，再由 Gap 决定下一刀。

```text
H3_STEP1=NOT_STARTED
H3_V1_COMMAND_PACKAGE=NOT_CREATED
H3_V1_RUN=NOT_STARTED
```
