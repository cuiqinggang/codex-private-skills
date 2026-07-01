---
name: super-tool-orchestrator
description: Use for L3-L5 Codex tasks that require Codex-first intelligence gathering, staged execution, GPT gate review, long-coding-flow, 12 Layer governance, final acceptance, external skill conflict control, or cautious skill evolution. Do not use for simple Q&A, one-off writing, or ordinary short edits.
---

# Super Tool Orchestrator

## Purpose

Turn complex user goals into tasks that are:

- clear in goal and boundary,
- routed to the right skills,
- staged into verifiable gates,
- reviewed by GPT when the task is strategic or high risk,
- executed by Codex with evidence,
- recoverable through handoff files,
- closed only through final acceptance,
- eligible for cautious self-improvement.

This skill is a coordinator. It does not replace `long-coding-flow`, `complete-claude-style-replica-flow`, `chatgpt-screenshot-bridge`, `system-evolution`, or domain skills.

## When Not To Use

Do not use this skill for:

- simple Q&A, translation, explanation, or brainstorming;
- one-off writing or rewriting tasks;
- single-step file edits that do not need staged verification;
- ordinary code fixes that fit an existing domain skill;
- image generation or image repair tasks;
- tasks where the user explicitly asks not to use long-task orchestration;
- account login, captcha, payment, API key, Cookie, or production admin operations;
- direct installation, copying, adaptation, merge, or overwrite of external skills without audit and user approval.

## Hard Rules

1. Codex-first means Codex gathers context, evidence, relevant skills, local history, and public mature references before GPT planning. It does not mean Codex-final.
2. GPT is the planning and review brain for L4-L5 tasks; Codex is the execution, evidence, verification, and sedimentation body.
3. Do not claim final PASS without `final-acceptance.md` and `final-acceptance.json`.
4. Execution Plane submits claims only. It cannot self-accept.
5. Verification Plane accepts or rejects claims using evidence and deterministic checks.
6. Repair Loop is mandatory for rejected claims.
7. Keep the orchestrator lean. Put detailed policies in `references/`, templates in `templates/`, and repeatable checks in `scripts/`.
8. External skills such as `anthropic-agent-skills` are sources. Do not bulk-install or overwrite local skills without conflict audit and user approval.
9. Stop before account login, captcha, payment, API keys, cookies, production configuration, long-lived background services, or global rule changes.
10. Screenshot bridge is text-only planning transport. Stop on login, captcha, account/security, payment, privacy-sensitive forms, or unsafe UI state.
11. Do not activate screenshot bridge by default. Use it only when the current task explicitly requires GPT web review/transport, the user has allowed it, and safer file/manual transfer is insufficient.
12. For L4-L5, do not execute implementation work before creating a Codex intelligence brief and routing decision.
13. For L5, GPT review must be based on a Codex intelligence brief. Do not ask GPT for a final plan from raw user text alone unless the brief is explicitly unavailable and the reason is recorded.
14. For L3-L5, final acceptance must include evidence files, verification results, known limitations, and handoff/next actions. A final acceptance file that only repeats claims is invalid.
15. Evolution candidate is not a patch. Do not modify existing skills from an evolution candidate unless a separate patch plan is approved.
16. External skills are read-only references by default. Installing, copying, adapting, merging, or overwriting external skills requires external-skill-audit and user approval.
17. Runtime task reports should be written into the task workspace, not into this skill directory. The skill reports directory is only for skill creation, validation, and sample reports.

## Task Level Routing

Use `references/task-levels.md` for details.

| Level | Route |
|---|---|
| L0 | Answer directly. No orchestration. |
| L1 | Short Codex execution with brief verification. |
| L2 | Standard Codex workflow with tests/checks. |
| L3 | Use `long-coding-flow`. |
| L4 | Use `long-coding-flow` + 12 Layer governance + evolution candidate review. |
| L5 | Codex intelligence brief -> GPT review via bridge -> gated Codex execution -> GPT gate reviews -> final acceptance. |

Upgrade to L4/L5 when the task spans multiple systems, skills, long execution, global configuration proposals, production-like planning, strategic architecture, or self-evolution. If accounts, payment, captcha, API keys, cookies, or production admin actions are involved, stop and request explicit user approval before any action.

## Required Workflow For L4-L5

1. Build a Codex intelligence brief from `templates/codex-intelligence-brief/brief.md`.
2. Read only the relevant policy references:
   - `references/architecture.md`
   - `references/gpt-codex-loop.md`
   - `references/safety-boundaries.md`
   - `references/external-skill-sources.md` when external skills are involved
   - `references/evolution-policy.md` when skill improvement is involved
3. Create or update a task package using `templates/universal-task-package/`.
4. Validate the package with `scripts/validate-task-package.ps1`.
5. For GPT review, send a gate review request from `templates/gate-review-request/request.md`.
6. Execute only the approved current gate.
7. Record evidence, verification, and claims.
8. If rejected, use `templates/repair-command-package/package.md`.
9. Close with final acceptance using `templates/final-acceptance/`.
10. Consider evolution only through `templates/evolution-candidate/candidate.md`.

## Output Contract

For substantial tasks, produce or update:

- a task package,
- a gate review request/result when GPT is used,
- verification evidence,
- handoff/next action notes,
- final acceptance files,
- evolution candidates only when validated.

## References

- `references/architecture.md`: component roles and system shape.
- `references/task-levels.md`: L0-L5 routing.
- `references/gpt-codex-loop.md`: Codex-first and GPT gate review protocol.
- `references/bridge-policy.md`: screenshot bridge boundaries.
- `references/long-coding-flow-integration.md`: how to use the long task package.
- `references/twelve-layer-governance.md`: 12 Layer control plane mapping.
- `references/external-skill-sources.md`: Anthropic and other skill source rules.
- `references/evolution-policy.md`: self-improvement rules.
- `references/safety-boundaries.md`: stop conditions.
- `references/conflict-policy.md`: skill and file conflict rules.
- `references/acceptance-policy.md`: final PASS rules.
