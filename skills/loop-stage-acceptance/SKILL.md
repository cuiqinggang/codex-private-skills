---
name: loop-stage-acceptance
description: Execute staged or looped tasks with mandatory first draft, self-check, defect list, repair rounds, honest PASS/BLOCKED gating, per-round records, final acceptance report, and reusable lesson capture. Use when the user says Loop 执行规则, loop execution, staged acceptance, 自查修复, 验收标准, 最多 3 轮, BLOCKED 报告, 总验收报告, 可复用经验沉淀, or asks Codex to save a repeatable stage-by-stage quality workflow.
---

# Loop Stage Acceptance

## Purpose

Apply a strict loop discipline to multi-stage work. Each stage must produce a first result, inspect it against explicit acceptance criteria, list defects, repair defects, and repeat until the stage passes or reaches the maximum repair limit.

Do not claim success unless all key acceptance items pass. If the maximum repair rounds are exhausted, stop and report `BLOCKED`.

## Core Workflow

For every stage:

1. Define or restate the stage goal and key acceptance criteria.
2. Generate the first version of the stage result.
3. Self-check the result against the acceptance criteria.
4. List all failed or uncertain items.
5. Repair only the failed or risky items unless broader change is necessary.
6. Self-check again.
7. Continue repair and self-check for at most 3 repair rounds.
8. Proceed to the next stage only when all key acceptance items pass.
9. Stop with a `BLOCKED` report if key acceptance items still fail after 3 repair rounds.
10. Record every round using `references/stage-log-template.md`.

## Per-Round Record

Each round must record:

- current stage and round number
- what changed
- why it changed
- acceptance items that passed
- acceptance items that did not pass
- decision: continue, advance, or block

## PASS Rules

A stage may pass only when all key acceptance items are met or explicitly waived by the user. Do not downgrade a key failure into a note or caveat just to continue.

The whole task may pass only after:

- every stage passed or was explicitly removed from scope by the user
- the final output includes a total acceptance report
- reusable lessons are captured when the run reveals a repeatable rule, checklist, template, script, or failure mode

## BLOCKED Rules

Return `BLOCKED` when any key acceptance item remains unresolved after 3 repair rounds in the same stage, or when required information, access, tooling, or user input is missing and cannot be safely inferred.

The `BLOCKED` report must include:

- blocked stage
- failed acceptance items
- repair rounds already attempted
- why further repair is unsafe or impossible
- exact user input, access, or external change needed to continue

## Final Report

End looped tasks with:

- final status: `PASS`, `PARTIAL`, or `BLOCKED`
- stage-by-stage acceptance summary
- important defects found and repaired
- remaining risks or skipped non-key items
- reusable lessons captured or a clear note that none were found

## Reuse And Growth

Treat this skill as an expandable container. When a future loop run produces a reusable checklist, failure review, template, or script, add it under this skill or a more specific related skill.

Before adding material:

- keep `SKILL.md` concise
- put detailed reusable formats in `references/`
- avoid overwriting existing files without a timestamped backup
- preserve trigger phrases and acceptance evidence

Use `references/stage-log-template.md` for detailed round logs.

Read `references/loop-prompt-patterns.md` when the task is about writing, improving, or choosing a Loop prompt for dashboards, long Codex tasks, skill conversion, low-cost exploration, image/video work, Obsidian archiving, software repair, or one-person AI company planning.

Read `references/case-ai-company-os-loop-rule-integration.md` when the task is about integrating Loop Prompt rules into another skill package, especially when the user provides a Codex command package with explicit allow/forbid boundaries, backup requirements, manifest generation, evidence reports, or H-drive synchronization.

Read `references/case-loop-engineering-video-standard.md` when the task involves Loop Engineering, `/loops`, validation-driven agents, harnesses, routines vs loops, cron vs loop, mega-prompt vs loop, or deciding whether a task is suitable for loop execution.
