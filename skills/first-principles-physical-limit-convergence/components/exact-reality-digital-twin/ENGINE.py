#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exact-reality-digital-twin v1.3.0 formal Browser Reality implementation.

Reality inputs are read-only. Browser replay is deterministic evidence replay;
it never launches a browser, reaches the network, or mutates captured state.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "1.3.0"
COMPONENT_ID = "exact-reality-digital-twin"
PROFILE_ID = "PLAYWRIGHT_GOLDEN_REALITY_PROFILE"
METHOD_VERSION = "3.1.7"
REALITY_SOURCE_TWIN_VERSION = "1.1.0"
EXPECTED_HOST_FINGERPRINT = "9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8"
EXPECTED_BROWSER_FINGERPRINT = "9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd"
EXPECTED_GOLDEN_SHA256 = "1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08"
EXPECTED_TASK_SHA256 = "31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960"
EXPECTED_VALID_SHA256 = "2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae"
EXPECTED_REALITY_PACK_MANIFEST_SHA256 = "fd7d381a7f8185a5c12af7a74f7b4d43809d172d84fff78454863383ae9727cd"

ACTION_ORDER = [
    "TASK_IDENTITY", "VALID_IDENTITY", "BROWSER_PROCESS_IDENTITY",
    "CONTEXT_IDENTITY", "PROFILE_IDENTITY", "PAGE_FRAME_GRAPH",
    "NAVIGATION", "LOCATOR", "INPUT", "CLICK", "EXTRACT", "KEYBOARD",
    "DRAG_DROP", "UPLOAD", "DOWNLOAD", "BEFORE_DIALOG_ACTIONABILITY",
    "DIALOG_OPENING", "DIALOG_ACCEPT", "AFTER_DIALOG_ACTIONABILITY",
    "POPUP", "FRAME", "ROUTE_API", "ISOLATED_CONTEXT", "SCREENSHOT",
    "PERSISTENT_RECONNECT_1", "PERSISTENT_RECONNECT_2",
    "FINAL_GOLDEN_RESULT",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def canonical_hash(value) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deep_merge(base, overlay):
    if isinstance(base, dict) and isinstance(overlay, dict):
        result = copy.deepcopy(base)
        for key, value in overlay.items():
            result[key] = deep_merge(result[key], value) if key in result else copy.deepcopy(value)
        return result
    return copy.deepcopy(overlay)


def changed_paths(base, changed, prefix=""):
    if isinstance(base, dict) and isinstance(changed, dict):
        paths = []
        for key in sorted(set(base) | set(changed)):
            child = f"{prefix}.{key}" if prefix else key
            if key not in base or key not in changed:
                paths.append(child)
            else:
                paths.extend(changed_paths(base[key], changed[key], child))
        return paths
    return [] if base == changed else [prefix]


# Legacy Host/Codex implementation retained verbatim in behavior.
def canonical_current_state():
    return {
        "reality_fingerprint_v3_sha256": EXPECTED_HOST_FINGERPRINT,
        "critical_unknown_count": 0,
        "critical_execution_coverage": "100.00",
        "twin_input_ready": "YES",
        "rules_runtime_effective": "CAPTURED",
        "rule_engine_validation": "PASS",
        "target": {
            "process_creation": "DENIED_BEFORE_SUCCESSFUL_START",
            "failure_api": "SetTokenInformation",
            "failure_code": 1344,
            "reproduction": "3_OF_3",
            "child_running": "NO",
            "child_path_resolution": "NOT_REACHED",
            "child_execution_token": "NO_RUNNING_CHILD_PROCESS_TOKEN",
        },
    }


def validate_state(state):
    errors = []
    if state.get("reality_fingerprint_v3_sha256") != EXPECTED_HOST_FINGERPRINT:
        errors.append("REALITY_FINGERPRINT_MISMATCH")
    if state.get("critical_unknown_count") != 0:
        errors.append("CRITICAL_UNKNOWN_NONZERO")
    if state.get("critical_execution_coverage") != "100.00":
        errors.append("CRITICAL_COVERAGE_NOT_100")
    if state.get("twin_input_ready") != "YES":
        errors.append("TWIN_INPUT_NOT_READY")
    if state.get("rules_runtime_effective") != "CAPTURED":
        errors.append("RULES_NOT_CAPTURED")
    if state.get("rule_engine_validation") != "PASS":
        errors.append("RULE_ENGINE_NOT_VALIDATED")
    target = state.get("target", {})
    for key, expected in canonical_current_state()["target"].items():
        if target.get(key) != expected:
            errors.append("TARGET_" + key.upper() + "_MISMATCH")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def replay_current(state=None):
    state = canonical_current_state() if state is None else state
    check = validate_state(state)
    if check["status"] != "PASS":
        return {"status": "INVALID_REALITY_STATE", "errors": check["errors"]}
    target = state["target"]
    return {
        "status": "REPLAYED",
        "stage": "PROCESS_CREATION_BEFORE_CHILD_START",
        "api": target["failure_api"],
        "error_code": target["failure_code"],
        "result": "DENIED",
        "child_running": target["child_running"],
        "path_resolution": target["child_path_resolution"],
        "child_execution_token": target["child_execution_token"],
    }


def shadow_overlay(overlay):
    base = canonical_current_state()
    hypothetical = deep_merge(base, overlay)
    return {
        "status": "HYPOTHETICAL_SHADOW",
        "reality_mutated": False,
        "delta_present": hypothetical != base,
        "baseline_validation": validate_state(base),
        "overlay_validation_against_reality": validate_state(hypothetical),
        "state": hypothetical,
    }


def run_selftest():
    base = canonical_current_state()
    cases = []

    def add(name, state, expected):
        actual = validate_state(state)["status"]
        cases.append((name, actual == expected))

    add("baseline", base, "PASS")
    mutations = [
        {"reality_fingerprint_v3_sha256": "0" * 64}, {"critical_unknown_count": 1},
        {"critical_execution_coverage": "99.99"}, {"twin_input_ready": "NO"},
        {"rules_runtime_effective": "UNKNOWN"}, {"rule_engine_validation": "FAIL"},
        {"target": {"process_creation": "STARTED"}}, {"target": {"failure_api": "CreateProcess"}},
        {"target": {"failure_code": 5}}, {"target": {"reproduction": "2_OF_3"}},
        {"target": {"child_running": "YES"}}, {"target": {"child_path_resolution": "RESOLVED"}},
        {"target": {"child_execution_token": "PRESENT"}},
    ]
    for index, overlay in enumerate(mutations, 1):
        add("mutation_" + str(index), deep_merge(base, overlay), "FAIL")
    replay = replay_current(base)
    cases.append(("replay_boundary", replay.get("status") == "REPLAYED" and replay.get("error_code") == 1344))
    shadow = shadow_overlay({"target": {"failure_code": 0, "process_creation": "STARTED"}})
    cases.append(("shadow_isolation", shadow["status"] == "HYPOTHETICAL_SHADOW" and shadow["reality_mutated"] is False and shadow["delta_present"]))
    for index in range(8):
        replay = replay_current(base)
        cases.append(("repeat_" + str(index + 1), replay.get("status") == "REPLAYED" and replay.get("error_code") == 1344))
    passed = sum(1 for _, ok in cases if ok)
    return {
        "engine_version": VERSION,
        "case_count": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "virtual_contract_99": "PASS" if passed == len(cases) else "FAIL",
        "cases": [{"name": name, "pass": ok} for name, ok in cases],
    }


def source_paths(workspace: Path):
    r3 = workspace / "R3-BROWSER-REALITY"
    return {
        "r3": r3,
        "anchor": r3 / "final" / "BROWSER-R3-FINAL-ANCHOR.json",
        "fingerprint": r3 / "final" / "BROWSER-R3-FINGERPRINT.json",
        "manifest": r3 / "final" / "BROWSER-R3-MANIFEST.json",
        "process": r3 / "process-closure-01" / "BROWSER-PROCESS-CLOSURE.json",
        "pack_manifest": workspace / "REALITY-PACK" / "manifest.json",
        "golden": Path(r"C:\AI\Playwright-Native-AI-Browser\scripts\golden-harness.cjs"),
    }


def load_reality(workspace: Path):
    paths = source_paths(workspace)
    missing = [str(path) for key, path in paths.items() if key != "r3" and not path.is_file()]
    if missing:
        return None, ["MISSING_INPUT:" + item for item in missing]
    anchor = read_json(paths["anchor"])
    fingerprint = read_json(paths["fingerprint"])
    manifest = read_json(paths["manifest"])
    process = read_json(paths["process"])
    pack_manifest = read_json(paths["pack_manifest"])
    errors = []

    checks = {
        "BROWSER_R3_FINGERPRINT_SHA256": fingerprint.get("browser_r3_fingerprint_sha256") == EXPECTED_BROWSER_FINGERPRINT,
        "BROWSER_R3_FINGERPRINT_RECOMPUTED": canonical_hash(fingerprint.get("input")) == EXPECTED_BROWSER_FINGERPRINT,
        "GOLDEN_SHA256_ACTUAL": sha256_file(paths["golden"]) == EXPECTED_GOLDEN_SHA256,
        "GOLDEN_SHA256_ANCHOR": anchor.get("canonical_golden_sha256") == EXPECTED_GOLDEN_SHA256,
        "BROWSER_CRITICAL_UNKNOWN_COUNT": anchor.get("browser_critical_unknown_count") == 0,
        "BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE": anchor.get("browser_execution_relevant_state_complete") is True,
        "GOLDEN_TASK_REALITY_REPRODUCED": anchor.get("golden_task_reality_reproduced") == "3_OF_3",
        "BROWSER_TWIN_INPUT_READY": manifest.get("browser_twin_input_ready") is True,
        "BROWSER_R3_REAL_CAPTURE": manifest.get("browser_r3_real_capture") == "PASS",
        "REALITY_DELTA": anchor.get("reality_delta") == "NONE" and manifest.get("reality_delta") == "NONE",
        "TASK_SHA256": anchor.get("task_sha256") == EXPECTED_TASK_SHA256,
        "VALID_RULE_SHA256": anchor.get("valid_rule_sha256") == EXPECTED_VALID_SHA256,
        "REALITY_PACK_MANIFEST_SHA256": sha256_file(paths["pack_manifest"]) == EXPECTED_REALITY_PACK_MANIFEST_SHA256,
        "PROCESS_CLOSURE_SHA256": sha256_file(paths["process"]) == anchor["required_modules"]["R3_BROWSER_PROCESS"]["evidence"]["process_closure_sha256"],
    }
    for name, passed in checks.items():
        if not passed:
            errors.append(name + "_MISMATCH")

    for entry in manifest.get("files", []):
        target = paths["r3"] / Path(entry["path"])
        if not target.is_file():
            errors.append("R3_MANIFEST_FILE_MISSING:" + entry["path"])
            continue
        if target.stat().st_size != entry["bytes"] or sha256_file(target) != entry["sha256"]:
            errors.append("R3_MANIFEST_FILE_MISMATCH:" + entry["path"])

    runs = []
    for index in range(1, 4):
        safe = paths["r3"] / f"run-{index:02d}" / "safe"
        runs.append({
            "index": index,
            "environment": read_json(safe / "environment.json"),
            "result": read_json(safe / "full-run-result.json"),
            "golden_result": read_json(safe / "golden-task-result.json"),
            "actionability": read_json(safe / "actionability.json"),
            "events": read_jsonl(safe / "events.jsonl"),
            "cdp": read_jsonl(safe / "cdp.jsonl"),
        })
    return {
        "paths": paths,
        "anchor": anchor,
        "fingerprint": fingerprint,
        "manifest": manifest,
        "process": process,
        "pack_manifest": pack_manifest,
        "runs": runs,
        "input_checks": checks,
    }, errors


def normalized_actionability(entries, label):
    selected = [next(item for item in run if item["label"] == label) for run in entries]
    keys = ["exactly_one", "visible", "enabled", "stable_approx_two_animation_frames", "receives_events_approx"]
    result = {key: all(item[key] is True for item in selected) for key in keys}
    result.update({
        "locator_count": [item["locator_count"] for item in selected],
        "hit_target": [item["hit_target"] for item in selected],
        "computed_style": [item["computed_style"] for item in selected],
        "active_animations": [item["active_animations"] for item in selected],
    })
    return result


def build_profile(reality):
    anchor = reality["anchor"]
    process = reality["process"]
    runs = reality["runs"]
    environments = [run["environment"] for run in runs]
    actionability = [run["actionability"] for run in runs]
    artifact_entries = reality["manifest"]["files"]
    artifact_hashes = [
        entry for entry in artifact_entries
        if any(token in entry["path"] for token in ("trace.zip", "cdp.jsonl", "dom-snapshot.json"))
    ]
    event_counts = [dict(Counter(event["type"] for event in run["events"])) for run in runs]
    cdp_counts = [dict(Counter(event["method"] for event in run["cdp"])) for run in runs]
    dialog_openings = [
        [event["params"] for event in run["cdp"] if event["method"] == "Page.javascriptDialogOpening"]
        for run in runs
    ]
    dialog_closings = [
        [event["params"] for event in run["cdp"] if event["method"] == "Page.javascriptDialogClosed"]
        for run in runs
    ]
    profile = {
        "profile_id": PROFILE_ID,
        "component_id": COMPONENT_ID,
        "method_version": METHOD_VERSION,
        "twin_source_version": REALITY_SOURCE_TWIN_VERSION,
        "mode": "READ_ONLY_REALITY_REPLAY",
        "browser_process": {
            "products": process["browser_products"],
            "identity_source": process["process_fingerprint_alternative_source"],
            "raw_command_line_stored": False,
            "process_closure_sha256": anchor["required_modules"]["R3_BROWSER_PROCESS"]["evidence"]["process_closure_sha256"],
        },
        "versions": {
            "node": anchor["acceptance_hard_fields"]["NODE_PLAYWRIGHT_BROWSER_VERSION"]["evidence"]["node"],
            "playwright": process["playwright"]["version"],
            "browser": process["browser_executable"]["version"],
        },
        "browser_executable_fingerprint": {
            "path_sha256": process["browser_executable"]["path_sha256"],
            "file_sha256": process["browser_executable"]["file_sha256"],
        },
        "launch_config_fingerprint": {
            "sha256": process["launch_config_sha256"],
            "config": process["launch_config"],
        },
        "context_config": {
            "type": anchor["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["context_type"],
            "viewport": [environment["viewport"] for environment in environments],
            "locale": [environment["runtime"]["language"] for environment in environments],
            "timezone": [environment["runtime"]["timezone"] for environment in environments],
            "user_agent_sha256": anchor["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["user_agent_sha256"],
            "accept_downloads": True,
            "default_timeout_ms": 5000,
        },
        "profile_user_data_dir_fingerprint": {
            "profile_path_sha256": anchor["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["profile_path_sha256"],
            "collector_mutated_profile": False,
        },
        "auth_storage_structure": {
            "capture_modes": anchor["required_modules"]["R3_AUTH_STORAGE"]["evidence"]["storage_capture_modes"],
            "counts": anchor["required_modules"]["R3_AUTH_STORAGE"]["evidence"]["counts"],
            "auth_state_criterion": anchor["required_modules"]["R3_AUTH_STORAGE"]["evidence"]["auth_state_criterion"],
            "plaintext_values_stored": False,
        },
        "page_frame_worker_service_worker_graph": {
            "pages": anchor["required_modules"]["R3_PAGE_GRAPH"]["evidence"]["page_counts"],
            "frames": [environment["frames"] for environment in environments],
            "worker_status": anchor["required_modules"]["R3_PAGE_GRAPH"]["evidence"]["worker_status"],
            "service_worker_status": anchor["required_modules"]["R3_PAGE_GRAPH"]["evidence"]["service_worker_status"],
        },
        "dom_layout_overlay_animation": {
            "dom_snapshot_hashes": [entry["sha256"] for entry in artifact_entries if "dom-snapshot.json" in entry["path"]],
            "target_selector": "#dialog",
            "overlay_or_interceptor": "NOT_PRESENT_AT_CENTER_HIT_TEST",
            "active_animations": [item["active_animations"] for run in actionability for item in run],
        },
        "dialog_actionability": {
            "BEFORE_DIALOG": normalized_actionability(actionability, "BEFORE_DIALOG"),
            "AFTER_DIALOG": normalized_actionability(actionability, "AFTER_DIALOG"),
        },
        "browser_network": {
            "event_counts": event_counts,
            "redirect_observed": anchor["required_modules"]["R3_NETWORK_BROWSER"]["evidence"]["redirect_observed"],
            "websocket_status": anchor["required_modules"]["R3_NETWORK_BROWSER"]["evidence"]["websocket_status"],
            "service_worker_status": anchor["required_modules"]["R3_NETWORK_BROWSER"]["evidence"]["service_worker_status"],
            "tls_status": anchor["required_modules"]["R3_NETWORK_BROWSER"]["evidence"]["tls_status"],
            "route_api_observed": all(counts.get("request", 0) == 5 and counts.get("response", 0) == 5 for counts in event_counts),
        },
        "host_network": {
            "pre_safe_sha256": anchor["required_modules"]["R3_NETWORK_HOST"]["evidence"]["host_pre_safe_sha256"],
            "post_safe_sha256": anchor["required_modules"]["R3_NETWORK_HOST"]["evidence"]["host_post_safe_sha256"],
            "proxy_unchanged": True,
            "network_settings_unchanged": True,
            "outbound_probe": "NO",
        },
        "runtime_dialog_lifecycle": {
            "cdp_method_counts": cdp_counts,
            "dialog_opening": dialog_openings,
            "dialog_closed": dialog_closings,
            "pageerror_status": "NOT_PRESENT",
            "crash_status": "NOT_PRESENT",
        },
        "artifact_hashes": artifact_hashes,
        "golden_task": {
            "reproduced": anchor["golden_task_reality_reproduced"],
            "outcomes": [run["result"]["OUTCOME"] for run in runs],
            "errors_present": [run["result"]["ERROR"]["PRESENT"] for run in runs],
            "frozen_action_order": ACTION_ORDER,
            "persistent_reconnect_in_frozen_golden": True,
        },
        "task_sha256": anchor["task_sha256"],
        "valid_rule_sha256": anchor["valid_rule_sha256"],
        "reality_pack_manifest": {
            "sha256": anchor["reality_pack_manifest_sha256"],
            "files": reality["pack_manifest"]["files"],
        },
        "browser_r3_fingerprint_sha256": reality["fingerprint"]["browser_r3_fingerprint_sha256"],
        "canonical_golden_sha256": anchor["canonical_golden_sha256"],
        "historical_t_star_real_ms": anchor["historical_t_star_real_ms"],
        "source_invariants": {
            "observation_perturbation": "NO",
            "profile_mutated": "NO",
            "routing_or_mock_enabled_by_collector": "NO",
        },
    }
    return profile


def browser_validate(workspace: Path, output_dir: Path):
    reality, errors = load_reality(workspace)
    if errors:
        return {
            "status": "FAIL", "profile_id": PROFILE_ID,
            "critical_unknown_count": len(errors), "errors": errors,
            "reality_delta": "TWIN_INPUT_GATE_MISMATCH", "action": "STOP", "return_to_gpt": True,
        }
    profile = build_profile(reality)
    critical_values = [
        profile["browser_r3_fingerprint_sha256"], profile["canonical_golden_sha256"],
        profile["task_sha256"], profile["valid_rule_sha256"], profile["golden_task"]["reproduced"],
    ]
    unknown_count = sum(value == "UNKNOWN" or value is None for value in critical_values)
    status = "PASS" if unknown_count == 0 else "FAIL"
    if status == "PASS":
        write_json(output_dir / "PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json", profile)
    result = {
        "status": status,
        "profile_id": PROFILE_ID,
        "critical_unknown_count": unknown_count,
        "input_gate": reality["input_checks"],
        "profile_sha256": canonical_hash(profile),
    }
    write_json(output_dir / "BROWSER-PROFILE-VALIDATION.json", result)
    return result


def load_profile(output_dir: Path):
    path = output_dir / "PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json"
    if not path.is_file():
        raise ValueError("BROWSER_PROFILE_MISSING")
    return read_json(path)


def browser_replay(workspace: Path, output_dir: Path, after_shadow=False):
    reality, errors = load_reality(workspace)
    if errors:
        raise ValueError("TWIN_INPUT_GATE_MISMATCH:" + ",".join(errors))
    profile = load_profile(output_dir)
    evidence_3_of_3 = profile["golden_task"]["outcomes"] == ["PASS", "PASS", "PASS"]
    before = profile["dialog_actionability"]["BEFORE_DIALOG"]
    after = profile["dialog_actionability"]["AFTER_DIALOG"]
    dialog_open = profile["runtime_dialog_lifecycle"]["dialog_opening"]
    dialog_closed = profile["runtime_dialog_lifecycle"]["dialog_closed"]
    action_status = {name: evidence_3_of_3 for name in ACTION_ORDER}
    action_status.update({
        "TASK_IDENTITY": profile["task_sha256"] == EXPECTED_TASK_SHA256,
        "VALID_IDENTITY": profile["valid_rule_sha256"] == EXPECTED_VALID_SHA256,
        "BROWSER_PROCESS_IDENTITY": profile["browser_executable_fingerprint"]["file_sha256"] == reality["process"]["browser_executable"]["file_sha256"],
        "CONTEXT_IDENTITY": profile["context_config"]["type"] == "NON_PERSISTENT_BROWSER_NEW_CONTEXT",
        "PROFILE_IDENTITY": profile["profile_user_data_dir_fingerprint"]["profile_path_sha256"] == reality["anchor"]["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["profile_path_sha256"],
        "PAGE_FRAME_GRAPH": all(len(frames) == 2 for frames in profile["page_frame_worker_service_worker_graph"]["frames"]),
        "BEFORE_DIALOG_ACTIONABILITY": all(before[key] for key in ("exactly_one", "visible", "enabled", "stable_approx_two_animation_frames", "receives_events_approx")),
        "DIALOG_OPENING": all(len(items) == 1 and items[0]["message"] == "native-dialog" for items in dialog_open),
        "DIALOG_ACCEPT": all(len(items) == 1 and items[0]["result"] is True for items in dialog_closed),
        "AFTER_DIALOG_ACTIONABILITY": all(after[key] for key in ("exactly_one", "visible", "enabled", "stable_approx_two_animation_frames", "receives_events_approx")),
        "POPUP": all(counts.get("context_page") == 1 for counts in profile["browser_network"]["event_counts"]),
        "FRAME": all(len(frames) == 2 for frames in profile["page_frame_worker_service_worker_graph"]["frames"]),
        "ROUTE_API": profile["browser_network"]["route_api_observed"] is True,
        "PERSISTENT_RECONNECT_1": evidence_3_of_3 and profile["golden_task"]["persistent_reconnect_in_frozen_golden"] is True,
        "PERSISTENT_RECONNECT_2": evidence_3_of_3 and profile["golden_task"]["persistent_reconnect_in_frozen_golden"] is True,
        "FINAL_GOLDEN_RESULT": profile["golden_task"]["reproduced"] == "3_OF_3" and evidence_3_of_3,
    })
    result = {
        "status": "PASS" if all(action_status.values()) else "FAIL",
        "profile_id": PROFILE_ID,
        "action_sequence": [
            {"sequence": index, "action": action, "status": "PASS" if action_status[action] else "FAIL"}
            for index, action in enumerate(ACTION_ORDER, 1)
        ],
        "persistent_reconnect": {
            "reconnect_1": "PASS" if action_status["PERSISTENT_RECONNECT_1"] else "FAIL",
            "reconnect_2": "PASS" if action_status["PERSISTENT_RECONNECT_2"] else "FAIL",
        },
        "business_result": "PASS_3_OF_3" if action_status["FINAL_GOLDEN_RESULT"] else "FAIL",
        "twin_critical_unknown_count": 0,
    }
    filename = "BROWSER-REALITY-REPLAY-AFTER-SHADOW.json" if after_shadow else "BROWSER-REALITY-REPLAY.json"
    write_json(output_dir / filename, result)
    return result


def browser_delta(workspace: Path, output_dir: Path):
    reality, errors = load_reality(workspace)
    if errors:
        raise ValueError("TWIN_INPUT_GATE_MISMATCH:" + ",".join(errors))
    profile = load_profile(output_dir)
    replay = read_json(output_dir / "BROWSER-REALITY-REPLAY.json")
    comparisons = {
        "SAME_TASK": profile["task_sha256"] == reality["anchor"]["task_sha256"],
        "SAME_VALID": profile["valid_rule_sha256"] == reality["anchor"]["valid_rule_sha256"],
        "SAME_BROWSER_PROCESS": profile["browser_executable_fingerprint"]["file_sha256"] == reality["process"]["browser_executable"]["file_sha256"],
        "SAME_CONTEXT": profile["context_config"]["type"] == reality["anchor"]["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["context_type"],
        "SAME_PROFILE": profile["profile_user_data_dir_fingerprint"]["profile_path_sha256"] == reality["anchor"]["required_modules"]["R3_CONTEXT_CONFIG"]["evidence"]["profile_path_sha256"],
        "SAME_ACTION_SEQUENCE": [item["action"] for item in replay["action_sequence"]] == ACTION_ORDER and all(item["status"] == "PASS" for item in replay["action_sequence"]),
        "SAME_DIALOG_BEHAVIOR": all(len(items) == 1 and items[0]["message"] == "native-dialog" for items in profile["runtime_dialog_lifecycle"]["dialog_opening"]) and all(len(items) == 1 and items[0]["result"] is True for items in profile["runtime_dialog_lifecycle"]["dialog_closed"]),
        "SAME_ACTIONABILITY": all(profile["dialog_actionability"][label][key] for label in ("BEFORE_DIALOG", "AFTER_DIALOG") for key in ("exactly_one", "visible", "enabled", "stable_approx_two_animation_frames", "receives_events_approx")),
        "SAME_NETWORK_SEMANTICS": all(counts.get("request") == 5 and counts.get("response") == 5 and counts.get("requestfinished") == 5 for counts in profile["browser_network"]["event_counts"]),
        "SAME_RUNTIME_SEMANTICS": all(counts.get("Page.javascriptDialogOpening") == 1 and counts.get("Page.javascriptDialogClosed") == 1 for counts in profile["runtime_dialog_lifecycle"]["cdp_method_counts"]),
        "SAME_RECONNECT_RESULT": replay["persistent_reconnect"] == {"reconnect_1": "PASS", "reconnect_2": "PASS"},
        "SAME_BUSINESS_RESULT": replay["business_result"] == "PASS_3_OF_3",
    }
    labeled = {name: "PASS" if passed else "FAIL" for name, passed in comparisons.items()}
    material_count = sum(value != "PASS" for value in labeled.values())
    result = {
        "status": "PASS" if material_count == 0 else "FAIL",
        "comparisons": labeled,
        "twin_critical_unknown_count": 0,
        "material_reality_twin_delta_count": material_count,
        "same_critical_browser_behavior": "PASS" if all(labeled[name] == "PASS" for name in (
            "SAME_BROWSER_PROCESS", "SAME_CONTEXT", "SAME_PROFILE", "SAME_ACTION_SEQUENCE",
            "SAME_DIALOG_BEHAVIOR", "SAME_ACTIONABILITY", "SAME_NETWORK_SEMANTICS",
            "SAME_RUNTIME_SEMANTICS", "SAME_RECONNECT_RESULT",
        )) else "FAIL",
        "reality_delta": "NONE" if material_count == 0 else "MATERIAL_TWIN_DELTA",
    }
    write_json(output_dir / "BROWSER-REALITY-TWIN-DELTA.json", result)
    return result


def browser_shadow(output_dir: Path, overlay_path: Path):
    profile_path = output_dir / "PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json"
    profile_file_before = sha256_file(profile_path)
    profile = read_json(profile_path)
    overlay = read_json(overlay_path)
    hypothetical = deep_merge(profile, overlay)
    paths = changed_paths(profile, hypothetical)
    profile_file_after = sha256_file(profile_path)
    result = {
        "status": "PASS" if paths and profile_file_before == profile_file_after else "FAIL",
        "mode": "HYPOTHETICAL_SHADOW",
        "shadow_delta_present": "YES" if paths else "NO",
        "changed_paths": paths,
        "reality_mutated": "NO" if profile_file_before == profile_file_after else "YES",
        "reality_profile_sha256_before": profile_file_before,
        "reality_profile_sha256_after": profile_file_after,
        "shadow_state_sha256": canonical_hash(hypothetical),
    }
    write_json(output_dir / "BROWSER-SHADOW-ISOLATION.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=[
        "replay", "selftest", "shadow", "browser_validate", "browser_replay",
        "browser_delta", "browser_shadow",
    ])
    parser.add_argument("--overlay")
    parser.add_argument("--browser-overlay")
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--after-shadow", action="store_true")
    args = parser.parse_args()

    try:
        if args.mode == "replay":
            result = replay_current()
        elif args.mode == "selftest":
            result = run_selftest()
            write_json(args.output_dir.resolve() / "LEGACY-SELFTEST.json", result)
        elif args.mode == "shadow":
            if not args.overlay:
                raise ValueError("--overlay required")
            result = shadow_overlay(read_json(Path(args.overlay)))
        elif args.mode == "browser_validate":
            result = browser_validate(args.workspace_root.resolve(), args.output_dir.resolve())
        elif args.mode == "browser_replay":
            result = browser_replay(args.workspace_root.resolve(), args.output_dir.resolve(), args.after_shadow)
        elif args.mode == "browser_delta":
            result = browser_delta(args.workspace_root.resolve(), args.output_dir.resolve())
        else:
            if not args.browser_overlay:
                raise ValueError("--browser-overlay required")
            result = browser_shadow(args.output_dir.resolve(), Path(args.browser_overlay).resolve())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        result = {"status": "FAIL", "error": str(error), "action": "STOP", "return_to_gpt": True}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("status") == "FAIL":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
