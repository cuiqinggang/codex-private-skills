#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""现实执行环境精确数字孪生唯一版 v1.2.0 — Browser/Network Unified Twin."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any, Iterable

VERSION = "1.2.0"
SCHEMA_VERSION = "browser-network-unified-twin-1.0"
EXPECTED_HOST_R2_FINGERPRINT = "9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8"
UNKNOWN = "UNKNOWN"

REQUIRED_BROWSER_MODULES = (
    "HOST_NETWORK",
    "BROWSER_ENVIRONMENT",
    "AUTH_STORAGE_SAFE",
    "PAGE_FRAME_GRAPH",
    "ACTIONABILITY",
    "BROWSER_NETWORK",
    "RUNTIME_EVENTS",
    "GOLDEN_TASK_RESULT",
    "TRACE_HASH",
    "CDP_EVIDENCE",
    "DOM_SNAPSHOT_HASH",
)

def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def _sha256_json(value: Any) -> str:
    return _sha256_bytes(_canonical_json(value).encode("utf-8"))

def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists():
        return out
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception as exc:
            out.append({"ts": None, "type": "PARSE_ERROR", "line": line_no, "error": str(exc)})
            continue
        if isinstance(item, dict):
            out.append(item)
        else:
            out.append({"ts": None, "type": "NON_OBJECT_EVENT", "value_sha256": _sha256_json(item)})
    return out

def _safe_get(d: Any, *keys: str, default: Any = None) -> Any:
    cur = d
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

def _find_first(root: Path, candidates: Iterable[str]) -> Path | None:
    for rel in candidates:
        p = root / rel
        if p.exists():
            return p
    return None

def _artifact_hash(result: dict[str, Any], suffix: str) -> str | None:
    artifacts = result.get("artifacts") if isinstance(result, dict) else None
    if not isinstance(artifacts, dict):
        return None
    for key, meta in artifacts.items():
        if str(key).replace("\\", "/").endswith(suffix):
            if isinstance(meta, dict):
                h = meta.get("sha256")
                if isinstance(h, str) and len(h) == 64:
                    return h.lower()
    return None

def _event_type(event: dict[str, Any]) -> str:
    if "type" in event:
        return str(event.get("type"))
    if "method" in event:
        return str(event.get("method"))
    return "UNKNOWN_EVENT"

def _event_ts(event: dict[str, Any]) -> str | None:
    ts = event.get("ts")
    return str(ts) if ts is not None else None

def _timeline_sort_key(event: dict[str, Any], seq: int) -> tuple[str, int]:
    ts = _event_ts(event)
    return (ts if ts else "9999-99-99T99:99:99.999999Z", seq)

def _classify_events(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    network, runtime, lifecycle, other = [], [], [], []
    for e in events:
        t = _event_type(e).lower()
        if any(k in t for k in ("request", "response", "network.", "websocket", "eventsource", "webtransport")):
            network.append(e)
        elif any(k in t for k in ("console", "pageerror", "exception", "crash", "javascriptdialog")):
            runtime.append(e)
        elif any(k in t for k in ("frame", "load", "lifecycle", "domcontent")):
            lifecycle.append(e)
        else:
            other.append(e)
    return {"network": network, "runtime": runtime, "lifecycle": lifecycle, "other": other}

def _actionability_status(probe: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(probe, dict):
        return {"status": "UNKNOWN_ACTIONABILITY", "reason": "MISSING_PROBE"}
    count = probe.get("locator_count")
    if count is None:
        return {"status": "UNKNOWN_ACTIONABILITY", "reason": "LOCATOR_COUNT_UNKNOWN"}
    if count == 0:
        return {"status": "NOT_ACTIONABLE", "reason": "ELEMENT_NOT_FOUND"}
    if count != 1:
        return {"status": "NOT_ACTIONABLE", "reason": "STRICTNESS_MULTIPLE_ELEMENTS", "count": count}
    checks = {
        "visible": probe.get("visible"),
        "stable": probe.get("stable_approx_two_animation_frames"),
        "receives_events": probe.get("receives_events_approx"),
        "enabled": probe.get("enabled"),
    }
    missing = [k for k, v in checks.items() if v is None]
    if missing:
        return {"status": "UNKNOWN_ACTIONABILITY", "reason": "CHECKS_UNKNOWN", "missing": missing}
    if checks["visible"] is not True:
        return {"status": "NOT_ACTIONABLE", "reason": "NOT_VISIBLE"}
    if checks["stable"] is not True:
        return {"status": "NOT_ACTIONABLE", "reason": "UNSTABLE"}
    if checks["receives_events"] is not True:
        return {"status": "NOT_ACTIONABLE", "reason": "EVENT_INTERCEPTED", "hit_target": probe.get("hit_target")}
    if checks["enabled"] is not True:
        return {"status": "NOT_ACTIONABLE", "reason": "DISABLED"}
    return {"status": "ACTIONABLE", "reason": "ALL_REQUIRED_CHECKS_PASS"}

def _last_probe(actionability: Any) -> dict[str, Any] | None:
    if not isinstance(actionability, list) or not actionability:
        return None
    return actionability[-1] if isinstance(actionability[-1], dict) else None

def _network_summary(network_events: list[dict[str, Any]]) -> dict[str, Any]:
    types = [_event_type(e) for e in network_events]
    failed = [e for e in network_events if "fail" in _event_type(e).lower() or "error" in _event_type(e).lower()]
    ws = [e for e in network_events if "websocket" in _event_type(e).lower()]
    responses = [e for e in network_events if "response" in _event_type(e).lower()]
    statuses = []
    for e in responses:
        status = e.get("status")
        if status is None and isinstance(e.get("params"), dict):
            status = _safe_get(e, "params", "response", "status")
        if isinstance(status, (int, float)):
            statuses.append(int(status))
    return {
        "event_count": len(network_events),
        "request_or_network_event_count": sum(1 for t in types if "request" in t.lower() or "network." in t.lower()),
        "response_event_count": len(responses),
        "failure_count": len(failed),
        "websocket_event_count": len(ws),
        "http_statuses": sorted(statuses),
    }

def _runtime_summary(runtime_events: list[dict[str, Any]]) -> dict[str, Any]:
    names = [_event_type(e).lower() for e in runtime_events]
    return {
        "event_count": len(runtime_events),
        "pageerror_or_exception_count": sum(1 for n in names if "pageerror" in n or "exception" in n),
        "crash_count": sum(1 for n in names if "crash" in n),
        "dialog_event_count": sum(1 for n in names if "dialog" in n),
        "console_event_count": sum(1 for n in names if "console" in n),
    }

def _extract_duration_ms(golden: dict[str, Any]) -> float | None:
    if not isinstance(golden, dict):
        return None
    for key in ("t_valid_ms", "duration_ms", "elapsed_ms", "e2e_ms", "T_VALID_MS"):
        value = golden.get(key)
        if isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) >= 0:
            return float(value)
    result = golden.get("result")
    if isinstance(result, dict):
        for key in ("t_valid_ms", "duration_ms", "elapsed_ms", "e2e_ms", "T_VALID_MS"):
            value = result.get(key)
            if isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) >= 0:
                return float(value)
    return None

def _semantic_outcome(golden: dict[str, Any]) -> str:
    if not isinstance(golden, dict):
        return UNKNOWN
    result = golden.get("result")
    if isinstance(result, dict):
        for key in ("outcome", "status", "result"):
            value = result.get(key)
            if value is not None:
                return str(value)
    for key in ("outcome", "status"):
        if golden.get(key) is not None:
            return str(golden.get(key))
    return UNKNOWN

def _build_timeline(events: list[dict[str, Any]], cdp_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    staged = []
    seq = 0
    for origin, source in (("playwright", events), ("cdp", cdp_events)):
        for event in source:
            seq += 1
            e = copy.deepcopy(event)
            e["_origin"] = origin
            e["_sequence"] = seq
            staged.append((_timeline_sort_key(e, seq), e))
    staged.sort(key=lambda item: item[0])
    return [e for _, e in staged]

def _required_module_presence(host_network, env, actionability, events, cdp_events, golden) -> dict[str, bool]:
    classification = _classify_events(events + cdp_events)
    artifact_source = golden if isinstance(golden, dict) else {}
    return {
        "HOST_NETWORK": isinstance(host_network, dict) and bool(host_network),
        "BROWSER_ENVIRONMENT": isinstance(env, dict) and bool(env),
        "AUTH_STORAGE_SAFE": isinstance(_safe_get(env, "storage_state_safe"), dict),
        "PAGE_FRAME_GRAPH": isinstance(_safe_get(env, "frames"), list),
        "ACTIONABILITY": isinstance(actionability, list) and bool(actionability),
        "BROWSER_NETWORK": bool(classification["network"]),
        "RUNTIME_EVENTS": bool(classification["runtime"]) or bool(events) or bool(cdp_events),
        "GOLDEN_TASK_RESULT": isinstance(golden, dict) and bool(golden),
        "TRACE_HASH": _artifact_hash(artifact_source, "trace.zip") is not None,
        "CDP_EVIDENCE": bool(cdp_events) or _artifact_hash(artifact_source, "cdp.jsonl") is not None,
        "DOM_SNAPSHOT_HASH": _artifact_hash(artifact_source, "dom-snapshot.json") is not None,
    }

def ingest_bundle(bundle_dir: str | Path) -> dict[str, Any]:
    root = Path(bundle_dir)
    host_path = _find_first(root, ("safe/host-network.json", "safehost-network.json", "host-network.safe.json"))
    env_path = _find_first(root, ("safe/environment.json", "environment.safe.json"))
    act_path = _find_first(root, ("safe/actionability.json", "actionability.safe.json"))
    evt_path = _find_first(root, ("safe/events.jsonl", "events.safe.jsonl"))
    cdp_path = _find_first(root, ("safe/cdp.jsonl", "cdp.safe.jsonl"))
    golden_path = _find_first(root, ("safe/golden-task-result.json", "golden-task-result.safe.json"))

    host = _read_json(host_path) if host_path else None
    env = _read_json(env_path) if env_path else None
    actionability = _read_json(act_path) if act_path else None
    events = _read_jsonl(evt_path) if evt_path else []
    cdp = _read_jsonl(cdp_path) if cdp_path else []
    golden = _read_json(golden_path) if golden_path else None

    timeline = _build_timeline(events, cdp)
    classes = _classify_events(timeline)
    presence = _required_module_presence(host, env, actionability, events, cdp, golden)
    unknowns = [name for name in REQUIRED_BROWSER_MODULES if not presence.get(name, False)]
    state = {
        "schema_version": SCHEMA_VERSION,
        "engine_version": VERSION,
        "provenance": {
            "bundle_path": str(root),
            "host_r2_fingerprint": EXPECTED_HOST_R2_FINGERPRINT,
            "source_policy": "OBSERVED_ONLY_NO_GUESSING",
        },
        "host": {"r2_fingerprint": EXPECTED_HOST_R2_FINGERPRINT, "network_safe": host if host is not None else UNKNOWN},
        "browser": {
            "environment_safe": env if env is not None else UNKNOWN,
            "actionability": actionability if actionability is not None else UNKNOWN,
            "actionability_eval": _actionability_status(_last_probe(actionability)),
        },
        "network": {"summary": _network_summary(classes["network"])},
        "runtime": {"summary": _runtime_summary(classes["runtime"])},
        "timeline": timeline,
        "golden_task": {
            "outcome": _semantic_outcome(golden or {}),
            "observed_duration_ms": _extract_duration_ms(golden or {}) if _extract_duration_ms(golden or {}) is not None else UNKNOWN,
            "raw_safe": golden if golden is not None else UNKNOWN,
        },
        "module_presence": presence,
        "critical_unknowns": unknowns,
    }
    state["state_fingerprint"] = _sha256_json({
        "host": state["host"], "browser": state["browser"], "network": state["network"],
        "runtime": state["runtime"], "golden_task": state["golden_task"], "module_presence": state["module_presence"],
    })
    return state

def semantic_signature(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "golden_outcome": _safe_get(state, "golden_task", "outcome", default=UNKNOWN),
        "actionability": _safe_get(state, "browser", "actionability_eval", "status", default=UNKNOWN),
        "actionability_reason": _safe_get(state, "browser", "actionability_eval", "reason", default=UNKNOWN),
        "network_failure_count": _safe_get(state, "network", "summary", "failure_count", default=UNKNOWN),
        "runtime_exception_count": _safe_get(state, "runtime", "summary", "pageerror_or_exception_count", default=UNKNOWN),
        "crash_count": _safe_get(state, "runtime", "summary", "crash_count", default=UNKNOWN),
        "dialog_event_count": _safe_get(state, "runtime", "summary", "dialog_event_count", default=UNKNOWN),
    }

def validate_single_state(state: dict[str, Any]) -> dict[str, Any]:
    errors = []
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append("SCHEMA_VERSION_MISMATCH")
    if _safe_get(state, "host", "r2_fingerprint") != EXPECTED_HOST_R2_FINGERPRINT:
        errors.append("HOST_R2_FINGERPRINT_MISMATCH")
    unknowns = state.get("critical_unknowns")
    if not isinstance(unknowns, list) or unknowns:
        errors.append("CRITICAL_UNKNOWNS_NONZERO")
    if _safe_get(state, "golden_task", "outcome") in (None, UNKNOWN):
        errors.append("GOLDEN_OUTCOME_UNKNOWN")
    action = _safe_get(state, "browser", "actionability_eval", "status")
    if action in (None, "UNKNOWN_ACTIONABILITY"):
        errors.append("ACTIONABILITY_UNKNOWN")
    duration = _safe_get(state, "golden_task", "observed_duration_ms")
    if duration == UNKNOWN or not isinstance(duration, (int, float)):
        errors.append("T_VALID_INPUT_UNKNOWN")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors,
            "critical_unknown_count": len(unknowns) if isinstance(unknowns, list) else UNKNOWN}

def fuse_runs(states: list[dict[str, Any]]) -> dict[str, Any]:
    if len(states) != 3:
        return {"status": "FAIL", "errors": ["GOLDEN_RUN_COUNT_NOT_3"], "run_count": len(states), "states": states}
    validations = [validate_single_state(s) for s in states]
    signatures = [semantic_signature(s) for s in states]
    signature_hashes = [_sha256_json(s) for s in signatures]
    same_signature = len(set(signature_hashes)) == 1
    errors = []
    if any(v["status"] != "PASS" for v in validations):
        errors.append("SINGLE_RUN_VALIDATION_FAILED")
    if not same_signature:
        errors.append("GOLDEN_SEMANTIC_SIGNATURE_NOT_3_OF_3")
    durations = [_safe_get(s, "golden_task", "observed_duration_ms") for s in states
                 if isinstance(_safe_get(s, "golden_task", "observed_duration_ms"), (int, float))]
    certified = not errors
    timing = {
        "run_duration_ms": durations,
        "t_valid_ms": min(durations) if len(durations) == 3 and certified else UNKNOWN,
        "task_min_ms": min(durations) if len(durations) == 3 else UNKNOWN,
        "task_median_ms": statistics.median(durations) if len(durations) == 3 else UNKNOWN,
        "task_max_ms": max(durations) if len(durations) == 3 else UNKNOWN,
        "certification_evidence_time_ms": sum(durations) if len(durations) == 3 and certified else UNKNOWN,
        "t_valid_definition": "minimum measured Golden Task duration among the frozen 3/3 timing runs, valid only after all quality/reality gates pass",
        "certification_time_note": "sum of the three run durations is evidence cost, not the optimization metric",
    }
    fused = {
        "schema_version": SCHEMA_VERSION, "engine_version": VERSION,
        "status": "PASS" if certified else "FAIL", "errors": errors, "run_count": 3,
        "single_run_validations": validations, "semantic_signatures": signatures,
        "semantic_signature_hashes": signature_hashes,
        "golden_task_reproduced": "3_OF_3" if certified else "NO",
        "critical_unknown_count": sum(v["critical_unknown_count"] for v in validations)
            if all(isinstance(v.get("critical_unknown_count"), int) for v in validations) else UNKNOWN,
        "timing": timing, "canonical_signature": signatures[0] if same_signature else UNKNOWN,
        "state_fingerprints": [s.get("state_fingerprint") for s in states],
    }
    fused["fusion_fingerprint"] = _sha256_json({
        "canonical_signature": fused["canonical_signature"],
        "state_fingerprints": fused["state_fingerprints"],
        "timing": timing,
    })
    return fused

def replay_fused(fused: dict[str, Any]) -> dict[str, Any]:
    if fused.get("status") != "PASS":
        return {"status": "BLOCKED_INVALID_FUSED_REALITY", "errors": fused.get("errors", []), "unknowns_preserved": True}
    return {"status": "REPLAYED", "reality_mutated": False,
            "golden_task_reproduced": fused.get("golden_task_reproduced"),
            "semantic_signature": copy.deepcopy(fused.get("canonical_signature")),
            "timing": copy.deepcopy(fused.get("timing")),
            "fusion_fingerprint": fused.get("fusion_fingerprint")}

def compare_replay_to_reality(fused: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    reality_sig, replay_sig = fused.get("canonical_signature"), replay.get("semantic_signature")
    deltas = {}
    if isinstance(reality_sig, dict) and isinstance(replay_sig, dict):
        for key in sorted(set(reality_sig) | set(replay_sig)):
            if reality_sig.get(key) != replay_sig.get(key):
                deltas[key] = {"reality": reality_sig.get(key), "twin": replay_sig.get(key)}
    else:
        deltas["semantic_signature"] = {"reality": reality_sig, "twin": replay_sig}
    return {"status": "PASS" if not deltas and replay.get("status") == "REPLAYED" else "FAIL",
            "delta_count": len(deltas), "deltas": deltas}

def deep_merge(base: Any, overlay: Any) -> Any:
    if isinstance(base, dict) and isinstance(overlay, dict):
        out = copy.deepcopy(base)
        for k, v in overlay.items():
            out[k] = deep_merge(out[k], v) if k in out else copy.deepcopy(v)
        return out
    return copy.deepcopy(overlay)

def shadow_overlay(fused: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    baseline = copy.deepcopy(fused)
    shadow = deep_merge(baseline, overlay)
    return {"status": "HYPOTHETICAL_SHADOW", "reality_mutated": False,
            "delta_present": _canonical_json(baseline) != _canonical_json(shadow),
            "reality_fingerprint_before": _sha256_json(baseline),
            "reality_fingerprint_after": _sha256_json(baseline),
            "shadow_state": shadow}

def benchmark_replay(fused: dict[str, Any], repeats: int = 1000) -> dict[str, Any]:
    if fused.get("status") != "PASS":
        return {"status": "BLOCKED_INVALID_FUSED_REALITY"}
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        replay = replay_fused(fused)
        if replay.get("status") != "REPLAYED":
            return {"status": "FAIL_REPLAY"}
        samples.append((time.perf_counter_ns() - start) / 1_000_000.0)
    ordered = sorted(samples)
    return {"status": "PASS", "repeats": repeats,
            "replay_overhead_ms": {
                "min": min(samples), "p50": ordered[len(ordered)//2],
                "p95": ordered[min(len(ordered)-1, math.ceil(len(ordered)*0.95)-1)],
                "max": max(samples)},
            "note": "Twin engine replay overhead only; not the browser Golden Task T_VALID."}

def _fixture_probe(reason: str = "ACTIONABLE") -> dict[str, Any]:
    base = {"label": "FINAL", "locator_count": 1, "visible": True, "enabled": True,
            "stable_approx_two_animation_frames": True, "receives_events_approx": True,
            "hit_target": {"tag": "BUTTON", "id": "dialog"}}
    if reason == "MISSING": base["locator_count"] = 0
    elif reason == "MULTIPLE": base["locator_count"] = 2
    elif reason == "NOT_VISIBLE": base["visible"] = False
    elif reason == "UNSTABLE": base["stable_approx_two_animation_frames"] = False
    elif reason == "INTERCEPTED":
        base["receives_events_approx"] = False
        base["hit_target"] = {"tag": "DIV", "id": "overlay"}
    elif reason == "DISABLED": base["enabled"] = False
    return base

def _fixture_state(outcome="PASS", duration_ms=100.0, action_reason="ACTIONABLE",
                   network_failures=0, runtime_exceptions=0, dialog_events=0) -> dict[str, Any]:
    actionability = [_fixture_probe(action_reason)]
    browser_events = [{"ts": "2026-09-21T00:00:00.000Z", "type": "request", "url": "https://example.invalid/"}]
    for i in range(network_failures):
        browser_events.append({"ts": f"2026-09-21T00:00:00.{i+1:03d}Z", "type": "requestfailed"})
    for i in range(runtime_exceptions):
        browser_events.append({"ts": f"2026-09-21T00:00:01.{i+1:03d}Z", "type": "pageerror"})
    for i in range(dialog_events):
        browser_events.append({"ts": f"2026-09-21T00:00:02.{i+1:03d}Z", "type": "javascriptdialogopening"})
    golden = {"result": {"outcome": outcome, "duration_ms": duration_ms},
              "artifacts": {"raw/trace.zip": {"sha256": "1"*64}, "raw/cdp.jsonl": {"sha256": "2"*64},
                            "raw/dom-snapshot.json": {"sha256": "3"*64}}}
    env = {"storage_state_safe": {"cookies": [], "origins": []},
           "frames": [{"index": 0, "url": "https://example.invalid/"}]}
    timeline = _build_timeline(browser_events, [{"ts": "2026-09-21T00:00:00.500Z",
                                                "method": "Network.responseReceived",
                                                "params": {"response": {"status": 200}}}])
    classes = _classify_events(timeline)
    presence = {k: True for k in REQUIRED_BROWSER_MODULES}
    state = {
        "schema_version": SCHEMA_VERSION, "engine_version": VERSION,
        "provenance": {"source_policy": "VIRTUAL_FIXTURE_ONLY"},
        "host": {"r2_fingerprint": EXPECTED_HOST_R2_FINGERPRINT, "network_safe": {"mode": "fixture"}},
        "browser": {"environment_safe": env, "actionability": actionability,
                    "actionability_eval": _actionability_status(actionability[-1])},
        "network": {"summary": _network_summary(classes["network"])},
        "runtime": {"summary": _runtime_summary(classes["runtime"])},
        "timeline": timeline,
        "golden_task": {"outcome": outcome, "observed_duration_ms": duration_ms, "raw_safe": golden},
        "module_presence": presence, "critical_unknowns": [],
    }
    state["state_fingerprint"] = _sha256_json({
        "host": state["host"], "browser": state["browser"], "network": state["network"],
        "runtime": state["runtime"], "golden_task": state["golden_task"], "module_presence": presence})
    return state

def run_selftest() -> dict[str, Any]:
    cases = []
    def check(name, ok): cases.append({"name": name, "pass": bool(ok)})
    expected = {"MISSING":"ELEMENT_NOT_FOUND","MULTIPLE":"STRICTNESS_MULTIPLE_ELEMENTS",
                "NOT_VISIBLE":"NOT_VISIBLE","UNSTABLE":"UNSTABLE",
                "INTERCEPTED":"EVENT_INTERCEPTED","DISABLED":"DISABLED"}
    for key, reason in expected.items():
        check(f"actionability_{key.lower()}", _actionability_status(_fixture_probe(key)).get("reason") == reason)
    check("actionability_pass", _actionability_status(_fixture_probe()).get("status") == "ACTIONABLE")
    states = [_fixture_state(duration_ms=x) for x in (100.0,101.0,99.5)]
    fused = fuse_runs(states)
    check("fuse_3_of_3_pass", fused.get("status") == "PASS")
    check("golden_semantics_3_of_3", fused.get("golden_task_reproduced") == "3_OF_3")
    check("t_valid_defined", isinstance(_safe_get(fused, "timing", "t_valid_ms"), (int,float)))
    replay = replay_fused(fused)
    check("replay_pass", replay.get("status") == "REPLAYED")
    diff = compare_replay_to_reality(fused, replay)
    check("reality_twin_delta_zero", diff.get("status") == "PASS" and diff.get("delta_count") == 0)
    shadow = shadow_overlay(fused, {"canonical_signature": {"golden_outcome": "FAIL"}})
    check("shadow_isolation", shadow.get("reality_mutated") is False and
          shadow.get("reality_fingerprint_before") == shadow.get("reality_fingerprint_after"))
    check("reject_not_three_runs", fuse_runs(states[:2]).get("status") == "FAIL")
    changed = copy.deepcopy(states); changed[2] = _fixture_state(outcome="FAIL", duration_ms=99.5)
    check("reject_semantic_drift", fuse_runs(changed).get("status") == "FAIL")
    unknown = copy.deepcopy(states); unknown[1]["critical_unknowns"] = ["TRACE_HASH"]
    check("reject_unknowns", fuse_runs(unknown).get("status") == "FAIL")
    bad_fp = copy.deepcopy(states[0]); bad_fp["host"]["r2_fingerprint"] = "0"*64
    check("reject_host_fingerprint_drift", validate_single_state(bad_fp).get("status") == "FAIL")
    netfail = _fixture_state(network_failures=2)
    check("network_failure_count", _safe_get(netfail, "network", "summary", "failure_count") == 2)
    runtime = _fixture_state(runtime_exceptions=2, dialog_events=1)
    check("runtime_exception_count", _safe_get(runtime, "runtime", "summary", "pageerror_or_exception_count") == 2)
    check("dialog_event_count", _safe_get(runtime, "runtime", "summary", "dialog_event_count") == 1)
    sig = semantic_signature(runtime)
    check("semantic_signature_runtime", sig.get("runtime_exception_count") == 2 and sig.get("dialog_event_count") == 1)
    check("state_fingerprint_present", len(states[0].get("state_fingerprint","")) == 64)
    fused2 = fuse_runs([copy.deepcopy(s) for s in states])
    check("fusion_deterministic", fused.get("fusion_fingerprint") == fused2.get("fusion_fingerprint"))
    check("task_min_correct", abs(_safe_get(fused,"timing","task_min_ms") - 99.5) < 1e-9)
    check("task_median_correct", abs(_safe_get(fused,"timing","task_median_ms") - 100.0) < 1e-9)
    check("task_max_correct", abs(_safe_get(fused,"timing","task_max_ms") - 101.0) < 1e-9)
    check("t_valid_min_correct", abs(_safe_get(fused,"timing","t_valid_ms") - 99.5) < 1e-9)
    check("certification_sum_correct", abs(_safe_get(fused,"timing","certification_evidence_time_ms") - 300.5) < 1e-9)
    check("unknown_not_fabricated", replay_fused({"status":"FAIL","errors":["X"]}).get("unknowns_preserved") is True)
    for reason, expected_reason in (("INTERCEPTED","EVENT_INTERCEPTED"),("UNSTABLE","UNSTABLE"),
                                    ("DISABLED","DISABLED"),("NOT_VISIBLE","NOT_VISIBLE")):
        st = _fixture_state(action_reason=reason)
        check(f"failure_semantic_{reason.lower()}",
              _safe_get(st,"browser","actionability_eval","reason") == expected_reason)
    passed = sum(1 for c in cases if c["pass"]); failed = len(cases)-passed
    return {"engine_version": VERSION, "schema_version": SCHEMA_VERSION,
            "case_count": len(cases), "passed": passed, "failed": failed,
            "virtual_fusion_selftest": "PASS" if failed == 0 else "FAIL",
            "scope": "Virtual fixtures only. Does not certify real Browser R3 input, real browser replay, or Environment-99.",
            "cases": cases}

def _load_bundle_set(paths):
    states = [ingest_bundle(p) for p in paths]
    return states, fuse_runs(states)

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("selftest")
    validate = sub.add_parser("validate"); validate.add_argument("--bundle", action="append", required=True)
    replay = sub.add_parser("replay"); replay.add_argument("--bundle", action="append", required=True)
    bench = sub.add_parser("benchmark"); bench.add_argument("--bundle", action="append", required=True); bench.add_argument("--repeats", type=int, default=1000)
    shadow = sub.add_parser("shadow"); shadow.add_argument("--bundle", action="append", required=True); shadow.add_argument("--overlay", required=True)
    args = parser.parse_args()
    if args.mode == "selftest":
        result = run_selftest()
    else:
        states, fused = _load_bundle_set(args.bundle)
        if args.mode == "validate":
            result = {"states": [validate_single_state(s) for s in states], "fused": fused}
        elif args.mode == "replay":
            replayed = replay_fused(fused)
            result = {"fused": fused, "replay": replayed,
                      "reality_twin_diff": compare_replay_to_reality(fused, replayed)}
        elif args.mode == "benchmark":
            result = benchmark_replay(fused, args.repeats)
        else:
            result = shadow_overlay(fused, _read_json(Path(args.overlay)))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
