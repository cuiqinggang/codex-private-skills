#!/usr/bin/env python3
"""
H3-P0-JEV-SHADOW-01

Known-answer offline/shadow replay against OpenRouter Decisions API.
This script never starts H3, never touches the frozen H3 runtime, and never
writes an API key to evidence.

Environment:
  OPENROUTER_API_KEY

Endpoint:
  POST https://openrouter.ai/api/alpha/decisions
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "typesafe/jev-1.13"
DEFAULT_THRESHOLDS = [round(x / 100, 2) for x in range(50, 100)]
PROVIDER_POLICY = {
    "zdr": True,
    "data_collection": "deny",
}
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET = SCRIPT_DIR / "H3-P0-JEV-SHADOW-DATASET-v1.json"
DEFAULT_RESULT = SCRIPT_DIR / "H3-P0-JEV-SHADOW-RESULT-v1.json"
DEFAULT_SUMMARY = SCRIPT_DIR / "H3-P0-JEV-SHADOW-RESULT-v1.md"


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    k = (len(xs) - 1) * p
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def post_decisions(api_key: str, payload: dict[str, Any], timeout: float, retries: int) -> tuple[dict[str, Any], float, int]:
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "User-Agent": "h3-p0-jev-shadow/1.0",
        },
        method="POST",
    )
    started = time.perf_counter()
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
            elapsed_ms = (time.perf_counter() - started) * 1000.0
            return json.loads(raw), elapsed_ms, attempt
        except urllib.error.HTTPError as exc:
            retryable = exc.code in (408, 409, 425, 429, 500, 502, 503, 504, 524, 529)
            if retryable and attempt <= retries:
                time.sleep(min(2.0, 0.25 * (2 ** (attempt - 1))))
                continue
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail[:1000]}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt <= retries:
                time.sleep(min(2.0, 0.25 * (2 ** (attempt - 1))))
                continue
            raise RuntimeError(f"OpenRouter transport error: {exc}") from exc


def normalize_question(question: dict[str, Any]) -> dict[str, Any]:
    q = dict(question)
    if q.get("type") == "noul" and "criteria" not in q:
        q["criteria"] = {
            "false": "No: the proposition asked by instructions is not supported by the supplied state.",
            "true": "Yes: the proposition asked by instructions is supported by the supplied state.",
        }
    return q


def build_batch(cases: list[dict[str, Any]], mode: str) -> list[tuple[str, dict[str, Any], list[dict[str, Any]]]]:
    if mode == "case":
        return [
            (
                case["id"],
                {
                    "state": case["state"],
                    "questions": {case["id"]: normalize_question(case["question"])},
                },
                [case],
            )
            for case in cases
        ]

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if mode == "family":
        for case in cases:
            groups[case["family"]].append(case)
    elif mode == "mega":
        groups["all"] = cases
    else:
        raise ValueError(f"Unknown batch mode: {mode}")

    batches: list[tuple[str, dict[str, Any], list[dict[str, Any]]]] = []
    for name, members in groups.items():
        state = {"cases": {case["id"]: case["state"] for case in members}}
        questions: dict[str, Any] = {}
        for case in members:
            q = normalize_question(case["question"])
            q["instructions"] = (
                f"Evaluate only state.cases.{case['id']}. "
                + q["instructions"]
            )
            questions[case["id"]] = q
        batches.append((name, {"state": state, "questions": questions}, members))
    return batches


def extract_answer(response: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    answers = response.get("answers")
    if not isinstance(answers, dict) or case["id"] not in answers:
        return {
            "valid": False,
            "reason": "missing_answer",
            "predicted": None,
            "confidence": 0.0,
            "gold_probability": 0.0,
        }

    answer = answers[case["id"]]
    if not isinstance(answer, dict):
        return {
            "valid": False,
            "reason": "answer_not_object",
            "predicted": None,
            "confidence": 0.0,
            "gold_probability": 0.0,
        }

    qtype = case["question"]["type"]
    gold = case["gold"]

    if qtype == "noul":
        p = answer.get("noul")
        if not isinstance(p, (int, float)) or not (0.0 <= float(p) <= 1.0):
            return {
                "valid": False,
                "reason": "invalid_noul_probability",
                "predicted": None,
                "confidence": 0.0,
                "gold_probability": 0.0,
                "raw_answer": answer,
            }
        p = float(p)
        predicted = p >= 0.5
        confidence = max(p, 1.0 - p)
        gold_probability = p if bool(gold["noul"]) else 1.0 - p
        return {
            "valid": True,
            "predicted": predicted,
            "gold": bool(gold["noul"]),
            "correct": predicted == bool(gold["noul"]),
            "confidence": confidence,
            "gold_probability": gold_probability,
            "raw_answer": answer,
        }

    if qtype == "choice":
        predicted = answer.get("choice")
        probabilities = answer.get("probabilities")
        criteria = case["question"].get("criteria", {})
        if predicted not in criteria:
            return {
                "valid": False,
                "reason": "illegal_choice",
                "predicted": predicted,
                "confidence": 0.0,
                "gold_probability": 0.0,
                "raw_answer": answer,
            }
        confidence = answer.get("confidence")
        if not isinstance(confidence, (int, float)):
            if isinstance(probabilities, dict) and probabilities:
                numeric = [float(v) for v in probabilities.values() if isinstance(v, (int, float))]
                confidence = max(numeric) if numeric else 0.0
            else:
                confidence = 0.0
        gold_choice = gold["choice"]
        gold_probability = 0.0
        if isinstance(probabilities, dict) and isinstance(probabilities.get(gold_choice), (int, float)):
            gold_probability = float(probabilities[gold_choice])
        elif predicted == gold_choice:
            gold_probability = float(confidence)
        return {
            "valid": True,
            "predicted": predicted,
            "gold": gold_choice,
            "correct": predicted == gold_choice,
            "confidence": float(confidence),
            "gold_probability": gold_probability,
            "raw_answer": answer,
        }

    return {
        "valid": False,
        "reason": "unsupported_question_type",
        "predicted": None,
        "confidence": 0.0,
        "gold_probability": 0.0,
    }


def normalize_usage(response: dict[str, Any]) -> dict[str, Any]:
    usage = response.get("usage")
    if not isinstance(usage, dict):
        return {}
    keep = {}
    for key in (
        "prompt_tokens",
        "input_tokens",
        "completion_tokens",
        "output_tokens",
        "total_tokens",
        "cost",
        "total_cost",
    ):
        if key in usage:
            keep[key] = usage[key]
    return keep


def numeric_cost(usage: dict[str, Any]) -> float:
    for key in ("cost", "total_cost"):
        value = usage.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return 0.0


def run_once(api_key: str, model: str, cases: list[dict[str, Any]], mode: str, timeout: float, retries: int) -> dict[str, Any]:
    batches = build_batch(cases, mode)
    observations = []
    request_records = []
    run_started = time.perf_counter()

    for batch_name, request_core, members in batches:
        payload = {
            "model": model,
            "state": request_core["state"],
            "questions": request_core["questions"],
            "provider": PROVIDER_POLICY,
        }
        response, elapsed_ms, attempts = post_decisions(api_key, payload, timeout, retries)
        usage = normalize_usage(response)
        request_records.append(
            {
                "batch": batch_name,
                "case_count": len(members),
                "elapsed_ms": elapsed_ms,
                "attempts": attempts,
                "usage": usage,
                "response_id": response.get("id"),
                "provider": response.get("provider"),
                "model": response.get("model"),
            }
        )
        for case in members:
            parsed = extract_answer(response, case)
            parsed.update(
                {
                    "id": case["id"],
                    "family": case["family"],
                    "critical": bool(case.get("critical")),
                    "domain": case.get("domain"),
                    "batch": batch_name,
                }
            )
            observations.append(parsed)

    total_ms = (time.perf_counter() - run_started) * 1000.0
    valid = [x for x in observations if x.get("valid")]
    correct = [x for x in valid if x.get("correct")]
    critical_errors = [x for x in valid if x.get("critical") and not x.get("correct")]
    invalid = [x for x in observations if not x.get("valid")]
    mean_gold_probability = statistics.fmean(x["gold_probability"] for x in valid) if valid else 0.0
    request_latencies = [x["elapsed_ms"] for x in request_records]
    total_cost = sum(numeric_cost(x["usage"]) for x in request_records)

    return {
        "mode": mode,
        "total_ms": total_ms,
        "case_count": len(cases),
        "request_count": len(request_records),
        "accuracy": (len(correct) / len(valid)) if valid else 0.0,
        "correct": len(correct),
        "valid": len(valid),
        "invalid_outputs": len(invalid),
        "critical_errors": len(critical_errors),
        "mean_gold_probability": mean_gold_probability,
        "cost_usd": total_cost,
        "request_latency_ms": {
            "p50": percentile(request_latencies, 0.50),
            "p95": percentile(request_latencies, 0.95),
            "max": max(request_latencies) if request_latencies else None,
        },
        "observations": observations,
        "requests": request_records,
    }


def threshold_sweep(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for threshold in DEFAULT_THRESHOLDS:
        accepted = []
        for run in runs:
            for item in run["observations"]:
                if item.get("valid") and float(item.get("confidence", 0.0)) >= threshold:
                    accepted.append(item)
        errors = [x for x in accepted if not x.get("correct")]
        critical_errors = [x for x in errors if x.get("critical")]
        total_valid = sum(run["valid"] for run in runs)
        rows.append(
            {
                "threshold": threshold,
                "accepted": len(accepted),
                "coverage": (len(accepted) / total_valid) if total_valid else 0.0,
                "accepted_accuracy": ((len(accepted) - len(errors)) / len(accepted)) if accepted else None,
                "accepted_errors": len(errors),
                "critical_autoaccepted_errors": len(critical_errors),
            }
        )
    return rows


def aggregate_mode(mode: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    totals = [x["total_ms"] for x in runs]
    costs = [x["cost_usd"] for x in runs]
    accuracies = [x["accuracy"] for x in runs]
    invalid = sum(x["invalid_outputs"] for x in runs)
    critical_errors = sum(x["critical_errors"] for x in runs)
    sweep = threshold_sweep(runs)
    qualifying = [
        row for row in sweep
        if row["accepted"] > 0
        and row["accepted_errors"] == 0
        and row["critical_autoaccepted_errors"] == 0
        and row["coverage"] >= 0.70
    ]
    best_gate = qualifying[0] if qualifying else None
    p50_ms = percentile(totals, 0.50)
    p95_ms = percentile(totals, 0.95)
    answers_per_second = (len(runs[0]["observations"]) / (p50_ms / 1000.0)) if p50_ms else None
    return {
        "mode": mode,
        "repeats": len(runs),
        "accuracy_mean": statistics.fmean(accuracies) if accuracies else 0.0,
        "accuracy_min": min(accuracies) if accuracies else 0.0,
        "critical_errors_total": critical_errors,
        "invalid_outputs_total": invalid,
        "run_total_ms": {
            "p50": p50_ms,
            "p95": p95_ms,
            "min": min(totals) if totals else None,
            "max": max(totals) if totals else None,
        },
        "cost_usd_per_run": {
            "mean": statistics.fmean(costs) if costs else 0.0,
            "max": max(costs) if costs else 0.0,
        },
        "answers_per_second_at_p50": answers_per_second,
        "best_zero_error_gate_min_70pct_coverage": best_gate,
        "threshold_sweep": sweep,
    }


def choose_result(aggregates: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = []
    for agg in aggregates:
        gate = agg.get("best_zero_error_gate_min_70pct_coverage")
        if (
            gate
            and agg["invalid_outputs_total"] == 0
            and agg["accuracy_min"] >= 0.95
            and agg["critical_errors_total"] == 0
        ):
            eligible.append(agg)

    if eligible:
        winner = min(eligible, key=lambda x: float(x["run_total_ms"]["p95"] or float("inf")))
        return {
            "role": "GATED_SHADOW_PASS",
            "best_mode": winner["mode"],
            "gate": winner["best_zero_error_gate_min_70pct_coverage"],
            "reason": "Zero critical errors, at least 95% exact accuracy on every replay, zero invalid outputs, and a zero-error confidence gate covering at least 70% of decisions.",
        }

    advisory = [
        agg for agg in aggregates
        if agg["invalid_outputs_total"] == 0 and agg["accuracy_mean"] >= 0.80
    ]
    if advisory:
        winner = max(advisory, key=lambda x: x["accuracy_mean"])
        return {
            "role": "ADVISORY_ONLY",
            "best_mode": winner["mode"],
            "gate": winner.get("best_zero_error_gate_min_70pct_coverage"),
            "reason": "Useful signal exists, but the automatic-gating release criteria were not met.",
        }

    return {
        "role": "REJECT_FOR_CONTROL",
        "best_mode": None,
        "gate": None,
        "reason": "Accuracy or output validity is insufficient even for advisory control use.",
    }


def write_summary(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# H3-P0 Jev Shadow Result v1",
        "",
        f"Status: {result['decision']['role']}",
        "",
        "## Contract",
        "",
        f"- Model: {result['model']}",
        f"- Endpoint: {result['endpoint']}",
        f"- Cases: {result['dataset_case_count']}",
        f"- H3 GPU reruns: {result['h3_gpu_runs']}",
        "- Provider privacy: ZDR required; data collection denied",
        "- Frozen H3-P0 mutated: NO",
        "",
        "## Batch modes",
        "",
        "| mode | accuracy mean | accuracy min | critical errors | invalid outputs | end-to-end P50 ms | P95 ms | mean cost/run USD | answers/s @ P50 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for agg in result["aggregates"]:
        lines.append(
            "| {mode} | {amean:.4f} | {amin:.4f} | {crit} | {invalid} | {p50:.2f} | {p95:.2f} | {cost:.8f} | {aps:.2f} |".format(
                mode=agg["mode"],
                amean=agg["accuracy_mean"],
                amin=agg["accuracy_min"],
                crit=agg["critical_errors_total"],
                invalid=agg["invalid_outputs_total"],
                p50=float(agg["run_total_ms"]["p50"] or 0.0),
                p95=float(agg["run_total_ms"]["p95"] or 0.0),
                cost=float(agg["cost_usd_per_run"]["mean"] or 0.0),
                aps=float(agg["answers_per_second_at_p50"] or 0.0),
            )
        )

    lines += [
        "",
        "## Decision",
        "",
        f"- Role: {result['decision']['role']}",
        f"- Best mode: {result['decision']['best_mode']}",
        f"- Reason: {result['decision']['reason']}",
    ]
    gate = result["decision"].get("gate")
    if gate:
        lines += [
            f"- Confidence threshold: {gate['threshold']}",
            f"- Auto coverage: {gate['coverage']:.4f}",
            f"- Accepted accuracy: {gate['accepted_accuracy']:.4f}",
            f"- Critical autoaccepted errors: {gate['critical_autoaccepted_errors']}",
        ]

    lines += [
        "",
        "## Interpretation",
        "",
        "- This is a known-answer shadow replay, not production certification.",
        "- It measures whether Jev can replace selected finite semantic decisions with typed probabilities.",
        "- It does not claim any reduction in H3 GPU generation time.",
        "- Deterministic QC, arithmetic, hashes, decoding, and final acceptance remain code-owned.",
        "- GPT/DeepSeek remain responsible for open-ended synthesis and new plan creation.",
        "",
        "## Baseline",
        "",
        "GPT control-plane latency baseline was not fabricated. A real end-to-end speedup ratio is only emitted when an independently measured baseline is supplied.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--modes", default="mega,family,case")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--out", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--baseline-gpt-ms", type=float, default=0.0)
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_KEY_MISSING: set OPENROUTER_API_KEY in the local process environment; do not commit or paste it into evidence.", file=sys.stderr)
        return 3

    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
    cases = dataset["cases"]
    modes = [x.strip() for x in args.modes.split(",") if x.strip()]
    all_runs: dict[str, list[dict[str, Any]]] = {}

    print(f"H3-P0-JEV-SHADOW-01 model={args.model} cases={len(cases)} repeats={args.repeats} modes={','.join(modes)}")
    print("H3_GPU_RUNS=0 PRIVACY=ZDR+DATA_COLLECTION_DENY")

    for mode in modes:
        mode_runs = []
        for repeat in range(1, args.repeats + 1):
            run = run_once(api_key, args.model, cases, mode, args.timeout, args.retries)
            run["repeat"] = repeat
            mode_runs.append(run)
            print(
                f"mode={mode} repeat={repeat}/{args.repeats} "
                f"accuracy={run['accuracy']:.4f} critical_errors={run['critical_errors']} "
                f"invalid={run['invalid_outputs']} total_ms={run['total_ms']:.2f} "
                f"cost_usd={run['cost_usd']:.8f}"
            )
        all_runs[mode] = mode_runs

    aggregates = [aggregate_mode(mode, runs) for mode, runs in all_runs.items()]
    decision = choose_result(aggregates)
    result = {
        "schema": "H3-P0-JEV-SHADOW-RESULT-v1",
        "timestamp_unix": time.time(),
        "model": args.model,
        "endpoint": ENDPOINT,
        "provider_policy": PROVIDER_POLICY,
        "dataset": str(args.dataset),
        "dataset_case_count": len(cases),
        "h3_gpu_runs": 0,
        "frozen_h3_mutated": False,
        "aggregates": aggregates,
        "decision": decision,
        "runs": all_runs,
    }

    if args.baseline_gpt_ms > 0 and decision.get("best_mode"):
        winning = next(x for x in aggregates if x["mode"] == decision["best_mode"])
        p50 = float(winning["run_total_ms"]["p50"] or 0.0)
        if p50 > 0:
            result["measured_control_plane_speedup_vs_supplied_gpt_baseline"] = args.baseline_gpt_ms / p50
            result["baseline_gpt_ms"] = args.baseline_gpt_ms

    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_summary(args.summary, result)

    print("ROLE=" + decision["role"])
    print("BEST_MODE=" + str(decision.get("best_mode")))
    if decision.get("gate"):
        print("BEST_THRESHOLD=" + str(decision["gate"]["threshold"]))
        print("AUTO_COVERAGE=" + f"{decision['gate']['coverage']:.4f}")
    print("RESULT_JSON=" + str(args.out))
    print("RESULT_MD=" + str(args.summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
