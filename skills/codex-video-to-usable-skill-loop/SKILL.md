---
name: codex-video-to-usable-skill-loop
description: Use when the user provides a valuable video, tutorial, article, screenshot, chat record, failure review, or successful Codex method and asks to preserve it, deploy it, avoid it getting lost, turn it into rules/SOP/checklists/templates/AGENTS.md patches, or make future Codex tasks automatically reuse it.
---

# codex-video-to-usable-skill-loop

## Purpose

Turn high-value learning material into long-lived Codex capability: a skill, rule patch, SOP, checklist, template, preflight check, usage log, and clickable acceptance evidence.

The goal is not to summarize material. The goal is to make future Codex work measurably better by causing the lesson to be discovered and reused before similar tasks start.

## Mandatory Workflow

1. Intake the material into `K:\AI\inbox\codex-learning-materials\01-new` or the active project `materials` folder.
2. Judge material value using `rules/MATERIAL-VALUE-JUDGEMENT-RULE.md`.
3. If high value, extract executable lessons: triggers, failure modes, rules, SOP steps, checklists, templates, scripts, and acceptance criteria.
4. Write reusable skill assets into the most relevant C-drive Codex skill first. Do not overwrite existing `SKILL.md`, `AGENTS.md`, or `README.md` without a timestamped backup. Treat K-drive copies as backup/history/reference unless the user explicitly asks to restore from them.
5. Bind every lesson to trigger phrases, preflight checks, a failure-review entry point, usage logging, and acceptance evidence.
6. Run `scripts/preflight_reuse_check.py` before complex related work to search existing skills, workspaces, and rules.
7. Generate or update a clickable HTML acceptance page showing what was created and how future runs will trigger it.
8. Report an honest status: `PASS`, `REVIEW_READY`, `PARTIAL`, or `BLOCKED`.

## Required Outputs

For each converted material, produce:

- material value judgment
- executable lesson extraction
- rule patch
- SOP or checklist
- optional templates or scripts when they reduce repeated work
- AGENTS.md patch draft, not direct unsafe overwrite
- clickable HTML acceptance page
- final deployment report
- usage log entry

## Anti-Dust Requirements

A lesson is not considered deployed unless it includes:

- applicable scenarios
- trigger keywords
- Codex preflight action
- failure review entry point
- recent-use log location
- verification evidence
- next-run reuse instruction

If any item is missing, mark the deployment `PARTIAL` and fix it before claiming `PASS`.

## Resource Map

- `rules/MATERIAL-VALUE-JUDGEMENT-RULE.md`: decide whether a material deserves skill conversion.
- `rules/CODEX-PREFLIGHT-REUSE-CHECKLIST.md`: required reuse scan before complex tasks.
- `sop/VIDEO-TO-USABLE-SKILL-SOP.md`: end-to-end conversion procedure.
- `templates/`: reusable drafts for AGENTS patches, failure reviews, lesson extraction, and acceptance pages.
- `scripts/scan_reusable_assets.py`: scan existing K-drive and local Codex skill assets.
- `scripts/preflight_reuse_check.py`: task-specific reuse check before starting work.

## Start-of-Task Rule

Before starting a complex task related to learning material, Codex must check whether a mature skill, workspace, SOP, rule patch, or failure review already exists. Runtime skill loading is C-drive first:

- `C:\Users\A\.codex\skills`
- `K:\AI\skills` as backup/history/reference only
- `K:\AI\workspaces` as backup/history/reference only

If reusable C-drive material exists, read and apply it. If only K-drive material exists, use it as evidence or a restore candidate, then prefer creating or repairing the C-drive skill entry. If none exists, proceed with a new plan and consider whether the result should be converted back into this loop.

