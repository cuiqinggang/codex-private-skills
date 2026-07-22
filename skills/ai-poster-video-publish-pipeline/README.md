# AI海报视频制作与审核后自动发布技能包

## 新手如何使用

准备 5 项信息：宣传主题、宣传图/能力图要求、平台版本要求、发布文案、是否允许审核后自动发布。然后按 `RUNBOOK.md` 的 G01-G10 执行。

推荐目录结构：

```text
work/
  input/
    00-promo-wechat.png
    00-promo-douyin.png
    01-student-learning.png
    02-family-tutoring.png
    03-office-productivity.png
    04-content-creation.png
    05-local-business.png
    06-teacher-knowledge.png
    07-design-creativity.png
    08-life-assistant.png
    09-complex-task.png
  output/
  publish_package/
  reports/
```

## 输入图片放哪里

把图片放到本次任务的 `input/` 目录。宣传图必须分微信版和抖音版：微信版可以带联系方式，抖音版不得含电话、微信、二维码、可微我、加我等导流信息。能力图只展示 AI 能力，不放联系方式。

## 配置文件怎么写

复制 `templates/config.full.json` 或 `templates/config.short.json` 到本次任务目录，修改 `slides[].file` 为 `input/` 里的文件名，修改 `output` 为目标 MP4 路径。full 版保留宣传图首尾重复；short 版保留核心能力图。

## 如何生成视频

```powershell
.\scripts\build-slideshow.ps1 -ConfigPath .\templates\config.full.json -InputImageFolder .\work\input -OutputPath .\work\output\full.mp4
.\scripts\build-slideshow.ps1 -ConfigPath .\templates\config.short.json -InputImageFolder .\work\input -OutputPath .\work\output\short.mp4
```

脚本输出 1080x1920、30fps、H.264 MP4，默认稳定静态展示，只使用淡入淡出。

## 如何生成发布包

```powershell
.\scripts\prepare-publish-package.ps1 `
  -DouyinVideo .\work\output\full-douyin.mp4 `
  -WechatMomentsVideo .\work\output\full-wechat.mp4 `
  -WechatGroupsVideo .\work\output\short-wechat.mp4 `
  -DouyinCaption .\templates\douyin-caption.txt `
  -WechatMomentsCaption .\templates\wechat-moments-caption.txt `
  -OutputRoot .\work\publish_package
```

输出目录包含 `douyin`、`wechat_moments`、`wechat_groups` 三个包。

## 如何审核

先运行：

```powershell
.\scripts\validate-video.ps1 -VideoPath .\work\output\full-douyin.mp4 -ReportDir .\work\reports
.\scripts\check-platform-package.ps1 -PackagePath .\work\publish_package -ReportPath .\work\reports\platform-check.json
```

再人工检查图片、视频、标题、文案、联系方式、免费/3000元表述、视频稳定性、首尾宣传图。审核通过后，复制 `templates/publish-approved.template.json` 为本次任务的 `publish-approved.json` 并填写真实范围。

## 如何执行审核后自动发布

只有 `publish-approved.json` 同时满足 `approved_by_user=true` 和 `allow_auto_click_publish=true`，才允许自动打开官方平台入口或已登录官方客户端执行上传、填写、点击发布。遇到验证码、人脸、短信、安全提示、违规提示、付费推广、删除文件、批量私信、批量群发陌生对象，必须停止。

## 输出文件在哪里

- 视频：本次任务 `output/`。
- 平台发布包：本次任务 `publish_package/`。
- 审核文件：本次任务 `publish-approved.json`。
- 发布证据：本次任务 `reports/`。
- 最终报告：本次任务 `reports/final-report.md`。
## 2026-05-31 Audio Update

If the user wants music, the final deliverable should not stay silent. Use `AUDIO-GUIDE.md`.

Default rule: reuse an existing good local soundtrack or user-provided music. Do not default to crude generated tones or simple oscillator music. The 2026-05-31 case proved that such music can pass technical checks but still sound bad.

Example:

```text
examples/ai-promo-ppt-style-video-20260531
```
