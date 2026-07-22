---
name: download-douyin-to-desktop
description: 使用已实测的 GreenVideo 网页把有权保存的公开抖音作品下载到 Windows 真实桌面“抖音下载”。用户说“下载这个抖音”“把这个抖音视频保存到桌面”“下载这条抖音链接”“保存这个抖音图集”，或提供 douyin.com、v.douyin.com、iesdouyin.com、dy.tt 分享文字时使用。
---

# 下载抖音到桌面

仅处理用户本人、已获授权或依法允许保存的公开内容；不得绕过付费、私密访问、DRM、验证码或平台权限。

日常下载只运行一个执行智能体，按以下顺序完成：

1. 将用户的整段分享文字作为 `-InputText` 传给本技能脚本，并加 `-PrepareBrowser`。只在返回 `STATUS=BROWSER_READY` 后继续，保存返回的 `SESSION_ID`。如果识别为主页、合集或批量链接，先说明预计数量并取得确认。
2. 使用 Chrome 浏览器能力打开 `https://greenvideo.cc/douyin`。只把已验证的抖音公开网址填入输入框，点击“开始”。不得提交 Cookie、账号资料或本地文件。
3. 解析完成后点击“视频”一栏的“点击下载”。认领新打开的媒体标签，确认当前网址是 HTTPS、页面存在唯一 `<video>`，并截图确认视频正在播放。
4. 优先对唯一 `video` 定位器调用浏览器的 `downloadMedia()`。若该能力不可用，聚焦播放页后发送 `Ctrl+S`；系统“另存为”窗口出现时保存到返回的 `DESTINATION`。出现验证码时必须让用户接管，不得绕过。
5. 等待浏览器下载结束，再以相同 `-InputText`、`-FinalizeBrowser` 和 `-SessionId` 调用脚本。脚本只接收本会话开始后新增且通过 ffprobe 的唯一视频，校验大于 100KB、时长大于 0、存在视频流、SHA-256 一致，然后移动到真实桌面“抖音下载”。
6. 只有脚本返回 `STATUS=PASS` 才能报告成功。回复作品标题、文件类型、文件大小、实际保存路径、来源网址和引擎 `GreenVideo Browser`。不得把解析成功、在线播放或临时文件说成下载成功。

调用入口：

```powershell
${REDACTED_SECRET}
```

浏览器下载完成后：

```powershell
${REDACTED_SECRET}
```
