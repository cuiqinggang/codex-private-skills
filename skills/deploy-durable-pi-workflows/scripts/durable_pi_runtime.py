"""Temporal adapter for a frozen Pi job and independently verified receipt."""

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import timedelta
from uuid import uuid4

if sdk_path := os.environ.get("DURABLE_PI_TEMPORAL_SDK_PATH"):
    sys.path.insert(0, sdk_path)

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy, WorkflowIDReusePolicy
from temporalio.exceptions import ApplicationError, WorkflowAlreadyStartedError
from temporalio.service import RPCError, RPCStatusCode
from temporalio.worker import UnsandboxedWorkflowRunner, Worker


ACTIVITY = "durable_pi_execute"
HEARTBEAT_TIMEOUT = timedelta(seconds=10)
MAXIMUM_ATTEMPTS = 2
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")


def read_bytes(path):
    return path.read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def contained(root, path):
    if not isinstance(path, str) or not path:
        raise ValueError("Expected a nonempty job path")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"Path outside the job: {path}")
    return resolved


def write_json_once(path, value):
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # Hard-link the completed temporary file to publish it without overwriting
        # a receipt another process already committed for this job.
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def command_array(value):
    if not isinstance(value, list) or not value or not all(
        isinstance(argument, str) and argument and "\0" not in argument for argument in value
    ):
        raise ValueError("Entry point must be a nonempty argument array")
    return value


class Job:
    def __init__(self, directory, workflow_id):
        self.root = directory.resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Job path is not a directory")
        self.request_path = self.root / "request.json"
        raw = read_bytes(self.request_path)
        self.request_sha256 = digest(raw)
        self.request = json.loads(raw)
        self.task_id = self.request["task_id"]
        if not isinstance(self.task_id, str) or not TASK_ID.fullmatch(self.task_id):
            raise ValueError("Invalid task ID")
        self.workflow_id = workflow_id or f"durable-pi-{self.task_id}"
        if not TASK_ID.fullmatch(self.workflow_id) and self.workflow_id != f"durable-pi-{self.task_id}":
            raise ValueError("Invalid Workflow ID")
        self.queue = f"durable-pi-{self.task_id}"
        self.entrypoint = command_array(self.request["entrypoint"])
        self.resume_entrypoint = self.request.get("resume_entrypoint")
        self.resume_preflight = self.request.get("resume_preflight")
        if self.resume_entrypoint is not None or self.resume_preflight is not None:
            command_array(self.resume_entrypoint)
            command_array(self.resume_preflight)
        self.cwd = contained(self.root, self.request.get("cwd", "."))
        if not self.cwd.is_dir():
            raise ValueError("Entry point directory does not exist")
        self.receipt = contained(self.cwd, self.request["receipt"])
        self.attempt_record = self.root / "ATTEMPT-STARTED.json"
        self.resume_record = self.root / "RESUME-STARTED.json"
        self.commit_record = self.root / "ACTIVITY-COMMITTED.json"
        self.dispatch = self.root / "DISPATCH.json"
        self.control_records = {self.request_path, self.attempt_record, self.resume_record, self.commit_record, self.dispatch}
        if self.receipt in self.control_records:
            raise ValueError("Receipt path overlaps Temporal control records")

    @property
    def identity(self):
        return {"task_id": self.task_id, "request_sha256": self.request_sha256}

    def verify_request(self, identity):
        if identity != self.identity or file_digest(self.request_path) != self.request_sha256:
            raise ValueError("Frozen Pi request identity or bytes changed")

    def verify_child_receipt(self):
        raw = read_bytes(self.receipt)
        proof = json.loads(raw)
        if proof.get("task_id") != self.task_id or proof.get("status") != "PASS":
            raise ValueError("Child did not produce a matching PASS receipt")
        artifacts = proof.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError("Child receipt must name independently verified artifacts")
        seen = set()
        for artifact in artifacts:
            path = contained(self.cwd, artifact["path"])
            sha = artifact["sha256"]
            if path in seen or path in self.control_records or path == self.receipt:
                raise ValueError("Artifact path is duplicated or overlaps control records")
            if not isinstance(sha, str) or not SHA256.fullmatch(sha) or file_digest(path) != sha:
                raise ValueError("Artifact hash disagrees with child receipt")
            seen.add(path)
        return digest(raw), len(seen)


@workflow.defn(name="DurablePiJob")
class DurablePiJob:
    @workflow.run
    async def run(self, identity: dict) -> dict:
        return await workflow.execute_activity(
            ACTIVITY,
            identity,
            start_to_close_timeout=timedelta(days=1),
            heartbeat_timeout=HEARTBEAT_TIMEOUT,
            retry_policy=RetryPolicy(maximum_attempts=MAXIMUM_ATTEMPTS),
        )


class JobActivity:
    def __init__(self, job):
        self.job = job

    def read_committed(self, identity, info):
        job = self.job
        committed = json.loads(read_bytes(job.commit_record))
        receipt_sha256, artifact_count = job.verify_child_receipt()
        expected = {**identity, "workflow_id": info.workflow_id, "run_id": info.workflow_run_id,
                    "activity_id": info.activity_id, "receipt_sha256": receipt_sha256,
                    "artifact_count": artifact_count}
        if committed != expected:
            raise ValueError("Committed receipt binding or fingerprint changed")
        return {**committed, "reused_verified_result": True}

    async def verify_while_heartbeating(self, operation, identity):
        verification = asyncio.create_task(asyncio.to_thread(operation))
        while not verification.done():
            activity.heartbeat({"stage": "verifying", **identity})
            await asyncio.wait((verification,), timeout=1)
        return await verification

    async def wait_process(self, process, identity, stage):
        try:
            while process.returncode is None:
                activity.heartbeat({"stage": stage, **identity})
                await asyncio.sleep(1)
        finally:
            if process.returncode is None:
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
            await process.wait()
        return process.returncode

    async def resume_plan(self, binding, identity):
        job = self.job
        if not job.resume_entrypoint or not job.attempt_record.is_file() or job.resume_record.exists():
            raise ValueError("No verified commit or eligible resume recipe; reconcile the original job")
        if json.loads(read_bytes(job.attempt_record)) != binding:
            raise ValueError("The original Pi attempt did not belong to this Activity")
        # This is a separately registered read-only business check. It is responsible for
        # establishing the old executor is stopped and every prior effect is accounted for.
        environment = {**os.environ, "DURABLE_PI_TASK_ID": job.task_id,
                       "DURABLE_PI_REQUEST_SHA256": job.request_sha256}
        preflight_path = job.root / "RESUME-PREFLIGHT.json"
        with preflight_path.open("xb") as output, (job.root / "resume-preflight.log").open("xb") as error:
            process = await asyncio.create_subprocess_exec(*job.resume_preflight, cwd=job.cwd, env=environment,
                stdin=subprocess.DEVNULL, stdout=output, stderr=error)
            if await self.wait_process(process, identity, "reconciling") != 0:
                raise ValueError("Independent read-only reconciliation did not authorize resume")
        proof = json.loads(read_bytes(preflight_path))
        if proof.get("status") != "RESUME_SAFE" or any(proof.get(key) != value for key, value in identity.items()):
            raise ValueError("Independent resume proof does not match this job")
        session_id = proof.get("session_id")
        if not isinstance(session_id, str) or not TASK_ID.fullmatch(session_id):
            raise ValueError("Independent resume proof did not name the original session")
        checkpoint = contained(job.cwd, proof["checkpoint"])
        if checkpoint in job.control_records or checkpoint == job.receipt:
            raise ValueError("Independent resume proof must name a business checkpoint")
        sha = proof["checkpoint_sha256"]
        if not isinstance(sha, str) or not SHA256.fullmatch(sha):
            raise ValueError("Independent resume proof did not provide a valid checkpoint digest")
        if await self.verify_while_heartbeating(lambda: file_digest(checkpoint), identity) != sha:
            raise ValueError("Original checkpoint fingerprint disagrees with independent resume proof")
        job.verify_request(identity)
        write_json_once(job.resume_record, {**binding, "session_id": session_id,
                        "checkpoint": str(checkpoint), "checkpoint_sha256": sha})
        environment.update(DURABLE_PI_RESUME_SESSION_ID=session_id, DURABLE_PI_RESUME_CHECKPOINT=str(checkpoint))
        return job.resume_entrypoint, environment

    @activity.defn(name=ACTIVITY)
    async def execute(self, identity: dict) -> dict:
        info = activity.info()
        job = self.job
        try:
            if (info.heartbeat_timeout != HEARTBEAT_TIMEOUT or info.retry_policy is None
                    or info.retry_policy.maximum_attempts != MAXIMUM_ATTEMPTS):
                raise ValueError("Temporal did not schedule the required heartbeat and retry policy")
            if info.workflow_id != job.workflow_id:
                raise ValueError("Workflow ID disagrees with the assigned job")
            job.verify_request(identity)
            if job.commit_record.exists():
                committed = await self.verify_while_heartbeating(lambda: self.read_committed(identity, info), identity)
                activity.heartbeat({"stage": "verified", **identity, "receipt_sha256": committed["receipt_sha256"]})
                return committed
            binding = {**identity, "workflow_id": info.workflow_id,
                       "run_id": info.workflow_run_id, "activity_id": info.activity_id}
            if info.attempt == 1 and not job.attempt_record.exists() and not job.receipt.exists():
                write_json_once(job.attempt_record, binding)
                argv, environment, log_name, stage = job.entrypoint, None, "pi.log", "executing"
            elif info.attempt == 2 and not job.receipt.exists():
                argv, environment = await self.resume_plan(binding, identity)
                log_name, stage = "pi-resume.log", "resuming"
            else:
                raise ValueError("No verified commit record; reconcile the original job before any resume")
            activity.heartbeat({"stage": stage, **identity})
            with (job.root / log_name).open("xb") as log:
                process = await asyncio.create_subprocess_exec(
                    *argv, cwd=job.cwd, env=environment, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                )
                if await self.wait_process(process, identity, stage) != 0:
                    raise ValueError(f"Pi command exited with code {process.returncode}; reconcile original state")
            job.verify_request(identity)
            receipt_sha256, artifact_count = await self.verify_while_heartbeating(job.verify_child_receipt, identity)
            committed = {**binding, "receipt_sha256": receipt_sha256, "artifact_count": artifact_count}
            write_json_once(job.commit_record, committed)
            activity.heartbeat({"stage": "verified", **identity, "receipt_sha256": receipt_sha256})
            return {**committed, "reused_verified_result": False}
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise ApplicationError(str(error), type="PiJobNeedsReconciliation", non_retryable=True) from error


async def verify_workflow_binding(client, handle, job):
    history = await handle.fetch_history()
    start = history.events[0].workflow_execution_started_event_attributes
    if start.workflow_type.name != "DurablePiJob":
        raise ValueError("Existing Workflow has a different type")
    inputs = await client.data_converter.decode(start.input.payloads)
    if inputs != [job.identity]:
        raise ValueError("Existing Workflow belongs to a different frozen request")


def prior_dispatch(job):
    if not job.dispatch.exists():
        return None
    recorded = json.loads(read_bytes(job.dispatch))
    expected = {**job.identity, "workflow_id": job.workflow_id, "task_queue": job.queue}
    if {key: recorded.get(key) for key in expected} != expected or not recorded.get("run_id"):
        raise ValueError("Persisted dispatch identifies a different frozen request")
    return recorded


async def submit(client, job):
    job.verify_request(job.identity)
    recorded = prior_dispatch(job)
    if recorded:
        handle = client.get_workflow_handle(job.workflow_id, run_id=recorded["run_id"])
    elif job.attempt_record.exists() or job.commit_record.exists() or job.receipt.exists():
        # An attempted job with missing dispatch must be reconciled by identity.
        # Never create it in a new/empty Temporal namespace.
        handle = client.get_workflow_handle(job.workflow_id)
    else:
        try:
            handle = await client.start_workflow(DurablePiJob.run, job.identity, id=job.workflow_id,
                                                 task_queue=job.queue, id_reuse_policy=WorkflowIDReusePolicy.REJECT_DUPLICATE)
        except WorkflowAlreadyStartedError:
            handle = client.get_workflow_handle(job.workflow_id)
    description = await handle.describe()
    handle = client.get_workflow_handle(job.workflow_id, run_id=description.run_id)
    await verify_workflow_binding(client, handle, job)
    receipt = {**job.identity, "workflow_id": job.workflow_id, "run_id": description.run_id,
               "task_queue": job.queue}
    if not job.dispatch.exists():
        try:
            write_json_once(job.dispatch, receipt)
        except FileExistsError:
            pass
    if json.loads(read_bytes(job.dispatch)) != receipt:
        raise ValueError("Persisted dispatch identifies a different run")
    return {**receipt, "status": description.status.name}


async def status(client, job):
    recorded = prior_dispatch(job)
    handle = client.get_workflow_handle(job.workflow_id, run_id=recorded["run_id"] if recorded else None)
    try:
        observed = await handle.describe()
    except RPCError as error:
        if error.status != RPCStatusCode.NOT_FOUND or recorded:
            raise
        return {**job.identity, "workflow_id": job.workflow_id, "status": "NOT_FOUND"}
    handle = client.get_workflow_handle(job.workflow_id, run_id=observed.run_id)
    await verify_workflow_binding(client, handle, job)
    pending = [{"activity_id": item.activity_id, "attempt": item.attempt, "maximum_attempts": item.maximum_attempts,
                "last_heartbeat_utc": item.last_heartbeat_time.ToJsonString()
                if item.HasField("last_heartbeat_time") else None}
               for item in observed.raw_description.pending_activities]
    history = await handle.fetch_history()
    scheduled = [event.activity_task_scheduled_event_attributes for event in history.events
                 if event.HasField("activity_task_scheduled_event_attributes")]
    attempts = [event.activity_task_started_event_attributes.attempt for event in history.events
                if event.HasField("activity_task_started_event_attributes")]
    result = {**job.identity, "workflow_id": job.workflow_id, "run_id": observed.run_id,
              "status": observed.status.name, "pending_activities": pending,
              "heartbeat_timeout_seconds": scheduled[0].heartbeat_timeout.seconds if scheduled else None,
              "activity_attempts_in_history": attempts}
    if observed.status.name == "COMPLETED":
        result["result"] = await handle.result()
    return result


async def main(args):
    job = Job(args.job, args.workflow_id)
    client = await Client.connect(args.address)
    if args.mode == "worker":
        runner = JobActivity(job)
        async with Worker(client, task_queue=job.queue, workflows=[DurablePiJob], activities=[runner.execute],
                          workflow_runner=UnsandboxedWorkflowRunner()):
            await asyncio.Event().wait()
        return
    result = await (submit(client, job) if args.mode == "submit" else status(client, job))
    print(json.dumps(result, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--address", required=True)
    parser.add_argument("--job", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("submit", "worker", "status"))
    parser.add_argument("--workflow-id")
    asyncio.run(main(parser.parse_args()))
