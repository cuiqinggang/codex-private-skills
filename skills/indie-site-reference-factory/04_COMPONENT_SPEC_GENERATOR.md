# 04_COMPONENT_SPEC_GENERATOR

每个页面区块生成单独 spec：
- Navbar.spec.md
- Hero.spec.md
- FeatureGrid.spec.md
- Pricing.spec.md
- FAQ.spec.md
- Footer.spec.md

每个 spec 必须包含组件目的、桌面端布局、移动端布局、内容字段、视觉 token、交互状态、可替换资产、验收标准。

## 强制规格字段
每个组件 spec 必须包含：

- target screenshot crop 或截图区域说明
- desktop geometry：x / y / width / height / gap
- mobile geometry：x / y / width / height / gap
- typography：font-size / line-height / font-weight / color
- effects：background / border / radius / shadow / glow / opacity
- allowed rewrite：允许替换的品牌、文案、图片
- forbidden drift：不得改变的布局、比例、顺序、视觉层级
- acceptance threshold：组件相似度最低百分比

没有组件级几何规格，不得编码该组件。

## 首屏优先顺序
必须先完成首屏组件规格：

1. Navbar
2. HeroTitle
3. HeroSubtitle
4. PrimaryVisual
5. ChipsOrCTA
6. ScrollHint
7. FirstBelowFoldSection
8. MobileHero
9. MobileFirstSection

输出还必须包含：`outputs/progress/02_COMPONENT_SPECS_INDEX.md`。

## 输出要求
- 所有结论必须中文可读。
- 关键证据必须落盘。
- 没有真实 URL、截图、build 和 QA，不得标记 PASS。
