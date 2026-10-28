#!/usr/bin/env python3
"""Real HTTP soak of the dedicated PM2-managed local Louez server.

Default: 300 seconds, four concurrent clients, one forced child-process kill
after 60 seconds. PM2 must restart the application itself. This script never
invokes start/restart/reload/stop/delete and never dumps PM2 environment data.
Requires Windows for the explicit taskkill fault. No third-party Python modules.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import http.client
from http.cookies import SimpleCookie
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit

APP_NAME = "rental-n001"
RUN_CONTEXT = {}


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_cookie(path):
    if path is None:
        return ""
    raw = path.read_text(encoding="utf-8-sig").strip()
    try:
        value = json.loads(raw)
    except ValueError:
        value = raw
    if isinstance(value, dict):
        value = value.get("cookie", value.get("cookieHeader", value.get("cookies")))
    if isinstance(value, list):
        if all(isinstance(c, dict) and "name" in c and "value" in c for c in value):
            value = "; ".join(f'{c["name"]}={c["value"]}' for c in value)
        elif all(isinstance(c, str) for c in value):
            jar = SimpleCookie()
            for item in value:
                jar.load(item.removeprefix("Set-Cookie:").strip())
            value = "; ".join(f"{name}={morsel.value}" for name, morsel in jar.items())
    if not isinstance(value, str) or not value or "=" not in value:
        raise ValueError("Invalid explicitly supplied test cookie file")
    value = value.removeprefix("Cookie:").strip()
    if "\r" in value or "\n" in value:
        raise ValueError("Cookie header must be a single line")
    return value


def normalized(path):
    return os.path.normcase(os.path.normpath(str(Path(path).resolve())))


class DedicatedPM2:
    def __init__(self, root, node):
        self.root = root.resolve(strict=True)
        self.pm2_home = self.root / "runtime" / "pm2-home"
        self.cli = self.root / "runtime" / "node_modules" / "pm2" / "bin" / "pm2"
        self.server = self.root / "source" / "apps" / "web" / ".next" / "standalone" / "apps" / "web" / "server.js"
        if not self.cli.is_file() or not self.server.is_file():
            raise ValueError("Expected dedicated PM2 CLI or root/source standalone server.js is absent; refusing alternate source")
        # jlist can bootstrap a missing daemon. Require evidence of the already
        # configured dedicated daemon, rather than setting up another runtime.
        if not (self.pm2_home / "pm2.pid").is_file():
            raise ValueError("Dedicated PM2 daemon pid file is absent; no daemon will be started by this test")
        self.node = shutil.which(node)
        if not self.node:
            raise ValueError("Node executable is unavailable")
        self.env = dict(os.environ, PM2_HOME=str(self.pm2_home))

    def state(self):
        result = subprocess.run([self.node, str(self.cli), "jlist"], cwd=str(self.root), env=self.env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
                                encoding="utf-8", errors="replace", shell=False)
        if result.returncode:
            raise RuntimeError(f"Dedicated PM2 jlist failed with exit {result.returncode}; raw environment output withheld")
        try:
            entries = json.loads(result.stdout.strip())
        except ValueError:
            # Some PM2 versions print a version notice ahead of their JSON.
            entries = None
            for position, char in enumerate(result.stdout):
                if char != "[":
                    continue
                try:
                    candidate, _ = json.JSONDecoder().raw_decode(result.stdout[position:])
                    if isinstance(candidate, list):
                        entries = candidate
                        break
                except ValueError:
                    continue
            if entries is None:
                raise RuntimeError("Could not parse dedicated PM2 process list; raw environment output withheld")
        matches = [item for item in entries if item.get("name") == APP_NAME]
        if len(matches) != 1:
            raise RuntimeError("Expected exactly one dedicated rental-n001 PM2 entry")
        item = matches[0]
        details = item.get("pm2_env", {})
        actual = details.get("pm_exec_path")
        if not isinstance(actual, str) or normalized(actual) != normalized(self.server):
            raise RuntimeError("Dedicated app pm_exec_path differs from root/source standalone server.js; fault denied")
        pid = item.get("pid")
        if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
            raise RuntimeError("Dedicated app has no positive child PID")
        return {"name": APP_NAME, "pid": pid, "status": details.get("status"), "server_script": str(self.server)}

    def kill_exact_child_once(self, expected_pid):
        # Resolve the target again immediately before the only mutation.
        current = self.state()
        if current["status"] != "online" or current["pid"] != expected_pid:
            raise RuntimeError("Dedicated child changed before fault; no kill attempted")
        if sys.platform != "win32":
            raise RuntimeError("Windows taskkill is required for this explicit fault")
        completed = subprocess.run(["taskkill.exe", "/PID", str(expected_pid), "/F"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
                                   encoding="utf-8", errors="replace", shell=False)
        if completed.returncode:
            raise RuntimeError(f"The single dedicated child taskkill returned {completed.returncode}; no retry")
        return {"killed_pid": expected_pid, "command": "taskkill /PID <verified-dedicated-child> /F", "exit_code": 0}


class Metrics:
    def __init__(self, base, cookie, order_id, expected_number, timeout):
        self.base = base
        self.cookie = cookie
        self.order_id = order_id
        self.expected_number = expected_number
        self.timeout = timeout
        self.started = time.monotonic()
        self.lock = threading.Lock()
        self.records = []

    def get(self, endpoint, phase):
        path = "/api/health" if endpoint == "health" else "/dashboard/reservations/" + self.order_id
        headers = {"Accept": "application/json" if endpoint == "health" else "text/html"}
        if self.cookie:
            headers["Cookie"] = self.cookie
        connection_class = http.client.HTTPSConnection if self.base.scheme == "https" else http.client.HTTPConnection
        connection = connection_class(self.base.hostname, self.base.port, timeout=self.timeout)
        began = time.monotonic()
        record = {"endpoint": endpoint, "phase": phase, "start_seconds": began - self.started}
        try:
            connection.request("GET", path, headers=headers)
            response = connection.getresponse()
            body = response.read(16 * 1024 * 1024 + 1)
            record["http_status"] = response.status
            if response.status != 200:
                record.update(success=False, failure="http_" + str(response.status))
            elif len(body) > 16 * 1024 * 1024:
                record.update(success=False, failure="response_size_limit")
            elif endpoint == "order" and self.expected_number not in body.decode("utf-8", errors="replace"):
                record.update(success=False, failure="expected_order_number_missing")
            else:
                record.update(success=True)
        except Exception as exc:
            record.update(success=False, failure="connection_" + type(exc).__name__)
        finally:
            connection.close()
        ended = time.monotonic()
        record["end_seconds"] = ended - self.started
        record["latency_ms"] = (ended - began) * 1000
        with self.lock:
            self.records.append(record)
        return record


def percentile(values, fraction):
    values = sorted(values)
    return round(values[min(len(values) - 1, int((len(values) - 1) * fraction))], 3) if values else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base", default="http://localhost:4399")
    parser.add_argument("--node", default="node")
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--fault-at", type=float, default=60)
    parser.add_argument("--recovery-timeout", type=float, default=45)
    parser.add_argument("--request-timeout", type=float, default=10)
    parser.add_argument("--interval", type=float, default=.1)
    parser.add_argument("--order-id")
    parser.add_argument("--expected-order-number")
    parser.add_argument("--cookie-file", type=Path)
    parser.add_argument("--report", type=Path)
    options = parser.parse_args()
    RUN_CONTEXT.update(report_path=str(options.report or options.root / "evidence" / "louez-soak.json"),
                       started_at=utc_now())
    if sys.platform != "win32":
        parser.error("This explicitly authorized process-kill test requires Windows; no test was run")
    if options.seconds < options.fault_at + options.recovery_timeout + 5 or options.fault_at < 1:
        parser.error("--seconds must include the fault time, recovery timeout, and at least five further seconds")
    if not 1 <= options.workers <= 32 or options.interval < 0 or options.request_timeout <= 0:
        parser.error("Invalid worker count, interval or request timeout")
    if bool(options.order_id) != bool(options.expected_order_number) or (options.order_id and not options.cookie_file):
        parser.error("Order checks require --order-id, --expected-order-number and --cookie-file together")
    if options.order_id and not all(char.isalnum() or char in "-_" for char in options.order_id):
        parser.error("Invalid dedicated order ID")
    base = urlsplit(options.base)
    if base.scheme not in ("http", "https") or base.hostname not in ("localhost", "127.0.0.1", "::1") or base.username or base.password:
        parser.error("Only an explicit local loopback base URL is accepted")
    controller = DedicatedPM2(options.root, options.node)
    initial = controller.state()
    if initial["status"] != "online":
        raise RuntimeError("Dedicated application is not online before the test")
    metrics = Metrics(base, read_cookie(options.cookie_file), options.order_id, options.expected_order_number, options.request_timeout)
    RUN_CONTEXT["_metrics"] = metrics
    RUN_CONTEXT["initial_process"] = initial
    run_started_at = utc_now()
    preflight = [metrics.get("health", "preflight")]
    if options.order_id:
        preflight.append(metrics.get("order", "preflight"))
    if any(not item["success"] for item in preflight):
        raise RuntimeError("HTTP preflight failed; no fault was attempted")
    stop = threading.Event()
    workload_started_at = utc_now()
    load_start = time.monotonic()
    deadline = load_start + options.seconds
    failure_at = load_start + options.fault_at
    fault_start = None
    fault_end = None
    fault = {"attempts": 0, "automatic_pm2_recovery": False}
    RUN_CONTEXT["fault"] = fault
    monitoring_errors = []

    def worker(index):
        count = index
        while not stop.is_set():
            endpoint = "order" if options.order_id and count % 2 else "health"
            metrics.get(endpoint, "load")
            count += 1
            stop.wait(options.interval)

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=options.workers)
    try:
        futures = [pool.submit(worker, index) for index in range(options.workers)]
        while time.monotonic() < failure_at:
            stop.wait(min(.2, max(0, failure_at - time.monotonic())))
        current = controller.state()
        if current["status"] != "online":
            raise RuntimeError("Dedicated application is not online at the scheduled fault")
        fault_start = time.monotonic() - metrics.started
        fault["attempts"] = 1
        fault["started_at"] = utc_now()
        fault.update(controller.kill_exact_child_once(current["pid"]))
        recovery_deadline = time.monotonic() + options.recovery_timeout
        stable_health = 0
        new_state = None
        while time.monotonic() < recovery_deadline:
            try:
                observed = controller.state()
                healthy = metrics.get("health", "recovery_probe")["success"]
                if observed["status"] == "online" and observed["pid"] != current["pid"] and healthy:
                    stable_health += 1
                    new_state = observed
                    if stable_health >= 2:
                        break
                else:
                    stable_health = 0
            except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
                stable_health = 0
                monitoring_errors.append({"phase": "recovery", "error_type": type(exc).__name__})
            stop.wait(.25)
        if stable_health >= 2:
            fault_end = time.monotonic() - metrics.started
            fault.update(automatic_pm2_recovery=True, new_pid=new_state["pid"], recovered_at=utc_now(),
                         recovery_ms=round((fault_end - fault_start) * 1000, 3))
        else:
            fault["error"] = "PM2 did not restore a different online PID and two healthy probes before recovery timeout"
        while time.monotonic() < deadline:
            stop.wait(min(.2, max(0, deadline - time.monotonic())))
        stop.set()
        for future in futures:
            future.result(timeout=options.request_timeout + 5)
    finally:
        stop.set()
        pool.shutdown(wait=True, cancel_futures=True)
    load_end = time.monotonic()
    workload_ended_at = utc_now()
    final_state = controller.state()
    final_health = metrics.get("health", "final")
    final_order = metrics.get("order", "final") if options.order_id else None
    all_records = list(metrics.records)
    load_records = [record for record in all_records if record["phase"] in ("load", "recovery_probe")]
    failures = [record for record in load_records if not record["success"]]
    fault_window_end = fault_end if fault_end is not None else float("inf")
    def during_fault(record):
        return fault_start is not None and record["start_seconds"] <= fault_window_end and record["end_seconds"] >= fault_start
    expected_failures = [record for record in failures if during_fault(record)]
    outside_fault_failures = [record for record in failures if not during_fault(record)]
    groups = {}
    for record in load_records:
        name = record["endpoint"] + ":" + ("success" if record["success"] else record["failure"])
        groups[name] = groups.get(name, 0) + 1
    latencies = [record["latency_ms"] for record in load_records]
    success_count = sum(record["success"] for record in load_records)
    recovered = fault.get("automatic_pm2_recovery", False)
    final_online = final_state["status"] == "online" and final_state["pid"] == fault.get("new_pid")
    passed = (recovered and final_online and final_health["success"] and
              (final_order is None or final_order["success"]) and not outside_fault_failures and
              load_end - load_start >= options.seconds)
    report = {"scope": "limited_single_host_soak_and_process_recovery_not_production_high_availability",
              "started_at": run_started_at, "continuous_load_started_at": workload_started_at,
              "continuous_load_ended_at": workload_ended_at, "ended_at": utc_now(),
              "requested_seconds": options.seconds, "actual_continuous_load_seconds": round(load_end - load_start, 3),
              "workers": options.workers, "initial_process": initial, "final_process": final_state,
              "server_script_sha256": hashlib.sha256(controller.server.read_bytes()).hexdigest(),
              "requests": len(load_records), "successes": success_count, "failures": len(failures),
              "overall_success_rate": round(success_count / len(load_records), 6) if load_records else 0,
              "fault_window_failures": len(expected_failures), "outside_fault_window_failures": len(outside_fault_failures),
              "request_groups": groups,
              "latency_ms_all_completed_requests": {"p50": percentile(latencies, .5), "p95": percentile(latencies, .95),
                                                    "max": round(max(latencies), 3) if latencies else None},
              "fault": fault, "monitoring_errors": monitoring_errors,
              "failure_samples": failures[:60], "final_health": final_health,
              "order_number_verified_initially_and_finally": bool(options.order_id and final_order and final_order["success"]),
              "final_order": final_order, "passed_limited_test": passed,
              "limitations": ["One host and one brief deliberate process fault; does not establish production HA",
                              "Fault-window failures remain included in overall success rate",
                              "Application restart is exclusively performed by the already configured PM2 daemon"]}
    target = options.report or controller.root / "evidence" / "louez-soak.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    target.write_text(output, encoding="utf-8")
    print(output)
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        try:
            if RUN_CONTEXT.get("report_path"):
                aborted = {key: value for key, value in RUN_CONTEXT.items() if not key.startswith("_") and key != "report_path"}
                observed = RUN_CONTEXT.get("_metrics")
                if observed is not None:
                    records = list(observed.records)
                    aborted.update(observed_request_count=len(records),
                                   observed_failures=sum(not row["success"] for row in records),
                                   elapsed_seconds=round(time.monotonic() - observed.started, 3))
                aborted.update(ended_at=utc_now(), passed_limited_test=False,
                               interrupted=True, error_type=type(exc).__name__, reason=str(exc))
                target = Path(RUN_CONTEXT["report_path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(aborted, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass
        print("BLOCKED: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
