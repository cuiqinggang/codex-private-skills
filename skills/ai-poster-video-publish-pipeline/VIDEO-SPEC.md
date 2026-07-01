# VIDEO SPEC

## 输出规格

- 分辨率：1080x1920。
- 帧率：30fps。
- 编码：H.264 MP4。
- full 版：40-55 秒。
- short 版：25-35 秒。

## full 版模板

- 开场宣传图：5 秒。
- 能力图：每张 4.5 秒。
- 收尾宣传图：5 秒。
- 转场：0.5 秒淡入淡出。
- 总时长：约 40-55 秒。
- 顺序：宣传图开场 -> 学生学习 -> 家庭辅导 -> 职场办公 -> 内容创作 -> 本地商家 -> 教师知识整理 -> 设计创意 -> 生活助理 -> 综合复杂任务 -> 宣传图收尾。

## short 版模板

- 宣传图。
- 学生学习。
- 家庭辅导。
- 职场办公。
- 设计创意。
- 综合任务。
- 宣传图。
- 总时长：约 25-35 秒。

## 展示原则

- 默认静态稳定展示。
- 转场用淡入淡出。
- 禁止抖动、晃动、漂移、随机 Ken Burns、快速缩放、旋转、翻页、弹跳、震动。
- 如需极轻微放大，只允许 100% 到 102%，且验证不抖才允许。
- 如果任何动效导致文字发虚或画面不稳，必须关闭动效，改为静态展示。

## 构图原则

- 图片不能裁切标题、底部、电话、免费、3000元等关键信息。
- 非 9:16 图片使用模糊背景 + 前景完整图，不能拉伸变形。
- 前景图保持完整居中，背景可模糊填充。

## 验证

- `ffprobe` 验证参数。
- `ffmpeg` 抽帧。
- contact sheet 检查开头、中间、结尾。
- 检查免费/3000元/联系方式或抖音无联系方式。
- 检查不裁切、不拉伸、不抖动。
## Audio Spec

When music is requested:

- Produce a final `_with_music.mp4`; keep the base visual MP4 separately.
- Prefer existing good local audio or prior accepted video soundtracks.
- Do not default to crude generated tones or simple procedural music.
- Add fade in/out, usually 0.8-1.0 seconds.
- Keep audio at background level; verify with `volumedetect`.
- Verify the final MP4 has an audio stream with `ffprobe`.
- Subjective quality matters: the music should be calm, pleasant, non-harsh, and not monotonous.

See `AUDIO-GUIDE.md` for the 2026-05-31 audio failure and corrected workflow.
