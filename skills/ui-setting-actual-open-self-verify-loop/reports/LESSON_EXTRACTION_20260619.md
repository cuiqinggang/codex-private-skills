# Lesson Extraction: UI Setting Actual Open Self Verify Loop

## Source

User rule provided in chat on 2026-06-19:

`UI_SETTING_ACTUAL_OPEN_SELF_VERIFY_LOOP_RULE_V1`

## Value Judgment

Conclusion: HIGH_VALUE

Reasons:

- Prevents repeated false success on UI/configuration work.
- Converts a successful Cursor/Kilo localization verification pattern into a reusable SOP.
- Creates clear acceptance criteria for screenshots, rounds, and PASS vocabulary.
- Reduces the chance of damaging model/provider routes while changing UI settings.
- User explicitly said this must apply to future tasks.

## Problem Solved

Past failure mode: config is written, but the actual software is not reopened, the target panel is not visible, and the result is reported as complete without proof.

New rule: the task is not complete until the real UI is opened, screenshots are captured, the screenshots are inspected, and at least two verification rounds are recorded.

## Reusable Assets

- Skill trigger: `SKILL.md`
- SOP: `sop/UI_SETTING_ACTUAL_OPEN_SELF_VERIFY_LOOP_SOP.md`
- Checklist: `checklists/UI_SETTING_ACTUAL_OPEN_SELF_VERIFY_CHECKLIST.md`
- Report template: `templates/UI_SETTING_ACTUAL_OPEN_VERIFY_REPORT_TEMPLATE.md`
- Acceptance page: `acceptance/index.html`
- Usage log: `logs/RECENT_USE.md`

## Trigger Keywords

- 软件界面设置
- 插件设置
- 中文化
- 模型选择
- Provider 选择
- 工作区恢复
- UI 面板打开
- Cursor 设置
- Kilo Settings
- OpenRouter / DeepSeek 模型验证
- 实际打开验证
- 截图证据

## Next-Run Rule

When any trigger applies, load this skill and the screenshot skill before editing settings. Final status must be one of:

- `ACTUAL_OPEN_VERIFY_PASS`
- `PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE`
- `FAIL_NEEDS_FURTHER_FIX`
