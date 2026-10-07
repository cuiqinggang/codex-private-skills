---
name: douyin-ultra-direct
version: "1.0.0"
description: 抖音极速直下双入口技能。用户已复制抖音分享文本/短链后，可由 GPT 直接调用 Windows 本地下载核心；同一核心也支持桌面双击。
---

# 抖音极速直下

STATUS=PASS_FROZEN
VERSION=1.0.0
REALITY_ENTRY_TO_FINAL_VALID_MS=4428.736
CORE=C:\AI\Douyin-Ultra-Direct\run.py
HIDDEN_LAUNCHER=C:\AI\Douyin-Ultra-Direct\run-hidden.vbs
PRODUCTION_DESKTOP_ENTRY=C:\Users\A\Desktop\抖音极速直下.vbs
OUTPUT=C:\Users\A\Desktop\douyin_<content_id>_<timestamp>.mp4

## 用户操作

首选两种等价入口，共用同一核心：

1. 桌面入口：复制抖音分享文本/短链 → 双击“抖音极速直下” → 自动完成。
2. GPT 入口：复制抖音分享文本/短链 → 对 GPT 说“下载抖音” → GPT 直接调用本技能，不要求用户再次粘贴链接。

禁止把网页打开、API 地址、Cookie、媒体 URL、命令行参数暴露给用户作为日常操作步骤。

## GPT 执行规则

当用户明确要求下载剪贴板里的抖音链接时：

1. 使用当前在线 Windows 设备 DESKTOP-4A1EGTM。
2. 直接启动：
   C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe -X utf8 -B C:\AI\Douyin-Ultra-Direct\run.py
3. 若进程仍运行，只轮询同一 PID；禁止重复启动。
4. 读取 C:\AI\Douyin-Ultra-Direct\last_run.json。
5. 仅当 status=PASS 或 PASS_FALLBACK 且桌面输出存在时，向用户报告完成。
6. 用户不需要提供 API Key、Cookie 或打开网页。

## 核心路线

API parse → 最高分辨率非水印 MP4 → 同分辨率优先较大体积/较高码率的 H.264 候选 → 官方 direct URL 优先 → curl 下载到 .part → ffprobe 校验 H.264+A​AC+选定宽高 → 原子发布到桌面。
认证会话优先复用；失效时自动刷新。
主路失败才调用既有成熟本地下载器作为 fallback。

## 边界

- 不默认使用 HEVC。
- 不做 SHA256 热路径校验。
- 不做三路 CDN 每次测速。
- 不让用户手工选择 URL。
- 不让用户手工登录。
- 不修改 FlClash / Windows 网络代理。