# 已验成熟节点：Remotion官方播客模板

状态：`PASS_WITH_SCOPE`，2026-11-08，北京时间。用途：原工程的音频可视化、已有字幕渲染与带声导出。只覆盖已验证的固定案例。

## 完整配方

- 作者与原工程：https://github.com/remotion-dev/template-audiogram 。官方预览与说明：https://www.remotion.dev/templates/audiogram 。
- 源码提交：`dee9f3619127b8853a1e6cf8882332d9d332c32d`。本机跟踪源码未修改。
- 本机工程：`C:\AI\Video-Recipe-Reproduction-20261108\Mature-AV-R2\upstream-audiogram`。
- 输入：原工程public目录的dialogue.wav、captions.json与原图等。28项源码/素材SHA见同级 `upstream-file-manifest.json`，依赖锁定到已保存package-lock.json。
- 环境：Windows10，本机现有Node v24.14.0、npm11.9.0；项目Remotion4.0.541。锁文件SHA：`cd376a4bb8b4c0a48ff92b8231e4f4c86e3a73447bc37bab5089d3aa1b4e5146`。
- 初次按作者npm install配置，复用当前已安装环境；完整执行命令：`npx remotion render src/index.ts Audiogram <独立输出.mp4>`。无人为任务墙钟截止，不修改现有硬件性能保护。
- 原固定案例完整输出：1080×1080、30fps、814帧、27.136秒H.264/AAC。两次完整渲染均正常退出，00:49:074、00:43:968；初次工程/环境准备另计，完整T_VALID未建立。
- 首次输出SHA：`74ba19c6ff671c8804b67ae6733f1524b823e1ae7a81334256ccd3bc891887c0`。

## 验收与边界

两份完整视频解码无错误，814帧逐一对照，平均SSIM0.996698、最低0.994275；并非逐像素相同。两次解码音频相同，与原音频相关系数0.999865。复核3.5、9、17、25秒真实帧：原图和标题保持、字幕可读、所查帧无可见裁切。音画是作者原模板定义，不含人物口型任务。

复跑前先核对源提交、原输入、锁文件与输出，不重新下载环境或重复已通过工作。复用已安装工程时使用独立输出名。重装、换音频/字幕、改语言、换版式、自动转录及客户实际交付另验；不据此扩大到其他视频生成能力。

证据根：工程父目录；回执 `audiogram-full-run.json`、`full-verification.json`；成片 `Audiogram-Official-Full-R1.mp4`、`Audiogram-Official-Full-R2.mp4`。当前路线报告：https://chatgpt.com/library?file_id=libfile_fde3_f-12d10efbb39c819190b0c36ca84565bd_937029f1505c8191917e0968911c47f5&account_id=personal 。
