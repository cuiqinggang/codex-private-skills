# H3-P0 E2P — W4A8 compatibility preflight result

方法：first-principles-physical-limit-convergence v1.8.0
合同：H3-P0-E2P-W4A8-COMPATIBILITY-PREFLIGHT-CONTRACT-v1
基线：远端分支 codex/h3-p0-mature-convergence-v2，检查前 HEAD 13f4ab3d869bac6a3f88e160ba31201b2e1571d7。
边界：READ_ONLY=YES；GPU_RUNS_ALLOWED=0；GPU_RUNS_EXECUTED=0。

## 判定

SM75_BEHAVIOR=FALLBACK_SUPPORTED
W4A8_CANDIDATE_MATURE=NO
STATUS=COMPATIBILITY_INCONCLUSIVE
NEXT_ACTION=STOP_RETURN_TO_GPT

本机源码证明 W4A8 元数据可由 ComfyUI 识别，SM75 的 W4A8 linear 会跳过要求 SM80 的 CUDA/Triton 实现，并由 registry 选择 eager 实现。MIN_SM_VERSION=(8,0) 是快速矩阵乘法门槛，不代表量化格式整体被拒绝。该结论仅来自静态源码检查；本轮没有执行 W4A8、GPU 调用或 kernel 验证。候选文件本机缺失；外部同卡项目的 comfy-kitchen 精确版本未知；其标准 UNETLoader 与本机 Star7 KEEP loader 不同，故五项成熟条件无法全部证明。也无证据证明当前运行栈必然不适用。

## C1 — 当前本机身份

| 项目 | 回读值 |
| --- | --- |
| COMFY_KITCHEN_VERSION | 0.2.31 |
| COMFY_KITCHEN_PACKAGE_PATH | C:\AI\MiniMax-H3\.venv\Lib\site-packages\comfy_kitchen |
| installed build/commit | UNKNOWN；dist-info 无 direct_url.json |
| TORCH_VERSION | 2.9.1+cu130 |
| CUDA_RUNTIME | Torch build CUDA 13.0；未执行 torch.cuda 探针 |
| COMFYUI_COMMIT | 8a33128f2f8c5585c57486c07de481241e70a39c |
| STAR7_VERSION | NODE_VERSION=2.0.14 |
| STAR7_COMMIT | dc8ea63b51439ffd767eead53faaed23b550c504 |
| GPU/OS | 既有 E1/E2R 与合同：RTX 2080 Ti 22GB、sm75、Windows 10 |

来源：本机 comfy_kitchen-0.2.31.dist-info/METADATA；torch/version.py；两个仓库的 git rev-parse HEAD；Star7 nodes.py:21。只读回读，未修改环境。

## C2 — W4A8 layout 与真实源码分派

ASYM_W4A8_LAYOUT_PRESENT=YES
MIN_SM_VERSION=(8,0)
SM75_BEHAVIOR=FALLBACK_SUPPORTED
CUDA_W4A8_LINEAR_ON_SM75=NOT_SELECTED_BY_CONSTRAINT
TRITON_W4A8_LINEAR_ON_SM75=NOT_SELECTED_BY_CONSTRAINT
EAGER_W4A8_LINEAR_ON_SM75=SOURCE_REACHABLE
SM75_W4A8_END_TO_END_EXECUTED=NO

源码链：

1. ComfyUI/comfy/quant_ops.py:276-280 注册 asym_w4a8_int8 → AsymW4A8Int8Layout，quantize_input=False。ComfyUI/comfy/ops.py:1142-1229 读取 comfy_quant、weight_s_rel、weight_s_channel、可选 weight_codebook 并构造 QuantizedTensor。ops.py:1651-1667 仅按硬件禁用 NVFP4/MXFP8/FP8，没有禁用 W4A8。
2. comfy_kitchen/tensor/w4a8_int8.py:122-126 声明 MIN_SM_VERSION=(8,0)。tensor/base.py:125-132 把它用于 supports_fast_matmul。ComfyUI MoE expert 路径 ops.py:1529-1539 在此门槛不满足时通过 qw.dequantize() 和普通矩阵乘法回退。
3. 普通 Linear 路径 ComfyUI/comfy/ops.py:1360-1419 保留 weight-only quantized 分支。comfy_kitchen/tensor/w4a8_int8.py:322-333 的 handler 调用 :93-119 的 w4a8_int8_linear，后者由 registry 选 backend。
4. comfy_kitchen/backends/cuda/__init__.py:3359-3395 和 backends/triton/__init__.py:252-267 对 W4A8 linear 均设 min_compute_capability=(8,0)。backends/eager/__init__.py:400-414 允许 CUDA device 且无 SM 下限。registry.py:217-270 跳过不满足约束的 backend，选择下一可用实现。backends/eager/w4a8_int8.py:509-560 实现 INT4→INT8 解码加 int8 linear；存在 correction 时解量化再做普通 linear。CUDA dequant 同样要求 SM80（cuda/__init__.py:3328-3357），eager dequant 没有该下限（eager/__init__.py:387-399）。

CUDA 实现内部 cuda/__init__.py:2251-2273 另有 if not used 后退到 eager 的分支；SM75 首先被 registry 的 SM80 约束排除，不应将该内部回退写成 SM75 CUDA 快速路径。源码可达不等于目标模型端到端已验证，性能与实际资源占用 UNKNOWN。

## C3 — Star7 的作用

STAR7_PROVIDES_W4A8_KERNEL=NO
STAR7_CAN_PRESERVE_W4A8_METADATA=YES
STAR7_ALONE_MAKES_SM75_W4A8_EXECUTABLE=NO
STAR7_W4A8_END_TO_END_COMPATIBILITY=UNKNOWN

Star7 nodes.py:246-260 检查模块 quant_format/layout_type；:298-305 对量化模型设置 force_cast_weights=False；:387-427 调 ComfyUI 的 quant conversion、pick_operations 与 load_diffusion_model_state_dict。插件源码未注册 W4A8 kernel 或 backend。README.md:84 仅承诺保留 asym_w4a8_int8 原生量化调度，要求目标环境端到端验证。既有 E1 KEEP 只验证 INT8/ConvRot；没有已证明的 Star7+W4A8 冲突，也没有已证明的兼容。

## C4 — IvenKooLab 同卡路线等价性

| 比较项 | 判定 | 根据 |
| --- | --- | --- |
| SAME_GPU | YES | 项目 README 写明 2080 Ti 22G、sm75。 |
| SAME_OS | UNKNOWN | 所读一手资料未列可核对的 OS 版本。 |
| SAME_COMFY_KITCHEN_VERSION | UNKNOWN | 硬件说明提到 Torch 2.9.1+cu130，但未给出 comfy-kitchen 精确版本/commit；其 ComfyUI baseline 为 v0.33.1，不能等同本机 commit。 |
| SAME_W4A8_MODEL_FORMAT | UNKNOWN | 项目把同名 Kijai 模型列为 Route B，但本机无文件，无法核对实际 comfy_quant header、逐层 tensor keys 和当前 parser。 |
| SAME_LOADER_PATH | NO | 外部 API workflow 使用 class_type=UNETLoader；本机 KEEP 路线使用 Star7 Native FP16 Exact loader。两者有共用的 ComfyUI 底层加载函数，但入口及 Star7 patch 不同。 |

一手来源：
- https://github.com/IvenKooLab/minimax-h3-turing
- https://github.com/IvenKooLab/minimax-h3-turing/blob/main/docs/en/01-hardware-limits.md
- https://github.com/IvenKooLab/minimax-h3-turing/blob/main/docs/en/05-workflows.md
- https://raw.githubusercontent.com/IvenKooLab/minimax-h3-turing/main/workflows/h3_w4a8_t2v_compat_api.json

该项目的同卡实测证明存在一条可行 W4A8 路线，不证明当前本机版本、backend 分派和 Star7 KEEP 栈与之等价。其“cu130 CUDA dequant”解释与本机 0.2.31 源码中 W4A8 CUDA min_compute_capability=(8,0) 的差异原因 UNKNOWN。

## C5 — 候选文件

LOCAL_W4A8_FILE_PRESENT=NO
LOCAL_W4A8_FILE_SIZE=NOT_APPLICABLE
EXPECTED_FILENAME=minimax_h3_fl2va_pruned_w4a8_mixed.safetensors
EXPECTED_REMOTE_BYTES=12540858008
EXPECTED_REMOTE_SHA256=01aa7b92c007c599890461c325f9b7e3c96fb06c36f242f95b62f7f20e538dec

仅对 C:\AI\MiniMax-H3\ComfyUI\models\diffusion_models 做精确文件名目录查询。远端大小与 SHA 来自冻结合同；未下载、读取大文件或重新计算哈希。

## 五项成熟条件与停止

1. 当前 SM75 有源码可达的 eager 机制：YES_STATIC_SOURCE_PATH；端到端执行未验证。
2. 与 Kijai mixed 模型格式兼容：UNKNOWN。
3. 与当前 Star7 KEEP 栈无已证明冲突：NO_PROVEN_CONFLICT；端到端兼容 UNKNOWN。
4. 不需整体升级软件栈：SOURCE_PATH_PRESENT；目标模型运行结果 UNKNOWN。
5. 未来仅换 diffusion checkpoint 做 paired A/B：CONCEPTUALLY_DEFINED；候选文件缺失，loader/metadata 未验证。

故 W4A8_CANDIDATE_MATURE=NO，STATUS=COMPATIBILITY_INCONCLUSIVE；没有触发 NOT_APPLICABLE_CURRENT_RUNTIME 失败规则。保留 E1 KEEP。没有新 prompt、GPU benchmark、profiler、kernel trace、模型下载、包安装、源码/workflow/代理/系统设置修改。STOP → RETURN TO GPT；不得自动进入 GPU A/B。

CodeGraph usage：ComfyUI 和 Star7 仓库根均无 .codegraph；按 AGENTS.md 用定向 rg 与源码行读取；没有代码改动，无需刷新。Knowledge Brain usage：项目连续性预检沿用已回读的 INDEX、ROUTING_MAP 和相关 category index；本轮未改 KB，不做 sync。
