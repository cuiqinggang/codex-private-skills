# 12_STAGE_GATE_EXECUTION_PROTOCOL

## 2026-07-09 Real-Test Hardening Addendum

This addendum is mandatory for every future real reference-site clone test.

The Framer real test proved that a stage gate is only useful when it blocks bad intermediate work in public, before the next stage begins. During that test:

- `G30_PRIMARY_VISUAL` was initially blocked at Desktop=95%, Mobile=76%, Overall=87%.
- `G50_FIRST_SECTION` was initially blocked at Desktop=89%, Mobile=78%, Overall=85%.
- The final run passed only after local repairs inside the same gate.
- Final progress gate result: Desktop=95%, Mobile=95%, Overall=95%, `PROGRESS_GATE=CLONE_SIMILARITY_PASS`.

### Mandatory Chat Evidence Rule

For every visual gate (`G10` through `G60`, plus `G90` final), the executor must show the user a comparison image before moving forward.

Required user-visible evidence:

1. Four-image comparison board:
   - target desktop
   - generated desktop
   - target mobile
   - generated mobile
2. Desktop similarity percentage.
3. Mobile similarity percentage.
4. Overall similarity percentage.
5. Deduction logic.
6. Gate script output.
7. Explicit decision: pass or blocked.

If this evidence is not shown in the chat, the gate is not complete even if files exist on disk.

### Current-Score-First Rule

If a gate has blocked attempts and a later repaired pass, the current gated score must appear before historical blocked scores in the gate report. Historical failed scores must be labeled as `attempt score`, not `Desktop similarity` / `Mobile similarity` / `Overall similarity`, so validators do not read stale failure scores as the current decision.

### Rich Reference-Site Rule

Capability validation must use a visually valuable reference site, not an overly simple page. A useful test target should contain at least three high-signal visual structures, such as:

- strong hero typography
- distinct visual component or tool surface
- responsive mobile layout
- lower-section cards or gallery
- nontrivial color/lighting system

### Target-Pollution Rule

Cookie banners, popups, browser overlays, login walls, and capture artifacts must be documented in `G00_TARGET_CAPTURE` and excluded from scoring. They must not be copied into the independent generated site.

### Lower-Section Rule

A good hero is not enough. `G50_FIRST_SECTION` must prove that the clone can reproduce the first meaningful lower-section structure and visual richness. Plain gradient cards or generic placeholders are not acceptable for a rich reference site.

## 目的

本文件是技能包的阶段门禁源规则。它解决的问题是：不能等页面全部做完后才截图、打分、修复。真正的独立站复刻能力必须在每一个关键构建阶段被验证。

## 总规则

1. 每一关是同级硬门禁，不是建议清单。
2. 上一关没有 `STATUS=PASS`，下一关不得开始。
3. 每一关必须有独立 Markdown 报告，放在 `outputs/progress/stage-gates/`。
4. 视觉关必须有目标截图、生成截图、桌面分、移动分、综合分和扣分逻辑。
5. 分值不达标时，必须停留在当前关修复，不能先往下做。
6. 最终 `FINAL_SIMILARITY_GATE.md` 只能汇总各关结果，不能替代各关验证。

## 关卡序列

| Gate | 名称 | 产物 | 是否视觉关 | 进入下一关条件 |
| --- | --- | --- | --- | --- |
| G00_TARGET_CAPTURE | 目标捕获 | 真实 URL、目标桌面/移动/全页截图、`00_TARGET_BASELINE.md` | 否 | 文件完整，URL 和截图有效 |
| G01_GEOMETRY_SPEC | 几何图纸 | `01_GEOMETRY_SPEC.md` | 否 | Header/Hero/主视觉/首个下一区块/移动端均有 x/y/w/h |
| G02_COMPONENT_SPECS | 组件图纸 | `02_COMPONENT_SPECS_INDEX.md` 和组件 spec | 否 | 每个首屏组件都有 desktop/mobile geometry 和 forbidden drift |
| G03_BUILD_PLAN | 分段施工计划 | `03_BUILD_PLAN.md` | 否 | 计划列出每个视觉关和截图验证命令 |
| G10_NAVBAR | 导航栏 | `G10_NAVBAR.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G20_HERO_TEXT | Hero 文本层 | `G20_HERO_TEXT.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G30_PRIMARY_VISUAL | 主视觉组件 | `G30_PRIMARY_VISUAL.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G40_CTA_SCROLL | CTA/Chips/Scroll | `G40_CTA_SCROLL.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G50_FIRST_SECTION | 首屏下一区块 | `G50_FIRST_SECTION.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G60_MOBILE | 移动端复核 | `G60_MOBILE.md` + 4 张关卡截图 | 是 | 桌面/移动/综合均 >=95% |
| G90_FINAL | 最终验收 | `FINAL_SIMILARITY_GATE.md`、build、QA、ZIP | 是 | 所有关卡 PASS，最终截图 PASS，build PASS |

## 关卡截图命名

视觉关必须使用固定路径：

```text
evidence/screenshots/stage-gates/<GATE_ID>_target_desktop.png
evidence/screenshots/stage-gates/<GATE_ID>_generated_desktop.png
evidence/screenshots/stage-gates/<GATE_ID>_target_mobile.png
evidence/screenshots/stage-gates/<GATE_ID>_generated_mobile.png
```

没有这些截图，不得给该关相似度。

## 关卡报告最低内容

使用 `templates/STAGE_GATE_REPORT_TEMPLATE.md`。

每个视觉关报告必须包含：

- `Gate ID`
- `Gate name`
- `Target desktop screenshot`
- `Generated desktop screenshot`
- `Target mobile screenshot`
- `Generated mobile screenshot`
- `Desktop similarity`
- `Mobile similarity`
- `Overall similarity`
- `Formula`
- `Deductions`
- `Proceed allowed: YES/NO`

## 评分逻辑

桌面端：

- Layout geometry：25%
- Typography hierarchy：15%
- Color / lighting / background：15%
- Key component shape：20%
- Below-fold first section：15%
- Interaction affordance / state：10%

移动端：

- Mobile element order：25%
- Mobile layout geometry：25%
- Mobile typography：15%
- Mobile key visual：20%
- Mobile CTA / navigation：15%

综合：

```text
Overall = round(Desktop * 0.6 + Mobile * 0.4)
```

报告里的综合分必须和公式一致。否则该关 `INVALID_TEST`。

## 阻断规则

- 缺文件：`INVALID_TEST`
- 缺真实 URL：`INVALID_TEST`
- 缺 PNG 或 PNG 无效：`INVALID_TEST`
- 缺分数：`INVALID_TEST`
- 缺扣分逻辑：`INVALID_TEST`
- 综合分公式不一致：`INVALID_TEST`
- 分数完整但任一视觉分 <95：`GATE_BLOCKED`
- 报告写了 `Proceed allowed: YES` 但分数 <95：`GATE_BLOCKED`
- 报告写了 `CLONE_SIMILARITY_PASS` 但任一关未 PASS：`INVALID_TEST`

## 允许修复方式

同一关内可以多轮修复：

```text
G30_PRIMARY_VISUAL_R1.md
G30_PRIMARY_VISUAL_R2.md
G30_PRIMARY_VISUAL.md
```

但只有最终关卡报告 `G30_PRIMARY_VISUAL.md` 被 `validate_stage_gate.ps1` 判为 `STATUS=PASS` 后，才能进入下一关。
