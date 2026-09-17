# H3-P0 E2M — W4A8 Remote Metadata Preflight Contract v1

状态：`GPT_RAILROAD_READY / ZERO_GPU / NO_FULL_MODEL_DOWNLOAD`

方法：`first-principles-physical-limit-convergence v1.8.0`

## OBJECTIVE

在不下载完整 12.5GB W4A8 checkpoint、不启动 GPU、不修改运行环境的条件下，验证目标文件 `minimax_h3_fl2va_pruned_w4a8_mixed.safetensors` 的 safetensors header / metadata / tensor key 结构是否与本机当前 ComfyUI 0.34 + comfy-kitchen 0.2.31 + Star7 2.0.14 的 W4A8 parser/loader 静态兼容。

目标是把当前：

```text
W4A8_CANDIDATE_MATURE=NO
STATUS=COMPATIBILITY_INCONCLUSIVE
```

推进为：

```text
W4A8_MATURE_FOR_BOUNDED_AB=YES
```

或明确 `NO / INCONCLUSIVE`。

## CURRENT_STATE

```text
GPU=RTX 2080 Ti 22GB / sm75
OS=Windows 10
COMFYUI_COMMIT=8a33128f2f8c5585c57486c07de481241e70a39c
COMFY_KITCHEN_VERSION=0.2.31
TORCH=2.9.1+cu130
STAR7_VERSION=2.0.14
STAR7_COMMIT=dc8ea63b51439ffd767eead53faaed23b550c504
CURRENT_KEEP=E1 Star7 Native FP16 Exact
CURRENT_TOTAL_P50=10.562 s
```

E2P 已证明：SM75 W4A8 fast CUDA/Triton path 不满足 SM80 gate，但 eager backend 静态可达；Star7 可保留 W4A8 metadata/dispatch，但自身不提供 W4A8 kernel。

## ALLOWED_CHANGE

无本机性能或运行时改动。

只允许：

1. 读取公开远端目标文件元数据；
2. 优先使用 Hugging Face API / safetensors metadata endpoint / HTTP Range，只读取 safetensors header 所需最小字节；
3. 若需要 Range：先读取前 8 bytes 得到 header length，再只请求完整 header；禁止继续下载 tensor payload；
4. 读取本机现有 ComfyUI/comfy-kitchen/Star7 源码作静态对照；
5. 写 E2M md/json 报告。

## ALLOWED_FILES_OR_COMPONENTS

只读：

- 当前本机 ComfyUI source；
- current comfy-kitchen 0.2.31 source；
- current Star7 source；
- Hugging Face/Kijai 目标模型远端元数据；
- IvenKooLab 同卡 W4A8 公开 workflow/docs。

可写：

- 项目 `H3-P0-E2M-RESULT.md`
- 项目 `H3-P0-E2M-RESULT.json`
- 小型临时 header/metadata 文本文件（不得包含完整模型 payload）。

## HARD LIMITS

```text
GPU_RUNS_ALLOWED=0
NEW_PROMPTS_ALLOWED=0
FULL_MODEL_DOWNLOAD_ALLOWED=NO
MAX_REMOTE_MODEL_BYTES_FETCHED=64 MiB
PIP_INSTALL=NO
COMFYUI_UPDATE=NO
COMFY_KITCHEN_UPDATE=NO
STAR7_UPDATE=NO
SOURCE_MODIFICATION=NO
WORKFLOW_MODIFICATION=NO
PROXY_CHANGE=NO
SYSTEM_SETTING_CHANGE=NO
PROFILER=NO
KERNEL_TRACE=NO
```

如果 safetensors header 本身超过 64 MiB：停止并 `INCONCLUSIVE`，不得扩大预算。

## BASELINE

E2P 静态源码事实 + E1 KEEP 栈。

## REQUIRED CHECKS

### M1 Target file identity

必须确认：

```text
repo=Kijai/MiniMax-H3-experimental
filename=minimax_h3_fl2va_pruned_w4a8_mixed.safetensors
remote_size≈12.5GB
```

若平台提供 SHA/etag/xet oid，保存；不得伪造本地 SHA。

### M2 Safetensors header

获取并解析 header，至少记录：

- `__metadata__`；
- `_quantization_metadata` 或等价 quant metadata；
- comfy quant format/layout 标识；
- `weight_s_rel` / `weight_s_channel` / `weight_codebook` / correction 等相关 key 是否存在；
- 至少抽样若干 H3 linear layer 的 quantized tensor key/dtype/shape；
- 是否存在 parser 需要但文件缺失的关键 metadata/key。

只读 header，不读取 tensor payload。

### M3 Local ComfyUI parser compatibility

把实际 header 与当前源码逐项对照：

- ComfyUI `quant_ops.py` format registration；
- `ops.py` QuantizedTensor/parser；
- comfy-kitchen `AsymW4A8Int8Layout.Params` 所需字段；
- eager backend handler/dequant/linear 所需字段。

输出：

```text
LOCAL_PARSER_ACCEPTS_METADATA=YES/NO/UNKNOWN
LOCAL_EAGER_BACKEND_INPUTS_SATISFIED=YES/NO/UNKNOWN
```

### M4 Star7 static compatibility

沿 Star7 当前代码验证具体目标 metadata 是否会被：

- 识别为 quantized checkpoint；
- 保持 `force_cast_weights=false`；
- 保留 layout/quant metadata；
- 不被展开为 dense FP16；
- 不触发明确 unsupported branch。

输出：

```text
STAR7_STATIC_PARSE_COMPATIBLE=YES/NO/UNKNOWN
```

### M5 External same-card equivalence

确认 IvenKooLab workflow 指向同名/等价 Kijai W4A8 mixed FL2VA 文件，并记录已知差异：loader、ComfyUI version、unknown comfy-kitchen build。

不得把外部运行成功自动等同本机成功。

## SUCCESS_RULE

只有全部满足：

```text
TARGET_FILE_IDENTITY=PASS
HEADER_PARSED=PASS
QUANTIZATION_METADATA_PRESENT=PASS
LOCAL_PARSER_ACCEPTS_METADATA=YES
LOCAL_EAGER_BACKEND_INPUTS_SATISFIED=YES
STAR7_STATIC_PARSE_COMPATIBLE=YES
NO_EXPLICIT_SM75_REJECTION_BEFORE_EAGER_FALLBACK=YES
NO_FULL_STACK_UPGRADE_REQUIRED=YES
```

才允许：

```text
W4A8_MATURE_FOR_BOUNDED_AB=YES
NEXT_ACTION=RETURN_TO_GPT_FOR_E2W_CONTRACT
```

## FAILURE_RULE

任一明确结构冲突：

```text
W4A8_MATURE_FOR_BOUNDED_AB=NO
REASON=<exact mismatch>
STOP
```

## INCONCLUSIVE_RULE

如果远端 header 无法在 64 MiB 内获得、metadata 不可见、字段语义无法和 parser 对齐，或 Star7 代码路径仍有关键未知：

```text
W4A8_MATURE_FOR_BOUNDED_AB=NO
STATUS=METADATA_PREFLIGHT_INCONCLUSIVE
STOP
```

禁止因此下载完整模型。

## ROLLBACK

无运行时改动；删除临时 header 文件可选。不得修改模型目录。

## STOP_POINT

写：

```text
H3-P0-E2M-RESULT.md
H3-P0-E2M-RESULT.json
```

然后：

```text
commit
→ push codex/h3-p0-mature-convergence-v2
→ remote verify
→ STOP
→ RETURN TO GPT
```

## MAX_GPU_RUNS

`0`

## TIME_BUDGET

`WALL_STAGE_BUDGET <= 30 min`

## CODEX_BUDGET

`ONE_READONLY_METADATA_STAGE_ONLY`

## NEXT_ACTION_AFTER_EACH_OUTCOME

- PASS → return GPT; do not download full model automatically.
- FAIL → return GPT; W4A8 removed from current queue.
- INCONCLUSIVE → return GPT; no full download and no GPU.
