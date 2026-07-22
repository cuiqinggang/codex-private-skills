# External Skill Sources

## Anthropic Agent Skills

Current known source:

```text
${REDACTED_SECRET}
https://github.com/anthropics/skills.git
```

It is a marketplace/source repository, not one giant skill.

## Use Strategy

1. Check whether the task needs an external skill.
2. Prefer reading the relevant `SKILL.md` as a reference before installing.
3. If installation is needed, install only the specific skill.
4. If a local skill with the same name exists, perform conflict audit first.
5. Never bulk-install or overwrite local mature skills without user approval.

## Conflict Audit

Compare:

- local skill name and description,
- external skill name and description,
- overlapping triggers,
- scripts and references,
- safety differences,
- whether the external skill should be read-only reference, installed under a new name, or rejected.
