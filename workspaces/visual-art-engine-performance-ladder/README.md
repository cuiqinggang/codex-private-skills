# Visual Art Engine Performance Ladder — Shared Workspace

This directory is the shared evidence/report workspace for `visual-art-engine-performance-ladder`.

## Purpose

Use this workspace for cross-session handoff between ChatGPT and Codex during the rapid P0→P8 performance-optimization cycle.

- ChatGPT: reads the latest evidence, runs the `mature-replication-four-column` V4.0 review, decides the next step, and writes the next Codex command.
- Codex: performs local execution/measurement, preserves raw evidence, and pushes the resulting report bundle here.
- Do not treat a local-only path such as `C:\...` as sufficient handoff evidence.

## Required layout

```text
workspaces/visual-art-engine-performance-ladder/
  README.md
  LATEST.md
  stages/
    P0/
      <run-id>/
        REPORT.md
        timing-summary.json
        output-validation.json
        raw-websocket-events.jsonl
        benchmark-contract-snapshot.md
        environment-before.json
        environment-after.json
        ...other compact evidence needed to reproduce/review the run
    P1/
    ...
    P8/
```

## LATEST.md contract

After every completed stage run, Codex updates `LATEST.md` with:

- stage / run id
- working skill version
- method version
- final status
- Git commit containing the report bundle
- relative path to the report bundle
- four-column state (`CURRENT`, `EXTERNAL FRONTIER`, `FIRST-PRINCIPLES PHYSICAL TIME`, `ITERATIVE CONVERGENCE`)
- next requested action

## Rapid-iteration rule

During fast iteration, not every local skill patch needs to become a formal released skill version. However, every run that ChatGPT must review should publish its report/evidence bundle here so both sides operate from the same evidence.

Formal stable skill releases remain under:

`skills/visual-art-engine-performance-ladder`

and are synchronized at stable milestones / freeze points.

## Evidence policy

Push text/JSON/CSV/log evidence needed for review. Avoid unnecessary large media, model files, caches, generated binaries, or duplicate artifacts. For large outputs, keep hashes, metadata, and a precise external/local artifact reference unless the artifact itself is essential for review.

## Methodology

All stage reviews use the installed skill:

`mature-replication-four-column` — V4.0

with the fixed columns:

1. CURRENT
2. EXTERNAL FRONTIER
3. FIRST-PRINCIPLES PHYSICAL TIME
4. ITERATIVE CONVERGENCE

Do not create a parallel methodology in this workspace.
