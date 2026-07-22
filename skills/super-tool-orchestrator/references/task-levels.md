# Task Levels

## L0 Simple Answer

Use for direct explanation or small factual answers. Do not create files unless the user asks.

## L1 Short Execution

Use for one small local action, one file edit, or one simple command. Verify briefly.

## L2 Standard Task

Use normal Codex engineering workflow. Read relevant files, make scoped changes, run available checks, summarize.

## L3 Long Task

Use `long-coding-flow`. Required when the task may take more than one focused session, needs handoff, rollback, logs, or staged verification.

## L4 High-Risk / Multi-System / Evolution Task

Use `long-coding-flow`, 12 Layer governance, and evolution candidate review. Required for:

- skill creation or skill upgrade,
- multiple tools or agents,
- long-running automation,
- global configuration,
- production-like changes,
- high blast radius file changes,
- repeated failure repair.

## L5 Super Task

Use Codex-first intelligence brief and GPT gate review. Required for:

- "super tool" or system architecture design,
- multi-agent operating system design,
- combining GPT, Codex, Claude-style skills, bridge, evolution, or external skill sources,
- strategic business or product system decisions,
- tasks where GPT must be the final high-level reviewer.

## Upgrade Rules

Upgrade if scope expands, risk increases, verification becomes unclear, external skills conflict, or the task starts generating reusable system behavior.

## Downgrade Rules

Downgrade only when the goal is narrow, reversible, low risk, and does not need GPT review or long-task records.
