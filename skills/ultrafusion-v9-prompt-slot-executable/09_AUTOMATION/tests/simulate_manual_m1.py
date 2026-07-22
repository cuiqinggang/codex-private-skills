from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from common import EVIDENCE, sha256, write_json, write_text  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    out = EVIDENCE / "round2-manual-m1-simulation"
    out.mkdir(parents=True, exist_ok=True)
    question = "如何为一个每周三小时的个人阅读计划设置可执行检查点？"
    baseline = out / "A_Initial.txt"
    write_text(baseline, "先确定一本书和三次一小时阅读时段，每次记录页数与一个行动点。\n")
    baseline_hash = sha256(baseline)
    write_json(out / "A_INITIAL_SEAL.json", {"state": "A_INITIAL_SEALED", "sha256": baseline_hash, "comparison_open": False})
    stages = []
    for stage, package in [("A", "CP_A"), ("B", "CP_B"), ("C", "CP_C"), ("D", "CP_D")]:
        stages.append({"stage": stage, "command_package": package, "status": "FLOW_SIMULATION_ONLY", "real_model_call": False})
    write_json(out / "STAGE_TRACE.json", {"question": question, "stages": stages})
    final = out / "D_Final.txt"
    write_text(final, "模拟终稿：固定三次阅读时段；每次记录页数、摘要与行动；周末检查完成率并调整。此文本仅验证状态流。\n")
    final_hash = sha256(final)
    write_json(out / "D_FINAL_LOCK.json", {"state": "D_FINAL_LOCKED", "sha256": final_hash})
    write_json(out / "A_INITIAL_COMPARISON_COPY.json", {"state": "A_INITIAL_COMPARISON_COPY_OPENED", "source_sha256": baseline_hash, "opened_after_d_final_lock": True})
    write_text(out / "VALUE_REPORT.md", "# 模拟价值报告\n\n状态：FLOW_SIMULATION_ONLY\n\n未调用真实模型，不宣称质量提升。\n")
    states = ["RUN_CREATED", "QUESTION_REGISTERED", "A_INITIAL_GENERATED", "A_INITIAL_SEALED", "A_STAGE_READY", "A_STAGE_COMPLETE", "B_STAGE_READY", "B_STAGE_COMPLETE", "C_STAGE_READY", "C_STAGE_COMPLETE", "D_STAGE_READY", "D_FINAL_LOCKED", "A_INITIAL_COMPARISON_COPY_OPENED", "VALUE_COMPARISON_COMPLETE", "RUN_ACCEPTED"]
    write_json(out / "STATE_TRACE.json", {"states": states, "status": "FLOW_SIMULATION_ONLY"})
    write_text(EVIDENCE / "ROUND2_MANUAL_M1_FLOW_REPORT.md", "# ROUND2 MANUAL-M1 FLOW REPORT\n\n- Status: `PASS`\n- Mode: `FLOW_SIMULATION_ONLY`\n- A_Initial sealed before A: yes\n- D_Final locked before comparison copy opened: yes\n- Real model quality improvement proven: no\n")
    print("UF9_MANUAL_M1_PASS")
    print("FLOW_SIMULATION_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

