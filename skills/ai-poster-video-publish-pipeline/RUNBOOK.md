# RUNBOOK

本 Runbook 使用一个清晰门控推进。Level 0-2 自动执行；Level 3 或安全阻断停止。禁止真实发布，除非用户另行明确授权。

## G01 收集/生成素材

- purpose: 收集宣传主题、宣传图要求、能力图要求、平台版本、发布文案、自动发布授权意向。
- execution location: 本次任务工作目录。
- command or action: 建立 `input/`、`output/`、`publish_package/`、`reports/`，放入微信版宣传图、抖音版宣传图和能力图。
- success criteria: 微信宣传图、抖音宣传图、能力图清单齐全；宣传图和能力图分离。
- failure criteria: 抖音宣传图仍含电话、微信、二维码、可微我、加我；能力图混入联系方式。
- recovery: 回到图片生成或人工修图；抖音版重新去联系方式。
- continue/stop: 素材齐全继续；导流信息无法去除则 STOP。

## G02 生成平台版本

- purpose: 生成抖音安全版和微信可转化版素材集合。
- execution location: 本次任务工作目录。
- command or action: 抖音用无联系方式宣传图，微信用用户审核过的联系方式宣传图，能力图两端复用。
- success criteria: `input/douyin` 和 `input/wechat` 清楚分离。
- failure criteria: 抖音包混入微信版宣传图或联系方式。
- recovery: 替换抖音宣传图，重新检查关键词。
- continue/stop: 平台分离清楚继续；混用无法确认则 STOP。

## G03 生成轮播视频

- purpose: 生成 full/short 竖屏图片轮播视频。
- execution location: 技能包根目录或本次任务目录。
- command or action: `scripts/build-slideshow.ps1 -ConfigPath templates/config.full.json -InputImageFolder <input> -OutputPath <output.mp4>`。
- success criteria: 输出 1080x1920、30fps、H.264 MP4；full 版 40-55 秒；short 版 25-35 秒。
- failure criteria: ffmpeg 失败、图片缺失、视频非 H.264、时长或分辨率不符。
- recovery: 修正配置路径、图片文件名或依赖；重新生成。
- continue/stop: 视频生成继续；依赖缺失且无法修复则 STOP。

## G04 验证视频

- purpose: 验证视频参数、抽帧和画面稳定性。
- execution location: 本次任务目录。
- command or action: `scripts/validate-video.ps1 -VideoPath <output.mp4> -ReportDir reports`。
- success criteria: ffprobe PASS，生成 `video-validation.json`、`frames*.jpg`、`contact-sheet.jpg`。
- failure criteria: 参数不符、抽帧失败、文字被裁切、画面抖动或发虚。
- recovery: 关闭动效，改静态展示；修正图片适配和配置。
- continue/stop: 验证 PASS 继续；画面不稳则 STOP 并重做。

## G05 生成发布包

- purpose: 生成抖音、微信朋友圈、微信群三个发布包。
- execution location: 本次任务目录。
- command or action: `scripts/prepare-publish-package.ps1 -DouyinVideo <mp4> -WechatMomentsVideo <mp4> -WechatGroupsVideo <mp4> -OutputRoot publish_package`。
- success criteria: `publish_package/douyin`、`publish_package/wechat_moments`、`publish_package/wechat_groups` 都含视频、文案、封面或清单。
- failure criteria: 包缺视频、缺文案、抖音包混入联系方式、微信群缺白名单。
- recovery: 重新复制资产或生成白名单模板。
- continue/stop: 包完整继续；抖音导流信息命中则 STOP。

## G06 内容审核

- purpose: 人工审核图片、视频、标题、文案、平台版本、联系方式、敏感信息和免费/3000元表述。
- execution location: 本次任务目录和用户可见媒体播放器/图片查看器。
- command or action: 查看 `contact-sheet.jpg`、视频、caption 和 checklist；运行 `scripts/check-platform-package.ps1`。
- success criteria: 抖音无联系方式；微信联系方式已确认；文案不过度夸张；保留博士级专家AI、免费/3000元价值点；首尾宣传图存在。
- failure criteria: 抖音含导流信息、微信联系方式未经确认、视频不清楚或不稳。
- recovery: 修图、改文案、重建发布包并重新审核。
- continue/stop: 人工审核通过继续；否则 STOP。

## G07 生成 publish-approved.json

- purpose: 把人工审核结果固化为自动发布授权文件。
- execution location: 本次任务目录。
- command or action: 复制 `templates/publish-approved.template.json` 为 `publish-approved.json`，填写 `task_id`、`approved_scope`、`approved_assets`、`allow_auto_click_publish`。
- success criteria: `approved_by_user=true`，授权范围和资产路径准确，禁止动作完整。
- failure criteria: 文件缺失、范围不清、资产不存在、`allow_auto_click_publish` 未明确。
- recovery: 回到用户审核确认，重新填写。
- continue/stop: 授权明确继续；没有授权文件则 STOP。

## G08 审核后自动发布

- purpose: 在内容审核通过后自动完成上传、填写、点击发布。
- execution location: 官方抖音创作者服务平台、已登录官方客户端或已登录桌面微信。
- command or action: 读取 `publish-approved.json`；按授权范围打开官方入口，上传视频、填标题/简介、选封面，允许时自动点击发布。
- success criteria: 发布完成后截图、记录 URL/作品 ID/时间和平台回执。
- failure criteria: 验证码、人脸、短信、安全提示、违规提示、付费推广、扣费按钮、账号设置、群名不在白名单。
- recovery: 停止并让用户处理平台验证或授权；不要绕过风控。
- continue/stop: 机械发布成功继续归档；任何高风险动作 STOP。

## G09 发布证据归档

- purpose: 保存发布证据，避免只口头报告。
- execution location: 本次任务 `reports/`。
- command or action: 保存 `douyin-posted-screenshot.png`、`wechat-moments-posted-screenshot.png`、`publish-log.md`、`publish-result.json`。
- success criteria: 每个平台有截图和日志，结果 JSON 写明成功/失败/停止原因。
- failure criteria: 无截图、无日志、发布状态不确定。
- recovery: 重新观察官方页面或客户端；无法确认则标记 UNKNOWN，不得伪造成功。
- continue/stop: 证据齐全继续最终报告；证据不足则 STOP。

## G10 最终报告

- purpose: 汇总输入素材、视频路径、发布包路径、审核结果、发布结果、截图证据和异常情况。
- execution location: 本次任务 `reports/final-report.md`。
- command or action: 写最终报告，附 `validate-video`、`check-platform-package`、`verify-skill-package` 证据。
- success criteria: 报告列明文件、命令、PASS/FAIL、跳过项、残余风险、回滚路径。
- failure criteria: 未验证就宣布 PASS，缺关键路径或缺证据。
- recovery: 补跑验证，补截图，或把状态降为 FAIL/UNKNOWN。
- continue/stop: 报告完成后结束。

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
## G05A Add Background Music When Requested

- purpose: Add pleasant, background-level music to the final promo video when the user requests music or prior runs establish music as expected.
- execution location: current task workspace.
- command or action: first search for user-provided audio or prior local videos with acceptable audio; extract and trim existing audio; apply fade in/out; lower volume; mux with the base MP4.
- success criteria: final `_with_music.mp4` exists; ffprobe shows both video and audio streams; duration matches the base video; volume is background-level; the track is not crude, harsh, or monotonous.
- failure criteria: final video is silent; audio is technically valid but unpleasant; crude oscillator/procedural music is used without explicit user approval; volume is too loud or clips.
- recovery: replace the audio with an existing good local soundtrack or user-provided music; produce another `_with_music.mp4`; keep the rejected attempt documented in the report if it affected the run.
- continue/stop: continue after audio technical checks and listening/known-good-source check pass; if no acceptable music source exists, report that and keep a silent version instead of inventing bad music.

Reference: `AUDIO-GUIDE.md` and `examples/ai-promo-ppt-style-video-20260531`.
