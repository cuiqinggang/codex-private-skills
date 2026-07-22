# 03_DESIGN_SYSTEM_EXTRACTION

生成 DESIGN_SYSTEM.md，包含 Color tokens、Typography tokens、Spacing scale、Border radius、Shadow scale、Layout/container width、Button styles、Card styles、Section rhythm、Responsive breakpoints、Motion notes。

这些 token 是“参考结构”，不是原样抄袭品牌视觉。如果涉及品牌色，必须生成替代色方案。

## 高相似复刻规则
合规替代色不能变成自由换风格。允许替换品牌色名称和表达，但必须保留目标站的视觉关系：

- 暗/亮模式关系
- 主背景明度
- 主视觉发光或阴影强度
- 标题与副标题的对比关系
- 按钮、chips、卡片的层级关系

如果替代色导致整体气质偏离，必须在相似度评分中扣分。

输出：outputs/design/DESIGN_SYSTEM.md

## 输出要求
- 所有结论必须中文可读。
- 关键证据必须落盘。
- 没有真实 URL、截图、build 和 QA，不得标记 PASS。
