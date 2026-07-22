---
name: codex-video-to-usable-skill-loop
description: Use when the user provides a valuable video, tutorial, article, screenshot, chat record, failure review, or successful Codex method and asks to preserve it, deploy it, avoid it getting lost, turn it into rules/SOP/checklists/templates/AGENTS.md patches, or make future Codex tasks automatically reuse it.
---

# codex-video-to-usable-skill-loop

## Purpose

Turn high-value learning material into long-lived Codex capability: a skill, rule patch, SOP, checklist, template, preflight check, usage log, and clickable acceptance evidence.

The goal is not to summarize material. The goal is to make future Codex work measurably better by causing the lesson to be discovered and reused before similar tasks start.

## Mandatory Workflow

${REDACTED_SECRET}
2. Judge material value using `rules/MATERIAL-VALUE-JUDGEMENT-RULE.md`.
3. If high value, extract executable lessons: triggers, failure modes, rules, SOP steps, checklists, templates, scripts, and acceptance criteria.
4. For high-value knowledge material, compile it into the C-drive LLM Wiki route when appropriate: `raw source -> source page -> concept/entity pages -> index update -> optional skill/SOP`. See `rules/RULE-PATCH-20260708-llm-wiki-ingest-query-lint.md`.
5. Write reusable skill assets into the most relevant C-drive Codex skill first. H is history-only and must never receive writes. Do not create an automatic safety backup. A C-to-K backup is allowed only after the C copy validates and the user explicitly approves that specific backup action.
6. Bind every lesson to trigger phrases, preflight checks, a failure-review entry point, usage logging, and acceptance evidence.
7. Run `scripts/preflight_reuse_check.py` before complex related work to search C-drive skills, documents, and rules. Add `--include-backups` only when the user explicitly asks to inspect or restore K-drive backup/history. A missing C-drive asset must block and must not enable backup scanning automatically.
8. Generate or update a clickable HTML acceptance page showing what was created and how future runs will trigger it.
9. Report an honest status: `PASS`, `REVIEW_READY`, `PARTIAL`, or `BLOCKED`.

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
- `rules/RULE-PATCH-20260708-llm-wiki-ingest-query-lint.md`: high-value material must be compiled into LLM Wiki source/concept/entity pages when reusable.
- `sop/VIDEO-TO-USABLE-SKILL-SOP.md`: end-to-end conversion procedure.
- `sop/SOP-20260708-llm-wiki-ingest-query-lint.md`: ingest/query/lint workflow for the C-drive Obsidian LLM Wiki route.
- `checklists/LLM-WIKI-INGEST-QUERY-LINT-CHECKLIST-20260708.md`: acceptance checklist for Wiki compilation and lint.
- `templates/`: reusable drafts for AGENTS patches, failure reviews, lesson extraction, and acceptance pages.
- `scripts/scan_reusable_assets.py`: scan C-drive Codex skill assets by default; K-drive backup/history scanning requires `--include-backups`.
- `scripts/preflight_reuse_check.py`: task-specific reuse check before starting work.
- `scripts/wiki_lint_basic.ps1`: read-only basic lint for the C-drive Obsidian LLM Wiki layer.

## Start-of-Task Rule

Before starting a complex task related to learning material, Codex must check whether a mature skill, workspace, SOP, rule patch, or failure review already exists. Runtime skill loading is C-drive first:

${REDACTED_SECRET}
${REDACTED_SECRET}
- `K:\AI\skills` and `K:\AI\workspaces` only through explicit `--include-backups`

If reusable C-drive material exists, read and apply it. Do not probe K during ordinary preflight. If the C-drive hot library is missing the required asset, return `BLOCKED_C_SOURCE_MISSING`. Inspect or restore K backup material only after the user explicitly authorizes that separate operation; never auto-fallback.

