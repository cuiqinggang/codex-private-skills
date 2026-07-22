---
name: indie-site-reference-factory
description: Use when the user wants to analyze a public reference website or owned website, extract design systems and component specs, generate an independent Next.js/React/Tailwind landing site, enforce per-stage screenshot similarity gates with user-visible comparison images, rewrite brand/copy legally, and deliver a deployable package with real-site test evidence.
---

# indie-site-reference-factory

## 2026-07-09 Hard Rule From Real Framer Test

This skill is only valid when it behaves as a strict gate system, not a loose final screenshot workflow.

Before any real clone test, read:

1. `12_STAGE_GATE_EXECUTION_PROTOCOL.md`
2. `commands/06_real_stage_gate_visual_proof.md`
3. `references/FRAMER_STAGE_GATE_REAL_TEST_20260709.md` when validating the skill itself or when the target is visually rich.

Mandatory execution rule:

- Every visual gate must show a four-image comparison board in the chat before the next gate starts.
- The chat must include desktop/mobile/overall percentages, deduction logic, gate script output, and pass/block decision.
- A visual gate below 95% blocks progress. Repair inside the same gate and re-run screenshots/scoring/script.
- Historical blocked attempts must remain as proof, but current gated scores must appear before blocked attempt records.
- A simple page is not enough to validate clone capability; use a visually valuable indie/product site.
- Target pollution such as cookie banners must be documented and excluded from scoring, not cloned.

Proven calibration:

- Framer real test G30 initially blocked at 87%, then passed at 96% after local repair.
- Framer real test G50 initially blocked at 85%, then passed at 95% after local repair.
- Final progress gate returned `PROGRESS_GATE=CLONE_SIMILARITY_PASS` with Desktop=95%, Mobile=95%, Overall=95%.

## 中文定位

这是一个“参考站拆解 + 独立站工业化生成 + 分阶段视觉门禁”的技能包。
它不是让 Codex 看完目标站后自由发挥，而是把公开参考网站或用户自有网站拆解成可执行的规格、组件、工程和逐关验收证据。

## 合规边界

默认模式是“参考结构 + 合规二次生成”，不是仿冒。

禁止：
- 复制 Logo、品牌名、客户案例、完整文案、版权图片或法律文本。
- 制作钓鱼网站。
- 绕过登录、付费墙、反爬或访问限制。

允许：
- 学习布局结构、组件节奏、视觉层级、响应式规则和交互模式。
- 在自有/授权网站场景中做迁移式重建。
- 用替代品牌、替代文案和替代资产生成独立站。

## 必读顺序

1. `00_RULES_LEGAL_SAFETY.md`
2. `01_PRECHECK.md`
3. `11_STRICT_CLONE_EXECUTION_PROTOCOL.md`
4. `12_STAGE_GATE_EXECUTION_PROTOCOL.md`
5. 按任务需要读取 `02`-`10` 和 `commands/`

复杂任务开始前，先运行 `codex-video-to-usable-skill-loop` 的复用预检。K 盘只作备份/参考，不作默认热路径。

## 核心执行模型

本技能包采用“同级制阶段门禁”：

- 不能跳关。
- 不能最后才截图对比。
- 不能用 build 通过替代视觉相似度。
- 不能用最终修好后的结果回填前面关卡。
- 每一关必须有独立证据、独立评分、独立判定。

每次真实测试必须创建：

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

每一关推进前必须运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\validate_stage_gate.ps1 -WorkRoot <workroot> -Gate <GATE_ID>
```

如果该关输出不是 `STATUS=PASS`，不得进入下一关。

## 相似度门禁

视觉关卡最低推进阈值：

- 桌面相似度 >= 95%
- 移动端相似度 >= 95%
- 综合相似度 >= 95%
- 综合公式必须是：`桌面 * 0.6 + 移动 * 0.4`

低于阈值时，只能在同一关内继续修复和重新截图，不得进入下一关。

最终只有桌面端、移动端、综合相似度全部 >= 95%，且工程 build 通过，才允许标记：

`CLONE_SIMILARITY_PASS`

否则必须标记：

- `INVALID_TEST`：缺真实 URL、截图、进度包、百分比逻辑或门禁证据。
- `GATE_BLOCKED`：某一阶段证据存在但未达到推进阈值。
- `PARTIAL_SIMILARITY`：最终综合 70%-94%，或任一端低于 95%。
- `FAIL_SIMILARITY`：最终综合低于 70%。

## 必须公开给用户

每一关完成后，在对话里同步：

- 当前关卡 ID 和名称
- 目标图路径
- 生成图路径
- 桌面/移动/综合百分比
- 扣分逻辑
- 门禁脚本输出
- 是否允许进入下一关

## 触发关键词

参考站拆解、独立站工业化生成、AI website cloner、/clone-website、网站逆向、设计系统提取、组件规格、视觉 QA、分阶段门禁、逐关截图对比、NovaLanding、Next.js 独立站、合规二次创作。

## 记录要求

使用后追加到 `RECENT_USE_LOG.md`。
失败、低分、用户指出“不像/完全不是一个东西/牛头不对马嘴”时，追加到 `FAILURE_REVIEW.md`，并回到对应关卡重跑。
