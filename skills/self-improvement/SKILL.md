---
name: self-improvement
description: Use when this Windows Codex studio needs to record reusable lessons, mistakes, corrections, successful baselines, or workflow follow-ups without depending on old OpenClaw memory files. Use for local task retrospectives and skill improvement notes; only update durable memory when the user explicitly asks.
---

# Self Improvement Windows Studio

Use this skill to turn task evidence into reusable local guidance.

## Boundaries

- Do not edit Codex memory files unless the user explicitly asks to update memory.
- Do not invent durable preferences from one-off behavior.
- Do not store secrets, account data, private tokens, or sensitive personal content.
- Prefer project docs or skill updates when the lesson is workflow-specific.

## Workflow

1. Identify the reusable lesson: failure mode, command, port boundary, rollback, verification, or skill trigger.
2. Decide destination:
   - current final answer for one-time lesson
   - project docs for workspace-specific rule
   - skill update for repeatable workflow
   - memory note only when explicitly requested
3. Keep the note short and evidence-backed.
4. Include date, scope, what worked, what failed, and next action.
5. Verify the note does not expose secrets or overgeneralize.

## Codex Rollout Self-Improvement Audit

Use the rollout audit route when the user asks whether Codex can become
smarter over time, asks to review recent Codex work, or asks to turn repeated
work into skills, agents, or scheduled automations.

Reference:

- `references/codex-rollout-self-improvement-prompt-20260706.md`

Local helper:

- `scripts/run-codex-self-improvement-audit.ps1`

Audit rule:

1. Look back over recent work, preferably the last 30 days.
2. Use available evidence in this order: Codex session/task summaries, durable
   reports, Knowledge Brain indexes, existing skills, and automation records.
3. Only act on candidates that repeated at least twice or are clearly likely
   to recur, have stable inputs and outputs, improve quality/speed/reliability,
   and are not already covered.
4. Choose the smallest useful form: skill, subagent, automation, extend
   existing, or skip.
5. Create only high-confidence, narrow, practical assets with acceptance
   evidence.

## Verification

- PASS: lesson is concise, scoped, evidence-backed, and stored in the right place.
- FAIL: lesson is vague, sensitive, not reusable, or written to memory without explicit request.
