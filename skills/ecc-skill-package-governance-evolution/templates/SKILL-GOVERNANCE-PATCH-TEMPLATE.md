# Skill Governance Patch Template

## purpose

Patch an existing skill package with a new governance rule or verification gate.

## inputs

- target skill package path
- source-of-truth files
- current reports/index if present
- mature case final report if needed

## forbidden scope

- unrelated workspaces
- secrets
- production config
- full reports read by default

## gates

1. G00 source readback
2. G01 backup
3. G02 patch source-of-truth
4. G03 patch templates/prompts
5. G04 add or update scripts
6. G05 smoke trap
7. G06 final verification
8. G07 final report

## required evidence

- readback report
- backup report
- changed file list
- script outputs
- final report

## script verification

Run package-specific verification or deterministic checklist fallback.

## final status codes

- ECC_SKILL_GOVERNANCE_PATCH_PASS

## failure status codes

- ECC_SKILL_GOVERNANCE_PATCH_STOP
