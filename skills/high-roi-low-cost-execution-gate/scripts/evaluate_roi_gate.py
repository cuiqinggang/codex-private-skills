#!/usr/bin/env python3
"""Evaluate a proposed Codex package/project against the ROI gate."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


REQUIRED_TEXT = (
    "name_cn",
    "directory_name_en",
    "purpose",
    "save_location",
    "invocation",
    "real_problem",
    "existing_alternative",
    "evidence_level",
)


def ratio(benefit_per_month: float, investment: float, months: float) -> float | None:
    if investment > 0:
        return benefit_per_month * months / investment
    if benefit_per_month > 0:
        return math.inf
    return None


def payback(investment: float, benefit_per_month: float) -> float | None:
    if benefit_per_month > 0:
        return investment / benefit_per_month
    return None


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_TEXT if not str(data.get(key, "")).strip()]
    numeric_keys = (
        "problem_frequency_per_month",
        "loss_minutes_each",
        "investment_minutes",
        "investment_cost",
        "expected_saving_minutes_per_month",
        "expected_saving_cost_per_month",
        "success_rate_before",
        "success_rate_after",
        "expected_uses_per_month",
    )
    numbers: dict[str, float] = {}
    for key in numeric_keys:
        try:
            numbers[key] = float(data[key])
        except (KeyError, TypeError, ValueError):
            missing.append(key)

    if "duplicates_existing_capability" not in data:
        missing.append("duplicates_existing_capability")

    if missing:
        return {
            "decision": "BLOCKED_MISSING_DATA",
            "missing_fields": sorted(set(missing)),
            "reason": "必填字段缺失；不得先实施后补数字。",
        }

    months = float(data.get("evaluation_months", 3))
    if months <= 0 or any(value < 0 for value in numbers.values()):
        return {"decision": "BLOCKED_MISSING_DATA", "reason": "月份和数值不得为负。"}
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(data["directory_name_en"])):
        return {
            "decision": "BLOCKED_MISSING_DATA",
            "reason": "英文目录名必须使用小写字母、数字和连字符。",
        }
    if not all(0 <= numbers[key] <= 100 for key in ("success_rate_before", "success_rate_after")):
        return {"decision": "BLOCKED_MISSING_DATA", "reason": "成功率必须在 0–100 之间。"}

    time_ratio = ratio(
        numbers["expected_saving_minutes_per_month"],
        numbers["investment_minutes"],
        months,
    )
    cost_ratio = ratio(
        numbers["expected_saving_cost_per_month"],
        numbers["investment_cost"],
        months,
    )
    time_payback = payback(
        numbers["investment_minutes"], numbers["expected_saving_minutes_per_month"]
    )
    cost_payback = payback(
        numbers["investment_cost"], numbers["expected_saving_cost_per_month"]
    )
    finite_ratios = [v for v in (time_ratio, cost_ratio) if v is not None]
    best_ratio = max(finite_ratios, default=0.0)
    success_delta = numbers["success_rate_after"] - numbers["success_rate_before"]
    evidence = str(data.get("evidence_level", "UNKNOWN")).upper()
    duplicate = bool(data.get("duplicates_existing_capability", False))
    improvements = (
        numbers["expected_saving_minutes_per_month"] > 0
        or numbers["expected_saving_cost_per_month"] > 0
        or success_delta > 0
    )
    paybacks = [v for v in (time_payback, cost_payback) if v is not None]
    best_payback = min(paybacks, default=None)

    if duplicate:
        decision, reason = "DO_NOT_BUILD", "与现有成熟能力重复；优先复用或增量修改。"
    elif numbers["expected_uses_per_month"] < 1:
        decision, reason = "DO_NOT_BUILD", "预计月使用少于 1 次。"
    elif not improvements or success_delta < 0:
        decision, reason = "DO_NOT_BUILD", "没有净改善，或成功率预计下降。"
    elif best_ratio < 1:
        decision, reason = "DO_NOT_BUILD", "评估期内收益低于投入。"
    elif (
        evidence == "PROVEN"
        and best_ratio >= 2
        and best_payback is not None
        and best_payback <= 3
    ):
        decision, reason = "EXECUTE", "证据可验证，收益明显高于成本。"
    else:
        decision, reason = "PILOT_ONLY", "有潜力但证据或收益倍数不足，只允许最小规模测试。"

    def printable(value: float | None) -> float | str | None:
        if value is None:
            return None
        if math.isinf(value):
            return "Infinity"
        return round(value, 3)

    return {
        "decision": decision,
        "reason": reason,
        "evaluation_months": months,
        "time_benefit_ratio": printable(time_ratio),
        "cost_benefit_ratio": printable(cost_ratio),
        "time_payback_months": printable(time_payback),
        "cost_payback_months": printable(cost_payback),
        "success_rate_change_pp": round(success_delta, 3),
        "expected_uses_per_month": numbers["expected_uses_per_month"],
        "evidence_level": evidence,
        "duplicates_existing_capability": duplicate,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON input")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    print(json.dumps(evaluate(data), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
