# 本机视频资产复用核查（2026-11-10）

每次调用先核对 [固定资产清单](LOCAL-ASSET-INDEX-20261110.json) 的完整路径、大小、版本、精度和完整指纹记录；文件变更或来源不明才重算完整指纹。直接复用既有模型路径，不搬运或复制大文件来建立新订单。

## 已核实的现有环境

- 原安装：`C:/AI/ComfyUI_Aaki_v3`，原 Python / Torch 2.9.1+cu130 / ComfyUI 0.9.2 继续使用。
- FFmpeg、FFprobe、Windows Media Player 已有；本次未重装制作主程序。
- UMT5 文本编码器 6,735,906,897 字节已复用，完整 SHA 与原配方要求一致。
- 旧技能 `C:/Users/A/.codex/skills/comfyui-aaki-v3-video-baseline/SKILL.md` 登记 Wan2.2-TI2V-5B 与 Remotion；既有 H3、SVD、MuseTalk 独立记录继续保留，按各自已验边界使用。
- C盘AI资产及用户HF缓存元数据已补查；该范围内没有发现本次之前已存在的同版 S2V 主模型、音频编码器和Wan2.1 VAE。此结论保持在已查范围。
- BF16 32.59GB 与 FP8 16.39GB 是不同文件。先下载BF16、因真实内存压力中止后改用官方FP8，增加了准备成本；保留原记录，后续默认使用已装FP8分支。

## 固定资产与恢复位置

`C:/AI/Video-Recipe-Reproduction-20261110/S2V-15/ASSET-REUSE-INDEX.json`

该目录的 `model-downloads` 保存此次新增文件；共享 UMT5 沿原安装路径读取。后续新订单引用这些固定文件，只新建订单输入、输出和证据。原程序目录、系统网络、驱动、Torch及注意力/offload保护设置保持原状态。

当前任务从同目录 `CONTINUE.md` 与 `evidence/R1Q` 核账；执行器、prompt_id、模型准备和原生history分别读回。已有提交意图时先核对队列和history。当前三阶段脚本只用于该任务；新订单沿保存的原生工作流分配唯一任务标识，按原接口映射新输入，保留提交与成片来源。

## 证据与能力状态

- 原始查核：同目录 `evidence/reuse-model-inventory.json`、`reuse-original-skills-readback.json`、`asset-reuse-check.json`。
- 四个当前所需模型的复用检查 `ready_to_reuse=true`，该检查启动下载数0；核对已完成完整指纹后的未变更文件元数据。
- BF16 原案例在模型加载阶段因可用内存约0.5GB、分页增长和响应延迟而保护性中止；没有宣称CUDA OOM、采样失败或作品不合格。
- FP8 主模型完整指纹已通过，首轮原生采样进行中。重复、蓝裙迁移和作品质量尚未完成，不登记为已认证能力。
- 后续完成情况以原任务最新原生history、实际文件与审核为准，继承已完成部分。

[复用核查报告](https://chatgpt.com/library?file_id=libfile_fde3_f-303251326060819189a3036ecb19237f_937029f1505c8191917e0968911c47f5&account_id=personal)；[原始核查证据](https://chatgpt.com/library?file_id=libfile_fde3_f-a88ee7f9778c8191947b565c4c2c41df_937029f1505c8191917e0968911c47f5&account_id=personal)。
