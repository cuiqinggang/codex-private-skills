# 06_VISUAL_QA_AND_REPAIR

视觉 QA 是逐关门禁，不是最终补救。

## 必须生成的截图

最终站点截图：

- `evidence/screenshots/generated_desktop.png`
- `evidence/screenshots/generated_mobile.png`
- `evidence/screenshots/generated_fullpage.png`

每个视觉关截图：

```text
evidence/screenshots/stage-gates/<GATE_ID>_target_desktop.png
evidence/screenshots/stage-gates/<GATE_ID>_generated_desktop.png
evidence/screenshots/stage-gates/<GATE_ID>_target_mobile.png
evidence/screenshots/stage-gates/<GATE_ID>_generated_mobile.png
```

## 评分必须用百分比

桌面端相似度：

- Layout geometry：25%
- Typography hierarchy：15%
- Color / lighting / background：15%
- Key component shape：20%
- Below-fold first section：15%
- Interaction affordance / state：10%

移动端相似度：

- Mobile element order：25%
- Mobile layout geometry：25%
- Mobile typography：15%
- Mobile key visual：20%
- Mobile CTA / navigation：15%

综合相似度：

- Desktop 60%
- Mobile 40%

## 每一关必须公开

每关修复后必须在对话里给出：

- Gate ID
- 目标桌面截图
- 当前桌面截图
- 目标移动截图
- 当前移动截图
- 桌面相似度百分比
- 移动端相似度百分比
- 综合相似度百分比
- 扣分逻辑
- `validate_stage_gate.ps1` 输出
- 是否允许进入下一关

没有截图，不得给百分比。没有门禁脚本 PASS，不得进入下一关。

## 修复循环

不能机械限制为 3 轮。低于 95% 就停留在当前关继续修复，直到：

- 当前关达到 `STATUS=PASS`；或
- 明确标记 `GATE_BLOCKED` 并停止，不得继续假装后续构建有效。

## 判定

- `CLONE_SIMILARITY_PASS`：所有阶段视觉关 PASS，最终桌面/移动/综合均 >=95%，build PASS。
- `GATE_BLOCKED`：某一关有证据但分数未达 95%，禁止继续。
- `PARTIAL_SIMILARITY`：最终综合 70%-94%，或任一端低于 95%。
- `FAIL_SIMILARITY`：最终综合低于 70%。
- `INVALID_TEST`：缺进度包、截图、百分比、扣分逻辑、真实 URL 或门禁报告。
