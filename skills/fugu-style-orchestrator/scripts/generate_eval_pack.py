#!/usr/bin/env python3
"""Generate a reproducible Fugu-style orchestration evaluation pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TASKS = [
    {
        "id": "S01",
        "category": "smoke",
        "title": "complex_task_routing",
        "prompt": "Given a complex Codex task, produce route JSON with roles, model choices, evidence requirements, budget, and stop conditions.",
        "evidence_required": ["route_json"],
    },
    {
        "id": "S02",
        "category": "smoke",
        "title": "bug_review",
        "prompt": "Review a short buggy code sample and identify root causes, fixes, and tests.",
        "evidence_required": ["findings", "tests"],
    },
    {
        "id": "S03",
        "category": "smoke",
        "title": "source_backed_comparison",
        "prompt": "Compare two model systems using cited sources and separate official claims from independent evidence.",
        "evidence_required": ["citations", "claim_status_table"],
    },
    {
        "id": "C01",
        "category": "codex",
        "title": "rollback_command_pack",
        "prompt": "Create a reversible command package for a local tool configuration change.",
        "evidence_required": ["files", "rollback_steps", "validation_log"],
    },
    {
        "id": "C02",
        "category": "codex",
        "title": "long_task_checkpoint_plan",
        "prompt": "Design a two-hour autonomous run with checkpoints, heartbeat, failure gates, and final ZIP delivery.",
        "evidence_required": ["run_plan", "checkpoint_schema", "final_gate"],
    },
    {
        "id": "H01",
        "category": "hard",
        "title": "agentic_code_repair",
        "prompt": "Repair a failing repository issue using planner, executor, verifier, and repair roles.",
        "evidence_required": ["diff", "test_output", "verifier_report"],
    },
]


SCORECARD = """# Fugu-Style Evaluation Scorecard

## Scoring

| Dimension | Points | Score | Notes |
|---|---:|---:|---|
| Correctness | 30 |  |  |
| Completeness | 20 |  |  |
| Evidence | 15 |  |  |
| Execution quality | 15 |  |  |
| Verification and repair | 10 |  |  |
| Cost efficiency | 10 |  |  |
| Total | 100 |  |  |

## Verdict

PASS: 90-100
ACCEPTED_WITH_LIMITS: 75-89
PARTIAL: 60-74
FAIL: below 60

## Required Metadata

- Task id:
- Route:
- Models used:
- Estimated input tokens:
- Estimated output tokens:
- Estimated cost:
- Runtime:
- Evidence paths:
- Verifier:
- Required repairs:
"""


RUN_PLAN = """# Fugu-Style Evaluation Run Plan

1. Run each task in three modes: baseline single model, local orchestrated model matrix, premium optional judge.
2. Record role assignments before execution.
3. Keep raw outputs in `raw_outputs/`.
4. Keep evidence in `evidence/`.
5. Score with `scorecard.md`.
6. Mark each claim as official, third-party, independently rerun, or unverified.
7. Stop premium testing when budget is exhausted or local verification already passes.

## Directory Layout

```text
eval_pack/
  tasks.jsonl
  scorecard.md
  run_plan.md
  raw_outputs/
  evidence/
  reports/
```
"""


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output directory for the evaluation pack.")
    parser.add_argument("--profile", default="generic", help="Profile label, e.g. codex-supertool.")
    args = parser.parse_args()

    out = Path(args.output).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in ["raw_outputs", "evidence", "reports"]:
        (out / name).mkdir(exist_ok=True)

    tasks = []
    for task in TASKS:
        item = dict(task)
        item["profile"] = args.profile
        item["route_modes"] = ["baseline_single", "local_orchestrated", "premium_optional"]
        item["score_dimensions"] = {
            "correctness": 30,
            "completeness": 20,
            "evidence": 15,
            "execution_quality": 15,
            "verification_repair": 10,
            "cost_efficiency": 10,
        }
        tasks.append(item)

    write_jsonl(out / "tasks.jsonl", tasks)
    (out / "scorecard.md").write_text(SCORECARD, encoding="utf-8")
    (out / "run_plan.md").write_text(RUN_PLAN, encoding="utf-8")
    (out / "manifest.json").write_text(
        json.dumps(
            {
                "name": "fugu_style_eval_pack",
                "profile": args.profile,
                "task_count": len(tasks),
                "verdicts": ["PASS", "ACCEPTED_WITH_LIMITS", "PARTIAL", "FAIL", "BLOCKED"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Created evaluation pack at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
