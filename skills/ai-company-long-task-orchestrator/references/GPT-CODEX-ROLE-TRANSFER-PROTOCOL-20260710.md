# GPT—Codex Role and Transfer Protocol

This is the durable canonical protocol. User-facing copies may be exported to dated task folders, but this skill must never depend on those folders.

## Role contract

- **GPT** performs reasoning inside the active controller: goal extraction, option analysis, planning, risk judgment, evidence interpretation, and repair strategy. GPT output is not verified fact until the controller checks it.
- **Codex** is the controller for repository, local-file, terminal, test, Git, browser, or system work. It inspects reality, performs changes, validates results, stores evidence, repairs findings, and delivers.
- **Independent review agent** is a newly instantiated, read-only-first reviewer. It receives original requirements and evidence but not the main agent's self-score. It reports P0/P1/P2/P3 findings.
- **ChatGPT Work** is a separate general-work surface for cross-app, office, document, slide, sheet, email, or business workflows. It is not an implicit Codex subagent.

## Required state sequence

`Route -> Read-only preflight -> Task contract -> Plan -> Execute -> Main self-check -> Independent/fallback review -> Repair/review -> Deliver -> Preserve lessons`

Each handoff must include:

`FROM / TO / INPUT / OUTPUT / EVIDENCE / OPEN_RISKS / NEXT_GATE`

## Review closure

- Multi-agent available: `REVIEW_MODE=INDEPENDENT_AGENT`; the original reviewer rechecks fixes as `CLOSED / OPEN / REGRESSION`.
- Multi-agent unavailable: `REVIEW_MODE=SELF_REVIEW_FALLBACK`; Codex runs an isolated second-pass checklist and must not call it independent review.
- P0/P1 block delivery. Any open P2 blocks `PASS`; use `PARTIAL` or `REVIEW_READY` unless repaired.

## Cross-surface transfer gate

Before sending materials to ChatGPT Work, record:

- `DATA_CLASSIFICATION`
- `REDACTION_DONE`
- `SECRETS_PII_SCAN`
- `FILES_ACTUALLY_ATTACHED`
- `ACCESS_AND_PLUGIN_CHECK`
- `DATA_CONTROL_CHECK`
- `SENSITIVE_TRANSFER_APPROVAL`

Remove secrets, tokens, passwords, PII, customer data, irrelevant logs, and unnecessary absolute paths. A local path is not an attachment. Use the minimum necessary files or a redacted summary. If the plan, plugin, workspace permission, or connected service is unavailable, stop or use a redacted manual handoff.

## Required final declaration

```text
PRIMARY_CONTROLLER=CODEX | CHATGPT_WORK
MODEL_ROLE=GPT_REASONING_INSIDE_CONTROLLER
REVIEW_MODE=INDEPENDENT_AGENT | SELF_REVIEW_FALLBACK | CHATGPT_WORK_EXTERNAL_REVIEW
REVIEWER=<actual reviewer>
STATUS=PASS | REVIEW_READY | PARTIAL | BLOCKED
```

