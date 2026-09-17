#!/usr/bin/env python3
"""Codex capacity-aware model routing with durable, replay-safe checkpoints."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable


ACK = "ROUTER_OK"
PROBE_PROMPT = "Reply with exactly: ROUTER_OK"
EFFORT_ORDER = ("none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra")
CAPACITY_MARKERS = ("selected model is at capacity", "server_overloaded")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def classify_error(raw: str) -> str:
    value = raw.casefold()
    if any(marker in value for marker in CAPACITY_MARKERS):
        return "CAPACITY"
    if any(marker in value for marker in ("rate_limit", "rate limit", "too many requests", "429")):
        return "RATE_LIMIT"
    if any(marker in value for marker in ("unauthorized", "authentication", "invalid api key", "401", "403")):
        return "AUTH_ERROR"
    if any(marker in value for marker in ("network", "dns", "connection", "timeout", "timed out", "tls")):
        return "NETWORK_ERROR"
    return "OTHER_ERROR"


def codex_executable() -> str:
    executable = shutil.which("codex")
    if not executable:
        raise RuntimeError("Codex CLI unavailable")
    return executable


def current_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").resolve()


def _levels(model: dict[str, Any]) -> list[str]:
    raw = model.get("supportedReasoningEfforts") or model.get("supported_reasoning_levels") or []
    levels = []
    for entry in raw:
        if isinstance(entry, str):
            levels.append(entry)
        elif isinstance(entry, dict):
            effort = entry.get("reasoningEffort") or entry.get("effort") or entry.get("reasoning_effort")
            if effort:
                levels.append(effort)
    return levels


def lowest_effort(model: dict[str, Any], policy: dict[str, Any]) -> str:
    levels = _levels(model)
    for effort in EFFORT_ORDER:
        if effort in levels:
            return effort
    return policy.get("probe_reasoning_effort", "low")


def _normalized_models(raw: list[dict[str, Any]], source: str) -> list[dict[str, Any]]:
    models = []
    seen = set()
    for entry in raw:
        slug = entry.get("model") or entry.get("slug") or entry.get("id")
        if not isinstance(slug, str) or not slug or slug in seen:
            continue
        if entry.get("hidden") is True or entry.get("visibility") == "hide":
            continue
        seen.add(slug)
        models.append({"model": slug,
                       "priority": entry.get("priority", 9999),
                       "is_default": bool(entry.get("isDefault", False)),
                       "supported_reasoning_levels": _levels(entry),
                       "capability_class": entry.get("capabilityClass") or entry.get("modelSpecialty") or entry.get("capability_class"),
                       "source": source})
    return models


class CodexCatalog:
    def __init__(self, codex_home: Path | None = None, executable: str | None = None):
        self.codex_home = codex_home or current_codex_home()
        self.executable = executable or codex_executable()

    def live(self, timeout: float = 20) -> list[dict[str, Any]]:
        proc = subprocess.Popen([self.executable, "app-server", "--stdio"],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, encoding="utf-8",
                                errors="replace")
        responses: queue.Queue[dict[str, Any]] = queue.Queue()
        errors: list[str] = []

        def read_stdout() -> None:
            assert proc.stdout is not None
            for line in proc.stdout:
                try:
                    responses.put(json.loads(line))
                except json.JSONDecodeError:
                    pass

        def read_stderr() -> None:
            assert proc.stderr is not None
            for line in proc.stderr:
                if len(errors) < 20:
                    errors.append(line.rstrip())

        threading.Thread(target=read_stdout, daemon=True).start()
        threading.Thread(target=read_stderr, daemon=True).start()

        def send(message: dict[str, Any]) -> None:
            assert proc.stdin is not None
            proc.stdin.write(json.dumps(message) + "\n")
            proc.stdin.flush()

        def response_for(request_id: int) -> dict[str, Any]:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if proc.poll() is not None and responses.empty():
                    raise RuntimeError("app-server exited before model/list response")
                try:
                    message = responses.get(timeout=min(.2, max(.01, deadline - time.monotonic())))
                except queue.Empty:
                    continue
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError("app-server model/list rejected")
                    return message.get("result") or {}
            raise TimeoutError("app-server model/list timed out")

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "codex-capacity-aware-model-router", "version": "1.0.0"}}})
            response_for(1)
            send({"method": "initialized", "params": {}})
            cursor = None
            models: list[dict[str, Any]] = []
            page = 0
            while True:
                page += 1
                params: dict[str, Any] = {"includeHidden": False}
                if cursor:
                    params["cursor"] = cursor
                send({"id": page + 1, "method": "model/list", "params": params})
                response = response_for(page + 1)
                models.extend(response.get("data") or [])
                next_cursor = response.get("nextCursor")
                if not next_cursor:
                    break
                if next_cursor == cursor:
                    raise RuntimeError("model/list pagination cursor did not advance")
                cursor = next_cursor
            normalized = _normalized_models(models, "codex_app_server_model_list")
            if not normalized:
                raise RuntimeError("app-server returned no visible models")
            return normalized
        finally:
            if proc.poll() is None:
                proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

    def cache(self) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        path = self.codex_home / "models_cache.json"
        payload = read_json(path, {})
        models = _normalized_models(payload.get("models") or [], "codex_home_models_cache")
        if not models:
            raise RuntimeError("models_cache.json has no visible models")
        return models, {"cache_path": str(path), "cache_fetched_at": payload.get("fetched_at"),
                        "cache_mtime": dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(),
                        "cache_age_seconds": max(0, time.time() - path.stat().st_mtime)}

    def discover(self) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        timestamp = utc_now()
        try:
            models = self.live()
            return models, {"model_discovery_source": "codex_app_server_model_list",
                            "model_discovery_timestamp": timestamp,
                            "model_candidate_count": len(models)}
        except Exception as exc:
            models, metadata = self.cache()
            return models, {"model_discovery_source": "codex_home_models_cache",
                            "model_discovery_timestamp": timestamp,
                            "model_candidate_count": len(models),
                            "live_catalog_error_class": type(exc).__name__, **metadata}


def ordered_candidates(models: list[dict[str, Any]], requested: str | None,
                       policy: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    denied = set(policy.get("denied_models") or [])
    minimum = policy.get("min_capability_class")
    eligible = [m for m in models if m["model"] not in denied and
                (minimum is None or m.get("capability_class") == minimum)]
    if not eligible:
        raise RuntimeError("no eligible models in current catalog")
    by_name = {m["model"]: m for m in eligible}
    if requested is None:
        requested = next((m["model"] for m in eligible if m.get("is_default")), eligible[0]["model"])
    if requested not in by_name:
        raise RuntimeError("requested model absent or denied in current catalog")
    requested_priority = by_name[requested].get("priority")
    requested_class = by_name[requested].get("capability_class")
    preferred = [m for name in policy.get("preferred_models") or []
                 if (m := by_name.get(name)) is not None]
    remaining = sorted(eligible, key=lambda m: (
        m["model"] != requested,
        m.get("capability_class") != requested_class,
        m not in preferred,
        preferred.index(m) if m in preferred else 9999,
        abs((m.get("priority") or 9999) - (requested_priority or 9999)),
        m.get("priority") or 9999,
        m["model"],
    ))
    return requested, remaining


def probe_model(model: dict[str, Any], policy: dict[str, Any], neutral_workdir: Path) -> str:
    neutral_workdir.mkdir(parents=True, exist_ok=True)
    effort = lowest_effort(model, policy)
    cmd = [codex_executable(), "exec", "--ephemeral", "--skip-git-repo-check",
           "--sandbox", "read-only", "--json", "-C", str(neutral_workdir),
           "-m", model["model"], "-c", f"model_reasoning_effort={effort}",
           PROBE_PROMPT]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=policy.get("probe_timeout_seconds", 90),
                                check=False)
    except subprocess.TimeoutExpired:
        return "NETWORK_ERROR"
    except OSError:
        return "OTHER_ERROR"
    messages = []
    for line in result.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        if item.get("type") == "agent_message":
            messages.append((item.get("text") or "").strip())
    if result.returncode == 0 and messages and messages[-1] == ACK:
        return "PASS"
    return classify_error(result.stdout + "\n" + result.stderr)


class Router:
    def __init__(self, root: Path, policy: dict[str, Any],
                 discover: Callable[[], tuple[list[dict[str, Any]], dict[str, Any]]],
                 probe: Callable[[dict[str, Any], dict[str, Any], Path], str],
                 now: Callable[[], float] = time.time):
        self.root = root
        self.policy = policy
        self.discover = discover
        self.probe = probe
        self.now = now
        self.state_dir = root / "state"
        self.logs_dir = root / "logs"
        self.router_path = self.state_dir / "router-state.json"
        self.health_path = self.state_dir / "model-health.json"
        self.checkpoint_path = self.state_dir / "checkpoint.json"
        self.events_path = self.logs_dir / "route-events.jsonl"

    def event(self, payload: dict[str, Any]) -> None:
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        event = {"timestamp": utc_now(), **payload,
                 "REQUESTED_MODEL": payload.get("requested_model", "UNKNOWN"),
                 "ACTUAL_MODEL": payload.get("actual_model", "UNKNOWN"),
                 "FALLBACK_REASON": payload.get("fallback_reason", "NONE"),
                 "ERROR_CLASS": payload.get("error_class", "NONE"),
                 "PROBE_RESULT": payload.get("probe_result", "UNKNOWN"),
                 "TIMESTAMP": utc_now()}
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def save_result(self, result: dict[str, Any]) -> None:
        for upper, lower, fallback in (
            ("REQUESTED_MODEL", "requested_model", "UNKNOWN"),
            ("ACTUAL_MODEL", "actual_model", "UNKNOWN"),
            ("FALLBACK_REASON", "fallback_reason", "NONE"),
            ("ERROR_CLASS", "error_class", "NONE"),
            ("PROBE_RESULT", "probe_result", "UNKNOWN"),
            ("TASK_ID", "task_id", "UNKNOWN"),
            ("THREAD_ID", "thread_id", "UNKNOWN"),
            ("CHECKPOINT_PATH", "checkpoint_path", "UNKNOWN"),
            ("LOCAL_WORK_REPLAY", "local_work_replay", False),
        ):
            result[upper] = result.get(lower, fallback)
        discovery = result.get("model_discovery") or {}
        result["MODEL_DISCOVERY_SOURCE"] = discovery.get("model_discovery_source", "UNKNOWN")
        result["MODEL_DISCOVERY_TIMESTAMP"] = discovery.get("model_discovery_timestamp")
        result["MODEL_CANDIDATE_COUNT"] = discovery.get("model_candidate_count")
        write_json(self.router_path, result)

    def checkpoint(self, task: dict[str, Any], blocker: str | None = None) -> dict[str, Any]:
        previous = read_json(self.checkpoint_path, {})
        value = {**previous, **task}
        value.setdefault("completed_steps", [])
        value.setdefault("do_not_repeat", [])
        value.setdefault("artifact_paths", [])
        value["local_work_replay"] = False
        if blocker:
            value["current_blocker"] = blocker
            value["task_state"] = "CHECKPOINTED"
        value["updated_at"] = utc_now()
        write_json(self.checkpoint_path, value)
        return value

    def route(self, task: dict[str, Any], requested_model: str | None = None,
              observed_capacity_model: str | None = None) -> dict[str, Any]:
        state = read_json(self.router_path, {})
        checkpoint = self.checkpoint(task, "REMOTE_MODEL_CAPACITY" if observed_capacity_model else None)
        now = self.now()
        if state.get("router_state") == "ALL_MODELS_CAPACITY" and now < state.get("next_health_check_epoch", 0):
            state["task_state"] = "CHECKPOINTED"
            state["local_work_replay"] = False
            self.save_result(state)
            return state
        health = read_json(self.health_path, {"models": {}})
        if observed_capacity_model:
            health["models"][observed_capacity_model] = {
                "status": "CAPACITY", "checked_at": utc_now(),
                "cooldown_until_epoch": now + self.policy["capacity_cooldown_seconds"]}
            write_json(self.health_path, health)
        try:
            models, discovery = self.discover()
            requested, candidates = ordered_candidates(models, requested_model, self.policy)
        except Exception as exc:
            result = {"router_state": "MODEL_DISCOVERY_UNKNOWN", "task_state": "CHECKPOINTED",
                      "requested_model": requested_model or "UNKNOWN", "actual_model": "UNKNOWN",
                      "error_class": type(exc).__name__, "local_work_replay": False,
                      "checkpoint_path": str(self.checkpoint_path)}
            self.save_result(result)
            self.checkpoint(task, "MODEL_DISCOVERY_UNKNOWN")
            return result

        results = []
        fallback_reason = "CAPACITY" if observed_capacity_model else "NONE"
        for candidate in candidates:
            model_name = candidate["model"]
            record = health["models"].get(model_name, {})
            if record.get("status") == "CAPACITY" and now < record.get("cooldown_until_epoch", 0):
                probe_result = "CAPACITY_COOLDOWN"
                error_class = "CAPACITY"
            else:
                probe_result = self.probe(candidate, self.policy, self.root / "probe")
                error_class = "NONE" if probe_result == "PASS" else probe_result
                health["models"][model_name] = {
                    "status": probe_result, "checked_at": utc_now(),
                    "cooldown_until_epoch": now + self.policy["capacity_cooldown_seconds"]
                    if probe_result == "CAPACITY" else 0}
                write_json(self.health_path, health)
            results.append({"model": model_name, "probe_result": probe_result,
                            "error_class": error_class,
                            "probe_reasoning_effort": lowest_effort(candidate, self.policy)})
            self.event({"requested_model": requested, "actual_model": model_name if probe_result == "PASS" else "UNKNOWN",
                        "fallback_reason": fallback_reason, "error_class": error_class,
                        "probe_result": probe_result, "task_id": task.get("task_id"),
                        "thread_id": checkpoint.get("thread_id"),
                        "continuation_thread_id": checkpoint.get("continuation_thread_id"),
                        "checkpoint_path": str(self.checkpoint_path)})
            if probe_result == "PASS":
                selected_state = ("PRIMARY_SELECTED" if model_name == requested else
                                  "THIRD_SELECTED" if len(results) == 3 else "FALLBACK_SELECTED")
                result = {"router_state": selected_state,
                          "task_state": "CHECKPOINTED" if checkpoint.get("task_state") == "CHECKPOINTED" else "READY",
                          "requested_model": requested, "actual_model": model_name,
                          "fallback_reason": fallback_reason if model_name == requested else "CAPACITY",
                          "error_class": "NONE", "probe_result": "PASS",
                          "model_discovery": discovery, "probe_results": results,
                          "task_id": task.get("task_id"), "thread_id": checkpoint.get("thread_id"),
                          "checkpoint_path": str(self.checkpoint_path),
                          "local_work_replay": False, "updated_at": utc_now()}
                self.save_result(result)
                self.checkpoint({**task, "requested_model": requested,
                                 "actual_model": model_name, "fallback_reason": result["fallback_reason"]})
                return result
            if error_class != "CAPACITY":
                result = {"router_state": "BLOCKED_" + error_class,
                          "task_state": "CHECKPOINTED", "requested_model": requested,
                          "actual_model": "UNKNOWN", "fallback_reason": fallback_reason,
                          "error_class": error_class, "probe_result": probe_result,
                          "model_discovery": discovery, "probe_results": results,
                          "task_id": task.get("task_id"),
                          "checkpoint_path": str(self.checkpoint_path),
                          "local_work_replay": False, "updated_at": utc_now()}
                self.save_result(result)
                self.checkpoint(task, error_class)
                return result
            fallback_reason = "CAPACITY"

        result = {"router_state": "ALL_MODELS_CAPACITY", "task_state": "CHECKPOINTED",
                  "requested_model": requested, "actual_model": "UNKNOWN",
                  "fallback_reason": "ALL_CANDIDATES_CAPACITY", "error_class": "CAPACITY",
                  "probe_result": "CAPACITY", "model_discovery": discovery,
                  "probe_results": results, "task_id": task.get("task_id"),
                  "checkpoint_path": str(self.checkpoint_path),
                  "next_health_check_epoch": now + self.policy["all_models_recheck_seconds"],
                  "local_work_replay": False, "updated_at": utc_now()}
        self.save_result(result)
        self.checkpoint(task, "BLOCKED_REMOTE_CAPACITY")
        return result


def handoff_prompt(checkpoint: dict[str, Any], model: str) -> str:
    if not checkpoint.get("next_action"):
        raise RuntimeError("checkpoint has no NEXT_ACTION; cannot safely resume")
    keys = ("task_id", "workdir", "branch", "last_remote_head", "completed_steps",
            "do_not_repeat", "current_blocker", "next_action", "artifact_paths",
            "requested_model", "previous_actual_model")
    payload = {key.upper(): checkpoint.get(key) for key in keys}
    payload.update({"NEW_ACTUAL_MODEL": model, "FALLBACK_REASON": "CAPACITY",
                    "LOCAL_WORK_REPLAY": "NO"})
    return ("Continue the same logical task from this checkpoint. Do not repeat completed local work.\n"
            + json.dumps(payload, ensure_ascii=False, indent=2))


def _thread_id_from_json(stdout: str) -> str | None:
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            return event.get("thread_id")
    return None


def continue_task(router: Router, task: dict[str, Any], requested_model: str | None = None,
                  runner: Callable[[list[str], Path], tuple[int, str, str]] | None = None) -> dict[str, Any]:
    """Route and continue a checkpointed task; never re-run local steps itself."""
    checkpoint = router.checkpoint(task)
    if not checkpoint.get("next_action"):
        raise RuntimeError("NEXT_ACTION is required before continuing")
    def real_runner(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", check=False)
        return result.returncode, result.stdout, result.stderr
    run = runner or real_runner
    observed_capacity = None
    while True:
        route = router.route(checkpoint, requested_model, observed_capacity)
        if route.get("probe_result") != "PASS":
            return route
        model = route["actual_model"]
        prompt = handoff_prompt(checkpoint, model)
        workdir = Path(checkpoint.get("workdir") or router.root)
        thread_id = checkpoint.get("thread_id")
        if thread_id:
            cmd = [codex_executable(), "exec", "resume", "--json", "-m", model,
                   thread_id, prompt]
        else:
            cmd = [codex_executable(), "exec", "--json", "-C", str(workdir),
                   "--skip-git-repo-check", "-m", model, prompt]
        code, stdout, stderr = run(cmd, workdir)
        if code != 0 and thread_id and any(marker in (stdout + "\n" + stderr).casefold()
                                            for marker in ("model switch unsupported", "cannot switch model on resume", "resume model change unsupported")):
            # Continue from the checkpoint in a new thread, never from the original task prompt.
            cmd = [codex_executable(), "exec", "--json", "-C", str(workdir),
                   "--skip-git-repo-check", "-m", model, prompt]
            code, stdout, stderr = run(cmd, workdir)
            if code == 0:
                checkpoint["continuation_thread_id"] = _thread_id_from_json(stdout)
        if code == 0:
            new_thread = _thread_id_from_json(stdout)
            router.checkpoint({**checkpoint, "actual_model": model,
                               "thread_id": new_thread or thread_id,
                               "continuation_thread_id": checkpoint.get("continuation_thread_id"),
                               "task_state": "CONTINUED"})
            route["task_state"] = "CONTINUED"
            route["thread_id"] = new_thread or thread_id
            router.save_result(route)
            return route
        error_class = classify_error(stdout + "\n" + stderr)
        if error_class != "CAPACITY":
            router.checkpoint(checkpoint, error_class)
            route["router_state"] = "BLOCKED_" + error_class
            route["task_state"] = "CHECKPOINTED"
            router.save_result(route)
            return route
        router.checkpoint(checkpoint, "REMOTE_MODEL_CAPACITY")
        observed_capacity = model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Codex capacity-aware model router")
    parser.add_argument("command", choices=("discover", "route", "continue", "status", "checkpoint"))
    script_parent = Path(__file__).resolve().parent
    default_root = script_parent.parent if script_parent.name == "scripts" else script_parent
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--task-file", type=Path)
    parser.add_argument("--requested-model")
    parser.add_argument("--observed-capacity-model")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    policy_path = args.policy or root / "router-policy.json"
    policy = read_json(policy_path, {})
    catalog = CodexCatalog()
    router = Router(root, policy, catalog.discover, probe_model)
    if args.command == "discover":
        try:
            models, metadata = catalog.discover()
            result = {**metadata, "models": [m["model"] for m in models]}
        except Exception as exc:
            result = {"model_discovery_source": "UNKNOWN", "error_class": type(exc).__name__}
    elif args.command == "status":
        result = read_json(router.router_path, {"router_state": "NOT_ROUTED"})
    else:
        task = read_json(args.task_file, {}) if args.task_file else read_json(router.checkpoint_path, {})
        if args.command == "checkpoint":
            result = router.checkpoint(task)
        elif args.command == "continue":
            result = continue_task(router, task, args.requested_model)
        else:
            result = router.route(task, args.requested_model, args.observed_capacity_model)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("router_state") not in ("MODEL_DISCOVERY_UNKNOWN", "ALL_MODELS_CAPACITY") else 2


if __name__ == "__main__":
    sys.exit(main())
