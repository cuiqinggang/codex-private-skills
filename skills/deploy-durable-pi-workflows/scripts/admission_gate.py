"""Check a frozen long-workflow plan and forward its existing submit command once."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
import sys
from uuid import uuid4
from zipfile import ZipFile


CHECKS = {
    "route_identity": ("approved_entry_mode", "actual_executor_identity"),
    "work_directory": ("resolved_work_directory", "path_budget", "required_output_write"),
    "scheduler_reachability": ("resolved_scheduler_endpoint", "native_read_under_submit_identity"),
    "stage_recovery": ("owned_stage_process", "unknown_effect_reconciliation"),
    "readback_recovery": ("same_run_readback", "stale_observation_handling"),
    "fault_prerequisite": ("required_signoffs", "isolated_fault_target"),
}
INTENT = "ADMISSION-INTENT.json"
PRIOR_MARKERS = (
    INTENT, "SUBMISSION-INTENT.json", "DISPATCH.json", "NATIVE-START.json",
    "STATUS.json", "ATTEMPT-STARTED.json", "OFFICIAL-PI-ACCEPTED.json",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def data(path):
    result = json.loads(path.read_bytes())
    require(isinstance(result, dict), f"{path.name}: expected a JSON object")
    return result


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_hash(path, expected):
    require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected), "Invalid SHA-256")
    require(digest(path) == expected, f"{path.name}: frozen SHA-256 mismatch")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def resolve(root, value, confined=False):
    require(nonempty(value), "Expected a non-empty path")
    path = (root / value).resolve()
    if confined:
        require(path != root and path.is_relative_to(root), "Path leaves the frozen work directory")
    return path


def verify_files(root, plan):
    request = plan["request"]
    request_path = resolve(root, request["path"], confined=True)
    verify_hash(request_path, request["sha256"])
    body = data(request_path)
    require(body.get("task_id") == plan["task_id"] and body.get("scheduler") == plan["scheduler"],
            "Frozen request task or scheduler differs from the admission plan")
    pinned_paths = {request_path}
    for item in plan["inputs"]:
        path = resolve(root, item["path"])
        verify_hash(path, item["sha256"])
        pinned_paths.add(path)
    return pinned_paths


def archive_budget(root, spec, pinned_paths):
    if spec is None:
        return
    archive = resolve(root, spec["archive"])
    destination = resolve(root, spec["destination"], confined=True)
    limit = spec["limit"]
    require(archive in pinned_paths, "Archive must be among the frozen hashed inputs")
    require(type(limit) is int and limit > len(str(destination)), "Invalid extraction path budget")
    with ZipFile(archive) as source:
        for name in source.namelist():
            member = PureWindowsPath(name)
            require(not member.anchor and ".." not in member.parts, "Unsafe archive member path")
            target = destination.joinpath(*member.parts)
            require(len(str(target)) <= limit, "Archive member exceeds the frozen extraction path budget")


def argv(item):
    command = item["argv"]
    require(isinstance(command, list) and command and all(nonempty(part) for part in command),
            "Frozen command must be a non-empty argv array of strings")
    return command


def verify_command_source(root, entry, pinned_paths):
    source = resolve(root, entry["source"])
    require(source in pinned_paths, "Command source is missing from the frozen hashed inputs")
    for argument in argv(entry):
        try:
            if resolve(root, argument) == source:
                return
        except (OSError, ValueError):
            continue
    raise ValueError("Frozen command does not include its declared source as a path argument")


def probe_env(identity):
    return {**os.environ, **{f"ADMISSION_{key.upper()}": value for key, value in identity.items()}}


def validate_probes(entries, scenario):
    kinds = list(CHECKS)
    if scenario == "normal":
        kinds.remove("fault_prerequisite")
    require([entry["kind"] for entry in entries] == kinds,
            "Required probes are missing, duplicated, or out of order")
    for entry in entries:
        allowed = {"read_only", "isolated_scratch"} if entry["kind"] == "work_directory" else {"read_only"}
        require(entry["effect"] in allowed, f'{entry["kind"]}: forbidden probe effect')
        seconds = entry["timeout_seconds"]
        require(type(seconds) is int and seconds > 0, f'{entry["kind"]}: invalid probe timeout')
        argv(entry)


def run_probes(root, entries, identity):
    received = {}
    for entry in entries:
        kind = entry["kind"]
        challenge = uuid4().hex
        bindings = {**identity, "kind": kind, "challenge": challenge, "effect": entry["effect"]}
        try:
            result = subprocess.run(argv(entry), cwd=root, env=probe_env(bindings),
                                    stdin=subprocess.DEVNULL, capture_output=True,
                                    timeout=entry["timeout_seconds"], check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ValueError(f"{kind}: probe could not complete ({type(error).__name__})") from error
        require(result.returncode == 0, f"{kind}: capability probe failed (exit {result.returncode})")
        try:
            proof = json.loads(result.stdout)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"{kind}: probe did not return JSON evidence") from error
        require(isinstance(proof, dict) and all(proof.get(k) == v for k, v in bindings.items()),
                f"{kind}: probe evidence belongs to a different task, identity, directory, or invocation")
        checks = proof.get("checks")
        evidence = proof.get("evidence")
        require(isinstance(checks, dict) and isinstance(evidence, dict), f"{kind}: concrete checks and evidence required")
        recorded = {}
        for item in CHECKS[kind]:
            summary = evidence.get(item)
            require(checks.get(item) is True and nonempty(summary),
                    f"{kind}: {item} was not proved")
            require(len(summary) <= 240 and summary.isprintable(),
                    f"{kind}: {item} needs a short, public-safe evidence summary")
            recorded[item] = summary
        received[kind] = recorded
    return received


def verify_return(result_path, identity, plan):
    result = data(result_path)
    for field in ("task_id", "request_sha256"):
        require(result.get(field) == identity[field], f"Submission result disagrees on {field}")
    require(result.get("scheduler", plan["scheduler"]) == plan["scheduler"], "Submission result disagrees on scheduler")
    if plan["scheduler"] == "temporal":
        require(result.get("workflow_id") == plan["workflow_id"] and nonempty(result.get("run_id")),
                "Temporal result lacks the frozen Workflow ID and actual Run ID")
        return {"workflow_id": result["workflow_id"], "run_id": result["run_id"]}
    require(result.get("workflow_name") == plan["workflow_id"] and nonempty(result.get("workflow_id")),
            "Conductor result lacks the frozen workflow name and actual workflow instance ID")
    return {"workflow_id": result["workflow_id"], "workflow_name": result["workflow_name"]}


def admit(mode, plan_path, pinned_hash):
    root = plan_path.parent
    require(Path.cwd().resolve() == root, "Run from the exact frozen work directory")
    verify_hash(plan_path, pinned_hash)
    plan = data(plan_path)
    require(type(plan["schema_version"]) is int and plan["schema_version"] == 1, "Unsupported admission plan")
    work_directory = Path(plan["work_directory"])
    require(work_directory.is_absolute() and work_directory.resolve() == root,
            "Plan was not frozen for this absolute work directory")
    require(plan["scheduler"] in {"temporal", "conductor"}, "Unknown scheduler")
    require(plan["scenario"] in {"normal", "worker", "scheduler_restart"}, "Unknown workflow scenario")
    require(plan["role"] == "pi_submitter" and all(nonempty(plan[k]) for k in ("route", "task_id", "workflow_id")),
            "Expected a frozen Pi submitter role, route, task, and workflow")
    identity = {k: plan[k] for k in ("task_id", "scheduler", "scenario", "route", "role", "workflow_id")}
    identity = {**identity, "request_sha256": plan["request"]["sha256"], "work_directory": str(root)}
    entries = plan["probes"]
    validate_probes(entries, plan["scenario"])
    submit = plan["submit"]
    result_path = resolve(root, submit["result_file"], confined=True) if submit["result_file"] is not None else None
    submit_argv = argv(submit)
    pinned_paths = verify_files(root, plan)
    for command in (*entries, submit):
        verify_command_source(root, command, pinned_paths)
    prior_markers = {root / name for name in PRIOR_MARKERS}
    if result_path is not None:
        require(result_path not in {plan_path, root / INTENT} | pinned_paths, "Submission result overlaps a frozen file or intent")
        prior_markers.add(result_path)
    require(not any(path.exists() or path.is_symlink() for path in prior_markers), "Prior submission evidence exists; reconcile original run first")
    archive_budget(root, plan.get("archive_path_budget"), pinned_paths)
    evidence = run_probes(root, entries, identity)
    verify_hash(plan_path, pinned_hash)
    verify_files(root, plan)
    checks = [entry["kind"] for entry in entries]
    if mode == "check":
        return {**identity, "state": "PREFLIGHT_PASSED", "checks": checks, "probe_evidence": evidence}

    require(not any(path.exists() or path.is_symlink() for path in prior_markers), "Prior submission evidence exists; reconcile original run first")
    with (root / INTENT).open("x", encoding="utf-8") as stream:
        json.dump({**identity, "plan_sha256": pinned_hash, "checks": checks, "probe_evidence": evidence,
                   "recorded_at": datetime.now(timezone.utc).isoformat(),
                   "state": "SUBMISSION_INTENT"}, stream)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        result = subprocess.run(submit_argv, cwd=root, env=probe_env(identity), stdin=subprocess.DEVNULL,
                                stdout=sys.stderr, stderr=sys.stderr, check=False)
        require(result.returncode == 0, f"Frozen submit command returned exit {result.returncode}")
        if result_path is not None:
            require(result_path.resolve() == result_path, "Submission result path changed after launch")
        reported = verify_return(result_path, identity, plan) if result_path is not None else {}
    except (OSError, ValueError, KeyError) as error:
        return {**identity, "state": "SUBMISSION_UNKNOWN", "reason": str(error)}
    return {**identity, **reported, "state": "SUBMIT_RETURNED", "native_acceptance": "PENDING_INDEPENDENT_READ"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "run"))
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    try:
        result = admit(args.mode, args.plan.resolve(), args.sha256)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"state": "BLOCKED", "reason": str(error)}
    print(json.dumps(result, ensure_ascii=True))
    return int(result["state"] not in {"PREFLIGHT_PASSED", "SUBMIT_RETURNED"})


if __name__ == "__main__":
    raise SystemExit(main())
