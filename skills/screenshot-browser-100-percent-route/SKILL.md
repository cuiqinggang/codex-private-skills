---
name: screenshot-browser-100-percent-route
description: Use when normal browser automation is unavailable or has failed and the user explicitly needs screenshot-recognition coordinate control of a browser with one-action-one-screenshot verification. Do not use for normal DOM/Playwright automation, OS desktop apps, bulk actions, or sending without confirmation.
---

# Screenshot Browser 100% Gated Route

从 OpenClaw 三轮验证路线 + Hermes 九轮实测迭代而来。

## 实测统计（2026-05-29，Hermes + ChatGPT）

| 轮次 | 首次粘贴 | 截图捕获 | 最终结果 |
|------|---------|---------|---------|
| R1 | ❌ | ✅ | ✅ ROUND1_OK |
| R2 | ❌ | ✅ | ✅ ROUND2_OK |
| R3 | ❌ | ✅ | ✅ ROUND3_OK |
| R4 | ❌ | ✅ | ✅ ROUND4_OK |
| R5 | ✅ | — | ✅ ROUND5_OK |
| R6 | ✅ | — | ✅ ROUND6_OK |
| R7 | ⚠️ 视觉误判 | ✅ | ✅ ROUND7_OK |
| R8 | ✅ | — | ✅ ROUND8_OK |
| R9 | ✅ | — | ✅ ROUND9_OK |

- 粘贴首次成功率：56%（5/9）
- 截图失败捕获率：**100%**（4/4）
- 重试后最终成功率：**100%**（9/9）

## 稳定操作公式

```
1. G01: 全桌面截图 + 枚举窗口
2. G02: 确认目标 Chrome 标题（'Google Chrome' in title，排除 Codex/Hermes）
3. G02: 确认地址栏 URL（Ctrl+L → Ctrl+C → 读剪贴板）
4. G03: Escape 关闭弹窗
5. G04-1: 点击页面中部（确保焦点在文档内）
6. G04-2: 多点点击底部 90%/92%/94%（覆盖输入框位置变化）
7. G04-3: 焦点测试（按 a → 退格）
8. G04-4: 粘贴文本
9. G04-5: 截图 → 视觉验证"请逐字抄出输入框的文字" ← 不可跳过！
10. G05: 确认后 Enter 发送
11. G06: 等待 → 截图 → 视觉确认 marker 回复
```

## 硬规则

- 每次操作后必须截图验证，不可连续两个动作不验证
- 视觉查询用"逐字抄出"而非 yes/no（yes/no 误判率约 20%）
- 窗口标题会随对话变化，搜索用 `'Google Chrome' in title` 而非硬编码
- 快捷键不可靠（Ctrl+Shift+O、/），多点物理点击更稳定
- 不能靠固定坐标
- 不能用 Ctrl+A
- 前台不是目标窗口 → 截图作废
- 页面打开 ≠ 成功，必须看到 marker 回复

## 铁律

> **不确定 → 截图。变化了 → 截图。操作完 → 截图。一条截图解万难。**

## 状态码

`XIAOLONGXIA_BOOT_REPLAY_3X_VERIFY_PASS`
`9_ROUND_100_PERCENT_GATED_SUCCESS_20260529`
