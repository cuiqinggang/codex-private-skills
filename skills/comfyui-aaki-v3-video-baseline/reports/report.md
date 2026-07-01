# ComfyUI-aki-v3 第三阶段稳定化报告

生成时间：2026-05-24 00:27:38 +08:00  
Skill 包：`H:\AI\skills\comfyui-aaki-v3-video-baseline`  
ComfyUI 安装路径：`H:\AI\ComfyUI_Aaki_v3`

## 结论

第三阶段已按“稳定化和目录规范”完成。本轮没有安装新模型，没有升级 ComfyUI 核心，没有重装环境，没有重新生成视频。

当前可复用日用链路：

`GPT 关键图/分镜 -> ComfyUI Wan2.2 5B 生成短视频片段 -> output\remotion_inbox -> Remotion 后续合成`

## 已整理 Skill 包

现有 skill 已读取并补充以下内容：

- `H:\AI\skills\comfyui-aaki-v3-video-baseline\DAILY-RUN.md`
- `H:\AI\skills\comfyui-aaki-v3-video-baseline\RECOVERY.md`
- `H:\AI\skills\comfyui-aaki-v3-video-baseline\WAN22-5B-SHOT-SOP.md`
- `H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\smoke-check.ps1`
- `H:\AI\skills\comfyui-aaki-v3-video-baseline\workflows\wan22_5b_lowrisk_ui_workflow.json`
- `H:\AI\skills\comfyui-aaki-v3-video-baseline\prompts\wan22_5b_lowrisk_api_prompt.json`

`SKILL.md` 已增加日用导航、输出目录和 smoke check 入口。

## 输出目录规范

已确认/创建：

- 原始视频输出：`H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\video`
- 人工筛选保留：`H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\video_selected`
- Remotion 导入入口：`H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\remotion_inbox`

建议最终交给 Remotion 的命名：

```text
scene##_shot##_take##_wan22_5b_512x512_12fps.mp4
```

## 当前 PASS 基线

第二阶段成功视频：

`H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\video\wan22_5b_smoke_20260523_224438_00001_.mp4`

模型路径：

- `H:\AI\ComfyUI_Aaki_v3\ComfyUI\models\diffusion_models\wan2.2_ti2v_5B_fp16.safetensors`
- `H:\AI\ComfyUI_Aaki_v3\ComfyUI\models\text_encoders\umt5_xxl_fp8_e4m3fn_scaled.safetensors`
- `H:\AI\ComfyUI_Aaki_v3\ComfyUI\models\vae\wan2.2_vae.safetensors`

固定低风险参数：

- 图生视频
- `512x512`
- `37` frames
- `12` fps
- `3.083333` seconds
- `12` steps
- `cfg 5.0`
- CLIP on CPU

第二阶段观测：

- 生成耗时：`1783.136` seconds
- 峰值显存：`16946 MiB`
- 输出视频：H.264 MP4

## Smoke Check

只读检查脚本：

```powershell
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\smoke-check.ps1
```

该脚本只验证：

- ComfyUI 服务 HTTP 可用
- `/system_stats` 可用
- 三个模型文件存在
- workflow/prompt 存在
- `video`、`video_selected`、`remotion_inbox` 目录存在
- GPU 能被 `nvidia-smi` 识别

它不会提交 prompt，也不会生成视频。

## 未执行事项

- 未安装新模型
- 未安装 LTX
- 未安装 FramePack
- 未安装 Wan2.2 14B
- 未安装 S2V
- 未安装 Fun InP
- 未升级 ComfyUI 核心
- 未删除现有模型
- 未修改 Hermes、New API、小龙虾、Open WebUI、Remotion 配置

## 后续建议

下一步只建议做“素材生产小批量演练”：

1. 用 GPT 生成 3-5 个关键图和分镜说明。
2. 每个 shot 使用同一 Wan2.2 5B workflow 单独生成。
3. 把可用结果复制到 `video_selected`。
4. 把最终剪辑素材复制到 `remotion_inbox`。
5. 在 Remotion 侧只消费 `remotion_inbox`，不要直接扫 ComfyUI 原始输出目录。

