"""Windows enhanced Pi entry for a frozen, durable local job."""

import argparse
from contextlib import contextmanager
from hashlib import sha256
import json
import msvcrt
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import psutil


RUNTIME = Path(__file__).with_name("durable_pi_runtime.py")
WORKSPACE = Path.home() / "Documents" / "DurablePi"
CLI = Path(os.environ.get("DURABLE_PI_TEMPORAL_CLI_PATH") or WORKSPACE / "runtime/temporal/temporal.exe")
SDK = Path(os.environ.get("DURABLE_PI_TEMPORAL_SDK_PATH") or WORKSPACE / "runtime/temporal-sdk")
ACTIVE = Path(os.environ["LOCALAPPDATA"]) / "EnhancedPi/durable-active"
APPROVED = ACTIVE.with_name("durable-approved")
TERMINAL = {"COMPLETED", "FAILED", "CANCELED", "TERMINATED", "CONTINUED_AS_NEW", "TIMED_OUT"}


def read_json(path):
    return json.loads(path.read_bytes())


def job_key(job):
    return sha256(str(job).casefold().encode()).hexdigest()


def approval_record(job):
    raw = (job / "request.json").read_bytes()
    request = json.loads(raw)
    if "entrypoint" not in request:
        raise ValueError("Missing frozen entrypoint")
    commands = [request[name] for name in ("entrypoint", "resume_preflight", "resume_entrypoint")
                if name in request]
    pinned = {}
    for command in commands:
        if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
            raise ValueError("Expected frozen command argument arrays")
        program = Path(command[0])
        if not program.is_absolute() or not program.is_file():
            raise ValueError("Executable must be a fixed absolute file")
        pinned[str(program.resolve())] = sha256(program.read_bytes()).hexdigest()
        cwd = job / request.get("cwd", ".")
        for argument in command[1:]:
            path = cwd / argument
            if path.is_file() and path.suffix.casefold() in {".py", ".ps1", ".bat", ".cmd", ".exe", ".js", ".vbs"}:
                pinned[str(path.resolve())] = sha256(path.read_bytes()).hexdigest()
    return {"job": str(job), "request_sha256": sha256(raw).hexdigest(), "programs_sha256": pinned}


def store(path, value):
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


@contextmanager
def exclusive_job(job):
    with (job / "SUPERVISOR.lock").open("a+b") as lock:
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise SystemExit("This job already has a supervisor. Use status.") from error
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def new_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def runtime_args(job, address, mode):
    return [sys.executable, "-B", "-X", "utf8", str(RUNTIME),
            "--address", address, "--job", str(job), "--mode", mode]


def call_runtime(job, address, mode, env):
    completed = subprocess.run(runtime_args(job, address, mode), env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                               timeout=20)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "Temporal request failed")
    return json.loads(completed.stdout)


def process_identity(process):
    if process is None:
        return None
    try:
        return {"pid": process.pid, "created": psutil.Process(process.pid).create_time()}
    except psutil.NoSuchProcess:
        return None


def check_previous_processes(job):
    path = job / "LOCAL-PROCESSES.json"
    if not path.is_file():
        return
    previous = read_json(path)
    for name in ("service", "worker"):
        record = previous.get(name)
        if not record:
            continue
        try:
            if psutil.Process(record["pid"]).create_time() == record["created"]:
                raise RuntimeError(f"Prior {name} is still running for this task. Reconcile it before reattaching.")
        except psutil.NoSuchProcess:
            continue


def stop(process):
    if process is not None and process.poll() is None:
        process.terminate()
        process.wait()


def supervise(job, env):
    if not (job / "request.json").is_file() or not CLI.is_file() or not SDK.is_dir():
        raise SystemExit("Missing request.json or installed Windows Temporal runtime")
    database = job / "temporal.sqlite"
    dispatch = job / "DISPATCH.json"
    status_file = job / "STATUS.json"
    if (dispatch.is_file() or (job / "ATTEMPT-STARTED.json").exists()) and not database.is_file():
        raise SystemExit("Original Temporal database is missing; preserve the job and reconcile")
    previous = read_json(status_file) if status_file.is_file() else {}
    if previous.get("status") in TERMINAL:
        print(json.dumps(previous, ensure_ascii=True), flush=True)
        return 0 if previous["status"] == "COMPLETED" else 1
    check_previous_processes(job)
    port = new_port()
    address = f"127.0.0.1:{port}"
    server = worker = None
    with (job / "temporal.log").open("ab") as server_log, (job / "worker.log").open("ab") as worker_log:
        try:
            def record_processes():
                store(job / "LOCAL-PROCESSES.json", {
                    "service_pid": server.pid, "worker_pid": worker.pid if worker else None,
                    "service": process_identity(server), "worker": process_identity(worker),
                    "address": address, "supervisor_pid": os.getpid()})

            def start_server():
                return subprocess.Popen(
                    [str(CLI), "server", "start-dev", "--ip", "127.0.0.1", "--port", str(port),
                     "--headless", "--db-filename", str(database)],
                    stdin=subprocess.DEVNULL, stdout=server_log, stderr=server_log, env=env,
                )

            def wait_for_service(mode):
                for _ in range(45):
                    if server.poll() is not None:
                        raise RuntimeError("Temporal service exited during startup. See temporal.log")
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=1):
                            pass
                        return call_runtime(job, address, mode, env)
                    except (OSError, subprocess.TimeoutExpired):
                        time.sleep(.5)
                    except RuntimeError as error:
                        if ("Namespace default is not found" not in str(error)
                                and "Connection" not in str(error) and "UNAVAILABLE" not in str(error)):
                            raise
                        time.sleep(.5)
                raise RuntimeError("Temporal service or namespace never became ready")

            server = start_server()
            record_processes()
            wait_for_service("submit")
            observed = wait_for_service("status")
            store(status_file, observed)
            print(json.dumps(observed, ensure_ascii=True), flush=True)
            worker_starts = 0
            server_restarts = 0
            while True:
                if observed["status"] in TERMINAL:
                    print(json.dumps(observed, ensure_ascii=True), flush=True)
                    return 0 if observed["status"] == "COMPLETED" else 1
                if server.poll() is not None:
                    if server_restarts == 1:
                        raise RuntimeError("Temporal service exited twice; inspect the original job")
                    server = start_server()
                    server_restarts += 1
                    record_processes()
                    observed = wait_for_service("status")
                    store(status_file, observed)
                    if observed["status"] in TERMINAL:
                        continue
                if worker is None or worker.poll() is not None:
                    if worker_starts == 2:
                        raise RuntimeError("Worker did not remain available; inspect worker.log and resume this job")
                    worker = subprocess.Popen(runtime_args(job, address, "worker"), env=env,
                                              stdin=subprocess.DEVNULL, stdout=worker_log, stderr=worker_log)
                    worker_starts += 1
                    record_processes()
                time.sleep(2)
                try:
                    observed = call_runtime(job, address, "status", env)
                except (OSError, subprocess.TimeoutExpired):
                    continue
                except RuntimeError as error:
                    if server.poll() is not None or "Connection" in str(error):
                        continue
                    raise
                if observed["status"] == "NOT_FOUND":
                    raise RuntimeError("Original workflow is unavailable in its database")
                store(status_file, observed)
        finally:
            stop(worker)
            stop(server)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("approve", "run", "status", "resume", "resume-pending"))
    parser.add_argument("job", type=Path, nargs="?")
    args = parser.parse_args()
    if args.command == "resume-pending":
        return resume_pending()
    if args.job is None:
        parser.error("Task directory required")
    job = args.job.resolve(strict=True)
    if not job.is_dir():
        parser.error("Task directory required")
    if args.command == "status":
        snapshot = job / "STATUS.json"
        previous = read_json(snapshot) if snapshot.is_file() else {"status": "NOT_OBSERVED"}
        print(json.dumps({**previous, "source": "last_native_observation"}, ensure_ascii=True), flush=True)
        return 0
    if args.command == "resume" and not (job / "temporal.sqlite").is_file():
        parser.error("resume needs the original Temporal database")
    record = approval_record(job)
    approval = APPROVED / f"{job_key(job)}.json"
    if args.command == "approve":
        APPROVED.mkdir(parents=True, exist_ok=True)
        if approval.exists() and read_json(approval) != record:
            parser.error("The approved manifest changed. Use a new job identity.")
        store(approval, record)
        print(json.dumps(record, ensure_ascii=True), flush=True)
        return 0
    if not approval.is_file() or read_json(approval) != record:
        parser.error("Use the trusted Windows Pi entry to approve this frozen job before execution")
    with exclusive_job(job):
        env = os.environ.copy()
        env["DURABLE_PI_TEMPORAL_SDK_PATH"] = str(SDK)
        ACTIVE.mkdir(parents=True, exist_ok=True)
        marker = ACTIVE / f"{job_key(job)}.json"
        request_hash = record["request_sha256"]
        if marker.is_file() and read_json(marker) != {"job": str(job), "request_sha256": request_hash}:
            raise SystemExit("Original pending request was modified")
        store(marker, {"job": str(job), "request_sha256": request_hash})
        try:
            return supervise(job, env)
        finally:
            snapshot = job / "STATUS.json"
            if snapshot.is_file() and read_json(snapshot).get("status") in TERMINAL:
                marker.unlink(missing_ok=True)


def resume_pending():
    for marker in sorted(ACTIVE.glob("*.json")):
        try:
            record = read_json(marker)
            job = Path(record["job"])
            if not job.is_dir() or not (job / "temporal.sqlite").is_file():
                continue
            if sha256((job / "request.json").read_bytes()).hexdigest() != record["request_sha256"]:
                raise ValueError("Original pending request was modified")
            snapshot = job / "STATUS.json"
            if snapshot.is_file() and read_json(snapshot).get("status") in TERMINAL:
                marker.unlink(missing_ok=True)
                continue
            with (job / "login-recovery.log").open("ab") as log:
                subprocess.Popen(
                    [sys.executable, "-B", "-X", "utf8", str(Path(__file__)), "resume", str(job)],
                    stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
        except (OSError, ValueError, KeyError) as error:
            print(f"{marker.name}: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
