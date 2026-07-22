# ECC 2.0 Cross-Harness 12 Layer Patch

Status: PATCH_INSTALL_PASS
Date: 2026-07-06
Source: affaan-m/ECC v2.0.0 public repository

## Scope

This patch absorbs ECC v2.0.0 control-plane ideas into the local
`ecc-staged-long-task-orchestration` package.

It does not install ECC, copy configs, change hooks, enable MCP servers, or
modify any global runtime settings.

## Source Ideas Absorbed

| ECC v2.0 idea | Local 12 Layer mapping |
| --- | --- |
| `ecc.session.v1` control-pane session adapters | Layer 1, 2, 5, 11 session and worker state evidence |
| `ecc.mcp.v1` MCP inventory | Layer 3 and 7 tool-surface selection, context-cost, secret redaction |
| Worktree lifecycle service | Layer 1, 4, 6, 8, 9 branch/worktree safety and conflict evidence |
| `orch-*` orchestrator family | Layer 1 and 4 operation classification and right-sized pipeline |

## New Layer Requirements

### Layer 1 - Control Plane / Orchestrator

For complex long tasks, Layer 1 must declare:

```text
operation_type:
size_tier:
active_harnesses:
session_snapshot_required:
mcp_inventory_required:
worktree_lifecycle_required:
human_gate_required:
```

`operation_type` values:

- `add-feature`
- `change-feature`
- `fix-defect`
- `refine-code`
- `build-mvp`

### Layer 3 - Skills / Progressive Disclosure

Layer 3 must decide whether ECC is:

```text
REFERENCE_ONLY
ADAPT_LIGHTLY
ADOPT_DIRECTLY
```

Default for this local system is `REFERENCE_ONLY` unless the user explicitly
asks to install or test ECC itself.

Tool/MCP inventory must include:

```text
tool_name
source
stateful
auth_required
context_cost
secret_exposure_risk
enabled_for_this_stage
reason
```

### Layer 4 - Planning / Work Decomposition

Planning must use the operation type:

- `fix-defect`: reproduce as a failing test/check before fixing.
- `change-feature`: capture old behavior and desired behavior.
- `add-feature`: research/reuse before building.
- `refine-code`: keep behavior stable and tests green.
- `build-mvp`: build first thin vertical slice from the spec.

Size tier controls ceremony:

```text
trivial -> current stage only
small -> light plan + verify
standard -> research/reuse + plan + verify
large -> full 12 Layer + human gates
```

### Layer 5 - Subagents / Context Isolation

If multiple workers or harnesses are involved, each worker must have:

```text
worker_id
harness
role
state
health
branch
worktree
objective
allowed_tools
output_artifacts
validation_artifacts
remaining_risks
```

### Layer 7 - Hooks / Lifecycle Triggers

Codex does not have full Claude-style hook parity. For Codex, lifecycle checks
must be instruction-backed through task package rules, approval policy, and
verification scripts.

Required lifecycle checks:

```text
before_stage: confirm operation_type, active tools, dirty worktree
before_tool_use: confirm tool is enabled for this stage
before_parallel_work: confirm worktree lifecycle inventory
before_handoff: write session snapshot and remaining risks
before_final_pass: run verification and final acceptance
```

### Layer 8 - Scripts / Deterministic Checks

When applicable, deterministic checks must inspect:

```text
session_snapshot_present
mcp_inventory_present
worktree_lifecycle_present
operation_type_present
worker_records_present
dirty_or_conflict_worktree_not_removed
secret_values_absent
```

### Layer 9 - Verification Plane

Verification Plane must reject:

- session/worker state claims with no artifact;
- MCP inventory that exposes secrets;
- worktree cleanup plans that remove dirty, conflicted, merge-ready, or stale
  unmerged work;
- `orch-*` style tasks that skip their first move.

### Layer 11 - Compact / Handoff

Handoff must include:

```text
session_snapshot_summary:
tool_inventory_summary:
worktree_lifecycle_summary:
operation_type:
size_tier:
next_worker_or_harness:
next_resume_path:
remaining_risks:
```

### Layer 12 - Final Acceptance

Final Acceptance must state whether ECC 2.0 absorption was:

```text
REFERENCE_ONLY_PASS
ADAPT_LIGHTLY_PASS
PARTIAL
BLOCKED
```

For this patch, the valid status is:

```text
PATCH_INSTALL_PASS
REFERENCE_ONLY_PASS
```

## Anti-Install Guard

This patch is a rule absorption. It must not be used as approval to:

- install ECC;
- run `install.sh`, `install.ps1`, `npx ecc-install`, or plugin install;
- copy `.claude`, `.cursor`, `.codex`, `.opencode`, hooks, or MCP config;
- modify global Claude Code/Codex/Cursor settings.

Any of those requires a separate explicit user request and a fresh permission
gate.

## Trigger Keywords

ECC 2.0, control-pane, session adapter, MCP inventory, worktree lifecycle,
orch-pipeline, orch-build-mvp, orch-fix-defect, cross-harness, agent harness,
Codex Claude Code Cursor.
