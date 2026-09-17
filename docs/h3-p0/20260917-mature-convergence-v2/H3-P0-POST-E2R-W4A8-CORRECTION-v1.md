# H3-P0 Post-E2R W4A8 applicability correction v1

状态：`W4A8_STATUS=COMPATIBILITY_PREFLIGHT_REQUIRED / GPU_TEST_NOT_YET_UNLOCKED`

方法：`first-principles-physical-limit-convergence v1.8.0`

## 1. E2R 结论保持

E2R 已远端确认：`ATTRIBUTION_INCONCLUSIVE=YES`、`GPU_RUNS_EXECUTED=0`。因此现有 E1 日志不足以把慢尾唯一归因到 residency、Qwen conditioning、VAE 或 host-sync。

## 2. 修正前一轮 W4A8 一刀切判断

前一轮把 W4A8 直接标记成 `UNSUPPORTED_ON_CURRENT_HW` 过度简化，现予以撤销。

新增一手/同卡证据：

- `IvenKooLab/minimax-h3-turing` 明确声明其手册与生产数据来自 RTX 2080 Ti 22G / Turing sm_75；
- 其主生产路线使用 `minimax_h3_fl2va_pruned_w4a8_mixed.safetensors`，标准 `UNETLoader`；
- 其文档明确把 W4A8 视为该卡的可用量化路线，并给出真实渲染数据；
- Kijai 当前公开模型文件仍存在，大小 12,540,858,008 bytes，SHA256=`01aa7b92c007c599890461c325f9b7e3c96fb06c36f242f95b62f7f20e538dec`。

同时存在冲突证据：

- 当前 `Comfy-Org/comfy-kitchen` W4A8 实现中的 `AsymW4A8Int8Layout.MIN_SM_VERSION=(8,0)`；
- Star7 只承诺保留 `asym_w4a8_int8` 等原生量化调度，并明确说明最终端到端能力仍取决于相应环境。

因此当前状态必须改成：

```text
A2_W4A8_CURRENT_STATUS=COMPATIBILITY_PREFLIGHT_REQUIRED
OLD_BLOCKED_JUDGMENT=REVOKED
GPU_AB_TEST_UNLOCKED=NO
```

## 3. 为什么先做本机只读预检

同卡外部 W4A8 已证明“存在可行路径”，但不能证明当前本机安装的 comfy-kitchen/ComfyUI/Star7 组合会走同一条路径。

必须先确认：

1. 当前本机 `comfy-kitchen` 精确版本与 commit/build；
2. 本机实际 `AsymW4A8Int8Layout.MIN_SM_VERSION`；
3. 对 sm75 时 W4A8 metadata 会：
   - 被拒绝；
   - fallback 到 eager/dequant/int8 path；
   - 走其他 MixedPrecisionOps layout；
   - 或可被 Star7 正确保留；
4. 同卡项目使用的版本/路径是否与本机等价；
5. W4A8 模型当前是否已在本机；若不存在，本轮预检不得下载 12.5GB 文件。

## 4. 当前 Virtual-99 状态

```text
E1=KEEP
CURRENT_TOTAL_P50=10.562 s
CURRENT_TOTAL_P95=14.510 s
CURRENT_FAST_VALID=6.484 s
E2R_ATTRIBUTION=INCONCLUSIVE
W4A8=COMPATIBILITY_PREFLIGHT_REQUIRED
INT8_VAE=DEFER_HIGH_RISK
HOST_SYNC=NOT_MATURE_WITHOUT_ATTRIBUTION
NEXT_ACTION=E2P_W4A8_COMPATIBILITY_PREFLIGHT
GPU_RUNS_NEXT=0
```

只有 E2P 明确证明当前本机存在成熟 sm75 可执行 W4A8 路径，GPT 才允许生成新的 W4A8 paired A/B 命令包。
