# Context Budget Patch Template

## purpose

Add context budget, progressive disclosure, reports archive, and compact handoff rules.

## inputs

- target README
- target RUNBOOK
- source-of-truth map
- reports/index if present

## forbidden scope

- full-read reports by default
- full-read backups by default
- full-read all templates when one is needed

## gates

1. measure entry files and reports
2. add context budget source
3. patch entry files
4. create reports/index
5. add verify-context-budget
6. run verification

## required evidence

- context-budget-readback
- selected-template declaration
- loaded-source-files list
- reports-read list
- verify-context-budget output

## script verification

Run verify-context-budget-rules or package equivalent.

## final status codes

- ECC_CONTEXT_BUDGET_PATCH_PASS

## failure status codes

- ECC_CONTEXT_BUDGET_PATCH_STOP
