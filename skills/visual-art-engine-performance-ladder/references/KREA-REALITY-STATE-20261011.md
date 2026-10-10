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
