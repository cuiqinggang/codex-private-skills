# 02_RECON_SCREENSHOT

对目标 URL 执行：
1. 桌面端截图 1440x1200
2. 移动端截图 390x1200
3. 全页面截图
4. 记录页面标题
5. 记录 meta description
6. 记录主导航结构
7. 记录主要 section：Navbar、Hero、Features、Social proof、Pricing、FAQ、Footer
8. 记录字体、颜色、按钮、卡片、圆角、阴影、容器宽度
9. 如页面有动画，记录但不强行精确复刻

## 强制侦察深度
侦察不是存截图，而是后续高相似复刻的规格来源。必须记录桌面端和移动端的首屏结构差异。

每个关键元素必须记录：

- x / y / width / height
- font-size / line-height / font-weight
- color / background / border / radius / shadow / glow
- 与前后元素的间距
- 是否在移动端隐藏、替换或重排

必须覆盖：

- Header / Logo / Nav / CTA
- Hero title / subtitle
- Primary visual，例如 prompt box、hero media、canvas preview
- Chips / CTA / scroll hint
- 首屏以下第一个 section
- 移动端首屏和第一个 section

无法自动提取时，必须标记 `MANUAL_ESTIMATE`，不得留空。

## 阶段门禁
没有 `outputs/progress/00_TARGET_BASELINE.md` 和 `outputs/progress/01_GEOMETRY_SPEC.md`，不得进入组件规格或编码阶段。

输出：
- outputs/recon/TARGET_SITE_RECON.md
- outputs/progress/00_TARGET_BASELINE.md
- outputs/progress/01_GEOMETRY_SPEC.md
- evidence/screenshots/target_desktop.png
- evidence/screenshots/target_mobile.png
- evidence/screenshots/target_fullpage.png

## 输出要求
- 所有结论必须中文可读。
- 关键证据必须落盘。
- 没有真实 URL、截图、build 和 QA，不得标记 PASS。
