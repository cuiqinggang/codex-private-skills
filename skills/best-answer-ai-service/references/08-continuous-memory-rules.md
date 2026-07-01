# Continuous Memory Rules

## Why This Exists

Best Answer AI is evolving through many conversations, tests, and decisions. If useful details are not saved as they appear, they will be lost.

This skill is the accumulation layer.

## What to Save

Save:

- product positioning decisions;
- workflow rules;
- prompt and V15 process changes;
- temperature and runtime parameter updates;
- pricing and cost-control decisions;
- test results;
- user feedback;
- mature path discoveries;
- blocked paths and reasons;
- decisions about what not to do yet.

## What Not to Save

Do not save:

- random chat fragments without distilled value;
- duplicate notes;
- outdated claims without marking them as old;
- secrets, API keys, cookies, passwords, payment details;
- unnecessary domain brainstorming unless it affects current positioning.

## Update Pattern

When a new useful decision appears:

1. Identify the right reference file.
2. Add a concise dated note or update the rule.
3. Preserve the reason, not just the conclusion.
4. If it changes execution behavior, update `SKILL.md` too.
5. Keep files structured and searchable.

## Current Key Decisions to Preserve

As of 2026-06-28:

- The product is a web service, not an app.
- The user-facing name is `Best Answer AI`.
- The internal engine name is `UltraFusion Engine`.
- Domain and trademark are not priorities at this stage.
- English-first is the initial commercial direction.
- High-paying SaaS regions are the first target market.
- Free mode must not run unlimited Full A/B/C/D.
- Paid mode should likely use credits or answer packs.
- A/B/C/D are all extreme layers.
- Temperature strategy is now part of the runtime rules.
- max_tokens should be tested before final values are fixed.
- Mature path / yesterday-replay style is preferred over self-invented startup process.

## Packaging Rule

When creating a Codex handoff package for this project, include:

```text
SKILL.md
references/
test plan
current decisions
next action checklist
```

For Windows desktop delivery, package as a unique three-digit ZIP when Codex completes a task on the user's machine.
