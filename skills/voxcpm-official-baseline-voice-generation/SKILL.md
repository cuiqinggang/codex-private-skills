---
name: voxcpm-official-baseline-voice-generation
description: Use when generating short Chinese voiceovers with the existing VoxCPM2 official baseline, especially when the user asks for female voice, no large reinstall, no core-code modification, and final playback/ASR/volume/pitch validation.
---

# VoxCPM 官方基线口播生成

## 触发场景

- 用户要求用 VoxCPM / VoxCPM2 生成中文短口播。
- 用户说不要重新部署、不要乱装大模型、不要魔改 VoxCPM 核心代码。
- 用户明确要求女声、女生、普通女生标准声线。
- 需要交付可点击音频，并确认能播放、内容读对、音量正常、声线合格。

## 已验证环境

${REDACTED_SECRET}
- Python：`.venv`，CPython 3.11.15
- 包：`voxcpm==2.0.3`，`torch==2.11.0+cu128`，`torchaudio==2.11.0+cu128`
- 模型缓存：`work\voxcpm-official-baseline\.hf_home`
- GPU：RTX 2080 Ti，CUDA 可用
- 已验证女声参考：`reference_ai_doctor_original_female.wav`

## 必设环境变量

```powershell
${REDACTED_SECRET}
$env:HF_HUB_OFFLINE="1"
$env:HF_HUB_DISABLE_SYMLINKS_WARNING="1"
```

脚本中也应强制设置这些变量，避免 HuggingFace 在线校验卡住。

## SOP

1. 复用既有 VoxCPM 官方基线环境，不重新部署，不安装大型依赖。
2. 只写外围脚本、转码、裁剪、分段、拼接和验收流程，不改 VoxCPM 核心代码。
3. 如果用户明确要求女声，不要只靠默认声音或括号提示词；默认/提示版本可能实际偏男声。
4. 稳定女声优先使用已验证女声参考音频 `reference_ai_doctor_original_female.wav`。
5. 声线提示词可能会被模型读出来；一旦 ASR 发现提示词，不能直接交付。
6. 转 m4a 前后都要检查：时长、编码、采样率、体积、可解码。
7. 用 `volumedetect` 检查音量；只做轻微增益，避免爆音。
8. 用 whisper.cpp large-v3 转写验收；内容读错、漏读、读出提示词时不得交付。
9. 女声需求必须增加 F0/基频验收：median F0 建议 >= 165 Hz。低于阈值要判为偏男声或至少人工复核。
10. 最终文件放到当前任务的 `outputs` 目录，并给用户可点击链接。

## 女声纠偏规则

- 不得只凭文件名、提示词或 ASR 判定“女声合格”。
- 2026-07-08 失败复盘：默认/提示生成的“普通女生标准声线”实际 median F0 约 129.7 Hz，用户听感认为男声，判定反馈成立。
- 参考女声 `reference_ai_doctor_original_female.wav` 的 median F0 约 205.3 Hz。
- 新版女声参考生成文件 median F0 约 183.9 Hz，通过女声阈值。
- 女声交付至少做三重验收：ASR 正文、音量、F0 女声阈值。

## 验收标准

- m4a/AAC 可解码。
- 目标文案主体完整，ASR 识别正确。
- 不含声线提示词、括号提示、测试说明等非正文内容。
- 音量峰值不过载；短口播平均音量不要明显偏小。
- 女声需求 median F0 >= 165 Hz，且尽量接近已验证女声参考。
- 若用户反馈“洪、浑浊、不清楚”，必须增加清晰度验收：对比用户认可样本的低中频浑浊区和咬字清晰区，必要时只做外围 EQ/高通/限峰处理。
- 无遗留 VoxCPM 生成进程占用 GPU。

## 最近验收

- 2026-07-08：生成“AI博士学习”女声版 v2。
${REDACTED_SECRET}
- ASR：`AI博士来了，博士老师请不起，AI博士先使用，价值几百的资料免费送，留言，AI博士学习。`
- 音频：9.44 秒，AAC/m4a，48kHz，约 189KB；可解码。
- 音量：mean -22.6 dB，max -6.3 dB。
- 女声验收：median F0 183.9 Hz，通过。

## 清晰度纠偏

- 2026-07-08：用户指出女声 v2 “有点洪、浑浊”，但认可偏男初版的清晰度、亮度、清脆爽朗感。
- 修正做法：以用户认可初版作为清晰度参考，只对女声 v2 做外围音频处理，不重新部署模型，不改核心代码。
- 处理：高通、削减 230Hz/380Hz 低中频浑浊区、轻微提升 3.2kHz 咬字区、补音量并限峰。
- 验收：v3 presence_to_mud 从 v2 的 0.036 提升到 0.077，接近参考版 0.088；ASR、音量、女声 F0 均通过。
${REDACTED_SECRET}
