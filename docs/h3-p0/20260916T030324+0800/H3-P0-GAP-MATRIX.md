# H3-P0 Gap Matrix

| 信息 | 已有资料 | 当前核验状态 | 最终结论 | 是否仍缺失 | 对 H3-P0 的影响 | 来源 |
|---|---|---|---|---|---|---|
| H3 execution root | 主 Skill 指向独立 H3 根 | 目录与 launcher 已核验 | C:\AI\MiniMax-H3 | NO | 确定真实执行环境 | primary Skill；launcher |
| ComfyUI root | 主 Skill / launcher | 当前 Git 核验 | C:\AI\MiniMax-H3\ComfyUI | NO | 固定源码和 runtime | launcher；Git |
| execution entry | 历史 API 工作流 | workflow/launcher/source 已核验 | API JSON → POST /prompt → graph | NO | 可设计 T_PATH | workflow；ComfyUI server |
| workflow | K3 frozen baseline | 路径和 SHA 已核验 | k3-fl2va-5f-20step-api.json | NO | 可直接复用母版 | workflow；baseline report |
| H3 model | Skill 与 workflow | 路径/大小/mtime 已核验 | minimax_h3_fl2va_pruned_int8_convrot | PARTIAL | 文件可用；身份 SHA 后续核验 | workflow；filesystem |
| text encoder | Skill 与 workflow | 路径/大小/mtime 已核验 | qwen3vl_32b_minimax_h3_nvfp4_awq | PARTIAL | 文件可用；身份 SHA 后续核验 | workflow；filesystem |
| VAE | Skill 与 workflow | 路径/大小/mtime 已核验 | minimax_h3_video_vae_fp16 | PARTIAL | 文件可用；身份 SHA 后续核验 | workflow；filesystem |
| ComfyUI version | 旧环境记录 | CURRENT Git 核验 | v0.34.0-16-g8a33128f | NO | 固定代码语义 | Git HEAD |
| Python | 旧环境记录 | CURRENT executable 核验 | 3.11.15 | NO | 固定运行时 | H3 venv |
| PyTorch / CUDA | 旧环境记录 | CURRENT import 核验 | 2.9.1+cu130 / 13.0 | NO | 固定 GPU 栈 | H3 venv |
| NVIDIA driver | 历史记录 | CURRENT nvidia-smi | 591.74 | NO | 后续基线环境事实 | nvidia-smi |
| minimum frames | Skill 17k+5 / K3 5f | schema、validator、成功记录一致 | 5 | NO | 确认 T_GPU_CORE(5 frames) 合法 | nodes_minimax_h3.py；K3 |
| minimum resolution | 未完整记录 | CURRENT schema | 32×32 schema minimum | PARTIAL | 规格可定义；成功性未证明 | nodes_minimax_h3.py |
| minimum steps | workflow 20 | CURRENT scheduler schema | 1 schema minimum | PARTIAL | 规格可定义；1-step 成功性未证明 | BasicScheduler schema |
| input requirement | K3 图生视频 | CURRENT node schema | prompt required；images optional；audio no | PARTIAL | 空 prompt 仍不可假定 | nodes_minimax_h3.py |
| sampler / scheduler | K3 baseline | workflow 已核验 | res_multistep / beta | NO | 固定成熟母版 | workflow |
| GPU core node | 历史 node timing | workflow + source trace | node 12 SamplerCustomAdvanced | NO | 插桩主节点明确 | workflow；nodes_custom_sampler.py |
| GPU core module | 未精确 | CURRENT source trace | comfy.k_diffusion.sampling | NO | 核心实现明确 | samplers.py；sampling.py |
| GPU core function | 未精确 | CURRENT source trace | sample_res_multistep → res_multistep | NO | 可定位计算循环 | sampling.py |
| deep model function | 未精确 | CURRENT source trace | MiniMaxH3Model.forward | NO | 模型调用路径明确 | minimax/model.py |
| GPU start boundary | 无 CUDA 边界 | CURRENT source trace | before sampler_function call | NO | 可插 CUDA Event | samplers.py KSAMPLER.sample |
| GPU end boundary | 无 CUDA 边界 | CURRENT source trace | after return, before inverse scaling | NO | 可插 CUDA Event | samplers.py KSAMPLER.sample |
| GPU async risk | node wall timing | CUDA 调用语义与源码检查 | YES | NO | 必须同步避免虚假计时 | existing timer；PyTorch semantics |
| GPU sync method | generic sync elsewhere | sampler boundary 无 sync | none at boundary | NO | 需要最小插桩 | targeted source search |
| GPU timer capability | perf_counter node wall | 计时点已评估 | CUDA Events + synchronize | NO | 可可信测 T_GPU_CORE | source trace |
| PATH before GPU | workflow 历史 | node order/source trace | request 到 sampler enter | NO | T_PATH 可插桩 | workflow；execution source |
| PATH after GPU | workflow 历史 | node order/source trace | inverse/decode/save/result/QC | PARTIAL | decode 归属待 TASK_COMPLETED | workflow；execution source |
| model loading | ComfyUI 行为记录 | CURRENT source trace | prepare_sampling/load_models_gpu | NO | 冷热合同可定义 | samplers.py；model_management.py |
| model per-run load | 未明确 | cache/source 核验 | NO，按需/压力重载 | NO | 避免错误重复加载假设 | execution.py；model_management.py |
| VRAM persistence | 历史日志 | source/runtime 状态 | CONDITIONAL | PARTIAL | warm run 必须受控 | model_management.py |
| cache | TE-Speed 历史 | CURRENT defaults/source | RAM_PRESSURE；stock H3 off；TE optional | NO | 需区分 stock/TE | main.py；execution.py；TE report |
| warm/cold state | 历史耗时 | source 核验 | 行为已知，合同未冻结 | PARTIAL | 首轮运行前必须冻结 | source；reports |
| performance flags | launcher/logs | CURRENT launcher/runtime | 已形成明确清单 | NO | 环境复现输入 | launcher；8195 logs |
| current VRAM mode | 8195 NORMAL_VRAM log | 服务已停止 | live UNRESOLVED | YES | 启动后首轮需记录 | same-code log；port check |
| idle GPU state | 无当前快照 | CURRENT nvidia-smi | snapshot complete, not clean idle | PARTIAL | 运行前需定义/满足 idle gate | nvidia-smi |
| existing 5f success | K3 baseline | workflow/report 对应 | 678.907s technical pass | NO | 最小任务母版存在 | baseline snapshot |
| existing TE success | TE metrics | workflow/report 对应 | 400.248s / node12 257.781s | NO | 可选 compat 路线 | TE metrics |
| authoritative submitter | 多个 H3 scripts | 未找到 K3 一一绑定脚本 | API endpoint is authoritative; script gap | YES | 不阻断合同/插桩，首轮命令需明确 | targeted script review |
| model identity SHA | 无可信对应旧 SHA | size/mtime/path checked | NEEDS_REVERIFY | YES | 不阻断 preflight；影响长期身份锁定 | filesystem；reports |
| stock vs TE contract | 两条成熟路线 | 状态已核验 | UNRESOLVED | YES | 首轮 baseline 前必须选择 | primary Skill；TE report |

## Summary

H3_P0_LOCAL_PREFLIGHT=PASS
UNRESOLVED_FACTS_COUNT=7
STOP_CONDITION_MET=YES

六个停止条件均已具备：真实入口、最小合法任务、GPU 核心边界、PATH 边界、可信计时方法和成熟 workflow 母版均已确定。剩余项按事实保留，不通过猜测清零。
