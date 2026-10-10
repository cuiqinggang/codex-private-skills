# Krea FP8 本机部署现实证据状态（2026-10-11）
任务：在 Windows RTX 2080 Ti / 32GB RAM 上部署成熟 ComfyUI FLUX.1 Krea Dev FP8 模型，随后才允许厨房与人物独立生成品质测试。
- 正式选择技能：visual-art-engine-performance-ladder v1.2.0；选型记录：KREA-H3-SELECTION-V1.md；来源审计：IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md。
- 本机检查：C: 约 323.99GB 余量，CLIP-L/T5-FP8/ae VAE 文件存在；主模型原先不存在。
- 官方扩散权重：Comfy-Org/FLUX.1-Krea-dev_ComfyUI 的 flux1-krea-dev_fp8_scaled.safetensors，11904639672 字节，SHA256 b17a8c21703c4d6ffb0e300dd920eff3cfd35c9a72a1abaf107e3788e408b8d8。
- 首次标准 Hugging Face 库下载：HTTP 连通，传输约 73.5 MB 后 IncompleteRead/ProtocolError，未完成，不能计作安装。
- 本机成熟 aria2 工具经 HF 地址无法开始有效传输。转用 Comfy 官方工作流注明的 ModelScope 同仓库镜像，经 Range 获取 206 Partial Content，文件总长与官网一致。采用 aria2 8 分段可续传，最后观测约 792MiB/11GiB（6%），尚未完整。实际速度波动明显。
- 官方模板从 Comfy-Org/workflow_templates 原仓库读取，已保存缩排合并的真实 JSON 于 C:\AI\ComfyUI_Aaki_v3\data\output\krea_preflight_20261011\official_flux1_krea_dev.json；模板包含 DualCLIPLoader、UNETLoader、VAELoader、EmptySD3LatentImage、KSampler、VAEDecode 等原生节点的 subgraph。
- 模型预期路径：C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\diffusion_models\flux1-krea-dev_fp8_scaled.safetensors。
- 必须完整校验模型文件大小和 SHA256 后才允许 MODEL_INSTALLED=YES，继而实际加载官方工作流、从空白噪声采样、保留 prompt_id/history、两类品质大图比较、最终 H3 视频验收。
- FREEZE：MODEL_SELECTION=KREA_FIRST；MODEL_INSTALL=IN_PROGRESS_NOT_VALID；WORKFLOW_OFFICIAL_CACHED=YES；KREA_IMAGE_REALITY=NOT_RUN；KREA_QUALITY=NOT_VALID；KREA_H3=NOT_RUN；FINAL_VALID=NO。
- 不允许拿过去 SD1.5 的厨房图或 ChatGPT image_gen 图像充当 Krea 生图证据；不改 FlClash / 代理 / CUDA/Torch。

## 2026-10-11 00:43 之后官方工作流与完成下载核验更新
- 远程后台 aria2c 经 ModelScope 官方模板推荐镜像下载，下载进程 42528 返回 `stat=OK` 且退出码 0。文件名 `flux1-krea-dev_fp8_scaled.safetensors`，大小 **11904639672 字节**；原先 .aria2 续传控制文件现已消失。完整 SHA256 仍需以本机计算结果比对 `b17a8c21703c4d6ffb0e300dd920eff3cfd35c9a72a1abaf107e3788e408b8d8`，不可仅凭尺寸或下载 OK 宣称哈希通过。
- 官方 Krea ComfyUI 教程明确要求：Krea FP8（或者有更高显存时完整精度 Krea）、CLIP-L、T5-XXL（FP16 或低显存 FP8）、VAE `ae.safetensors`。**不是安装一个文件然后沿用旧 SD1.5/Canny 流程**。官方文档：https://docs.comfy.org/tutorials/flux/flux1-krea-dev 。
- 官方可执行模板：Comfy-Org/workflow_templates 的 `templates/flux1_krea_dev.json`，subgraph 节点为 DualCLIPLoader、UNETLoader、VAELoader、CLIPTextEncode、EmptySD3LatentImage、KSampler、ConditioningZeroOut、VAEDecode；默认 1024×1024、20 steps、CFG 1、Euler + Simple。按模板槽位：clip_name1=clip_l.safetensors、clip_name2=t5xxl_fp16.safetensors；官方教程文字中的槽位顺序与模板不一致，适配应以真实可执行模板与 ComfyUI 输入核验为准。
- 本机 ComfyUI `/object_info` 实测以上所需节点全存在，没有必要安装新节点；Krea 主模型下载后已出现在 UNETLoader 可选清单，T5 FP8 已出现在 DualCLIPLoader 可选清单，ae 已出现在 VAELoader 可选清单。**只表示清单识别，不等于成功加载与生成。**
- 现有 T5 `t5xxl_fp8_e4m3fn_scaled.safetensors` 来自 Comfy 官方推荐的 FLUX 编码器库，官方允许低显存 FP8；本机已另存只改这一个文件名的本地工作流，不篡改官方原件。官方原始模板保存为 `C:\AI\ComfyUI_Aaki_v3\data\output\krea_preflight_20261011\official_flux1_krea_dev.json`；适配模板为同目录 `krea_official_template_t5fp8_local.json`。
- 官方组件文件源：`https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn_scaled.safetensors`，`https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors`，`https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/blob/main/split_files/vae/ae.safetensors`。
- 已有 CLIP-L SHA256 本机实测 = `660c6f5b1abae9dc498ac2d21e1347d2abdb0cf6c0c0c8576cd796491d9a6cdd`，与官方页面吻合；其他文件哈希仍待完整审计。
- 提醒：RTX 2080 Ti 显存 22528MiB，官方说明大于 32GB 显存推荐 T5 FP16，所以保留现有 T5 FP8 是有官方依据的资源选型，不代表已认证与 FP16 输出像素无差异。不要在结果达标前为了速度改官方采样参数。
- 用户关心下载进度不可见：因为是 Windows 远程后台 PowerShell aria2c 命令下载，浏览器不会显示下载图标；文件直接保存到 `C:\AI\ComfyUI_Aaki_v3\ComfyUI\models\diffusion_models`。
- 最终门禁：MODEL_DOWNLOAD=COMPLETE；CHECKSUM_VALID、KREA_LOAD、KREA_REAL_GENERATION、QUALITY_PASS、H3_VALID 均需分别核验才可变成 PASS，未证明之前保持 FINAL_VALID=NO。
