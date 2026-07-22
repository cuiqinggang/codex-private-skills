# 11_STRICT_CLONE_EXECUTION_PROTOCOL

## 目的

本文件修正一次失败教训：只看截图后自由发挥，会生成“风格参考站”，不是“高相似复刻站”。本技能包必须用强制进度包和阶段门禁约束执行。

阶段门禁的细则以 `12_STAGE_GATE_EXECUTION_PROTOCOL.md` 为准。本文件只保留核心执行原则。

## 核心原则

1. 先逆向，再编码。
2. 先规格，再组件。
3. 先过关，再继续下一段。
4. 桌面端和移动端分开复刻。
5. 相似度必须用百分比表达。
6. 每个视觉关低于 95% 不得进入下一关。
7. 最终低于 95% 不得宣称克隆能力通过。
8. build 通过只证明工程能跑，不证明视觉相似。
9. 合规替换不等于自由改版。品牌、Logo、文案、图片可以替换，但布局几何、组件节奏、层级关系必须按目标站规格复现。

## 强制执行进度包

每次任务必须创建：

```text
outputs/progress/
  00_TARGET_BASELINE.md
  01_GEOMETRY_SPEC.md
  02_COMPONENT_SPECS_INDEX.md
  03_BUILD_PLAN.md
  stage-gates/
    G00_TARGET_CAPTURE.md
    G01_GEOMETRY_SPEC.md
    G02_COMPONENT_SPECS.md
    G03_BUILD_PLAN.md
    G10_NAVBAR.md
    G20_HERO_TEXT.md
    G30_PRIMARY_VISUAL.md
    G40_CTA_SCROLL.md
    G50_FIRST_SECTION.md
    G60_MOBILE.md
  ROUND_01_COMPARE.md
  FINAL_SIMILARITY_GATE.md
```

缺少 `outputs/progress/` 时，任务结论必须是 `INVALID_TEST`。

## 阶段 0：目标基线

必须先生成 `00_TARGET_BASELINE.md`：

- 目标 URL
- 桌面截图路径
- 移动截图路径
- 全页截图路径
- 桌面首屏结构
- 移动首屏结构
- 目标站首屏中哪些内容允许替换
- 目标站首屏中哪些几何结构必须保留

然后生成 `outputs/progress/stage-gates/G00_TARGET_CAPTURE.md` 并运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\validate_stage_gate.ps1 -WorkRoot <workroot> -Gate G00_TARGET_CAPTURE
```

没有 `STATUS=PASS`，不得进入下一阶段。

## 阶段 1：几何规格

必须生成 `01_GEOMETRY_SPEC.md`，逐项记录：

- Header：x/y/width/height/背景/字体/链接间距
- Logo 区：x/y/width/height/视觉占位，不复制原 Logo
- Hero title：x/y/width/height/font-size/line-height/font-weight/color
- Subtitle：x/y/width/height/font-size/line-height/color
- 主视觉组件：x/y/width/height/radius/border/shadow/glow/background
- Chips/CTA：x/y/width/height/gap/radius/color
- Scroll hint：x/y/font-size/color
- Below-fold 首个区块：x/y/width/height/结构层级
- Mobile 独立规格：不得直接继承 desktop

然后生成 `G01_GEOMETRY_SPEC.md` 并运行门禁脚本。没有 `STATUS=PASS`，不得编码。

## 阶段 2：组件规格

必须生成 `02_COMPONENT_SPECS_INDEX.md` 和每个组件 spec：

- Navbar
- HeroTitle
- HeroSubtitle
- PrimaryVisual
- ChipsOrCTA
- ScrollHint
- FirstBelowFoldSection
- MobileHero
- MobileFirstSection

每个 spec 必须含：

- 目标截图区域
- desktop geometry
- mobile geometry
- typography
- color/effect/radius/shadow
- allowed rewrite
- forbidden drift
- acceptance percentage

然后生成 `G02_COMPONENT_SPECS.md` 并运行门禁脚本。没有 `STATUS=PASS`，不得编码该组件。

## 阶段 3：构建计划

必须生成 `03_BUILD_PLAN.md`，并列出以下门禁：

1. `G10_NAVBAR`
2. `G20_HERO_TEXT`
3. `G30_PRIMARY_VISUAL`
4. `G40_CTA_SCROLL`
5. `G50_FIRST_SECTION`
6. `G60_MOBILE`

然后生成 `G03_BUILD_PLAN.md` 并运行门禁脚本。没有 `STATUS=PASS`，不得开始页面工程。

## 阶段 4：逐关构建和对比

每个视觉关必须输出：

- 目标桌面截图
- 当前桌面截图
- 目标移动截图
- 当前移动截图
- 桌面相似度百分比
- 移动相似度百分比
- 综合相似度百分比
- 扣分项
- 下一轮必须修复项
- `validate_stage_gate.ps1` 输出

如果没有当轮截图，不得给相似度。

如果脚本没有返回 `STATUS=PASS`，不得进入下一关。

## 相似度计算

桌面相似度：

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

公式：

```text
Overall = round(Desktop * 0.6 + Mobile * 0.4)
```

## 判定

- `CLONE_SIMILARITY_PASS`：所有视觉关 PASS，最终桌面 >= 95%，移动 >= 95%，综合 >= 95%，且工程 build 通过。
- `GATE_BLOCKED`：当前关截图和分数存在，但任一视觉分低于 95%。
- `PARTIAL_SIMILARITY`：最终综合 70%-94%，或桌面/移动任一低于 95%。
- `FAIL_SIMILARITY`：最终综合低于 70%。
- `INVALID_TEST`：缺截图、缺进度包、缺百分比逻辑、缺真实 URL、缺阶段门禁报告。

## 失败复盘硬规则

如果用户指出“不像”“完全不是一个东西”“牛头不对马嘴”，必须立即：

1. 暂停继续编码。
2. 撤回 PASS。
3. 找到最早失败关卡。
4. 修正该关相似度百分比。
5. 记录到 `FAILURE_REVIEW.md`。
6. 回到该关重跑截图和门禁。
7. 没有重新 PASS，不得继续后续关卡。
