---
name: video-universal-download
description: 跨站视频下载与按需交给 Codex 分析的轻量技能。用户给视频网址时优先调用本机 yt-dlp；只要文字时复用现有转写工具；需要视听联动时交由 Codex 组织画面、字幕、音频联合分析。兼容《三人行》第3版和 Windows 执行桥 V9.0。
---
# 跨站视频获取与 Codex 分析｜V1.0
状态：方案已登记；本机已发现 yt-dlp 2026.08.19 和 FFmpeg 8.1.1；跨站业务验收未完成，不能宣称生产成功率。
## 范围
- 输入：一个或多个可合法访问的视频 URL，或已有的本地视频文件。
- 默认输出：仅视频文件。禁止默认运行语音转写或 AI 分析。
- 用户仅要文字：优先已有字幕；否则调用用户本机现成文字提取/转写能力，不部署另一套重复服务。
- 用户要视频深度分析：由 Codex 执行/编排，联合转写文字、视频关键画面及必要音频证据，不能只靠字幕概括视觉内容；输出注明来源和无法确认项。
## 执行原则
1. 首先读取 skills/artificial-single-page-extreme-time-engine/SKILL.md 及《三人行》第3版；Windows 执行桥以 skills/gpt-windows-execution-bridge/SKILL.md 的 V9.0 为准，优先 C 再按桥规范降级。不得修改 FlClash、系统代理、浏览器环境；不得导出或记录登录 Cookies/Token。
2. 先复用已安装的 yt-dlp 和 FFmpeg，使用 yt-dlp --version、ffmpeg -version 只读确认。
3. 抖音默认保留现有“一键下载”入口；跨站调用 yt-dlp，不覆盖原脚本。遇失败按已知故障类型分析，再选择备用路径；不得承诺网站必然可下载。应遵守网站规则、版权及权限边界。
4. 优先简单可复现的直接命令，禁止无必要重装依赖、重新发明下载器或修改代理。对单视频禁用误下载整个播放列表：--no-playlist。使用受控输出目录、合理文件名与有界超时。
5. 可先用 yt-dlp --simulate --print title URL 做无下载探测；正式下载示例：yt-dlp --no-playlist -P "$HOME\\Desktop" -o "%(title).180B [%(id)s].%(ext)s" "URL"。当需要合并音视频，依赖 FFmpeg。
6. 若需要文本，先检测字幕资源；需要 AI 分析时调用 Codex，不默认替换为 DeepSeek。Codex 的视频分析取决于工具接入；不能假设它能直接理解任意 MP4。
7. 日志区分：模拟可提取 / 真正下载完成 / 文件可解码 / 内容分析通过。须提供实际产物路径和运行证据，禁止将模拟、安装成功当最终验收。
## 当前验收基线
2026-10-17 通过 Windows 执行接口检测：yt-dlp=2026.08.19；FFmpeg 可执行文件位于 WinGet 管理目录，版本路径为 8.1.1；Git=2.53.0；未进行跨站真实下载测试。
## 参考
- https://github.com/yt-dlp/yt-dlp
- https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- https://github.com/yt-dlp/yt-dlp/wiki/FAQ
