# FLUX.1 Krea Dev 本机独立生图首次现实执行 R1

执行结论：**G0/G1/G2=PASS；G3 视觉同等级品质=FAIL；FINAL_VALID=NO**。该图片是可核验的真实 ComfyUI 输出，但不是已通过原图同等级视觉门的正式精品基线。

## 来源
- Windows DESKTOP-4A1EGTM，ComfyUI v0.9.2，RTX 2080 Ti 22528MiB，32GB 内存。
- 官方工作流改为本机适配的 API 形式：UNETLoader → KSampler → VAEDecode → SaveImage，参考图不进入 workflow；空白噪声 EmptySD3LatentImage 作为唯一 latent 输入。
- 主模型 FLUX.1 Krea Dev FP8 Scaled；T5-XXL FP8 Scaled + CLIP-L；ae VAE；20 步 Euler / simple / CFG=1 / seed 202610110044 / 832×1024。
- Prompt ID `40b425ff-5308-4ae1-85b5-1b7c49daa952`。HTTP 200；history.json 中 status=success、completed=true；输出为 KREA_INDEPENDENT_REAL_R1_00001_.png。完整输入、输出和执行记录见本目录文件。
- **运行耗时**：ComfyUI 服务端日志 217.61s（包含首次加载及采样）；提交至图片及证据落盘 235.45s。20 步实际采样约 48 秒；不是完整端到端耗时。
- G3 视觉判断：已生成物体与自然摄影结构，但与目标参考图相比构图变化大、阴影较硬且暗、布料与木勺未忠实实现，不能据此宣布与原图同等级品质通过。

## 文件及 SHA-256
- [真实独立生成 PNG](generated.png): `c1cd6ff5ded8a5fd256a2f309c5372d8d6d9c6b4b0c2c7d656e4c8f215a0faa6`
- [程序直接拼接左右对照 PNG](comparison.png): `acd5d07c690cbcd8e01bb55481a1c3e34095452f79dfdfde2983efc6618fe7f0`
- [实际执行工作流](workflow_api.json): `345419a83f553c85f2864410c0b96c9a37b2f739e6e20f6f4037fd380b5c29e1`
- 本机原始参考图片 SHA-256：`f662282ef24ec945c00430be54b8eda5c4816e1c052c14e184af55e21a284945`（仅供人工对比，未送入 Krea 生成图节点）。
- 节点、种子、原始提示词、实际提交、history、显卡快照详见独立文件。

## 硬门禁
不使用 ChatGPT image_gen 作为 ComfyUI 出图；比较图通过普通 PIL 像素 contain+paste 合成。真实性通过 ≠ 艺术质量通过。下一轮从已有官方工作流继续改进，不将此张作为品质达标结果。
