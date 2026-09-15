# H3-P0 Source Map

| FACT | SOURCE | SOURCE_TYPE | CURRENT_VERIFIED | REUSABLE |
|---|---|---|---|---|
| H3 独立根与 Aaki 隔离 | C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\SKILL.md | PRIMARY_SKILL | YES | YES |
| 正式 8194 launcher | C:\Users\A\Desktop\Start-MiniMax-H3-8194-Manual.cmd | LAUNCHER | YES | YES |
| compat 8195 launcher | C:\AI\MiniMax-H3\compat-lab\Start-MiniMax-H3-Compat-Lab-8195-Manual.cmd | LAUNCHER | YES | YES |
| H3 Python runtime | C:\AI\MiniMax-H3\.venv\Scripts\python.exe | RUNTIME | YES | YES |
| ComfyUI version / HEAD | C:\AI\MiniMax-H3\ComfyUI\.git | GIT_STATE | YES | YES |
| Python / Torch / CUDA | H3 venv import output | RUNTIME_PROBE | YES | YES |
| NVIDIA driver / idle snapshot | nvidia-smi query | HARDWARE_PROBE | YES | YES |
| K3 canonical workflow | C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json | WORKFLOW | YES | YES |
| K3 workflow SHA | same workflow | SHA256 | YES | YES |
| TE-Speed workflow | C:\AI\MiniMax-H3\compat-lab\workflows\k3-fl2va-5f-20step-te-speed.json | WORKFLOW | YES | YES |
| H3 model path/name | canonical K3 workflow + filesystem | WORKFLOW / FILESYSTEM | YES | YES |
| text encoder path/name | canonical K3 workflow + filesystem | WORKFLOW / FILESYSTEM | YES | YES |
| VAE path/name | canonical K3 workflow + filesystem | WORKFLOW / FILESYSTEM | YES | YES |
| model identity SHA gap | existing reports + current size/mtime | EVIDENCE_AUDIT | YES | YES |
| minimum width/height | C:\AI\MiniMax-H3\ComfyUI\comfy_extras\nodes_minimax_h3.py | CURRENT_SOURCE | YES | YES |
| minimum frames and 17k+5 | nodes_minimax_h3.py align_frame_count / temporal_shape | CURRENT_SOURCE | YES | YES |
| minimum steps | current BasicScheduler schema audit | CURRENT_SOURCE | YES | YES |
| prompt/image/audio requirements | nodes_minimax_h3.py node schema | CURRENT_SOURCE | YES | YES |
| mature sampler/scheduler | canonical K3 workflow | WORKFLOW | YES | YES |
| workflow node order | canonical and TE-Speed API JSON | WORKFLOW_TRACE | YES | YES |
| GPU core node | node 12 SamplerCustomAdvanced | WORKFLOW_TRACE | YES | YES |
| SamplerCustomAdvanced entry | C:\AI\MiniMax-H3\ComfyUI\comfy_extras\nodes_custom_sampler.py | CURRENT_SOURCE | YES | YES |
| CFGGuider / model preparation | C:\AI\MiniMax-H3\ComfyUI\comfy\samplers.py | CURRENT_SOURCE | YES | YES |
| actual res_multistep loop | C:\AI\MiniMax-H3\ComfyUI\comfy\k_diffusion\sampling.py | CURRENT_SOURCE | YES | YES |
| deep H3 forward | C:\AI\MiniMax-H3\ComfyUI\comfy\ldm\minimax\model.py | CURRENT_SOURCE | YES | YES |
| GPU start/end candidate | samplers.py KSAMPLER.sample around sampler_function | SOURCE_TRACE | YES | YES |
| existing node wall timer | C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\10-OPTIMIZATION\te-speed-metrics.json and runner history | EXISTING_EVIDENCE | YES | YES |
| GPU async risk / CUDA Event candidate | current call chain + existing sync search | SOURCE_TRACE | YES | YES |
| PATH before/after | workflow node order + ComfyUI execution source | SOURCE_TRACE | YES | YES |
| model load location | samplers.py prepare_sampling + model_management.load_models_gpu | CURRENT_SOURCE | YES | YES |
| default cache mode | ComfyUI main.py / execution.py | CURRENT_SOURCE | YES | YES |
| unload/pressure behavior | ComfyUI model_management.py / execution.py | CURRENT_SOURCE | YES | YES |
| K3 baseline 678.907s | C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\10-OPTIMIZATION\00-BASELINE-SNAPSHOT.md | EXISTING_REPORT | NO | YES |
| TE-Speed 400.248 / 257.781s | C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\10-OPTIMIZATION\te-speed-metrics.json | EXISTING_EVIDENCE | NO | YES |
| H3-05 run01 107f | primary Skill / H3-05 report | EXISTING_REPORT | NO | YES |
| V1 22f no-cache run | existing H3 V1 metrics | EXISTING_EVIDENCE | NO | YES |
| 9f delivered from native 22f | primary Skill + h3-open-film-factory record | EXISTING_EVIDENCE | NO | YES |
| primary Skill recent history | RECENT_USE_LOG.md | SKILL_REFERENCE | NO | YES |
| historical failures | FAILURE_REVIEW.md | SKILL_REFERENCE | NO | YES |
| launcher constraints | references\H3-MANUAL-LAUNCHER-TEMPLATE.md | SKILL_REFERENCE | PARTIAL | YES |
| H3-05 quality contract | references\H3-05-QUALITY-GATE-SOP.md | SKILL_REFERENCE | NO | YES |
| Knowledge Brain routing | C:\Users\A\.codex\knowledge-brain\INDEX.md; ROUTING_MAP.md; indexes\skills-index.md | INDEX | YES | YES |

## Source interpretation

- CURRENT_VERIFIED=YES：本轮通过当前文件、runtime、Git 或只读系统状态核验。
- CURRENT_VERIFIED=NO：该事实是不可重复运行的历史结果，本轮按可信既有 evidence 引用。
- CURRENT_VERIFIED=PARTIAL：当前入口仍存在，但部分内容是历史运行态。
- REUSABLE=YES：后续 H3-P0 可以直接从此表定位，禁止再次从全盘搜索开始。

PRIMARY_SKILL_COVERAGE=HIGH
BROAD_LOCAL_SEARCH_AVOIDED=YES
SOURCE_MAP_COMPLETE=PASS
