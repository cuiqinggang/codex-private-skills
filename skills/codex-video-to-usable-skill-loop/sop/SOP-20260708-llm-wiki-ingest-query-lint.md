# SOP 20260708 - LLM Wiki Ingest Query Lint

## Use When

Use this SOP for high-value videos, articles, tutorials, screenshots, chat records, failure reviews, success methods, AI Company OS lessons, Obsidian knowledge workflows, or reusable Codex process improvements.

## Workflow

### 1. Intake

Capture the source in the active project `work/materials` folder or a dedicated raw folder. For media, generate transcript and key-frame evidence when useful.

### 2. Judge Value

Use `rules/MATERIAL-VALUE-JUDGEMENT-RULE.md`.

If the material is `HIGH_VALUE`, continue. If it is lower value, create only a candidate note or archive pointer.

### 3. Preserve Raw Evidence

Keep unmodified source evidence or a durable pointer to it. For videos, preserve at least:

- original path or source URL
- transcript
- key-frame/contact-sheet evidence when the video includes screens/slides
- run manifest if transcription or extraction was used

### 4. Compile Into LLM Wiki

Write the durable knowledge into:

```text
${REDACTED_SECRET}
```

Recommended shape:

```text
raw/<date-topic>/
wiki/sources/<source-page>.md
wiki/concepts/<concept-page>.md
wiki/entities/<entity-page>.md
index.md
schema/tags.md
```

### 5. Bind To Execution

If the material changes future Codex behavior, add or update:

- rule patch
- SOP
- checklist
- trigger phrases
- recent-use log
- acceptance evidence

### 6. Query Writeback

After a knowledge-base answer, ask internally:

- Did this answer produce a reusable conclusion?
- Did it form a rule, SOP, checklist, or template?
- Did it fix a previous mistake?
- Did it fill a gap in an existing Wiki page?

If yes, write back a source/concept/entity update or create a review-ready candidate.

### 7. Lint

When the user says "体检知识库" or a Wiki ingestion is completed, check:

- orphan pages
- missing links
- stale pages
- contradiction notes
- uncompiled high-value notes
- source coverage
- frontmatter consistency

### 8. Closeout

Create an acceptance page or report that lists:

- material source
- value judgment
- files created or updated
- future trigger phrases
- next-run reuse instruction
- PASS / REVIEW_READY / PARTIAL / BLOCKED

## Acceptance

Mark `PASS` only when the lesson is discoverable from both the skill layer and the Obsidian/LLM Wiki layer. Otherwise mark `REVIEW_READY` or `PARTIAL`.

