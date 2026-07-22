---
name: ai-poster-video-publish-pipeline
description: Use when creating AI promotional posters, AI capability images, stable image slideshow videos, Douyin and WeChat separated publish packages, content review approval JSON, post-review auto-publish execution, and publish evidence archives.
---

# AI海报视频制作与审核后自动发布技能包

## 目标

把“文字想法整理 -> 宣传图/能力图制作规划 -> 图片版本分离 -> 图片轮播视频生成 -> 平台发布包生成 -> 内容审核 -> 审核通过后自动发布 -> 发布证据归档”做成可复用、可更新、可验证、可审计的流水线。

## 输入

每次使用本技能包时，先收集 5 项输入：

1. 宣传主题。
2. 宣传图/能力图要求。
3. 平台版本要求，例如抖音、微信朋友圈、微信群。
4. 发布文案。
5. 是否允许审核后自动发布。

## 输出

- 内容规划：宣传图规划、能力图规划、平台差异、视频顺序、文案方向。
- 图片资产：微信版宣传图、抖音安全版宣传图、能力图。
- 轮播视频：full 版和 short 版 MP4。
- 平台发布包：`publish_package/douyin`、`publish_package/wechat_moments`、`publish_package/wechat_groups`。
- 审核文件：`publish-approved.json`。
- 发布证据：截图、日志、`publish-result.json`、最终报告。

## 适用场景

- AI学习资料、AI能力展示、课程资料、免费教学、线下转化类宣传。
- 需要同一套素材生成抖音安全版和微信可转化版。
- 需要把图片做成稳定、清楚、不晃动的竖屏轮播视频。
- 需要人工只审核内容，审核通过后自动完成上传、填写和点击发布。

## 不适用场景

- 未经用户审核就直接发布。
- 平台要求验证码、人脸、短信、安全验证、账号设置、付款或风控处理。
- 批量私信陌生人、自动加好友、自动评论引流、群控群发。
- 删除旧作品、删除素材、修改生产配置或读取密钥。

## 核心流程

1. 整理用户文字想法，形成宣传目标和素材清单。
2. 规划宣传图和能力图：宣传图负责转化，能力图负责展示 AI 实力。
3. 生成/收集图片，并强制分出微信版宣传图、抖音版宣传图、能力图。
4. 按固定顺序生成轮播视频：宣传图开场 -> 能力图依次展示 -> full 版宣传图收尾。
5. 生成平台发布包。
6. 运行内容审核门控。
7. 审核通过后生成 `publish-approved.json`。
8. 仅当 `allow_auto_click_publish=true` 时执行审核后自动发布。
9. 发布后截图和日志归档。
10. 输出最终报告和 PASS/FAIL 证据。

## 微信版/抖音版区别

- 微信版宣传图可以保留电话、微信、可微我等联系方式，但必须由用户审核确认。
- 抖音版宣传图必须去掉电话、微信、二维码、可微我、加我、联系我等站外导流信息。
- 能力图默认不含联系方式，避免平台混用和审核风险。
- 抖音包必须运行导流关键词检查；发现疑似导流内容必须 STOP。

## 宣传图与能力图分离原则

宣传图负责“免费 / 3000元 / AI学习资料 + 免费教学 / 联系方式或留言动作”等转化信息。能力图负责展示学生学习、家庭辅导、职场办公、内容创作、本地商家、教师知识整理、设计创意、生活助理、综合复杂任务等 AI 能力场景。不要把联系方式混入能力图。

## 视频制作原则

- 输出 1080x1920、30fps、H.264 MP4。
- full 版 40-55 秒，short 版 25-35 秒。
- 默认静态稳定展示，只允许淡入淡出。
- 禁止抖动、晃动、漂移、随机平移、快速缩放、旋转、翻页、弹跳、震动。
- 如需极轻微放大，只允许 100% 到 102%，且验证不抖才允许。
- 非 9:16 图片使用模糊背景 + 前景完整图，不能拉伸变形。
- 不得裁切标题、底部、电话、免费、3000元等关键信息。

## 发布审核原则

人工审核只发生在内容审核阶段。审核内容包括图片、视频、标题、文案、平台版本、联系方式、敏感信息、免费/3000元表述、视频稳定性和首尾宣传图是否出现。没有 `publish-approved.json` 不允许自动发布。

## 审核后自动发布原则

内容审核通过后，上传、填写、点击发布属于机械执行，不再要求用户在平台页面手动点发布。自动发布前必须读取 `publish-approved.json`，确认 `approved_by_user=true` 且 `allow_auto_click_publish=true`。发布后必须截图和记录结果。

## 风险停止条件

遇到验证码、人脸、短信、安全提示、违规提示、付费推广、删除文件、批量私信、批量群发陌生对象、修改账号设置、扣费按钮、非官方群控工具、密钥读取或任何平台风控提示，必须停止等待用户处理。

## 硬规则

1. 宣传图和能力图必须分离。宣传图负责转化，能力图负责展示AI实力。
2. 宣传图必须有微信版和抖音版。微信版可带联系方式；抖音版不得含电话、微信、二维码、可微我、加我等导流信息。
3. 视频第一张必须是宣传图。目的是让用户先看到免费、3000元、核心利益点。
4. full版视频最后必须再次出现宣传图。目的是看完能力展示后再次回到转化信息。
5. 视频默认稳定静态展示，只允许淡入淡出。禁止抖动、晃动、漂移、随机平移、快速缩放、旋转、翻页、弹跳、震动。
6. 如果任何动效导致文字发虚或画面不稳，必须关闭动效，改为静态展示。
7. 抖音包必须自动检查导流信息。发现电话、微信、二维码、可微我、加我等内容必须 STOP。
8. 内容审核通过后，自动发布属于机械执行，不需要用户再手动点发布。
9. 遇到验证码、人脸、短信、安全提示、违规提示、付费推广、删除文件、批量私信、批量群发陌生对象，必须停止等待用户处理。
10. 微信群只允许白名单群。禁止自动群发所有群，禁止自动私信所有好友。
11. 发布后必须截图留证，不能只口头报告“已发布”。
12. 任何最终 PASS 必须有验证脚本或确定性清单证据。

## 验证标准

- `scripts/verify-skill-package.ps1` 必须 PASS。
- 视频必须通过 `scripts/validate-video.ps1` 的 ffprobe 参数检查，并生成抽帧和 contact sheet。
- 抖音包必须通过 `scripts/check-platform-package.ps1` 的无联系方式检查。
- 发布前必须存在人工审核生成的 `publish-approved.json`。
- 发布后必须存在截图证据、发布日志和结果 JSON；不允许伪造发布成功。

## 关键文件

- `RUNBOOK.md`：G01-G10 实操门控。
- `PLATFORM-RULES.md`：抖音、微信朋友圈、微信群规则。
- `CONTENT-REVIEW-GATE.md`：内容审核门控。
- `AUTO-PUBLISH-GATE.md`：审核后自动发布门控设计。
- `VIDEO-SPEC.md`：视频规格和稳定展示规则。
- `PROMPT-TEMPLATES.md`：图片、视频、文案和 7 天内容计划模板。
- `templates/`：配置和文案模板。
- `scripts/`：视频生成、验证、平台包检查、发布包生成、技能包验证脚本。
## 2026-05-31 Audio Quality Addendum

For PPT-style promo videos, audio is part of final acceptance. If the user asks for music, do not ship a silent final video and do not use crude oscillator/procedural music as the default. Prefer existing good local music or an already acceptable soundtrack from a prior local video.

Read `AUDIO-GUIDE.md` before adding background music. The 2026-05-31 example in `examples/ai-promo-ppt-style-video-20260531` records the failure and correction:

- failed: simple Python-generated tones technically passed but sounded unpleasant and monotonous
- accepted: reused an existing soundtrack from a prior local video, trimmed it, faded in/out, lowered volume, and muxed it as AAC
- verification: ffprobe audio stream check plus volume check plus subjective/listening quality gate

## 2026-07-07 GPT 10s Real Promo Script Pack Addendum

When the user asks for a 10-second viral promo script, a GPT handoff pack, or a short real-material promo video for free AI learning materials / free teaching, first create a compact script-generation material pack before making a video.

Use:

- `references/gpt-10s-real-promo-script-pack-20260707.md`

Hard rule: do not ask GPT to generate music. GPT may describe the desired music mood, but final background music must come from a previously verified comfortable local track, a user-provided track, or another human-approved source. If no good music is available, keep a silent or voice-only version rather than using bad generated music.

The minimum GPT handoff pack must include:

- 10-second creative brief
- hook / proof / value / CTA structure
- per-second storyboard
- voiceover copy
- on-screen subtitles
- source asset index
- audio rule saying verified music only, no generated music
- acceptance checklist
