# Twelve Layer Governance

This is the user's Claude-style long-task control system, not an official Claude Code fixed standard and not a generic checklist.

## Layers

1. Control Plane / Orchestrator
2. Short Entry / Memory
3. Skills / Progressive Disclosure
4. Planning / Work Decomposition
5. Subagents / Context Isolation
6. Execution Plane
7. Hooks / Lifecycle Triggers
8. Scripts / Deterministic Checks
9. Verification Plane
10. Repair Loop
11. Compact / Handoff
12. Final Acceptance

## Governance Rules

- Control Plane sets goal, boundary, stop conditions, and acceptance authority.
- Skills are loaded progressively, not all at once.
- Execution Plane produces claims and evidence.
- Verification Plane accepts or rejects claims.
- Repair Loop handles rejected claims.
- Compact / Handoff makes the task restartable.
- Final Acceptance requires `final-acceptance.md` and `final-acceptance.json`.
