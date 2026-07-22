# 10_ACCEPTANCE_GATE

最终验收不是唯一验收。它只能汇总已经逐关通过的结果。

## 技能包级验收

[ ] `SKILL.md` 是否要求读取 `11` 和 `12`
[ ] `12_STAGE_GATE_EXECUTION_PROTOCOL.md` 是否存在
[ ] `templates/STAGE_GATE_REPORT_TEMPLATE.md` 是否存在
[ ] `scripts/validate_stage_gate.ps1` 是否存在
[ ] `scripts/validate_stage_gate.ps1` 是否能运行
[ ] 旧坏案例是否会被 `INVALID_TEST` 或 `FAIL_SIMILARITY` 拦截

## 真实测试验收

[ ] 合规判断是否存在
[ ] 环境预检是否存在
[ ] 真实目标 URL 是否存在
[ ] 目标站桌面截图是否存在
[ ] 目标站移动截图是否存在
[ ] 目标站全页截图是否存在
[ ] 生成站桌面截图是否存在
[ ] 生成站移动截图是否存在
[ ] 设计系统是否存在
[ ] 组件规格是否存在
[ ] Next.js 项目是否存在
[ ] npm install 是否执行
[ ] npm run lint 是否执行
[ ] npm run typecheck 是否执行
[ ] npm run build 是否执行
[ ] 合规替换是否执行
[ ] QA 报告是否存在
[ ] 最终 ZIP 是否创建

## 阶段门禁验收

[ ] `outputs/progress/00_TARGET_BASELINE.md` 是否存在
[ ] `outputs/progress/01_GEOMETRY_SPEC.md` 是否存在
[ ] `outputs/progress/02_COMPONENT_SPECS_INDEX.md` 是否存在
[ ] `outputs/progress/03_BUILD_PLAN.md` 是否存在
[ ] `outputs/progress/stage-gates/G00_TARGET_CAPTURE.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G01_GEOMETRY_SPEC.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G02_COMPONENT_SPECS.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G03_BUILD_PLAN.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G10_NAVBAR.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G20_HERO_TEXT.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G30_PRIMARY_VISUAL.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G40_CTA_SCROLL.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G50_FIRST_SECTION.md` 是否 PASS
[ ] `outputs/progress/stage-gates/G60_MOBILE.md` 是否 PASS

## 百分比验收

[ ] 每个视觉关是否给出桌面相似度百分比
[ ] 每个视觉关是否给出移动端相似度百分比
[ ] 每个视觉关是否给出综合相似度百分比
[ ] 每个视觉关综合分是否符合 `round(Desktop * 0.6 + Mobile * 0.4)`
[ ] 每个视觉关是否有目标图和生成图
[ ] 每个视觉关是否有扣分逻辑
[ ] 每个视觉关是否公开脚本输出
[ ] 桌面相似度是否 >= 95%
[ ] 移动端相似度是否 >= 95%
[ ] 综合相似度是否 >= 95%

## 禁止事项

如果任一视觉关未 PASS，不得继续下一关。

如果缺任意关键项，不得 PASS。

如果相似度低于 95%，不得使用“克隆能力通过”“高相似复刻通过”“PASS”等表述，只能标记 `GATE_BLOCKED`、`PARTIAL_SIMILARITY`、`FAIL_SIMILARITY` 或 `INVALID_TEST`。
