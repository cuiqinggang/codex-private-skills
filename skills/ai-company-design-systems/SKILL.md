---
name: ai-company-design-systems
description: "Use when designing, reviewing, or updating AI-company dashboards, 公司大屏, skills visualization systems, agent/workflow graphs, approval inboxes, and local-first design-system rules for capital-scarce AI-native companies."
---

# AI Company Design Systems

Use this skill to turn an AI-native company or solo-founder operating system into an auditable dashboard and skills-visualization design system.

This is not a landing-page skill. It is for operational surfaces: company command centers, skill graphs, revenue-path boards, context asset libraries, approval inboxes, and daily reports.

## Core Judgment

An AI-company design system should make the company readable and executable by humans and agents. It should expose context assets, skills, workflows, evidence, approvals, risks, revenue paths, and replay notes in dense but understandable views.

For capital-scarce founders, avoid copying traditional org charts, decorative SaaS dashboards, or high-maintenance component platforms. Preserve the durable operating model first; implement UI only after the data model and approval boundaries are clear.

## Inherit First

Before designing or implementing:

1. Load the active workspace rules and yesterday-replay routing rules.
2. Read `H:\AI\skills\ai-company-evolving-revenue-portfolio\SKILL.md` when available.
3. Check whether the task is research-only, design-only, validation, or implementation.
4. If current public examples matter, refresh GitHub/source research before using stale repo facts.
5. Stop for real payments, ads, outreach, publishing, account/security changes, legal/tax/financial commitments, irreversible deletion, or external customer promises.

## Mature References

Use public repositories as pattern references, not as blind dependencies:

- `shadcn-ui/ui`: editable React/Tailwind component baseline.
- `vercel/ai-elements`: AI prompt, response, generation, and tool-call UI ideas.
- `ant-design/ant-design`: dense enterprise workflows, tables, and form discipline.
- `carbon-design-system/carbon`: tokens, accessibility, governance, and status semantics.
- `tremorlabs/tremor-npm`: dashboard and metric composition patterns.
- `xyflow/xyflow`: skills, agents, workflows, and dependency graph visualization.
- `recharts/recharts`: simple charting for revenue paths, status, funnels, and trends.
- `langfuse/langfuse`: AI observability concepts such as traces, prompts, evals, datasets, metrics, and auditability.

Do not copy Polsia branding, private dashboards, prompts, payment mechanics, or account-gated behavior. Do not copy license-sensitive implementation details from any reference repository. Distill data concepts and interaction patterns.

## Design Model

Use five layers.

### 1. Tokens

Define roles before colors:

- app background,
- surface,
- subtle background,
- primary text,
- secondary text,
- divider,
- action accent,
- pass,
- warn,
- stop,
- running,
- info.

Avoid one-note palettes. The UI should not read as all purple, all beige, all slate, or all brown/orange.

### 2. Components

Minimum useful component set:

- app shell,
- command bar,
- tabs,
- data table,
- status badge,
- approval panel,
- metric strip,
- graph node,
- graph edge,
- evidence link row,
- empty state,
- error state.

Use cards only for repeated items or bounded tools. Do not nest cards inside cards. Keep headings compact inside panels and dashboards.

### 3. Data Objects

Represent these objects explicitly:

- `company`: idea, target user, offer, channels, risks, approval rules, context root.
- `skill`: path, trigger, inputs, outputs, allowed actions, forbidden actions, verification.
- `agent`: role, tools, allowed scope, handoff rules, human escalation.
- `workflow`: goal, steps, skills used, inputs, outputs, evidence, rollback, status.
- `revenue_path`: customer pain, offer, channel, cost, proof strength, repeatability, risk, next test, decision.
- `approval`: action, risk level, external effect, evidence, requester, decision, reviewer, timestamp.

### 4. Views

Required views:

- company command center,
- skills visualization,
- revenue path board,
- context asset library,
- approval inbox,
- daily report.

The first screen should show current operating state, not marketing copy.

### 5. Governance

Every meaningful action should have:

- source context,
- status,
- evidence path or URL,
- risk level,
- human approval requirement,
- rollback or stop note.

Human approval is required before external effects: payment, ads, cold outreach, publishing, account/security changes, legal/tax/financial commitments, irreversible deletion, and customer promises.

## Workflow

1. Define the dashboard or visualization objective in one sentence.
2. Inventory existing skills, company assets, workflows, reports, and evidence paths.
3. Choose the target view: command center, skill graph, revenue board, asset library, approval inbox, or report.
4. Define data objects before UI components.
5. Choose references only for the layer needed: component baseline, enterprise density, graph, chart, or AI observability.
6. Draft the design-system manifest using `templates\design-system-manifest.json`.
7. Validate the manifest with `scripts\validate-skill.ps1` or a task-local validator.
8. Only then implement or update UI, using the smallest local change.
9. Verify with a static check, test, screenshot, or browser check appropriate to the change.
10. Write a gate report with PASS / STOP evidence.

## Implementation Rules

- Prefer static files, schemas, reports, and small prototypes before running services.
- Do not use reserved local ports such as 3000, 3011, 8642, or 18789 for new work.
- For frontend implementation, follow the existing app stack and design conventions first.
- For skills visualization, prefer a graph model with typed nodes and typed edges.
- For dashboards, keep metric count small and decision-oriented.
- Do not add real external automation to a prototype.
- Do not publish, send, pay, delete, or modify accounts without explicit task scope and approval.

## Read As Needed

- For current research from this package, read `references\github-research-20260526.md`.
- For the distilled design model, read `references\design-system-rules-20260526.md`.
- For a reusable manifest skeleton, use `templates\design-system-manifest.json`.

## Completion Criteria

A design-system task is complete only when:

- target view and data objects are explicit,
- approval boundaries are represented,
- references used are named,
- implementation or prototype is minimal,
- validation evidence exists,
- output/report paths are recorded,
- final status is PASS, PARTIAL, or STOP with reasons.
