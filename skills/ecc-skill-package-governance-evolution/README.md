# ECC技能包治理进化技能包

English name: ECC Skill Package Governance Evolution

This skill package is for skill-package governance. It upgrades, compresses, audits, and verifies other skill packages.

It is not a business engineering task runner. It does not execute L4/L5 engineering work by itself.

## Based On Mature ECC Transformations

This package extracts reusable methods from recent ECC governance work:

- Context Budget（上下文预算）：控制一次读多少规则和报告。
- Progressive Disclosure（渐进加载）：用到什么读什么。
- Reports Archive（报告归档）：reports 是历史证据库，不默认全读。
- Script Verification（脚本验证）：硬规则必须用脚本或确定性检查验证。
- Stage Gate Script Verification（阶段门脚本验证）：每个 gate PASS 都需要验证产物。
- Declared Requirement 100%（声明要求 100%）：写过的 must 必须进入 ledger。
- Logical 100%（逻辑 100%）：证据闭环，不是绝对未来无 bug。
- Artifact Checkpoint Closure（产物检查点闭合）：文件、hash、git 状态、untracked disposition 闭合。

## Start Here

1. Read `RUNBOOK.md`.
2. Read `SOURCE-OF-TRUTH-MAP.md`.
3. Select one template from `templates\`.
4. Do not read reports by default.
5. Run `scripts\verify-governance-skill.mjs` before final PASS.

Status:
`ECC_SKILL_GOVERNANCE_EVOLUTION_SKILL_CREATED`
