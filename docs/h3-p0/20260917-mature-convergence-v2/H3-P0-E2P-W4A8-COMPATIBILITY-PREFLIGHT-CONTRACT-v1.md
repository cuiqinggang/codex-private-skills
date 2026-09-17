# H3-P0 E2P — W4A8 compatibility preflight contract v1

状态：`GPT_RAILROAD_READY / ZERO_GPU / READ_ONLY`

方法：`first-principles-physical-limit-convergence v1.8.0`

## OBJECTIVE

在不运行任何新 GPU prompt、不下载 12.5GB 模型、不修改运行环境的前提下，确认当前本机 Windows + RTX 2080 Ti sm75 + ComfyUI/comfy-kitchen/Star7 组合是否存在**成熟、可执行、可验证**的 W4A8 diffusion 路径。

## CURRENT_STATE

```text
E1=KEEP
CURRENT_WINNER=Star7 Native FP16 Exact + current int8_convrot diffusion
CURRENT_TOTAL_P50=10.562 s
CURRENT_TOTAL_P95=14.510 s
E2R_ATTRIBUTION=INCONCLUSIVE
GPU=RTX 2080 Ti 22GB sm75
OS=Windows 10
```

外部同卡事实：IvenKooLab/minimax-h3-turing 在 2080Ti 22G/sm75 上真实使用 W4A8 mixed diffusion + standard UNETLoader。

冲突事实：当前上游 comfy-kitchen 的 `AsymW4A8Int8Layout` 声明 `MIN_SM_VERSION=(8,0)`。

## ALLOWED_CHANGE

无。

```text
READ_ONLY=YES
GPU_RUNS_ALLOWED=0
MODEL_DOWNLOAD_ALLOWED=NO
PIP_INSTALL_ALLOWED=NO
GIT_CHECKOUT_CHANGE_ALLOWED=NO
SOURCE_EDIT_ALLOWED=NO
WORKFLOW_EDIT_ALLOWED=NO
PROXY_CHANGE_ALLOWED=NO
```

## ALLOWED_FILES_OR_COMPONENTS

只读：

- 本机当前 ComfyUI / Python 环境版本；
- 本机 `comfy_kitchen` 已安装源码/metadata；
- 本机 Star7 当前源码与日志能力；
- 本机模型目录中文件名/大小（禁止读取几十GB内容做无必要哈希）；
- GitHub/HuggingFace 已知公开源码/文档，只用于版本/机制核对；
- E1/E2R 已有报告与日志。

## BASELINE

当前 E1 KEEP 运行环境，不做任何修改。

## REQUIRED_CHECKS

### C1 — 本机 comfy-kitchen 身份

记录：

```text
COMFY_KITCHEN_VERSION
COMFY_KITCHEN_PACKAGE_PATH
BUILD/COMMIT if locally identifiable
TORCH_VERSION
CUDA_RUNTIME
COMFYUI_COMMIT
STAR7_VERSION/COMMIT
```

### C2 — 本机 W4A8 layout gate

在本机已安装源码中定位 W4A8 layout/dispatch，记录：

```text
ASYM_W4A8_LAYOUT_PRESENT
MIN_SM_VERSION
SM75_BEHAVIOR
```

必须基于源码给出 `SM75_BEHAVIOR`：

- `REJECTED`
- `FALLBACK_SUPPORTED`
- `OTHER_LAYOUT_SUPPORTED`
- `UNKNOWN`

不得凭外部文档猜测。

### C3 — Star7 与 W4A8 的关系

确认当前 Star7 是否只“保留量化调度”，还是自身提供 W4A8 sm75 kernel/fallback。

必须输出：

```text
STAR7_PROVIDES_W4A8_KERNEL=YES/NO/UNKNOWN
STAR7_CAN_PRESERVE_W4A8_METADATA=YES/NO
STAR7_ALONE_MAKES_SM75_W4A8_EXECUTABLE=YES/NO/UNKNOWN
```

### C4 — 同卡成熟项目等价性

对 `IvenKooLab/minimax-h3-turing` 的实测 W4A8 路线做版本/路径对照：

```text
SAME_GPU=YES
SAME_OS=UNKNOWN/YES/NO
SAME_COMFY_KITCHEN_VERSION=YES/NO/UNKNOWN
SAME_W4A8_MODEL_FORMAT=YES/NO/UNKNOWN
SAME_LOADER_PATH=YES/NO/UNKNOWN
```

重点不是复制其大任务性能，而是判断其 sm75 可运行机制是否能在本机当前环境复用。

### C5 — 候选模型存在性

只列目录，不下载：

```text
LOCAL_W4A8_FILE_PRESENT=YES/NO
EXPECTED_FILENAME=minimax_h3_fl2va_pruned_w4a8_mixed.safetensors
EXPECTED_REMOTE_BYTES=12540858008
EXPECTED_REMOTE_SHA256=01aa7b92c007c599890461c325f9b7e3c96fb06c36f242f95b62f7f20e538dec
```

如果本地已有同名文件，可记录大小；除非已有缓存哈希，不为本轮重新读取 12.5GB 生成 SHA。

## SUCCESS_RULE

只有全部满足才可判 `W4A8_CANDIDATE_MATURE=YES`：

1. 本机当前 sm75 路径有明确可执行机制，不是仅外部他机理论；
2. 该机制与 Kijai W4A8 mixed 模型格式兼容；
3. Star7 与该量化路径不存在已知冲突；
4. 不要求升级/替换整个 ComfyUI 栈才能运行；
5. 能定义单一变量的 paired A/B：
   `current int8_convrot diffusion → W4A8 mixed diffusion`，其余 E1 KEEP 栈固定。

## FAILURE_RULE

任一成立：

```text
LOCAL_SM75_W4A8_PATH_REJECTED=YES
OR requires unsupported full-stack change
OR model format incompatible
OR Star7/current runtime conflict proven
```

则：

```text
W4A8_CANDIDATE_MATURE=NO
STATUS=NOT_APPLICABLE_CURRENT_RUNTIME
```

## INCONCLUSIVE_RULE

如果本地源码与同卡公开结果仍无法闭合机制：

```text
W4A8_CANDIDATE_MATURE=NO
STATUS=COMPATIBILITY_INCONCLUSIVE
```

不得通过 GPU smoke test“试试看”来替代缺失的成熟机制证明。

## STOP_POINT

生成：

```text
H3-P0-E2P-RESULT.md
H3-P0-E2P-RESULT.json
```

包含 C1–C5、SUCCESS/FAIL/INCONCLUSIVE、所有来源、文件/源码位置。

随后：

```text
commit
→ push
→ remote verify
→ STOP
→ RETURN TO GPT
```

不得自动下载 W4A8，不得自动进入 GPU A/B。

## MAX_GPU_RUNS

`0`

## TIME_BUDGET

只读预检；禁止扩展为开放式源码探索。若当前安装源码无法明确回答，直接 `INCONCLUSIVE`。

## CODEX_BUDGET

`ONE_READ_ONLY_STAGE_ONLY`

## NEXT_ACTION_AFTER_EACH_OUTCOME

- `MATURE=YES` → 返回 GPT，由 GPT 生成 W4A8 paired A/B 完整合同；
- `NOT_APPLICABLE` → 返回 GPT，W4A8 退出当前候选；
- `INCONCLUSIVE` → 返回 GPT，不运行 GPU 猜测。
