# 《三人行》V2｜MiniMax H3 三套**纯本地**成熟流程与Reality回执（2026-10-13）

TASK_ID=H3-LOCAL-COMMERCIAL-20261013
SCOPE=WINDOWS_LOCAL_ONLY
STATUS=H3_A_REALITY_RUNNING_NOT_COMPLETE
METHOD_PROMOTION=NO
FINAL_VALID=NO
CLOUD_H3_GENERATION=EXCLUDED
OLD_V2_FROZEN_UNMODIFIED=YES

## 用户范围修正
2026-10-13 用户明确要求：MiniMax H3 必须使用 Windows 本机 GPU 生成，不把在线抽卡、官方托管API、OpenArt等云端路线计入A/B/C。显卡消耗允许但不能降低画质标准。先选择成熟现成流程，不从零发明图/视频后端；沿《三人行》V2 先复用实证、比较三路、Freeze后现实验收。旧的云端优先 V3 路由因用户本次约束在该节点不适用；不删除历史证据。

## 三条不同的本地成熟视频生产路线
### A｜原生H3 FL2VA / I2V（当前本机Reality）
成熟来源：ComfyUI官方Native Workflows（https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native）；ComfyUI官方H3概览（https://docs.comfy.org/tutorials/video/minimax/minimax-h3）；行业用户实测讲解 https://www.reddit.com/r/comfyui/comments/1vflhue/minimax_h3_imagetovideo_on_a_4070_ti_super/ 。
输入：一张已许可商业级源图+动作、运镜、音景提示；可选独立合格尾帧。模型：minimax_h3_fl2va_pruned_int8_convrot.safetensors、qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors、视频和音频VAE。官方20步质量基线优先，不默认将8步Turbo画质视为等价。H3在模型推理时生成连续视频及原生音频，不逐张调用imagegen。验收重点：完整时序/单镜头动作因果/道具恒定/手指/音画同步。
风险：始尾良好不保证中段动作稳定；旧历史107帧技术通过但视觉品质曾失败，不得以本次任务已排队代替作品验收。

### B｜原生H3 Ref2VA + Multiframe Reference（多参考和时间锚）
成熟来源：https://docs.comfy.org/tutorials/video/minimax/minimax-h3-multiframe 及 https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native ；可参考全本地成片教程 https://www.reddit.com/r/comfyui/comments/1w4qvnz/tutorial_create_ai_anime_videos_locally_with/ 。
输入：有授权的身份/风格/场景/道具参考图、必要音视频参考；MiniMaxH3 Reference to Video与MiniMaxH3AddGuide节点把首帧/关键构图锚定到明确帧号。使用官方本地ref2va INT8 checkpoint，不调用任何托管API。适合人物/物体身份和跨时刻固定构图。技术前提：ComfyUI>=0.34.0，本机已安装。品质优先保留20步，而非强制4步RefTurbo（官方指出低步数可能损害参考身份约束）。限制：参考图越多不必然越好，时间锚需正确构图，需实测声画和真实时间。

### C｜本地ComfyUI H3 Multishot CORE / 连续镜头拼接
成熟社区代码与导入流程：https://github.com/androdes/ComfyUI-H3-Multishot （其Quick Start链接到j lucasmcrell版本 https://github.com/jlucasmcrell/ComfyUI-H3-Multishot ）。只采用离线CORE图或审计后的本地组件，不调用云端。将15s创作拆成若干连续镜头，分段生成并由开源节点传递末尾画面/音频上下文、用成熟编辑器合成。适合复杂镜头/长期人物连续；比A/B增加节点安装、版本兼容、接缝与配音检查成本。开发者自报完整运行测试不等于本机工作流已PASS；本机当前未装该包，未经隔离审计不直接写入稳定ComfyUI。
参考创作者社区实拍：https://www.reddit.com/r/comfyui/comments/1wio4eg/i_opensourced_my_comfyui_workflow_for_minimax_h3/ （自报29秒4段成功，不能照搬生成时长与品质）。

硬件相同的成熟排障与可导入工作流：https://github.com/IvenKooLab/minimax-h3-turing （2080 Ti 22GB，sm_75）；本机优先检查此架构兼容，不照搬sm_80+ SageAttention/FP8内核。该手册作为A/B/C共用运行时技术底座，并不是第四条新视频生成路线。

## 已在Windows本机发生的Reality事实
- Windows 10，NVIDIA RTX 2080 Ti 22528MiB。调用nvidia-smi实测空闲20336MiB、当时已用1895MiB；当前机器其他进程与数据可能变化。
- H3官方INT8模型和Qwen3VL nvfp4编码器、视频VAE、音频VAE均已安装于 C:/AI/MiniMax-H3/ComfyUI/models。
- 本机 ComfyUI v0.34.0，Torch 2.9.1+cu130，comfy-kitchen CUDA backend可用，启动独立本地服务 http://127.0.0.1:8194；triton unavailable，默认使用pytorch attention；不会更改代理或已有其他ComfyUI实例。
- 复用旧 H3-05 冻结107帧20步原生音视频图作为**新派生工作流来源**，不修改原冻结JSON。将正式 V2 C001 native 源图复制到全新隔离目录：C:/AI/MiniMax-H3/projects/H3-LOCAL-COMMERCIAL-20261013/input/kitchen_C001.png；SHA256=D0C40B01E4A78D57C2B591A28A42EFBC6424FBDD82F6AAD88AE7F0A1550F2BE7。
- 隔离生成两个待用API图：A_FL2VA_107F_20STEP_API.json（短预检）和 A_FL2VA_362F_20STEP_API.json（约15秒完整版）；均864x480/24fps/20steps/beta scheduler/res_multistep/原生音频，实际提交的是**362帧版**。864x480为能在现有已证明运行的显存条件下进行第一轮时序验证，**不是**原生完整画质1344x768，也绝不冒称2K商业原生画质。
- 本地 REST API POST /prompt实际一次提交，返回 prompt_id=de21998b-d4dd-454d-abd8-7c58427104a3，node_errors={}。查询 /queue显示 queue_running=1 queue_pending=0、RUNNING_ID匹配，GPU当时已用3703MiB、利用率27%。这是**已提交和正在运行**，不是媒体交付。后续完成与否需读本机Comfy /history/<prompt_id> 与实际output文件，不猜测成功。
- 任务提交回执路径：C:/AI/MiniMax-H3/projects/H3-LOCAL-COMMERCIAL-20261013/A_15s_submit_receipt.json。隔离工作区和旧正式V2记录均保留；没有下载新模型、没有安装第三方节点、没有改FlClash。

## 后续Reality验收硬约束
本次A在真实输出前：RENDER=RUNNING、VIDEO=NOT_VERIFIED、AUDIO=NOT_VERIFIED、COMMERCIAL_QUALITY=UNKNOWN、FINAL_VALID=NO。不得因为有PID/queue接受就宣称作品成功。待真实完成，核对历史错误、输出视频/哈希、ffprobe帧数fps长度/音频、解码、真实播放听音、角色手部与物件数、动作连续性、身份、商业吸引力及素材与模型本地商用许可；对照旧107帧视觉失败原因。
如果A不合格，按GOOD/BAD/FIRST_DELTA分类为提示词/画面参考/运动控制/内存与推理错误；只切换成熟B多时间锚或C多镜头在必要且净收益正时做有界复验，旧稳定资产不删除。不得把原生视频生成失败理解为要重新用Codex画56张。
正式商用权限：ComfyUI当前说明本地H3商业使用需要单独MiniMax商业许可，模型可本地试片不代表可无证商业发布：https://comfy.org/minimax/license 。

## 路线排序
按现有资产+少装插件+单镜头15s+真实合格视频概率的虚拟结构判断：A先Reality；B适合A画面漂移时加强锚点；C适合多镜头/多段电影化；并非声称三个实际成片都合格。所有T_VALID统计必须含服务启动、生成、返工、验收完整时间；当前T_VALID=UNKNOWN。
