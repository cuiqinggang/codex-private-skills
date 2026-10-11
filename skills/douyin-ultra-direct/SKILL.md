---
name: douyin-ultra-direct
version: "1.2.0"
description: 抖音极速直下双入口+快速恢复技能。保存已认证高速下载路线、Windows生产入口、GPT直接调用规则和恢复方法，禁止下次从零重建。
---

# 抖音极速直下 v1.2.0

STATUS=PASS_FROZEN
VERSION=1.2.0
AUTHORITY_REPO=cuiqinggang/codex-private-skills
AUTHORITY_PATH=skills/douyin-ultra-direct/

## 时间与用户路径口径

正式电脑端：
T_VALID = 4,428.736ms

定义：
READY_STATE = clipboard 已含抖音分享文本/短链
→ 正式桌面隐藏入口启动
→ 新桌面 MP4 FINAL_VALID

该时间不包含用户完成“复制链接”的人工时间；这是符合当前极限短时间引擎的电脑端统一计时口径。

用户侧不强制计人工手速，而走门禁：
USER_PATH=复制抖音分享文本/短链 → 双击桌面“抖音极速直下” → 自动完成
USER_PATH_GATE=PASS

如果未来候选让电脑端更快、但用户操作明显变复杂，则候选不得替代当前方案。

## 用户操作

正式主入口：

复制抖音分享文本/短链
→ 双击桌面“抖音极速直下”
→ 自动完成
→ 桌面得到新 MP4

GPT 便利入口：

复制抖音分享文本/短链
→ 对 GPT 说“下载抖音”
→ GPT 直接调用本技能
→ 桌面得到新 MP4

日常操作禁止要求用户：
- 打开解析网页；
- 再次粘贴 URL；
- 复制媒体 URL；
- 手工选清晰度；
- 手工登录；
- 执行命令行。

## 已认证高速核心

本地生产核心：
C:\AI\Douyin-Ultra-Direct\run.py

桌面生产入口：
C:\Users\A\Desktop\抖音极速直下.vbs

网络权威文件：
- SKILL.md
- run.py
- run-hidden.vbs
- restore.ps1
- RESTORE.md
- R2_REALITY_FREEZE.md

## 核心高速路线

clipboard
→ 复用有效 session
→ API parse
→ 从 media.streams 选择日常 720P 非水印 MP4，优先合理码率且小于约 120 MB 的流
→ 保留源流 HEVC/H.264，避免为兼容性默认进行无意义的高码率重编码
→ 同一流优先 www.douyin.com 官方 direct URL
→ direct 失败才回 CDN
→ curl 下载到程序 work 目录 .part（桌面仅发布验收通过的 MP4）
→ ffprobe 检查源文件；H.264 直接通过，HEVC 调用既有 FFmpeg 转 H.264（NVENC 优先，libx264 备用；声音保留 AAC）
→ ffprobe 验收 H.264 + AAC + 选定宽高 + duration>0；转码前后时长差≤0.25秒
→ os.replace 原子发布
→ FINAL_VALID

主路失败才调用既有成熟本地下载器 fallback。

## 关键经验

本次提速的主要来源不是省掉几十毫秒代码，而是换对传输路径。

同一媒体可能同时有：
- 慢 CDN；
- 备用 CDN；
- 官方 direct URL。

Reality 证明官方 direct URL 在本机/本次网络下可出现数量级吞吐改善。

因此恢复时禁止退化为：
- 默认第一个 CDN 永远直下；
- 每次三路完整测速；
- 浏览器作为主路径；
- yt-dlp Cookie 作为主路径。

## GPT 执行规则

当用户已复制抖音链接并要求“下载抖音”：

1. 优先使用在线 Windows 设备。
2. 用户消息已提供明确链接时可传入 `--url <分享链接>`，避免依赖剪贴板当前内容；桌面双击仍默认读取剪贴板。直接运行：
   C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe -X utf8 -B C:\AI\Douyin-Ultra-Direct\run.py
3. 若进程仍运行，只观察同一 PID，禁止重复启动。
4. 读取 C:\AI\Douyin-Ultra-Direct\last_run.json。
5. 只有 status=PASS 或 PASS_FALLBACK 且输出存在，才报告完成。

## 恢复认证

RESTORE_STATIC_GATE=PASS
REALITY_EXECUTED_DURING_RESTORE=NO

已实际验证 restore.ps1 可在本机：
- 恢复/校验核心；
- 恢复桌面隐藏入口；
- py_compile PASS；
- curl/ffprobe FOUND；
- fallback PRESENT；
- 不执行视频下载 Reality。

## 恢复触发

若用户说：
- “恢复抖音极速直下”
- “恢复这次高速下载方法”
- “把抖音下载器恢复回来”
- “重新装回这个技能包”

必须：

1. 先读本技能包与 RESTORE.md；
2. 使用共同工作区文件恢复；
3. 禁止从零重新搜索/研发下载方案；
4. 优先执行 restore.ps1 或等价确定性恢复；
5. 恢复后先静态门禁；
6. 只有用户要求重新认证性能时才做新 Reality。

## 边界

- 不修改 FlClash / Windows 网络代理。
- 不把 demo 密码、Cookie、密钥写进仓库。
- session.cookies 是本机运行态，不属于网络技能包。
- 外部 API/CDN 未来变化时允许最小修复，但保持用户入口不复杂化。

## HEVC 兼容修复（2026-10-09）

版本 1.1.1。症状：桌面出现 .mp4.part，无法双击播放。
已确认根因：源文件为完整 HEVC+AAC MP4；旧验收只接受 H.264，报 VIDEO_NOT_H264:hevc 后没有原子发布。禁止直接改后缀冒充兼容修复。

同一分享链接 https://v.douyin.com/4UUX9Y6VmK8/ 已从解析源头完整重跑 PASS：
- 作品 7694654845978164618；1080×1920；50.501995 秒；H.264+AAC。
- T_SYSTEM_VALID=41158.814ms，其中 NVENC 兼容转换 37448.939ms。
- 完整音视频解码 exit=0；三个回归测试 PASS（H.264 不转码、编码失败保留源文件、时长不匹配拒绝发布）。
- 4.428736 秒仅是原 H.264 历史样本，禁止套用于 HEVC 转码或所有链接。
- 转码会产生有损重编码且文件可能增大；不缩小分辨率，音频复制。
- 临时文件保留在程序目录，成功后仅在桌面发布 .mp4。

## 2026-10-11 日常画质默认策略修复（v1.2.0）

事实：作品 7693881321340423475、24 分 46.7 秒，原算法默认最高分辨率 3840×2160，229.34 MB 的 HEVC 源经无必要 H.264/NVENC 高码率重编码变成 3,372,228,149 字节，累计 14 分 45.765 秒。属于默认档位及转码策略失误，不能将 4K 转码结果作为日常下载的推荐版本。

修复：默认选用不高于 1280×720 的无水印 MP4，并优先选同档位、解析器所报大小不超过 120,000,000 字节且码率相对较好的流；保留原始高压缩 HEVC/H.264 视频和 AAC 音频，不做不必要的 H.264 转码。仅原始格式完整验证通过才能原子发布至桌面。若使用者要求通用播放器兼容，应单独提供兼容转码选项或明确提示需要 HEVC 解码能力；不可把 HEVC 简单等同于所有 Windows 播放器可播放。

本链接现实复测：所选 1280×720 / 95,792,350 字节 / HEVC+AAC，真实下载 `T_VALID_MS=27084.918`，输出 `C:\Users\A\Desktop\douyin_7693881321340423475_20261011-195601.mp4`，`status=PASS`，`ffprobe duration=1486.703991`。播放器人工验证尚未完成。用户入口仍为复制链接、双击桌面入口、桌面 MP4，不改 FlClash/代理、不重写流程。历史 v1.1.1 性能数字仍属旧样本，不能当作新默认模式的速度保证。

注意：120MB 仅为默认优选阈值，不是下载硬性上限；不达条件时按最低可用合理清晰度回退。未来应按视频时长和可用流清晰度选择适配码率，并单独检验兼容性。
