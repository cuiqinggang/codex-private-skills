# 2026-10-16 抖音下载故障与恢复证据

任务输入：https://v.douyin.com/x2jZ6T5FqOQ/
作品：7669298890101094769，标题“一句话让你的 Codex 拥有永久记忆”。
方法：用户指定《三人行》第2版；Windows 路由 V7，C 首选、A 暂停、B 备用。

## 已完成
通过已实测的 Seekin 网页获得本作品 720P 视频源，使用 C 通道既有 curl/ffprobe/FFmpeg 保存并完整解码。
文件：C:\Users\A\Desktop\douyin_7669298890101094769_720p.mp4
大小：2848345 字节；720×1280；31.114739 秒；H.264 + AAC。
SHA256：d50c9c3a8b701068210c69a1a7116ecaf89d451fb212f08dcf78c46210e994e3。
完整音视频解码退出码 0。随后经 C 独立回读文件存在、字节数、SHA256 与媒体元数据一致。
证据：本机 C:/AI/Douyin-Ultra-Direct/repair-20261016-download.json。
用户常用播放器目视和音画同步：NOT_VERIFIED，不能宣称 FINAL_VALID。

## 真实故障
- 18:49 原入口识别链接成功，主解析返回 HTTP502，随后503/ENDPOINT_CIRCUIT_OPEN；重试后仍502/503，不能假称本地修复了第三方服务。
- 旧备用 SSR 为 ITEM_LIST_EMPTY；旧浏览器配置 shared-mcp 被占用。
- 现有 mcp-persistent.config.json 指向 127.0.0.1:9223；已核实 Chrome151/CDP 可达。不得另开浏览器、关闭现有已登录浏览器或修改代理。
- C 大文件写入真实超时（call f72ba1ab-42c9-47d7-a171-25b5e5c4cf85）；随后 C 真实读取恢复。暂存写入不能当成代码已部署。
- B 运行身份 NETWORK SERVICE，不能执行 A 用户 AppData 中的 Python；复用已有 ComfyUI 便携 Python可运行，不改变ACL。
- 修复候选的五项回归在本地与 Windows均通过；真实全流程仍失败：本机 Seekin 页面未出现可用结果按钮。扩大至原配置30秒CDP超时后已能连接，但不能把连接通过等同于下载通过。
- B 各轮记录：38892938388（用户目录解释器拒绝访问）；38893135749（只读取证）；38893300720（源码字节门阻止覆盖）；38893451749（5秒CDP超时）；38893693263（连接成功但结果未出现）；38893966759（同输入完整复验仍失败）。

## 当前正式状态
DOWNLOAD_FILE=DECODE_PASS
DESKTOP_FILE_RECHECK=PASS
ONE_CLICK_REPAIR=NOT_PASSED
CANDIDATE_PRODUCTION_ACTIVATION=NO
原 run.py 已自动恢复，SHA256=de432acd2c3ead2faaf56eaaa91c0380d44676b3b7a98772b8c4e36cadbb94e7。
备份：C:/AI/Douyin-Ultra-Direct/repair-backup-b-20261016-r2/run.py。
候选仅供后续差分与复验，禁止覆盖正式 run.py 或宣传为已完成修复。临时测试标签页由候选清理，不改变既有页面；未修改 FlClash、系统代理、凭据或浏览器自启动。

## 接续
优先保留已下载文件，禁止无意义重下。主API正常时保留原高速路径。
GPT便利入口可采用已验证的 Seekin 网页→既有C通道保存/验收作为人工智能兜底；这不等价桌面双击自动修复。
若要继续修复一键入口，先读取最新实际浏览器/页面证据，定位本机结果为空的第一差分，不能反复加超时或更换未经验证的网站。任何新候选都须从同一输入完整复验后才能替换生产入口。
