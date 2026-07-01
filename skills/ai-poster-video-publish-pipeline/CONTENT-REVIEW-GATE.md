# CONTENT REVIEW GATE

## 原则

人工审核只发生在内容审核阶段。审核通过后，上传、填写、点击发布属于机械执行；但没有 `publish-approved.json` 不允许自动发布。

## 审核内容

- 图片：宣传图、能力图、封面。
- 视频：full/short 版本、首尾宣传图、稳定性、清晰度、是否裁切。
- 标题和文案：抖音标题、抖音简介、朋友圈文案、微信群文案。
- 平台版本：抖音、微信朋友圈、微信群是否分离。
- 联系方式：抖音不得有联系方式；微信必须确认是否允许联系方式。
- 敏感信息：电话、微信、二维码、可微我、加我、过度承诺、违规词。
- 价值表达：免费/3000元表述是否准确，不夸大。
- 价值感：是否保留“博士级专家AI”的价值感。

## 抖音必检

- 抖音包必须通过无联系方式检查。
- 检查项包括电话、微信、二维码、可微我、加我、联系我、扫码、VX、V信、WeChat。
- 运行 `scripts/check-platform-package.ps1 -PackagePath publish_package -ReportPath reports/platform-check.json`。
- 发现任何导流信息必须 STOP，不能生成发布授权。

## 微信必检

- 微信朋友圈可以保留联系方式，但必须用户审核确认。
- 微信群只允许白名单群，不允许群发所有群。
- 微信包应标记是否含联系方式，并在 checklist 中记录。

## publish-approved.json

审核通过后生成：

```json
{
  "task_id": "AI_POSTER_VIDEO_TASK_YYYYMMDD",
  "approved_by_user": true,
  "approved_scope": ["douyin", "wechat_moments"],
  "allow_auto_click_publish": true,
  "approved_assets": {
    "douyin_video": "publish_package/douyin/video.mp4",
    "wechat_moments_video": "publish_package/wechat_moments/video.mp4"
  },
  "forbidden_actions": [
    "paid_promotion",
    "delete_files",
    "delete_old_posts",
    "bulk_private_message",
    "change_account_settings",
    "auto_add_friends",
    "auto_comment_spam"
  ]
}
```

`approved_scope` 只能包含用户审核过的平台。没有列入范围的平台不得发布。

## 停止条件

抖音含联系方式、微信联系方式未经确认、文案过度夸张、素材裁切、视频抖动、视频发虚、平台包混用、用户未审核、`publish-approved.json` 缺失或不完整，必须停止。

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
