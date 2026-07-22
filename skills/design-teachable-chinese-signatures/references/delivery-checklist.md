# 交付清单与机器验证

## 人工清单

- [ ] 姓名逐字与用户确认文本一致。
- [ ] 简繁体和异体统一。
- [ ] 每个字的识别笔画通过验字卡。
- [ ] 最终方案有三次真实书写记录，或明确标成“未测视觉候选”。
- [ ] 定稿图、透明图、笔顺说明、练习纸能够打开。
- [ ] 没有把私人姓名和笔迹默认公开。
- [ ] 没有宣称法律效力、代签能力或虚构成交价格。

## delivery.json

```json
{
  "name_confirmed": true,
  "character_integrity_passed": true,
  "human_three_write_status": "passed",
  "trials": [
    {"seconds": 4.2, "pen_lifts": 3, "skeleton_consistent": true, "legible": true},
    {"seconds": 4.0, "pen_lifts": 3, "skeleton_consistent": true, "legible": true},
    {"seconds": 3.8, "pen_lifts": 3, "skeleton_consistent": true, "legible": true}
  ],
  "files": ["final.png", "transparent.png", "stroke-order.pdf", "practice-sheet.svg"],
  "privacy_reviewed": true,
  "public_display_authorized": false
}
```

`human_three_write_status` 只能是 `passed`、`failed` 或 `untested`。只有 `passed` 才要求恰好三条合格记录；`untested` 必须在面向用户的说明中明确写出。
