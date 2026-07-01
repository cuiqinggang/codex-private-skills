# Design-System Rules 2026-05-26

## Product Position

Build an operational AI-company cockpit, not a marketing site.

Primary surfaces:

- company command center,
- skills visualization,
- revenue path board,
- context asset library,
- approval inbox,
- daily report.

## Required Layers

1. Tokens: color roles, status roles, density, typography, spacing.
2. Components: app shell, tabs, tables, badges, approval panels, metrics, graph nodes, graph edges, evidence links, empty/error states.
3. Data objects: company, skill, agent, workflow, revenue path, approval.
4. Views: command center, skill graph, revenue board, asset library, approval inbox, report.
5. Governance: evidence, risk, human approval, rollback, and stop conditions.

## Data Contracts

`skill`:

```text
skill_id
name
path
trigger
inputs
outputs
allowed_actions
forbidden_actions
verification
last_checked
```

`workflow`:

```text
workflow_id
goal
steps
skills_used
inputs
outputs
evidence
rollback
status
```

`approval`:

```text
approval_id
action
risk_level
external_effect
evidence
requester
decision
decided_by
decided_at
```

## Human Approval Stops

Stop before:

- payment,
- ads,
- cold outreach,
- publishing,
- account or security changes,
- legal, tax, or financial commitments,
- irreversible deletion,
- external customer promises.

## Visual Rules

- Dense, structured, and scannable beats decorative.
- Do not use a hero page as the first screen for this tool class.
- Do not nest cards.
- Keep status and approval visible in the layout.
- Use graph views for dependencies and capability boundaries, not decoration.
- Use charts only when they support a decision.
