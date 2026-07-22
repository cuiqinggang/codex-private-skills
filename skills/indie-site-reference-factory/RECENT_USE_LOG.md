# RECENT_USE_LOG

## 2026-07-10 Framer gate-proof writeback hardening

- User feedback: earlier loose/simple tests were not useful; only the real Framer gate test with per-stage visible comparison images proved the skill had value.
- Skill update: `SKILL.md` now directly points to the real Framer proof, `commands/06_real_stage_gate_visual_proof.md`, and `references/FRAMER_STAGE_GATE_REAL_TEST_20260709.md`.
- Validator update: `validate_stage_gate.ps1` now requires `<GATE_ID>_comparison.png` for every visual gate; `validate_progress_gate.ps1` also checks comparison boards and report references for G10-G60.
- Report update: Framer test reports G10-G60 now reference their comparison boards.
- Validation after update: quick_validate PASS; G10/G20/G30/G40/G50/G60 PASS; progress gate returned `PROGRESS_GATE=CLONE_SIMILARITY_PASS`.
${REDACTED_SECRET}

## 2026-07-09 Framer real stage-gate test

- Task: run a real, visually valuable indie-site clone test against https://www.framer.com after the stage-gate repair.
${REDACTED_SECRET}
- Evidence style: every visual gate produced a four-image comparison board and an explicit desktop/mobile/overall score before proceeding.
- Gate result: G30 was blocked at 87%, repaired locally, then passed at 96%; G50 was blocked at 85%, repaired locally, then passed at 95%.
- Final result: G90_FINAL PASS; validate_progress_gate.ps1 returned PROGRESS_GATE=CLONE_SIMILARITY_PASS with Desktop=95%, Mobile=95%, Overall=95%.
- Key rule reinforced: if a gate image is not shown in chat and not referenced in the progress package, the gate is not considered truly complete.

## 2026-07-09
- 任务：建设 indie-site-reference-factory 并执行真实 Framer 参考测试。
- 模式：reference_to_indie_site。
- 目标：生成 NovaLanding Next.js 独立站并完成截图/build/QA/ZIP。
- 用户复核：旧版没有达到克隆相似度要求，PASS 撤回。技能包已改为强制进度包与 95% 相似度门禁。
- 视频材料：视频补充材料已转写。核心内容：给定 URL 后，流程应先侦察源站，再提取字体、颜色和样式规范，生成组件文件，使用多个 AI agent 并行构建区块，最后合并并做视觉对比 QA。该视频强化了本技能包的“先证据、后生成、再验收”规则。

## 2026-07-09 阶段门禁系统修复

- 修复目标：把技能包从最终验收式流程升级为每关硬门禁。
- 新增：12_STAGE_GATE_EXECUTION_PROTOCOL.md、templates/STAGE_GATE_REPORT_TEMPLATE.md、scripts/validate_stage_gate.ps1。
- 更新：SKILL.md、05/06/10/11、commands/02、commands/05、scripts/validate_progress_gate.ps1。
- 验证：G00-G03 烟测 PASS；G10 低分 78/42/64 被 STATUS=GATE_BLOCKED；最终门禁缺阶段报告为 INVALID_TEST；quick_validate PASS；Knowledge Brain health/hot sync PASS。
${REDACTED_SECRET}
