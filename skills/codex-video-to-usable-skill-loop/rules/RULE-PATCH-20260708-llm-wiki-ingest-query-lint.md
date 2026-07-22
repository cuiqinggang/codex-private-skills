# RULE PATCH 20260708 - LLM Wiki Ingest Query Lint

## Status

active

## Purpose

Deploy the Karpathy-style LLM Wiki lesson as a reusable rule for high-value learning materials. The goal is to prevent valuable videos, articles, tutorials, success methods, and failure reviews from becoming one-off summaries.

## Core Rule

When a user provides high-value material, Codex must prefer this durable route:

```text
raw source -> LLM Wiki source page -> concept/entity pages -> index update -> optional skill/SOP/checklist
```

Do not stop at a chat summary. Do not only place the result in a skill package. If the lesson is reusable, it should also become human-readable Obsidian/Wiki knowledge.

## Trigger Phrases

Use this rule when the user says or implies:

- LLM Wiki
- Karpathy LLM Wiki
- 卡帕西知识库
- RAG vs Wiki
- 入库编译
- 体检知识库
- ingest/query/lint
- 知识复利
- 提前编译
- 结构化 Wiki
- 以后要用上
- 不要落灰
- 部署完成

## Required Behavior

1. Preserve raw evidence without editing the source material.
2. Create or update a source page that explains where the material came from.
3. Create concept/entity pages for reusable ideas, methods, tools, or rules.
4. Update the relevant index page.
5. Add the lesson to a skill/SOP/checklist only when it needs executable behavior.
6. After query-style answers, judge whether the answer should be written back into the Wiki.
7. When the user says "体检知识库", run a Wiki lint pass for orphan pages, missing links, stale pages, contradictions, uncompiled high-value notes, source coverage, and frontmatter consistency.

## System Split

Do not collapse the whole AI Company OS into LLM Wiki.

```text
LLM Wiki: knowledge body compilation
Knowledge Brain: routing and index layer
skills: executable capabilities
CodeGraph: code understanding
Documents/Codex: task outputs and acceptance reports
```

## C-Drive Hot Path

Default LLM Wiki target:

```text
${REDACTED_SECRET}
```

Historic `H:\AI` and `K:\AI` paths are backup/reference/migration clues only unless the user explicitly asks to use them.

## Acceptance Criteria

A high-value material ingestion is complete only when it has:

- raw/source evidence
- source page
- concept or entity page where appropriate
- index update
- necessary bidirectional links
- writeback log or recent-use record
- no obvious lint failure
- user-readable report or acceptance page

