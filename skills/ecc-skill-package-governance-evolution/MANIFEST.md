# ECC Skill Package Governance Evolution Manifest

## Package

- Directory: `H:\AI\skills\ecc-skill-package-governance-evolution`
- Chinese name: ECC技能包治理进化技能包
- Purpose: reusable method for skill package governance, compaction, source-of-truth mapping, context budget, progressive disclosure, script verification, stage gate verification, and governance iteration.

## Intended Use

Use this skill when a skill package needs:

1. Logic compaction.
2. Source-of-truth restructuring.
3. Context budget and progressive disclosure rules.
4. Reports archive indexing.
5. Claude-style mature practice migration.
6. Script verification for hard rules.
7. Stage gate secondary verification.
8. Declared Requirement 100% closure.
9. Logical 100% proof-chain closure.
10. Artifact Checkpoint Closure.
11. Multi-agent evidence audit.
12. Mature replay from a completed governance patch.
13. Skill-package readback before creating a new task package.

## Do Not Use For

Do not use this package to:

1. Execute L4/L5 engineering tasks directly.
2. Modify an unrelated project workspace without an explicit task.
3. Treat a skill governance patch as business-project completion.
4. Replace target-package verification with model self-claim.
5. Full-read reports or backups by default.

## Root Files

- `SKILL.md`
- `README.md`
- `RUNBOOK.md`
- `SOURCE-OF-TRUTH-MAP.md`
- `CONTEXT-BUDGET-RULES.md`
- `SCRIPT-VERIFICATION-RULES.md`
- `GOVERNANCE-EVOLUTION-METHOD.md`
- `MATURE-REPLAY-METHOD.md`
- `FAILURE-PATTERN-CATALOG.md`
- `GLOSSARY-ZH.md`
- `MANIFEST.md`

## Templates

- `templates\SKILL-GOVERNANCE-PATCH-TEMPLATE.md`
- `templates\SKILL-LOGIC-COMPACTION-TEMPLATE.md`
- `templates\SOURCE-OF-TRUTH-MAP-TEMPLATE.md`
- `templates\CONTEXT-BUDGET-PATCH-TEMPLATE.md`
- `templates\STAGE-GATE-SCRIPT-VERIFICATION-TEMPLATE.md`
- `templates\DECLARED-REQUIREMENT-100-TEMPLATE.md`
- `templates\ARTIFACT-CHECKPOINT-CLOSURE-TEMPLATE.md`
- `templates\FINAL-REPORT-TEMPLATE.md`
- `templates\COMPLETION-LEDGER-TEMPLATE.md`

## Scripts

- `scripts\verify-required-files.mjs`
- `scripts\verify-context-budget-rules.mjs`
- `scripts\verify-stage-gate-rules.mjs`
- `scripts\verify-governance-skill.mjs`

## Examples

- `examples\example-context-budget-patch-summary.md`
- `examples\example-stage-gate-script-verification-summary.md`

## Reports

- `reports\creation-20260527\G00-source-readback.md`
- `reports\creation-20260527\G01-directory-preparation.md`
- `reports\creation-20260527\G01-design.md`
- `reports\creation-20260527\G02-files-created.md`
- `reports\creation-20260527\G03-verification.md`
- `reports\creation-20260527\final-report.md`
- `reports\creation-20260527\verify-required-files.json`
- `reports\creation-20260527\verify-context-budget-rules.json`
- `reports\creation-20260527\verify-stage-gate-rules.json`
- `reports\creation-20260527\verify-governance-skill.json`

## Verification Requirement

Before final PASS, run:

```powershell
node scripts\verify-required-files.mjs
node scripts\verify-context-budget-rules.mjs
node scripts\verify-stage-gate-rules.mjs
node scripts\verify-governance-skill.mjs
```

All scripts must PASS. If a script fails, return to the matching creation gate and fix the package before final report.

## Final Status Codes

Allowed final PASS status codes for this creation task:

- `ECC_SKILL_GOVERNANCE_EVOLUTION_SKILL_CREATED`
- `ECC_SKILL_PACKAGE_MODIFICATION_METHOD_SAVED`
- `ECC_CONTEXT_BUDGET_AND_SCRIPT_VERIFICATION_REPLAYABLE`

Failure output must use the matching `Gxx_STOP` code and must not emit final PASS status codes.
