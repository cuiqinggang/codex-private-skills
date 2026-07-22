#!/usr/bin/env python3
"""覆盖严格模式的开放式优化和旧固定比例拒绝路径。"""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "compliant-evidence"
VALIDATOR_PATH = ROOT / "scripts" / "validate_run_evidence.py"
spec = importlib.util.spec_from_file_location("ecc_strict_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


def read_json(root: Path, name: str) -> dict:
    return json.loads((root / name).read_text(encoding="utf-8"))


def write_json(root: Path, name: str, value: dict) -> None:
    (root / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def make_valid_optimization(root: Path) -> None:
    config = read_json(root, "run-config.json")
    final = read_json(root, "final-acceptance.json")
    config["task_type"] = "optimization"
    config["optimization_stop_contract"] = {
        "baseline_metric":"严格证据结构错误数量",
        "target_metric":"结构错误为零且完成优化目标",
        "initial_candidates":["合并可复用证据"],
        "no_gain_round_limit":2,
        "cost_or_risk_limit":"不得降低独立审计关口",
        "max_window_minutes":120,
        "independent_stop_auditor_id":"agent-audit"
    }
    final["optimization_experiments"] = [
        {"candidate":"合并可复用证据","metric_before":"严格文件分散","metric_after":"结构完整且复用提高","result_chinese":"候选达到目标。","matched_candidate":"合并可复用证据","evidence_ids":["E-CHECK-SUCCESS"]}
    ]
    final["optimization_stop_decision"] = {
        "auditor_agent_id":"agent-audit",
        "accepted":True,
        "matched_stop_condition":"达到目标且候选方向完成",
        "experiment_evidence_ids":["E-CHECK-SUCCESS"]
    }
    write_json(root, "run-config.json", config)
    write_json(root, "final-acceptance.json", final)


def invalid_optimization_evidence(root: Path) -> None:
    make_valid_optimization(root)
    final = read_json(root, "final-acceptance.json")
    final["optimization_experiments"][0]["evidence_ids"] = ["E-NOT-EXIST"]
    final["optimization_stop_decision"]["experiment_evidence_ids"] = ["E-NOT-EXIST"]
    write_json(root, "final-acceptance.json", final)


def legacy_fixed_ratio(root: Path) -> None:
    config = read_json(root, "run-config.json")
    config["early_completion_threshold_ratio"] = 0.25
    write_json(root, "run-config.json", config)


def run_case(name: str, mutate: Callable[[Path], None], should_pass: bool) -> tuple[str, bool, list[str]]:
    with tempfile.TemporaryDirectory(prefix="ecc-strict-time-") as temp:
        root = Path(temp) / "evidence"
        shutil.copytree(EXAMPLE, root)
        mutate(root)
        outcome = validator.validate(root)
    actual = bool(outcome.get("pass"))
    return name, actual == should_pass, list(outcome.get("错误") or [])


def main() -> int:
    cases = (
        ("严格开放式优化正例", make_valid_optimization, True),
        ("严格优化引用不存在的实验依据", invalid_optimization_evidence, False),
        ("严格模式拒绝旧固定比例字段", legacy_fixed_ratio, False),
    )
    failures = []
    for name, mutate, should_pass in cases:
        case_name, correct, errors = run_case(name, mutate, should_pass)
        if not correct:
            failures.append({"case":case_name, "errors":errors})
    result = {"status":"PASS" if not failures else "FAIL", "status_chinese":"严格时间模式全部符合预期" if not failures else "严格时间模式存在错误放行", "total_cases":len(cases), "failed_cases":failures}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
