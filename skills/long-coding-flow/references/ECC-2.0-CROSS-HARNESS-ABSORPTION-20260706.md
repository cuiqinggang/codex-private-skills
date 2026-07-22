# ECC 2.0 Cross-Harness Absorption For Long Coding Flow

Status: READ_ONLY_ABSORBED
Date: 2026-07-06
Source: affaan-m/ECC v2.0.0 public repository

## Purpose

This note absorbs useful ECC v2.0.0 ideas into `long-coding-flow` without
installing ECC, copying hook configs, changing MCP settings, or replacing the
existing local workflow.

ECC v2.0.0 adds four ideas that strengthen long coding work:

1. Control-pane session snapshots.
2. MCP inventory and tool-surface normalization.
3. Worktree lifecycle classification.
4. `orch-*` operation routing.

## Local Adoption Boundary

Adopt as rules and checklist items only.

Do not:

- install ECC automatically;
- copy `.claude`, `.cursor`, `.codex`, `.opencode`, hooks, or MCP config;
- change Claude Code, Codex, Cursor, Kilo, Hermes, or Open WebUI globals;
- assume hook parity in Codex;
- stack ECC plugin and manual install methods.

## 1. Control-Pane Session Snapshot

ECC's `ecc.session.v1` idea becomes a local long-task session snapshot.

For long tasks, add this to `01-context.md` or `05-handoff.md` when more than
one harness, subagent, worktree, or long-running process is involved:

```text
session_snapshot:
  schema: local.long-coding.session.v1
  harnesses: Codex / Claude Code / Cursor / Kilo / Hermes / other
  repo_root:
  active_branch:
  worker_count:
  workers:
    - id:
      role:
      state: planned / running / blocked / completed / failed
      health: healthy / stale / degraded / unknown
      worktree:
      branch:
      command_or_runtime:
      objective:
      output_artifacts:
      validation_artifacts:
      remaining_risks:
```

Gate impact:

- G02 Environment must know active harnesses, branches, worktrees, and workers.
- G09 Handoff must record worker state and remaining risk, not only prose.
- A stale or unknown worker state blocks final PASS until explained.

## 2. MCP Inventory And Tool-Surface Normalization

ECC's `ecc.mcp.v1` idea becomes a local MCP/tool inventory rule.

Before a long task uses multiple MCPs, browser tools, GitHub tools, search
tools, or local automations, record:

```text
tool_inventory:
  harness:
  tool_or_mcp_name:
  source: built-in / plugin / local skill / CLI / REST API
  stateful: true / false
  auth_required: true / false
  context_cost: low / medium / high
  secret_exposure_risk: none / env-name-only / sensitive
  enabled_for_this_stage: true / false
  reason:
```

Default policy:

- Prefer CLI or skill wrapper for stateless one-shot work.
- Use MCP only when stateful interaction, browser/session state, streaming,
  auth handshake, or structured interactive browsing is truly needed.
- Keep unused MCP/tool surfaces disabled or out of the current stage context.
- Never print secret values; at most record environment variable names.

## 3. Worktree Lifecycle Classification

ECC's worktree lifecycle idea becomes a local parallel-work safety rule.

Before using parallel branches, worktrees, subagents, or multi-agent coding:

```text
worktree_lifecycle:
  base_branch:
  worktrees:
    - path:
      branch:
      state: main / detached / dirty / conflict / merge-ready / merged / stale / idle
      dirty: true / false
      ahead:
      behind:
      conflict_files:
      action: keep / merge / salvage / remove-after-approval
```

Safety rule:

- `dirty`, `conflict`, `merge-ready`, and `stale with unmerged commits` are not
  cleanup targets.
- `stale` means salvage candidate, not delete candidate.
- Only fully merged, clean worktrees can be proposed for removal, and destructive
  removal still needs explicit user approval.

## 4. `orch-*` Operation Routing

ECC's `orch-*` family becomes a local operation classifier for long tasks.

Before planning, classify the request:

```text
operation_type:
  add-feature: capability does not exist yet
  change-feature: behavior exists but desired behavior differs
  fix-defect: behavior is broken
  refine-code: behavior stays, structure improves
  build-mvp: spec or design doc becomes first vertical slice
```

First move by type:

- `fix-defect`: reproduce with a failing test or minimal failing check first.
- `change-feature`: find current behavior and update tests/checks with behavior.
- `add-feature`: research/reuse first, then thin vertical slice.
- `refine-code`: preserve behavior and keep tests green.
- `build-mvp`: read the spec and produce one end-to-end vertical slice first.

Size classification:

```text
trivial: one obvious small change
small: one file or one function
standard: 2-5 files or one real design choice
large: many files, public API, external dependency, or ambiguous spec
```

## Failure Modes Prevented

- Starting multi-agent work without knowing which workers exist.
- Letting hidden MCP/tool sprawl consume context or leak secrets.
- Deleting or overwriting parallel worktree changes.
- Treating a bug fix like a feature rewrite.
- Treating a refactor like behavior change.
- Assuming Codex has Claude-style hook parity.

## Trigger Keywords

ECC 2.0, control-pane, MCP inventory, worktree lifecycle, orch, orchestrator,
cross-harness, Claude Code Codex Cursor, long coding, parallel worktree,
multi-agent coding, agent harness.

## Next-Run Reuse Instruction

When a future long coding task mentions ECC, multi-harness work, MCPs, parallel
worktrees, multiple agents, or `orch-*`, read this file after `SKILL.md` and
before creating `02-plan.md`.
