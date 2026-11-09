# 数字人介绍视频专项：资料、原样复刻与中文迁移

更新：2026-11-09，北京时间。当前只推进固定正面头像或固定机位人物口播，搭配介绍页面、图片、PPT 或实际功能录屏。用户说的“昨日重现”在本任务中指原案例重放，不调用同名交易方法。

## 先看已有结果

- 原案例：公开的同一虚构人物、原视频和原英文语音，在本机用 MuseTalk 1.5 原程序生成两次。
- 换内容：保持同一人物，换成三句中文介绍，生成约 14.7 秒口播。
- 组合成片：中文口播与三张介绍页面合成 1280×720、25fps 视频，含句级字幕及两种人物位置。
- 本次没有改变生成核心、重训模型、手修嘴部、重定时或反复抽卡。
- 当前证明“实际产出＋原案例重复执行＋一次同人物换中文音频”。正常速度声画审片及主观口型准确性仍待核，不能登记为作品级质量验收通过。

本机任务目录：`C:/AI/Video-Recipe-Reproduction-20261108/Avatar-Specialist-20261109/`。成品、日志、模型摘要及审核边界见同目录与 [本轮证据记录](AVATAR-REALITY-20261109.json)。

## 按宣传目的选择展示方法

| 展示形式 | 成熟制作方式 | 本次状态 |
|---|---|---|
| 头像单独口播 | 固定正面人像/底片＋完整音轨，原生口型驱动 | 已实际生成原案例和中文实例；声画主观验收待核 |
| 人物与介绍卡片并列 | 已生成口播缩放叠加到排版模板，旁边放重点 | 已合成，抽帧核对排版与字幕 |
| PPT 主画面＋角落人物 | 先将幻灯片作为画面，人物画中画；切页按音轨定时 | 本次用三张图卡模拟页面；真实 PPT 导入未测 |
| 图片轮播＋人物讲解 | 客户图片作为主画面，配句级字幕与人物 | 本次是示意图卡；真实客户图片替换未测 |
| 功能录屏＋人物讲解 | 使用真实产品录屏做主轨，按解说剪辑，人物叠加 | 本次只有功能示意图；实际软件录屏未做 |
| 竖屏宣传 | 复用已合格口播，切换 9:16 排版，保留安全区 | 未测；不以本次横屏推定通过 |
| 固定全身人物 | 先有自然待机/动作底片，只驱动口型；动作靠已有片段剪辑 | 未测；本次不能证明全身动作能力 |
| 实时问答/直播 | 采用已有 LiveTalking 等流式整包 | 已整理官方入口，本轮不部署互动系统 |

## 数字人候选资料比较

下面是不同生成路线、整合产品或辅助环节，不能把 14 行算成 14 项已认证能力。除本轮 MuseTalk 案例与继承的 Audiogram 外，没有新增这些路线的本机推理结论。

| 路线/资料组 | 原始资料与完整方法入口 | 本任务取舍与具体边界 |
|---|---|---|
| MuseTalk 1.5 | [官方源程序](https://github.com/TMElyralab/MuseTalk/tree/0a89dec45a0192b824e3cf4daf96c239440c5ed8)；[同输入原成片、三次测试、配置与模型摘要](https://musetalkai.com/musetalk-vs-latentsync/) | 当前首选：本机已有匹配环境，原案例输入和十项模型摘要均核对；只生成口型，原底片决定其他动作；内部脸部区域 256×256 |
| SadTalker | [原项目、Windows 入口、图像/音频样例和 512 模型](https://github.com/OpenTalker/SadTalker) | 单图头像与头部运动的备选；完整画面模式不等于任意全身动作；未在本轮执行 |
| Sonic | [作者节点、配图工作流与共同音轨](https://github.com/Sean-Bradley/ComfyUI-Sonic)；[作者教程](https://sbcode.net/genai/lipsync-sonic/) | 已找到九组作者配图/工作流资料，不能算九位独立用户；当前没有本机出片结论 |
| LatentSync 1.6 | [官方代码](https://github.com/bytedance/LatentSync)；[与 MuseTalk 的同输入测试](https://musetalkai.com/musetalk-vs-latentsync/) | 同样品的纹理与口部表现可直接对照；1.6 官方显存门槛与旧 1.5 不混用；现有 MuseTalk 可直接复用，暂不新增环境 |
| Wav2Lip | [原项目、输入和推理命令](https://github.com/Rudrabha/Wav2Lip) | 原开源权重明确限非商业用途；商业产品/API 的效果不能当原开源模型证据；不选作本次免费商用宣传主线 |
| LivePortrait | [原项目](https://github.com/KwaiVGI/LivePortrait)；[实际用户 Windows 步骤、日志与成片](https://wellstsai.com/en/post/live-portrait/) | 表情/头部驱动辅助；本身不是“文案直接变口播”；不能由下载用户成片推定本机推理已完成 |
| EchoMimicV2 | [原项目、半身样例、音频、姿态对齐与模型说明](https://github.com/antgroup/echomimic_v2) | 半身动作的后续候选，姿态/参考要求多于固定头像；不把 v1 用户反馈自动归给 v2 |
| Hallo2 | [原项目、音频驱动及长视频入口](https://github.com/fudan-generative-vision/hallo2) | 更丰富人像动画的候选；高分辨率增强还包含其他组件；本轮未执行 |
| InfiniteTalk | [原项目](https://github.com/MeiGen-AI/InfiniteTalk)；[作者基础与 V2V 工作流](https://github.com/bluespork/InfiniteTalk-ComfyUI-workflows) | 已有发布者实际成片与两种工作流；相关图片/音轨仍要逐案例配齐；重型底座不作为固定头像第一步 |
| MultiTalk | [原项目与多人样例](https://github.com/MeiGen-AI/MultiTalk) | 多人对话的后续路线；本次只有单人，不为当前任务引入说话者分配和多人运动 |
| LiveTalking 整合系统 | [原项目、数字人/配音选项、录制与 API](https://github.com/lipku/LiveTalking)；[作者实际 MuseTalk 演示](https://www.bilibili.com/video/BV1bUwezvEnG/) | 符合未来持续讲解、动作片段切换和互动用途；底层模型与系统整包分别审核；本轮离线短片不部署实时推流 |
| Linly-Talker 整合系统 | [原项目](https://github.com/Kedreamix/Linly-Talker)；[图片/视频＋配音生成入口](https://github.com/Kedreamix/Linly-Talker/blob/main/app_talk.py) | 已有 TTS 与多个数字人模型的整合方法；固定文稿不需要额外 LLM/ASR 会话；未在本机装新整包 |
| Duix-Avatar（原 HeyGem 路线） | [现项目](https://github.com/duixcom/Duix-Avatar)；[轻量容器配方](https://github.com/duixcom/Duix-Avatar/blob/main/deploy/docker-compose-lite.yml)；[实际许可](https://github.com/duixcom/Duix-Avatar/blob/main/LICENSE) | 有桌面/容器整合入口；运行条件及许可按当前版本核对，不能照搬旧 fork 宣传；不为当前头像路线新建重型容器环境 |
| Remotion / FFmpeg 介绍片后期 | [Audiogram 原模板](https://github.com/remotion-dev/template-audiogram)；[FFmpeg 原项目](https://github.com/FFmpeg/FFmpeg) | 负责版面、切页、字幕、叠加和导出；不承担口型生成。继承 Audiogram 既有两次原样渲染；本轮组合使用 FFmpeg 原生滤镜 |

## 外部实践反馈如何参与决定

1. Sonu 的公开测试提供了同一底片、同一语音、原生输出、三次运行、配置和模型摘要，足以选择一个可对照的固定案例；它仍只有一个场景，没有独立听审，不能换算成普遍成功率。
2. LiveTalking 作者提供了真正使用 MuseTalk 的整合演示；Linly-Talker 提供图像/视频、配音和数字人的完整集成入口。这些支持“这类节点已经有实际集成方法”，不等于它们独立验证了本次 D24 固定案例或当前 Windows 主机。
3. Sonic 的 [Pixaroma 实作教程](https://www.youtube.com/watch?v=3pN2KA6-G0I)、[用户组合实例](https://www.reddit.com/r/comfyui/comments/1legiju/) 及原节点作者的成组工作流保留为可比较备选；版本与发布者分组沿用前轮反馈表。
4. LatentSync 的 [1.5 工作流实作](https://www.reddit.com/r/comfyui/comments/1je0xpz/best_lip_sync_latentsync_update_to_15/)、[用户原工作流运行反馈](https://www.reddit.com/r/comfyui/comments/1i2gnuu)、[Gradio/12GB 用户反馈](https://www.reddit.com/r/comfyui/comments/1lsli7n) 保留原条件，不把不同版本的运行反馈合并成当前品质承诺。
5. 安装笔记、只复述 README 的“研究”、付费整合包广告、仅问下载的评论均不计实际复现成片。本轮检出的两篇笔记中，一篇将 MuseTalk 错说成不支持视频输入，另一篇主要是调研和官方复述；均不作为独立成片成功证据。

综合决定：先复用已在本机存在、代码匹配、输入和模型可逐字节核对的 MuseTalk 固定正面案例，再改变音频。没有代表性统计分母，不给“99%”或其他虚构成功概率。其他候选没有运行不等于失败。

## 本次实际配方

### 原案例

- 代码提交：`0a89dec45a0192b824e3cf4daf96c239440c5ed8`；本轮 `git diff --stat` 为空。
- 模型版本：公开案例的 `TMElyralab/MuseTalk` revision `2bcb936e2fddb4d86db4c62fd45b387d0c061571` 及配套组件；十个文件 SHA256 与公开清单逐项核对。完整清单在 [model-audit.json](avatar-evidence-20261109/model-audit.json)。
- 输入底片：`d24-input.mp4`，512×512、25fps、91帧；SHA256 `895c94e8efff634b054abd17951e0c6e9cb8c1e864a0a9e4035b832f4a676a26`。
- 原语音：`d24-speech.wav`，单声道 16kHz，3.6318125 秒；SHA256 `89a902c22a5d0d75e8c37b1359ed5f71221d16f89fc9ca8e84b6ee1b336bec62`。
- 原始下载、输出、参数与配置来源均在 [配对案例](https://musetalkai.com/musetalk-vs-latentsync/)；原视频和语音不改字节，仅映射 Windows 路径。
- 参数：v15，FP16，batch=2，25fps，extra_margin=10，parsing_mode=jaw，左右 cheek=90，bbox_shift=0，无 CLI seed。
- 实际入口：`C:/AI/MuseTalk/.venv/Scripts/python.exe -m scripts.inference`。`run_replay.py` 保存了本轮完整命令，`replay-run.json` 记录启动和退出。
- 原样两次输出为 90 帧、视频轨 3.60 秒、音频约 3.632 秒。不同文件摘要是正常现象，不要求非确定性模型逐字节相同。

### 中文迁移与组合

1. `run_tts.py`：使用 edge-tts 7.3.1 原 CLI、`zh-CN-XiaoxiaoNeural`、默认语速和音高，逐句生成三段 MP3；另保留其句级 SRT。本次是在线服务，没有证明离线链路或永久稳定性。
2. FFmpeg 原生 concat 合并为单声道 16kHz PCM：`promotion.wav`，14.736 秒。页面时点取解码样本数，不用 MP3 容器填充估时。
3. `run_batch.py`：用同一个底片，在原生 YAML 中同时运行原案例第二次及中文音轨；不改网络或生成核心。产出 `replay-r2.mp4` 和 `avatar-promo-raw.mp4`。
4. `render_scenes.py`：用系统字体绘制三页介绍示意图和句级字幕；此环节是确定性排版，没有生成新的摄影图像。
5. `compose_demo.py`：FFmpeg 原生 trim/concat/scale/overlay 合成，人物连续讲解，页面在 3.76 和 9.28 秒切换，按 25fps 取最近帧；不拉伸语音、不改口型速度。

文案：

> 大家好，这是数字人介绍视频演示。
>
> 准备一段文案，就能搭配图片、演示文稿和功能画面。
>
> 更换文案后，同一个人物可以继续讲解，让重点更清楚。

## 成本和验收边界

| 项目 | 本轮观察 |
|---|---|
| 原样首次程序 | 02:43:173，含该次进程启动、模型载入、预处理、生成和封装；不含前期搜集和环境准备 |
| 原样第二次＋中文迁移批次 | 合计 03:36:944；共享同一进程中的模型，不能分摊后宣称某条单独耗时 |
| 三句 TTS | 00:04:537、00:03:593、00:02:682；不是完整交付耗时 |
| 本机页面合成 | 00:07:436；仅指已有口播和页面的合成，不含生成、研究、传输及审片 |
| 完整 T_VALID | 未认定：前期搜集起点未锁定，正常声画审片未完成 |
| 新增购买 | 本轮没有购买教程、整合包、API 或算力；本机电费/存储及服务长期可用性未测 |
| 画质 | 成片 720p 是排版画布；原人物 512p，MuseTalk 内部脸部区域 256p；不称原生高清脸部模型 |
| 视频/音频技术检查 | 原片、两次重放、中文原始口播和组合片均可完整解码；音轨留存和页面时点另有记录 |
| 图像对照 | 原样片与首次重放全帧 SSIM 0.995965；嘴部区域 0.987250；仅表示图像相近，不是口型准确率 |
| 重复对照 | 两次本机结果全帧 SSIM 0.996907；嘴部区域 0.987521；仅作重复产出结构证据 |
| 未完成 | 正常速度声画听审、逐句发音/口型主观验收、换人物、真实 PPT/录屏接入、长片、批量稳定性 |

正式宣传时的人像、音轨和各依赖分别使用适用授权素材；本次虚构头像样例只登记为功能演示素材，不推定已取得任意商业投放权。已有真人待机视频的场景，应优先沿模型支持的视频入口保留原自然动作；照片头像不自动获得眨眼、转头或手势能力。

完整实际命令、依赖、模型摘要、运行记录和技术检查保存在 [本轮证据目录](avatar-evidence-20261109/)，可读日志省略进度条，原生日志字节和摘要保留在本机。已经实际执行的最小组装脚本在 [配方脚本目录](../scripts/avatar-specialist-20261109/)。这些脚本重放当前固定环境和样例，不代表新电脑冷安装或任意素材已通过。

## 其他任务与原片进程

- 用户提供的剧情参考原片 `douyin_7705655755096984872_20261109-191648.mp4` 保留原文件和既有解析，时长 05:37:083，SHA256 `b124d0feffb7bf36b497a6a1b78214912858d99be8f5d708263e3adb2395e602`。本轮不继续生成剧情复刻；沿 [原片记录](TARGET-REALISTIC-DIALOGUE-20261109.md) 接续。
- Movie Builder、H3、换脸、换装、动作迁移和其他分类的原资料、已下载配方与缺项原位保留；不因本轮收窄而删除，也不将它们登记为已出片。
- 本轮优先级：固定头像中文介绍 → 正常声画验收 → 另一人物/自有素材及真实 PPT/录屏替换。先补最小缺项，不回到剧情制作或添加实时对话系统。

NEXT_PAGE_PROMPT：读取本文件、AVATAR-REALITY-20261109.json 和本机 Avatar-Specialist-20261109 原记录。继承原案两次实际输出及一次中文迁移，先正常速度复核 14.7 秒成片和左右原样对比；未过则查已知原配方条件或换现成成熟案例，禁止临时口型修补链。真实 PPT、客户图片、录屏、换人物和全身动作分别验收，不从示意图推定通过。其他路线留在原进程中。
