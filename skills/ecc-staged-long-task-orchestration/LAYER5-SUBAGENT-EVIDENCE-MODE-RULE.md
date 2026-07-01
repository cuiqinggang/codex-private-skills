# Layer 5 Subagent Evidence Mode Rule

## Purpose

Layer 5 evidence must state whether it is real subagent execution or logical
context isolation. Future runs must not blur this distinction.

## Mode A: Real Subagent Execution

Use when actual independent agents or processes are invoked.

```text
REAL_SUBAGENT_EXECUTION_REQUIRED = true
LOGICAL_CONTEXT_ISOLATION_ONLY_NOT_ACCEPTED = true
```

If real subagents are unavailable, the run must BLOCK rather than silently
downgrade.

## Mode B: Logical Context Isolation

Use when a single Codex execution simulates separate review contexts through
separate input/output evidence files.

```text
SUBAGENT_MODE = LOGICAL_CONTEXT_ISOLATION_ALLOWED
REAL_SUBAGENT_EXECUTION_REQUIRED = false
```

Required evidence:

1. independent input file for each role;
2. independent output file for each role;
3. `files_read`;
4. `files_written`;
5. `independent_conclusion`;
6. orchestrator receipt;
7. Verification Plane acceptance.

## Forbidden Claim

Do not describe logical context isolation as:

```text
REAL_SUBAGENT_EXECUTION
```

Use:

```text
LOGICAL_CONTEXT_ISOLATION_ONLY
```

## Status Codes

```text
LAYER5_LOGICAL_CONTEXT_ISOLATION_ACCEPTED
LAYER5_REAL_SUBAGENT_EXECUTION_REQUIRED
LAYER5_LOGICAL_CONTEXT_ISOLATION_NOT_ACCEPTED
ECC_LAYER5_CONTEXT_ISOLATION_MISSING_REJECTED
```
