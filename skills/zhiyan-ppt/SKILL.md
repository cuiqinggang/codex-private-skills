---
name: zhiyan-ppt
description: "Create complete Chinese presentations through one self-contained workflow combining editable PowerPoint delivery, high-end editorial or Swiss visual design, analysis-led charts, speaker notes and presenter HTML, and three-direction style exploration. Use for PPT、PPTX、演示文稿、汇报材料、路演、培训课件、微信展示、数据分析型演示、高级设计感、逐字稿、演讲模式、同材横评，或用户直接提到‘智演PPT’. Default to a polished native editable PPTX unless the setting clearly requires HTML presentation features."
---

# 智演PPT

完成从材料检查、证据治理、叙事冻结、视觉设计、生成、逐页验收到交付的整套中文演示任务。把下列四种能力视为本技能内置模式，不拆成外部技能依赖或额外用户入口。

## 选择一个主模式

按首条匹配规则选择：

1. 直播培训、公开演讲、串流、演讲者视图、计时、备注或逐字稿：**演讲增强**。
2. 风格未确定，或用户要求先看多个方向：**风格探索**。
3. 微信展示、产品故事、个人故事、作品集案例，或第一印象重于原生可编辑性：**高级视觉**。
4. 其他情况：**正式可编辑**。

用户说“高级，但必须能改”时，保持**正式可编辑**，吸收**高级视觉**的视觉语言。除非用户明确要求，不生成多套完整成稿。仅在请求含混或混合时读取 [references/routing.md](references/routing.md)。

## 执行统一工作流

1. 检查全部材料，确认受众、待做决定、页数、语言、交付场景、来源边界、品牌限制和格式。
2. 建立唯一证据清单，分开标记：来源事实、计算、推断、建议、假设、未知。禁止编造数字、引语、截图、Logo 或产品主张。使用 [references/evidence-manifest.md](references/evidence-manifest.md)。
3. 先冻结叙事，再做样式。每个内容页使用结论型标题，且只有一个主导视觉目的。
4. 按主模式只读取对应参考：
   - 原生可编辑 PPTX：[references/formal-pptx.md](references/formal-pptx.md)
   - 高级 HTML 展示：[references/high-design.md](references/high-design.md)
   - HTML 演讲体验：[references/presenter-html.md](references/presenter-html.md)
   - 三个视觉方向：[references/style-exploration.md](references/style-exploration.md)
5. 构建能完整解决请求的最小交付物。图表、对比、时间线、矩阵或证据标注必须提升决策价值；不添加装饰性数据图。
6. 逐页验证溢出、重叠、微小标签、字体、对比度、重复版式、来源、坐标轴误导、导航和文件完整性。运行 `python scripts/validate_presentation.py <deliverable>`，并补充真实渲染后的视觉检查。
7. 用简洁可下载文件名交付，说明格式、页数、可编辑性、验证动作和限制。

## 默认交付契约

- 默认交付真实 `.pptx`，文本、形状、表格和图表原生可编辑；有模板时保留模板。禁止用整页截图伪装可编辑。
- HTML 使用固定 `1920×1080` 舞台并等比缩放；核心导航离线可用。明确说明 HTML 源码可编辑，但不是原生 PowerPoint。
- 把最终 `.pptx` 或 `.html` 当成交付物，源脚本只是实现细节。

## 分析型演示规则

- 从受众必须做出的决定出发，再选择证据。
- 把密集材料压成：执行结论 → 驱动因素 → 证据 → 含义 → 行动。
- 只有当视觉编码比数字或短句更清楚时才使用图表。
- 标题写发现，证据旁写来源与限制。
- 全篇统一术语、日期、单位、分母、颜色语义和比较基线。
- 显式呈现不确定性与数据缺口。

## 同材横评

用户询问哪个模式更强时，不创建无关示例。读取 [references/benchmark.md](references/benchmark.md)，冻结同一份六页中文输入，按准确性、决策价值、视觉层级、可读性、可编辑性、稳定性和速度横评。

## 参考资产边界

需要“高级但可编辑”、编辑杂志风、Swiss/Editorial 版式或分析型财务演示时，读取 [references/apple-ai-analysis-reference.md](references/apple-ai-analysis-reference.md)，并按清单使用 `assets/reference-decks/Guizang-Style-Apple-AI-Analysis-Premium-Chinese.pptx`。该文件是视觉与结构参考，不是通用事实来源；不得把其中 Apple 数据、免责声明或品牌语言移植到无关项目。

## 防落灰与复盘

复杂演示开工前执行本机复用预检并优先读取本技能；触发与规则补丁见 [references/RULE-PATCH.md](references/RULE-PATCH.md)。出现打不开、溢出、字体替换、错数、假可编辑或现场导航失败时，写入 [references/FAILURE-REVIEW.md](references/FAILURE-REVIEW.md)。每次真实使用后追加 [references/RECENT-USE-LOG.md](references/RECENT-USE-LOG.md)，记录模式、格式、页数、耗时、返工与验收结果。全局规则仅提供草案，见 [references/AGENTS-PATCH-DRAFT.md](references/AGENTS-PATCH-DRAFT.md)，不得自动覆盖用户的 AGENTS.md。

