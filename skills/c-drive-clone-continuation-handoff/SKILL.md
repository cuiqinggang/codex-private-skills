---
name: c-drive-clone-continuation-handoff
description: Use when continuing this C-drive cleanup and clone-to-SSD project in a new Codex page; summarizes completed tasks 831-836, current disk layout, backup paths, created skills, safety constraints, and next-step clone rules.
---

# C Drive Clone Continuation Handoff

## Use The Handoff File First

Read the latest handoff document before taking action:

${REDACTED_SECRET}

If that desktop copy is missing, read the workspace copy:

${REDACTED_SECRET}

## Current Project State

Treat the handoff as the project source of truth:

- C: is on the 4TB ST4000 HDD, Disk 1.
- Target SSD is Great Wall GT6 1TB, Disk 0.
- Disk 0 has been prepared as GPT + `S:` + NTFS + `SSD_PREP`.
- Old Great Wall Windows 10 backup/recovery materials are on G:.
- C-drive clone has not yet been performed.

## Safety Rules

- Do not manually copy C-drive files to S:.
- Do not run sector-by-sector clone from 4TB source to 1TB target.
- Use resize-aware/intelligent/system clone.
- Reconfirm disk numbers before any destructive clone action.
- Preserve G/H/I/J because G holds the old SSD recovery package.

## Related Skills

Read these if relevant:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
