# BLUE8 完整配套接续审查 V1.4
日期：2026-11-10（北京时间）。
状态：CANDIDATE_IDENTIFIED / LOCAL_PREREQUISITES_MISSING；FINAL_VALID=NO。
本轮为只读资料/资产/工作流审查，新增GPU提交0、模型下载0、环境升级0。不是8秒作品交付，也不是生产配方认证。

## 继承而不重跑
权威前序：[V1.3](../../skills/video-extreme-time-engine/references/BLUE8-COMPLETE-PAIRING-V1_3-20261110.md)，blob 55166aeeec1137620ac147b15c2e8a1e7f3ada23。
原生56帧Ref2VA Turbo4生成08:44:200成功，但起始身体姿态与原片不符、口型不一致，不能扩8秒。
本轮已读取本机R2/freeze.json及extra-model-paths-native.yaml，未重投prompt c46e922a-1680-4508-9fb9-f4e8719cc0f0。
32B INT4与INT8 VAE已存在；不重复下载，不回退原NVFP4链。
旧固定时间停止不能证明模型卡死；“Model Initializing”含首步加载与前向。
时间目标与故障判据分开。现行本机规则明确不自行新增固定墙钟杀进程时间；正常进度不因到时终止。资源保护、真实异常及质量关卡继续保留，旧失败计入累计时间。

## 找到的完整候选及其反证
| 候选 | 完整材料/公开验证 | 与本任务的差距 | 判定 |
|---|---|---|---|
| Wan Animate Ultimate v2.0.0 | 作者JSON、下载表、预览、口型讲解；同时提供Wan Animate2与Wan2.2 Animate GGUF+face video | 本机缺所需主模型及部分配套；新版原生节点未齐；2080Ti速度、当前蓝裙质量未测 | 优先完成GGUF+face路径的兼容准入 |
| H3 Character Swap v1.1.0 | 原Ref2VA+专用换角LoRA+Turbo4；3060/32GB作者多段实测 | 作者/教程明确长片时序可能漂移；专用LoRA未在已查目录发现；新工作流需0.39+；INT4编码器并非作者原测组合 | 次候选，不能用随机种子重抽代替确定性验收 |
| Viggle-Animate H3 | 专用微调主模型、DMD、固定文本嵌入；3060作者舞蹈/说话样例 | 官方明确lip-sync弱；需要重绘原片某帧以保持姿态/机位对齐，不能直接用任意独立站姿图替代；已有Ref2VA不等于Viggle权重 | 不能单独覆盖当前严格动作+口型合同 |
| Wan Animate2官方原生脚本 | 官方推理、蒸馏权重、案例 | 官方默认8×A800720p、已测2×A800480p；不能原样当2080Ti整包 | 使用已验证消费卡适配流程，而非照搬官方服务器命令 |

优先候选依据是工作流的功能、材料完整性与消费卡现实案例，不是声称其已在本机认证。
没有找到同2080Ti的同合同速度，不等于不能开展有依据的本机适用性验证；它只意味着不能预先承诺30分钟或外推倍数。

## 实际核对了工作流，而非只读宣传
源：[The_frizzy1 Wan Animate Ultimate v2.0.0](https://github.com/Thefrizzy1/The_frizzy1-Workflows/tree/main/workflows/wan2.2/animate-ultimate)。
JSON blob：091b6f9b982fba276be1eee9a14340f0c71b00ae；
README blob：c4d587e2bb65f77244114ee4f860b98abb438326；
downloads blob：243bc9835b201cdfb14ee4a34fc07eda71bbace3。
已展开nodes与definitions.subgraphs，不把UUID子图名误判缺失插件。
- GGUF分支实际包含UnetLoaderGGUF、WanAnimateToVideo、CLIPVisionEncode、KSampler、TrimVideoLatent、VAEDecode、CreateVideo。
- 预处理实际包含RTDETR_detect、SDPoseKeypointExtractor、SDPoseDrawKeypoints、SDPoseFaceBBoxes、CropByBBoxes；脸部视频是明确控制输入。
- Animate2是另一分支：WanAnimate2ToVideo、WanAnimate2Cache等，不能和旧Animate模型/输入混用。
- 作者GGUF计时：81帧、480×864、queue到文件07:05，采样04:51、峰值VRAM11.7GB、RAM24.6GB，RTX3060/32GB。该行来自v1.0.0，当时relight未加载；v2.0.0修正加载后不得沿用为相同配置SLA。
- 作者81帧时间及片段说明并未建立当前24fps/192帧合同；不推算8秒总时间，不拿补帧冒充原生动作时序合格。

## 本机资产与版本的确定范围
只读检查范围：
C:/AI/MiniMax-H3/models；
C:/AI/MiniMax-H3/ComfyUI/models；
C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/models；
C:/AI/ComfyUI_Aaki_v3/ComfyUI/models；
另检查当前extra-model-paths指向的Star7原部署models目录。
未全盘搜索，不声称机器任何位置均无文件。

| 配套 | 本轮观察 |
|---|---|
| Aaki ComfyUI版本 | comfyui_version.py=0.9.2 |
| H3 ComfyUI版本 | comfyui_version.py=0.34.0 |
| Wan2.2通用5B | Aaki diffusion_models/wan2.2_ti2v_5B_fp16.safetensors，9999658848字节；不是Animate |
| UMT5 | Aaki text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors，6735906897字节；候选复用，仍须按源hash核对 |
| 已有Wan VAE | Aaki vae/wan2.2_vae.safetensors，1409400960字节；不能替代Animate要求的Wan2.1 VAE |
| 现有相关插件目录 | Aaki有controlnet_aux、ComfyUI-GGUF、ComfyUI-WanVideoWrapper；目录存在不等于当前工作流全部节点就绪 |
| 新候选所需核心节点 | Aaki未见SDPose扩展文件；两环境版本低于作者要求0.37.4，不能把完整JSON直接塞进去运行 |
| Animate/Viggle/CharacterSwap专用主权重或LoRA | 上述定向枚举未命中；这不是全盘不存在证明 |

旧Wan Animate v1.2下载表还披露了一个无法追溯的重命名速度LoRA，不能按该旧名字随意下载替代物。优先采用作者已明确修正依赖的新完整图，但需保留上面的v1/v2计时差异。

## 下一现实执行的确定入口
1. 选择单一分支：优先Wan2.2 Animate GGUF+pose+face，不能同时下载所有模型分支。
2. 先核对SM75可用dtype和注意力实现，优先源实现已有FP16/通用attention路径；不能给2080Ti强套仅Ampere起支持的Sage2/BF16内核。缺项应查对应成熟实现，不猜改核心。
3. 环境只作项目隔离安装/版本适配；保留现有H3与Aaki原环境。主模型、Wan2.1 VAE、CLIP vision、SDPose/RTDETR、必要LoRA依下载表按缺项准备，UMT5只读复用并校验；本轮未部署。
4. 在准确版本的实际object_info中核验节点和枚举，按源图连接。未通过接口准入不采样。
5. 原视频0–8秒/24fps保持原时间轴。先审核首帧骨架、脸框覆盖、偏头与手部相交帧；脸框不截嘴。预处理未通过不能进入生成。
6. 短段长度依所选Wan流程接口确定，不沿用H3的17n+5规则；必须覆盖开头姿态、实际发声与合手动作。模型尺寸要求和音频裁剪时窗同步冻结。
7. 正常运行按节点/采样进度记录，不新增五分钟截止；真实故障或既有资源保护才中止运行，质量失败停止扩片并审查匹配性。
8. 身体合格且嘴部仍差时，才评估现有MuseTalk1.5局部口型节点；不得在动作错误底片上补嘴。组合本身仍需验收，不能自动认证。
9. 短段合格再制作192帧8秒，全片逐帧/相邻帧检查与用户本机播放器声画验收；未完成保持FINAL_VALID=NO。
10. 只报告真实有效交付时间；检索、失败、安装、恢复均不清零。

## 一手来源
- [Wan2.2官方预处理指南](https://github.com/Wan-Video/Wan2.2/blob/main/wan/modules/animate/preprocess/UserGuider.md)：先审核姿态/面部/遮罩，基本姿态重定向要求正面伸展，不适合直接套偏头首帧。
- [Comfy官方Animate教程](https://github.com/Comfy-Org/docs/blob/main/tutorials/video/wan/wan2-2-animate.mdx)：骨架/面部控制、准确VAE与模型清单。
- [Ultimate工作流及下载表](https://github.com/Thefrizzy1/The_frizzy1-Workflows/tree/main/workflows/wan2.2/animate-ultimate)：双分支、实际消费卡测量、v2修订。
- [H3 Character Swap作者工作流](https://github.com/Thefrizzy1/The_frizzy1-Workflows/tree/main/workflows/minimax/h3-character-swap-12gb)。
- [Character Swap教程及限制](https://github.com/TheBeast-Spec/minimax-h3-character-swap-lora-comfyui/blob/main/README.md)：不是保证时序的确定性系统。
- [Viggle官方研究说明](https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame)：重绘帧条件与弱口型限制。
- [Viggle消费卡适配](https://github.com/Thefrizzy1/The_frizzy1-Workflows/tree/main/workflows/minimax/viggle-animate-h3)。
- [Wan Animate2官方](https://github.com/Wan-Video/Wan-Animate-2)：服务器默认配置，不能外推2080Ti。

## 复用与未完成
已读本机AGENTS、Knowledge Brain INDEX/ROUTING_MAP、obsidian-index视频条目和长期记忆入口；采用V1.3失败证据，拒绝把旧MuseTalk技术运行视为本任务艺术验收。无核心代码修改，CodeGraph不适用。未做全库同步。
本轮完成完整候选与本机缺口审查；隔离环境、缺失资产、SM75接口验证、预处理和新短段尚未完成，不报PASS。
NEXT_PAGE_PROMPT：读取本V1.4与V1.3。不要重投旧H3短段。优先审查已定位的Wan Animate Ultimate v2 GGUF+face完整图，保持版本/权重/节点组合一致；UMT5已有，主模型等缺项按准确表核对，不重新全盘寻找。原H3/Aaki版本不足，仅隔离适配；同2080Ti速度未知只限制承诺，不能变成永久不验证。首帧/pose/face预处理通过后再做代表短段，不自行新增墙钟杀进程截止。最终8秒与GUI声画仍未通过。
