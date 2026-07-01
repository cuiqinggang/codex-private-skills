# Skill Logic Compaction Template

## purpose

Compress duplicated skill package rules into source-of-truth files and short entry files.

## inputs

- README / RUNBOOK
- current rule files
- templates
- prompts

## forbidden scope

- deleting capabilities
- weakening hard gates
- reading all reports by default

## gates

1. map duplicates
2. choose authoritative source
3. rewrite entry files as navigation
4. update references
5. verify capability preservation

## required evidence

- duplicate map
- source-of-truth map
- capability preservation checklist
- keyword consistency check

## script verification

Run verify-required-files and context-budget checks.

## final status codes

- ECC_SKILL_LOGIC_COMPACTION_PASS

## failure status codes

- ECC_SKILL_LOGIC_COMPACTION_STOP
