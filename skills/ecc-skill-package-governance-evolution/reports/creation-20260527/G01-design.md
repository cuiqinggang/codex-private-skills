# G01 Design

TASK_ID: ECC-SKILL-GOVERNANCE-EVOLUTION-SKILL-CREATION-20260527

Design result:

`G01_PASS_SKILL_DIRECTORY_READY`

## Design Intent

Create a reusable skill package for future skill-package governance work. The package must be short-entry, source-of-truth mapped, context-budget aware, script-verifiable, and stage-gate verifiable.

## Design Constraints

- Do not execute L4/L5.
- Do not modify L4 Run01.
- Do not modify ECC baseline core rules.
- Do not full-read reports by default.
- Do not claim completion without scripts or deterministic checks.

## Package Shape

Root source files hold methods and rules.
Templates hold repeatable task skeletons.
Scripts enforce deterministic verification.
Reports record creation evidence.
Examples show how to summarize mature patches without copying all historical logs.
