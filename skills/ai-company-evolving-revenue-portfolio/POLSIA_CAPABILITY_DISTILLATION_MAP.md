# Polsia Capability Distillation Map

Polsia is not a copy target. It is a capability distillation sample for a local AI company system.

## Interface Map

```text
create_company(idea)
generate_company_workspace(company_id)
run_daily_autonomous_cycle(company_id)
create_task(company_id, task_type)
execute_agentic_task(task_id)
request_human_review(task_id)
generate_status_report(company_id)
export_company_data(company_id)
decide_continue_or_kill(company_id)
```

## Capability Translation

| Polsia visible capability | Local interface | Local implementation |
| --- | --- | --- |
| idea intake | `create_company(idea)` | Save idea, audience, offer, constraints, approval rules. |
| company workspace | `generate_company_workspace(company_id)` | Create folder, context files, task ledger, reports, assets, approvals. |
| daily cycle | `run_daily_autonomous_cycle(company_id)` | Read state, generate tasks, execute safe tasks, request approvals, report. |
| task queue | `create_task(company_id, task_type)` | Structured markdown/JSON task with cost, risk, owner, evidence. |
| coding/marketing/support tasks | `execute_agentic_task(task_id)` | Codex/Hermes/GPT runs only allowed local or draft tasks. |
| human override | `request_human_review(task_id)` | Stop before payment, sending, publishing, legal, deletion, account action. |
| status report | `generate_status_report(company_id)` | Daily markdown report with evidence, blockers, next tasks. |
| data export | `export_company_data(company_id)` | Zip or copy AI-readable company folder. |
| kill/continue decision | `decide_continue_or_kill(company_id)` | Score by proof, risk, cost, user response, repeatability. |

## Phase 1 Reproduce

Reproduce now:

- idea intake.
- workspace generation.
- market research.
- landing-page draft.
- local task queue.
- daily status report.
- export.
- human approval gates.

Do not reproduce yet:

- automatic cold outreach.
- ad campaign launch.
- Stripe/customer payments.
- revenue share.
- live customer support auto-replies.
- irreversible account/project operations.

## First Local Data Contracts

`company.md`:

```text
company_id:
idea:
target_user:
pain:
offer:
channels:
risk_notes:
approval_rules:
```

`task.md`:

```text
task_id:
company_id:
task_type:
goal:
cost_estimate:
risk_level:
requires_human_review:
inputs:
outputs:
status:
evidence:
```

`daily-report.md`:

```text
date:
company_id:
tasks_created:
tasks_done:
blocked_tasks:
human_review_needed:
metrics:
next_decision:
```
