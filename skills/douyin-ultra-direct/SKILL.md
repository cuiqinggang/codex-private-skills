---
name: douyin-ultra-direct
version: "1.1.0"
description: 抖音极速直下双入口+快速恢复技能。保存已认证高速下载路线、Windows生产入口、GPT直接调用规则和恢复方法，禁止下次从零重建。
---

# 抖音极速直下 v1.1

STATUS=PASS_FROZEN
VERSION=1.1.0
AUTHORITY_REPO=cuiqinggang/codex-private-skills
AUTHORITY_PATH=skills/douyin-ultra-direct/

## 时间口径

已认证：
T_SYSTEM_VALID = 4,428.736ms

定义：
clipboard 已含抖音分享文本/短链
→ 正式桌面隐藏入口启动
→ 新桌面 MP4 FINAL_VALID

注意：
该 4.428736s 不包含用户在抖音中完成“复制链接”的时间。
因此：
T_USER_VALID=UNMEASURED

以后比较完整用户方案时，必须从用户第一现实动作开始计时，不能把 T_SYSTEM_VALID 冒充完整用户 T*。

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
→ 从 media.streams 选择最高分辨率非水印 MP4
→ 同分辨率优先较大 size_bytes / bitrate，避免误选低码率 HEVC
→ 同一流优先 www.douyin.com 官方 direct URL
→ direct 失败才回 CDN
→ curl 下载到 .part
→ ffprobe 验收 H.264 + AAC + 选定宽高 + duration>0
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
2. 直接运行：
   C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe -X utf8 -B C:\AI\Douyin-Ultra-Direct\run.py
3. 若进程仍运行，只观察同一 PID，禁止重复启动。
4. 读取 C:\AI\Douyin-Ultra-Direct\last_run.json。
5. 只有 status=PASS 或 PASS_FALLBACK 且输出存在，才报告完成。

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
