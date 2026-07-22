#!/usr/bin/env python3
"""Validate evidence-backed online skill benchmarking records (schema 2.0).

The validator never downloads or executes candidate code. It rejects synthetic
scores, missing run evidence, weak license claims, empty search clusters, and
incomplete rollback records.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

DECISIONS = {"ABSORB", "COMPLEMENT", "REPLACE_COMPONENT", "KEEP_LOCAL", "REJECT", "DEFER"}
CANDIDATE_TYPES = {"EXECUTABLE", "SERVICE", "METHOD_OR_SPEC"}
MEASUREMENT_STATES = {"MEASURED", "NOT_AVAILABLE", "NOT_APPLICABLE", "NOT_MEASURED"}
CASES = ("normal", "boundary", "failure_recovery")
VARIANTS = ("local", "candidate", "enhanced")
METRICS = ("success", "safe", "quality", "steps", "human_interventions", "elapsed_seconds", "tokens")
RUN_FIELDS = ("run_id", "utc_start", "utc_end", "input_ref", "output_ref", "execution_method", "status")
SHA256_RE = re.compile(r"^[0-9A-Fa-f]{64}$")


def is_https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def is_utc(value: object) -> bool:
    return isinstance(value, str) and ("T" in value) and (value.endswith("Z") or "+" in value[10:])


def measured(metric: object) -> bool:
    return isinstance(metric, dict) and metric.get("measurement_state") == "MEASURED"


def metric_value(result: dict, metric: str) -> object | None:
    item = result.get("metrics", {}).get(metric, {})
    return item.get("value") if measured(item) else None


def validate_run(label: str, result: dict) -> list[str]:
    errors: list[str] = []
    metrics = result.get("metrics")
    if not isinstance(metrics, dict):
        return [f"{label}: missing metrics object"]
    any_measured = False
    for name in METRICS:
        item = metrics.get(name)
        if not isinstance(item, dict) or item.get("measurement_state") not in MEASUREMENT_STATES:
            errors.append(f"{label}/{name}: invalid or missing measurement_state")
            continue
        state = item["measurement_state"]
        if state == "MEASURED":
            any_measured = True
            if "value" not in item or item["value"] is None:
                errors.append(f"{label}/{name}: MEASURED requires value")
        elif "value" in item and item["value"] is not None:
            errors.append(f"{label}/{name}: {state} must not carry a value")
    evidence = result.get("run_evidence")
    if any_measured:
        if not isinstance(evidence, dict):
            errors.append(f"{label}: MEASURED metrics require run_evidence")
        else:
            for field in RUN_FIELDS:
                if not evidence.get(field):
                    errors.append(f"{label}: run_evidence missing {field}")
            if not is_utc(evidence.get("utc_start")) or not is_utc(evidence.get("utc_end")):
                errors.append(f"{label}: run UTC fields are invalid")
            if measured(metrics.get("quality")) and not evidence.get("evaluator_rubric_ref"):
                errors.append(f"{label}: measured quality requires evaluator_rubric_ref")
    elif evidence:
        errors.append(f"{label}: run_evidence present but no metric is MEASURED")
    return errors


def validate_license(label: str, license_info: object) -> list[str]:
    if not isinstance(license_info, dict):
        return [f"{label}: missing license object"]
    errors: list[str] = []
    status = license_info.get("status")
    if status not in {"VERIFIED", "NO_COPY", "UNKNOWN"}:
        errors.append(f"{label}: invalid license status")
    if status == "VERIFIED":
        evidence_url = license_info.get("evidence_url")
        proof = license_info.get("file_sha256_or_official_ref")
        if not is_https(evidence_url):
            errors.append(f"{label}: VERIFIED license needs direct HTTPS evidence_url")
        elif not any(token in evidence_url.lower() for token in ("license", "licence", "terms", "legal")):
            errors.append(f"{label}: repository homepage alone cannot verify a license")
        if not proof or (isinstance(proof, str) and proof.startswith("sha256:") and not SHA256_RE.fullmatch(proof[7:])):
            errors.append(f"{label}: VERIFIED license needs file SHA256 or official reference")
    return errors


def improvement(local: dict, enhanced: dict) -> bool:
    success_l, success_e = metric_value(local, "success"), metric_value(enhanced, "success")
    safe_l, safe_e = metric_value(local, "safe"), metric_value(enhanced, "safe")
    if safe_l is True and safe_e is not True:
        return False
    if success_l is False and success_e is True:
        return True
    quality_l, quality_e = metric_value(local, "quality"), metric_value(enhanced, "quality")
    if isinstance(quality_l, (int, float)) and isinstance(quality_e, (int, float)) and quality_e - quality_l >= 10:
        return True
    for name in ("elapsed_seconds", "tokens", "human_interventions", "steps"):
        left, right = metric_value(local, name), metric_value(enhanced, name)
        if isinstance(left, (int, float)) and left > 0 and isinstance(right, (int, float)):
            quality_ok = not (
                isinstance(quality_l, (int, float)) and isinstance(quality_e, (int, float))
                and quality_l - quality_e > 2
            )
            if quality_ok and (left - right) / left >= 0.15:
                return True
    return False


def validate_candidate(cluster_id: str, candidate: dict) -> list[str]:
    errors: list[str] = []
    label = f"{cluster_id}/{candidate.get('candidate_id', '<missing>')}"
    for field in ("candidate_id", "name", "candidate_type", "source_url", "license", "benchmark", "decision"):
        if field not in candidate:
            errors.append(f"{label}: missing field {field}")
    if errors:
        return errors
    candidate_type = candidate["candidate_type"]
    decision = candidate["decision"]
    if candidate_type not in CANDIDATE_TYPES:
        errors.append(f"{label}: invalid candidate_type")
    if decision not in DECISIONS:
        errors.append(f"{label}: invalid decision")
    if not is_https(candidate["source_url"]):
        errors.append(f"{label}: source_url must be HTTPS")
    errors.extend(validate_license(label, candidate["license"]))
    benchmark = candidate["benchmark"]
    any_improvement = False
    candidate_measured = False
    for case in CASES:
        row = benchmark.get(case) if isinstance(benchmark, dict) else None
        if not isinstance(row, dict):
            errors.append(f"{label}: missing benchmark case {case}")
            continue
        for variant in VARIANTS:
            result = row.get(variant)
            if not isinstance(result, dict):
                errors.append(f"{label}/{case}: missing {variant}")
                continue
            errors.extend(validate_run(f"{label}/{case}/{variant}", result))
            if variant == "candidate":
                candidate_measured |= any(measured(result.get("metrics", {}).get(m)) for m in METRICS)
        if isinstance(row.get("local"), dict) and isinstance(row.get("enhanced"), dict):
            any_improvement |= improvement(row["local"], row["enhanced"])
    if decision in {"ABSORB", "REPLACE_COMPONENT"}:
        if candidate["license"].get("status") == "UNKNOWN":
            errors.append(f"{label}: UNKNOWN license cannot enter absorption")
        if candidate_type == "METHOD_OR_SPEC":
            for case in CASES:
                row = benchmark.get(case, {})
                for variant in ("local", "enhanced"):
                    result = row.get(variant, {})
                    if not any(measured(result.get("metrics", {}).get(m)) for m in METRICS):
                        errors.append(f"{label}/{case}: METHOD absorption needs measured {variant} A/B")
        elif candidate_type == "EXECUTABLE" and not candidate_measured:
            errors.append(f"{label}: executable absorption requires isolated candidate run evidence")
        elif candidate_type == "SERVICE" and not candidate.get("service_authorized_and_tested"):
            errors.append(f"{label}: untested service cannot be absorbed")
        if not any_improvement:
            errors.append(f"{label}: no evidence-backed net improvement")
    return errors


def validate_search_clusters(clusters: list[dict]) -> list[str]:
    errors: list[str] = []
    for cluster in clusters:
        label = f"cluster/{cluster.get('cluster_id', '<missing>')}"
        search = cluster.get("search_evidence")
        if not isinstance(search, dict):
            errors.append(f"{label}: missing search_evidence")
            continue
        if not is_utc(search.get("utc")):
            errors.append(f"{label}: invalid search UTC")
        queries = search.get("queries")
        if not isinstance(queries, list) or not queries or not all(isinstance(q, str) and q.strip() for q in queries):
            errors.append(f"{label}: missing Chinese/English queries")
        if not search.get("source_type"):
            errors.append(f"{label}: missing source_type")
        results = search.get("result_ids")
        if not isinstance(results, list) or not results:
            errors.append(f"{label}: need result IDs or NO_VALID_CANDIDATE")
        elif results == ["NO_VALID_CANDIDATE"] and cluster.get("candidates"):
            errors.append(f"{label}: NO_VALID_CANDIDATE conflicts with candidates")
    return errors


def validate_rollback(data: object) -> list[str]:
    if not isinstance(data, dict) or not isinstance(data.get("writes"), list):
        return ["rollback_manifest: missing writes"]
    errors: list[str] = []
    for index, write in enumerate(data["writes"]):
        label = f"rollback_manifest/writes/{index}"
        for field in ("target_path", "before_state", "current_sha256", "recovery_action", "verify_command"):
            if not write.get(field):
                errors.append(f"{label}: missing {field}")
        if write.get("before_state") not in {"PRESENT", "ABSENT"}:
            errors.append(f"{label}: invalid before_state")
        if write.get("before_state") == "PRESENT" and not write.get("before_sha256"):
            errors.append(f"{label}: PRESENT needs before_sha256")
        if write.get("before_state") == "ABSENT" and write.get("before_sha256"):
            errors.append(f"{label}: ABSENT must not have before_sha256")
        if write.get("before_state") == "ABSENT" and write.get("recovery_action") != "MOVE_TO_RECOVERABLE_QUARANTINE":
            errors.append(f"{label}: new files require recoverable move action")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    data = json.loads(args.matrix.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    if str(data.get("schema_version")) != "2.0":
        errors.append("schema_version must be 2.0; legacy synthetic matrices are rejected")
    clusters = data.get("clusters", [])
    if not isinstance(clusters, list) or not clusters:
        errors.append("matrix has no clusters")
        clusters = []
    errors.extend(validate_search_clusters(clusters))
    seen: set[str] = set()
    candidates: list[dict] = []
    for cluster in clusters:
        cluster_id = cluster.get("cluster_id", "<missing>")
        for candidate in cluster.get("candidates", []):
            cid = candidate.get("candidate_id")
            if cid in seen:
                errors.append(f"duplicate candidate_id: {cid}")
            seen.add(cid)
            candidates.append(candidate)
            errors.extend(validate_candidate(cluster_id, candidate))
    accounting = data.get("raw_candidate_accounting", {})
    if accounting.get("raw_total") != 31 or accounting.get("accounted_total") != 31:
        errors.append("raw_candidate_accounting must close 31/31")
    if accounting.get("unmapped_raw_candidates") not in ([], 0):
        errors.append("unmapped_raw_candidates must be empty")
    errors.extend(validate_rollback(data.get("rollback_manifest")))
    decisions = {name: 0 for name in sorted(DECISIONS)}
    for candidate in candidates:
        if candidate.get("decision") in decisions:
            decisions[candidate["decision"]] += 1
    payload = {
        "status": "PASS" if not errors else "FAIL",
        "schema_version": data.get("schema_version"),
        "clusters": len(clusters),
        "candidates": len(candidates),
        "decisions": decisions,
        "errors": errors,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
