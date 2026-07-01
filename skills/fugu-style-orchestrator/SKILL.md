---
name: fugu-style-orchestrator
description: Fugu-style multi-agent orchestration skill for reproducing Sakana Fugu-like task routing, expert model selection, verifier loops, synthesis, benchmark evaluation, and low-cost model-matrix design. Use when Codex needs to design or run a multi-model answer system, compare Fugu/Fable/Mythos/Kimi/DeepSeek/GLM/Qwen-style agent workflows, build a low-cost extreme-answer skill pack, create benchmark tests for agentic coding/research tasks, or decide which model should plan, execute, verify, repair, and synthesize a complex task.
---

# Fugu 式多智能体调度

## Overview

Use this skill to turn a hard task into a learned-orchestration style workflow: route the request, select specialized model roles, run execution and verification loops, synthesize a single answer, and score the result with reproducible benchmarks.

This skill does not require Sakana Fugu access. It extracts the reusable method behind Fugu: dynamic task classification, expert delegation, verification, repair, and final synthesis.

## Quick Decision

Classify the user task first:

| Task type | Route |
|---|---|
| Simple rewrite, translation, short answer | Use one cheap model; skip orchestration. |
| Code edit, bug hunt, research, local automation | Use Planner -> Executor -> Verifier -> Repair loop. |
| High-risk or expensive decision | Add independent Judge and evidence requirements. |
| Long-running Codex/Kilo task | Add checkpoints, budget caps, heartbeat, and final ZIP delivery. |
| Benchmark or model comparison | Use the benchmark pack generator and scoring rubric. |

## Core Workflow

1. **Intake**: Restate objective, constraints, deliverable, time/budget, allowed tools, and evidence required.
2. **Task route**: Classify domain, difficulty, risk, required modalities, and whether external sources or local files are needed.
3. **Model-role assignment**: Pick roles, not just models: planner, executor, specialist, verifier, repairer, synthesizer.
4. **Execution scaffold**: Define the sequence, parallelizable branches, checkpoints, context passed to each role, and stop conditions.
5. **Evidence capture**: Require citations, logs, tests, screenshots, diffs, generated files, or benchmark scores as appropriate.
6. **Verifier loop**: Independently check factuality, instruction compliance, safety, completeness, and cost.
7. **Repair loop**: If verifier fails, send only the failing evidence and requirements to the repair role.
8. **Synthesis**: Merge outputs into one clear final result, with confidence level and residual risks.
9. **Delivery**: For Codex-style tasks, package outputs as a unique three-digit ZIP when requested.

## Role Defaults

Use local policy and available models first. For the user's current SuperTool direction, default to:

| Role | Preferred model family | Purpose |
|---|---|---|
| Planner / Controller | GLM-5.2 or strongest instruction follower | Decompose, enforce constraints, choose route. |
| Main Executor | DeepSeek V4 Pro or Kimi K2.7 Code | Code, implement, analyze large files. |
| Cheap Worker | DeepSeek V4 Flash or Kimi cheaper tier | Batch extraction, first-pass drafts, simple subtasks. |
| Vision Specialist | Qwen3-VL-235B | Screenshot, image, UI, chart, video-frame reading. |
| Verifier / Gate | GLM-5.2 plus one independent model when high risk | Catch mistakes and missing evidence. |
| Premium External Orchestrator | Fugu Ultra only for hard, bounded tasks | Expensive final review or stress test, not daily default. |

## Fugu-Style Patterns

Use these patterns when designing a workflow:

- **Single-worker routing**: choose one best model for ordinary tasks to preserve speed and cost.
- **Deep orchestration**: run multiple expert agents only when quality matters more than latency.
- **Critic before synthesis**: never merge outputs before an independent failure check.
- **Evidence-bound claims**: mark benchmark claims as official, third-party, or independently rerun.
- **Budget fuse**: set token/time caps before starting a long agent loop.
- **No silent model mystery**: when not using Fugu itself, record which model performed each role.

## References

Read only the needed reference:

- `references/fugu-method.md`: Fugu architecture, work steps, advantages, limits, and source notes.
- `references/reproduction-playbook.md`: How to reproduce the method with Kimi/DeepSeek/GLM/Qwen/Fugu.
- `references/benchmark-and-validation.md`: Test suite, scoring rubrics, gate review, and acceptance thresholds.
- `references/model-matrix-and-cost.md`: Model roles, cost comparison, route choices, and when to pay for Fugu Ultra.
- `references/source-dossier.md`: Verified source list and benchmark claim status.

## Scripts

Use `scripts/generate_eval_pack.py` to create a reproducible benchmark template:

```bash
python scripts/generate_eval_pack.py --output ./fugu_eval_pack --profile codex-supertool
```

The script writes task templates, scorecards, cost fields, and a run plan. Use it before running a real model comparison.

## Acceptance Rules

Accept a Fugu-style workflow only when:

- The route explains why orchestration is needed.
- The model roles are explicit.
- The verifier has different incentives or a separate pass from the executor.
- Evidence is attached for factual, benchmark, code, or file claims.
- Cost and latency are estimated before premium models are used.
- The final answer states what is proven, what is vendor-reported, and what still needs independent reproduction.
