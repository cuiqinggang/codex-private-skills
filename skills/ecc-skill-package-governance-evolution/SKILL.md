---
name: ecc-skill-package-governance-evolution
description: Internal specialist for modifying or compressing one skill package, or a proven highly overlapping cluster, with source-of-truth maps, context budgets, progressive disclosure, script verification, stage gates, requirement closure, and replayable acceptance. Do not use as the general personal-skill-library governance entry.
---

# ECC Skill Package Governance Evolution

## Purpose

中文说明：

这个技能包用于改造、压缩、治理、升级其他技能包。
它不直接执行 L4/L5 工程任务，而是提供一套方法，让技能包保持：

- 规则清晰
- 上下文轻量
- 按需加载
- 报告归档
- hard rule 有脚本验证
- gate PASS 有二次验证
- final PASS 有证据链

## When to use

使用场景：

1. 技能包变得太重，需要压缩。
2. 规则重复，需要 source-of-truth map。
3. reports 太多，需要 reports/index。
4. 任务中出现“写了但没验收”的问题。
5. 任务中出现“gate 说 PASS 但没有验证产物”的问题。
6. 需要把某次成功改造做成昨日重现方法。
7. 需要给未来 Codex 任务制定严谨命令包。

## Start here

1. Read README.md.
2. Read RUNBOOK.md.
3. Read SOURCE-OF-TRUTH-MAP.md.
4. Select one template.
5. Do not read reports by default.
6. Run `scripts\verify-governance-skill.mjs` before final PASS.

## Hard rules

1. Do not full-read reports by default.
2. Do not full-read backups by default.
3. Every declared requirement must enter ledger.
4. Every hard rule must have secondary verification.
5. Every gate PASS requires script or deterministic checklist evidence.
6. Final PASS must cite verification outputs.
