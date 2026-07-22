---
name: ui-design-system-router
description: Use when Codex must select a UI direction, generate or validate a project-specific DESIGN.md, audit or redesign an existing interface without changing business logic, or update an offline design-reference library. Triggers include UI 风格选择、设计系统、DESIGN.md、界面一致性、UI 审查、UI 重构、海外 SaaS、仪表盘和设计规范路由。
---

# UI Design System Router

Route product context to an original, maintainable design system. Treat bundled brand analyses as design-language references, never as permission to copy brand identity.

## Start workflow

1. Run the task-specific reuse preflight.
2. Identify product type, audience, geography, enterprise/consumer bias, density, conversion goal, dashboard need, brand tone, mobile share, stack, budget, and references.
3. Choose one workflow below and read its matching file in `workflows/`.
4. Search `catalog/catalog.json`; select one primary archetype and at most one supporting archetype.
5. Generate project-owned output using `scripts/compose_design_md.py`.
6. Validate with `scripts/validate_design_md.py`; fix every FAIL before handoff.
7. Apply `references/originality-rules.md` and `references/commercial-safety-rules.md`.
8. Log failures in `FAILURE_REVIEW.md` and successful use in `RECENT_USE_LOG.md`.

## Workflows

- Select direction: read `workflows/select-design-direction.md`.
- Generate project DESIGN.md: read `workflows/generate-project-design-md.md`.
- Audit an existing UI: read `workflows/audit-existing-ui.md`.
- Redesign existing UI: read `workflows/redesign-existing-project.md`; preserve business logic, APIs, database schema, routes, and accessibility.
- Update the library: read `workflows/update-design-library.md`; update only in a candidate Worktree and never replace the stable skill automatically.

## Hard gates

- Runtime output must not require GitHub, getdesign.md, external APIs, remote scripts, uncached fonts, or hotlinked images.
- Do not copy logos, trademarks, proprietary illustrations, full copy, restricted fonts, proprietary icon sets, or a unique whole-page composition.
- Keep `AGENTS.md`, `DESIGN.md`, `README.md`, and product requirements separate.
- Capture before/after desktop and mobile evidence for redesigns.
- Return `PASS`, `PASS_WITH_WARNINGS`, or `FAIL` from the validator; never claim completion on FAIL.

## Key resources

- Routing data: `catalog/archetypes.json`, `catalog/use-case-map.json`.
- Baselines: `references/accessibility-baseline.md`, `references/responsive-baseline.md`.
- Templates: `templates/`.
- Source provenance: `SOURCE_MANIFEST.json` and `reports/`.
- Bundled upstream references: `references/bundled/` (read selectively, never all by default).

