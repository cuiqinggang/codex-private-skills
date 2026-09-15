# H3-P0 本机差量事实采集

H3_P0_LOCAL_PREFLIGHT=PASS
ORIGINAL_TASK_RECOVERY=PASS
COLLECTED_AT=2026-09-16T03:03:24+08:00
MODE=READ / INSPECT / TRACE / MAP / REPORT
RUN_H3_GENERATION=NO
RUN_H3_BENCHMARK=NO
RUN_VIDEO_GENERATION=NO

本报告接续被打断的原任务，复用已完成的 31 项既有事实与 29 项 CURRENT 核验事实。没有重新扫描 C:\AI、重新运行 H3、重新 benchmark 或重新哈希巨型模型。

## 原任务恢复

EXISTING_WORK_RECOVERED=Skill 事实、CURRENT runtime、workflow/资产、source trace、GPU 边界、cache、性能状态、历史运行证据
EXISTING_FILES_FOUND=1 intermediate Markdown
EXISTING_FACTS_RECOVERED=60
REMAINING_GAPS=7

原中间文件：C:\Users\A\h3-p0-preflight-stage\20260916T030324+0800\H3-P0-LOCAL-FACTS.md。正式文件由中间成果与已保存的命令结果整理。

## 主知识源

PRIMARY_H3_KNOWLEDGE_SKILL=h3-high-fidelity-local-video-recreation
PRIMARY_H3_KNOWLEDGE_SKILL_PATH=C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation
PRIMARY_H3_KNOWLEDGE_SKILL_VERSION=UNDECLARED_IN_SKILL_METADATA
PRIMARY_SKILL_COVERAGE=HIGH
H3_P0_REQUIRED_FACTS_FOUND_INSIDE_PRIMARY_SKILL_PERCENT=74% (17/23 full or partial)
BROAD_LOCAL_SEARCH_AVOIDED=YES
REUSE_EXISTING_H3_WORKFLOW=YES

主 Skill 明确将 C:\AI\MiniMax-H3 定义为独立 H3 根并禁止混用 Aaki。先使用其 SKILL、RECENT_USE_LOG、FAILURE_REVIEW、launcher template 和 H3-05 quality gate，再只对漂移项与缺口做定点核验。

## CURRENT_LOCAL_H3_FACTS

H3_ACTIVE_ROOT=C:\AI\MiniMax-H3
COMFYUI_ROOT=C:\AI\MiniMax-H3\ComfyUI
H3_EXECUTION_ENTRY=ComfyUI API workflow JSON -> POST /prompt -> server execution graph
WORKFLOW_PATH=C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json
WORKFLOW_SHA256=89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5

H3_MODEL=C:\AI\MiniMax-H3\ComfyUI\models\diffusion_models\minimax_h3_fl2va_pruned_int8_convrot.safetensors
TEXT_ENCODER=C:\AI\MiniMax-H3\ComfyUI\models\text_encoders\qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VAE=C:\AI\MiniMax-H3\ComfyUI\models\vae\minimax_h3_video_vae_fp16.safetensors

COMFYUI_VERSION=v0.34.0-16-g8a33128f
COMFYUI_GIT_HEAD=8a33128f2f8c5585c57486c07de481241e70a39c
PYTHON_VERSION=3.11.15
TORCH_VERSION=2.9.1+cu130
CUDA_RUNTIME=13.0
NVIDIA_DRIVER=591.74

正式 8194 launcher 是 C:\Users\A\Desktop\Start-MiniMax-H3-8194-Manual.cmd，使用 C:\AI\MiniMax-H3\.venv\Scripts\python.exe 和 ComfyUI\main.py，参数包含 --fast-disk、--reserve-vram 3.5、--disable-pinned-memory。核验时 8194/8195 均未监听；CURRENT 指磁盘正式入口和 runtime。

## 资产身份

H3_MODEL_NAME=minimax_h3_fl2va_pruned_int8_convrot.safetensors
H3_MODEL_SIZE=20970379616
TEXT_ENCODER_NAME=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
TEXT_ENCODER_SIZE=15687142551
VAE_NAME=minimax_h3_video_vae_fp16.safetensors
VAE_SIZE=5207808496
MODEL_IDENTITY_NEEDS_REVERIFY=YES

没有找到能可靠绑定当前三大文件的旧 SHA；遵守 PRE-FLIGHT 约束，未全量哈希 20GB 级模型。

## 最小合法任务

证据优先来自当前 C:\AI\MiniMax-H3\ComfyUI\comfy_extras\nodes_minimax_h3.py 与当前 workflow。

MIN_LEGAL_WIDTH=32
MIN_LEGAL_HEIGHT=32
MIN_LEGAL_FRAME_COUNT=5
MIN_LEGAL_STEPS=1
MIN_LEGAL_INPUT_TYPE=text prompt + optional first/last image
PROMPT_REQUIRED=YES
IMAGE_REQUIRED=NO at node schema; YES for proven K3 FL2VA template
AUDIO_REQUIRED=NO
MINIMUM_REQUIRED_MODELS=FL2VA diffusion + MiniMax text encoder + H3 video VAE
SAMPLER=res_multistep
SCHEDULER=beta
OTHER_HARD_CONSTRAINTS=width/height step 32; length min 5, step 17; internal grid 17k+5
FIVE_FRAME_ASSUMPTION=CONFIRMED

32×32 与 1 step 是 schema 下限，不等于已有成功运行证据。5 帧由 schema、align_frame_count/temporal_shape 源码和成熟 K3 成功记录共同证明。

## H3_ACTUAL_CALL_CHAIN

POST /prompt
→ queue / validation / graph execution
→ node 3 VAELoader
→ node 5 LoadImage
→ node 2 CLIPLoader
→ node 7 MiniMaxH3ImageToVideo
→ node 1 UNETLoader
→ optional node 19 TESpeedMiniMaxH3
→ node 11 BasicScheduler
→ node 10 KSamplerSelect
→ node 9 BasicGuider
→ node 8 RandomNoise
→ node 12 SamplerCustomAdvanced
→ SamplerCustomAdvanced.execute
→ CFGGuider.sample / outer_sample
→ prepare_sampling / load_models_gpu
→ KSAMPLER.sample
→ sample_res_multistep → res_multistep
→ per-step model → MiniMaxH3Model.forward
→ node 13 VAEDecode
→ node 15 CreateVideo
→ node 16 SaveVideo
→ result / history

GPU_CORE_NODE=12 / SamplerCustomAdvanced
GPU_CORE_MODULE=comfy.k_diffusion.sampling
GPU_CORE_FUNCTION=sample_res_multistep -> res_multistep
GPU_CORE_SOURCE_FILE=C:\AI\MiniMax-H3\ComfyUI\comfy\k_diffusion\sampling.py
DEEP_MODEL_FUNCTION=comfy.ldm.minimax.model.MiniMaxH3Model.forward
GPU_CORE_START=C:\AI\MiniMax-H3\ComfyUI\comfy\samplers.py :: KSAMPLER.sample :: before samples = self.sampler_function(...) (~1005)
GPU_CORE_END=C:\AI\MiniMax-H3\ComfyUI\comfy\samplers.py :: KSAMPLER.sample :: after sampler_function returns, before inverse_noise_scaling (~1006)
BOUNDARY_CONFIDENCE=HIGH

该边界排除 prepare/load，覆盖 res_multistep latent denoising，在 decode/save 前结束。

## GPU 异步计时

GPU_ASYNC_RISK=YES
EXISTING_GPU_SYNC_METHOD=no H3 sampler-boundary synchronization
EXISTING_GPU_TIMER_METHOD=WebSocket node-transition wall clock via time.perf_counter
BEST_AVAILABLE_GPU_TIMER=torch.cuda.Event around sampler_function, followed by end_event.synchronize; retain wall-clock transition as cross-check

现有 257.781 秒是 node 12→13 wall time，不应冒充 CUDA Event 核心时间。本轮未插桩。

## PATH 边界

PATH_BEFORE_GPU=request construction; POST/ack; queue; validation; graph/cache; loaders; image load/resize; tokenize and CLIP conditioning; keyframe VAE encode; AV latent; optional TE patch; scheduler/sampler/guider/noise; prepare_sampling; model load/offload and transfers

PATH_AFTER_GPU=inverse noise scaling; output transfer; VAEDecode; CreateVideo; SaveVideo MP4/write/metadata; result/history; polling/fetch/copy; ffprobe/PyAV/black-frame QC; logging/evidence/UI

BOUNDARY_DECISION_REQUIRED=YES：GPU VAE decode 对最小视觉结果不可缺少。TASK_COMPLETED 若为 latent complete，decode 属 PATH_AFTER；若为有效视觉结果，应纳入或单列 T_GPU_DECODE。本轮不裁决。

## 模型加载、缓存与冷热态

MODEL_LOAD_PER_RUN=NO
MODEL_PERSISTENT_IN_VRAM=CONDITIONAL
CACHE_STATUS=RAM_PRESSURE node cache enabled; stock H3 cache OFF; TE-Speed optional on 8195
TEXT_ENCODER_CACHE=conditional node cache + CPU offload
VAE_CACHE=conditional node cache + CPU offload
FIRST_RUN_SPECIAL_COST=YES
WARM_RUN_BEHAVIOR=may reuse node results and loaded models; affected by memory pressure and input changes
COLD_RUN_BEHAVIOR=includes model load, device transfers and first initialization
MODEL_LOAD_LOCATION=CFGGuider.outer_sample -> prepare_sampling -> model_management.load_models_gpu
MODEL_UNLOAD_LOCATION=memory-pressure free_memory / soft_empty_cache; no forced unload every prompt
CACHE_INVALIDATION=input/node identity changes, pressure, graph cleanup, restart

## 当前性能机制

CURRENT_PERFORMANCE_FEATURES=--fast-disk; reserve-vram 3.5; disable-pinned-memory; PyTorch attention; H3 INT8/convrot; encoder NVFP4 AWQ emulated on Turing; model BF16/manual cast FP32; VAE FP16; CLIP FP16; async weight offload 2 streams observed; RAM_PRESSURE; stock H3 cache OFF; optional TE-Speed 8195
XFORMERS=not observed
FLASH_ATTENTION=not observed
TORCH_COMPILE=not observed
DYNAMIC_PREFETCH=not observed
VRAM_MODE=last same-code 8195 NORMAL_VRAM; live unresolved because service stopped

GPU 快照：RTX 2080 Ti；22528 MiB total、2060 MiB used、20171 MiB free；51°C；53.97 W；graphics 1050 MHz；memory 7000 MHz；250 W limit；P0；compute mode Default。无 H3 负载但不是干净 idle；未修改状态。

## 已有成功运行与母版

| RUN_ID | 规格 | 时间 | 结论 | TIMING_SCOPE |
|---|---|---:|---|---|
| K3-static-baseline | 1344×768 / 5f / 20 steps | 678.907s | technical pass | full execution wall |
| K3-TE-Speed | 1344×768 / 5f / 20 steps | 400.248s; sampler 257.781s | pass/adopted compat | execution/node wall |
| H3-05-run01 | 864×480 / 107f / 20 steps | 1743.805s | technical pass, visual rejected | full wall |
| h3v1-nocache-20260905T115217Z-36088a7c | 864×480 / 22f / 10 steps | total 180.254s; sampler 138.570s; VAE 38.420s | PASS | node wall |
| h3v1-test2-te-speed-123f64b3 | 864×480 / 22f / 10 steps | total 295.584s; sampler 166.879s | PASS but slower | node wall |
| h3off-20260903T111722Z-e652ed14 | 1344×768 / native 22f / delivered 9f | unknown | technical pass | UNKNOWN |

BEST_EXISTING_MINIMAL_TASK_CANDIDATE=C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json
WHY=minimum proven frame count, mature contract and locked workflow SHA; use controlled subtraction, not a second workflow

## LOCAL_UNKNOWN_GAPS

1. 三大模型没有可可靠绑定的旧 SHA。
2. TASK_COMPLETED 对 GPU VAE decode 的归属未裁决。
3. 首轮采用 stock 8194 还是 adopted TE-Speed 8195 未冻结。
4. 干净 idle 条件未定义；当前有 2060 MiB VRAM 占用。
5. 服务停止，live VRAM_MODE 无法核验。
6. 未找到 canonical K3 一一绑定的权威提交脚本；入口是 API JSON → POST /prompt。
7. prompt 结构必填，但空字符串合法性没有成功证据。

## 计数与就绪

REUSED_EXISTING_FACTS_COUNT=31
NEW_FACTS_COLLECTED_COUNT=29
UNRESOLVED_FACTS_COUNT=7
READY_TO_DEFINE_H3_P0_TASK_CONTRACT=YES
READY_TO_INSTRUMENT_T_PATH=YES
READY_TO_INSTRUMENT_T_GPU_CORE=YES
READY_FOR_FIRST_BASELINE_RUN=NO

首轮仍为 NO：须先冻结 TASK_COMPLETED/decode、stock/TE、cold/warm 条件并实施计时插桩。

## 治理

- 没有研究 EXTERNAL FRONTIER 或 FIRST-PRINCIPLES PHYSICAL LIMIT。
- 没有运行 H3、benchmark、视频生成、安装或环境修改。
- 没有修改冻结 CASE-001、P0 runner/adapter/certification 或 H3 workflow。
- Git 只保存四个小型事实文件。

Knowledge Brain usage：INDEX=YES；ROUTING_MAP=YES；indexes/skills-index.md=YES；OpenHuman=NO；sync=NO；health check=PASS。

CodeGraph usage：MCP=NO；CLI=NO（shim target module missing）；original/compat .codegraph=NO；status checked=YES；targeted source tracing fallback=YES；refresh=NO（no code changes）。
