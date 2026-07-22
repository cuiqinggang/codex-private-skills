# Architecture

## System Shape

The super tool is a long-task operating system, not a single giant prompt.

```text
User goal
  -> Codex intelligence collection
  -> GPT planning/review when needed
  -> Codex staged execution
  -> independent verification
  -> repair loop
  -> final acceptance
  -> evolution candidate
```

## Roles

| Component | Role | Boundary |
|---|---|---|
| GPT / ChatGPT | strategic planning, high-level judgment, gate review | does not directly operate files, accounts, production config, or secrets |
| Codex Desktop | local context, tools, execution, evidence, verification, handoff | does not self-declare final PASS on complex tasks |
| Screenshot bridge | text transport between Codex and GPT web | text-only, no sensitive account/security/payment workflows |
| long-coding-flow | long task stages, logs, verification, handoff, rollback | one bounded stage at a time |
| Claude-style 12 Layer | governance, separation of execution/verification/acceptance | not a generic 12-step checklist |
| system-evolution | sediment validated experience | default report/candidate mode, no production changes |
| external skills | mature source material and optional install targets | read or install only after conflict review |

## Core Principle

Do not merge all capabilities into one huge skill. The orchestrator chooses routes, loads only the relevant details, and delegates to existing skills.
