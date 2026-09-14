#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
R1_PATH = HERE / "run_r1_result_pipeline_parallel.py"

def load_r1():
    spec = importlib.util.spec_from_file_location("r1_search_runner", R1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("R1 runner import unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

r1 = load_r1()
base = r1.base
baseline_run_once = r1.baseline_run_once
TRIGGER_ON_SUCCESS = False
HISTORY_THEN_LOCAL = False
LOCAL_THEN_HISTORY = False

def short_artifact_identity(strategy, attempt, nonce):
    del strategy
    phase = "w" if attempt < 0 else "m"
    token = f"{phase}{abs(attempt):03d}-{nonce}"
    return {
        "token": token,
        "run_prefix": f"p/{token}",
        "raw_event_name": f"{token}.jsonl",
        "output_copy_name": f"{token}.png",
        "history_name": f"{token}.json",
        "equivalence_name": f"{token}.png",
    }

async def run_once_r2(session, endpoint, wf_path, fixture, outroot, evidence,
                      label, arm, strategy, attempt, artifact, ws_pool, client_ids):
    del fixture, ws_pool
    effective = "R2_EXECUTED_LOCAL_PARALLEL_V2"
    raw_path = evidence / "raw-events" / artifact["raw_event_name"]
    prefix = artifact["run_prefix"]
    if base.label_leak_count(prefix, raw_path.name, artifact):
        raise ValueError("TIMED_PATH_LABEL_LEAK")
    log = base.Log(raw_path, True)
    marks = {}
    prompt_id = None
    ws = None
    tasks = []

    def mark_once(name):
        marks.setdefault(name, time.perf_counter_ns())

    async def collect_terminal_events():
        while True:
            msg = await ws.receive(timeout=15)
            if msg.type.name == "TEXT":
                event = json.loads(msg.data)
                log.write("WS_TEXT", event)
                payload = event.get("data", {})
                if payload.get("prompt_id") != prompt_id:
                    continue
                kind = event.get("type")
                if kind == "execution_success":
                    mark_once("EXECUTION_SUCCESS")
                elif kind == "executing" and payload.get("node") is None:
                    mark_once("EXECUTING_NONE")
                    return
                elif kind in {"execution_error", "execution_interrupted"}:
                    raise RuntimeError(str(event))
            elif msg.type.name in {"CLOSED", "CLOSE", "ERROR"}:
                raise RuntimeError("websocket ended early")

    async def confirm_history():
        mark_once("HISTORY_GET_START")
        deadline = time.perf_counter() + 15
        while True:
            async with session.get(f"{endpoint}/history/{prompt_id}") as response:
                mark_once("HISTORY_HEADERS")
                body = await response.text()
                marks["HISTORY_BODY_DONE"] = time.perf_counter_ns()
                response.raise_for_status()
            history = json.loads(body)
            entry = history.get(prompt_id)
            status = entry.get("status", {}) if entry else {}
            if entry and status.get("completed") is True:
                if status.get("status_str") != "success":
                    raise ValueError("matching history completed without success")
                images = entry.get("outputs", {}).get("2", {}).get("images", [])
                if len(images) != 1:
                    raise ValueError("not exactly one output")
                return body, entry, images[0]
            if time.perf_counter() >= deadline:
                raise TimeoutError("matching explicitly successful history missing")
            await asyncio.sleep(0)

    async def read_and_validate_local(image):
        params = {"filename": image["filename"],
                  "subfolder": image.get("subfolder", ""),
                  "type": image.get("type", "output")}
        if params["type"] != "output":
            raise ValueError("unexpected output type")
        if base.label_leak_count(params):
            raise ValueError("HTTP_LABEL_LEAK")
        candidate = (outroot / params["subfolder"] / Path(params["filename"]).name).resolve()
        if not candidate.is_relative_to(outroot.resolve()):
            raise ValueError("output path escape")
        marks["LOCAL_READ_START"] = time.perf_counter_ns()
        deadline = time.perf_counter() + 15
        while True:
            try:
                data = candidate.read_bytes()
                break
            except FileNotFoundError:
                if time.perf_counter() >= deadline:
                    raise TimeoutError("matching local PNG not visible")
                await asyncio.sleep(0)
        marks["LOCAL_READ_DONE"] = time.perf_counter_ns()
        marks["PNG_VERIFY_START"] = time.perf_counter_ns()
        validation = base.validate_png(data)
        marks["PNG_VERIFY_DONE"] = time.perf_counter_ns()
        return data, validation, params

    try:
        ws_url = endpoint.replace("http://", "ws://").replace("https://", "wss://")
        ws = await session.ws_connect(f"{ws_url}/ws?clientId={client_ids[arm]}", timeout=10)
        submitted = base.workflow(wf_path, prefix)
        if base.label_leak_count(submitted):
            raise ValueError("WORKFLOW_LABEL_LEAK")
        log.write("WS_READY", {"arm": arm, "effective": effective})
        marks["REQUEST_START"] = time.perf_counter_ns()
        async with session.post(
            f"{endpoint}/prompt", json={"prompt": submitted, "client_id": client_ids[arm]}
        ) as response:
            response_text = await response.text()
            log.write("PROMPT_RESPONSE", {"status": response.status, "body": response_text})
            response.raise_for_status()
            prompt_id = json.loads(response_text)["prompt_id"]
        marks["QUEUE_ACK"] = time.perf_counter_ns()

        executed_image = None
        while executed_image is None or (
            TRIGGER_ON_SUCCESS and "EXECUTION_SUCCESS" not in marks
        ):
            msg = await ws.receive(timeout=15)
            if msg.type.name == "TEXT":
                event = json.loads(msg.data)
                log.write("WS_TEXT", event)
                payload = event.get("data", {})
                if payload.get("prompt_id") != prompt_id:
                    continue
                kind = event.get("type")
                if kind == "executing" and payload.get("node") is not None:
                    mark_once("EXECUTION_START")
                elif kind == "execution_success":
                    mark_once("EXECUTION_SUCCESS")
                elif kind == "executing" and payload.get("node") is None:
                    mark_once("EXECUTING_NONE")
                elif kind in {"execution_error", "execution_interrupted"}:
                    raise RuntimeError(str(event))
                if kind == "executed" and str(payload.get("node")) == "2":
                    marks["SAVE_DONE"] = time.perf_counter_ns()
                    images = payload.get("output", {}).get("images", [])
                    if len(images) != 1:
                        raise ValueError("executed event did not contain exactly one output")
                    executed_image = images[0]
            elif msg.type.name in {"CLOSED", "CLOSE", "ERROR"}:
                raise RuntimeError("websocket ended before SaveImage output")

        terminal_task = asyncio.create_task(collect_terminal_events())
        if LOCAL_THEN_HISTORY:
            png_task = asyncio.create_task(read_and_validate_local(executed_image))
            tasks = [terminal_task, png_task]
            png_bytes, validation, params = await png_task
            history_task = asyncio.create_task(confirm_history())
            tasks.append(history_task)
            history_raw, entry, history_image = await history_task
        elif HISTORY_THEN_LOCAL:
            history_task = asyncio.create_task(confirm_history())
            tasks = [terminal_task, history_task]
            history_raw, entry, history_image = await history_task
            png_task = asyncio.create_task(read_and_validate_local(executed_image))
            tasks.append(png_task)
            png_bytes, validation, params = await png_task
        else:
            history_task = asyncio.create_task(confirm_history())
            png_task = asyncio.create_task(read_and_validate_local(executed_image))
            tasks = [terminal_task, history_task, png_task]
            (history_raw, entry, history_image), (png_bytes, validation, params) = (
                await asyncio.gather(history_task, png_task)
            )
        history_params = {"filename": history_image["filename"],
                          "subfolder": history_image.get("subfolder", ""),
                          "type": history_image.get("type", "output")}
        if history_params != params:
            raise ValueError("executed output does not match successful history output")
        entry_sha = base.sha_bytes(
            json.dumps(entry, sort_keys=True, separators=(",", ":")).encode()
        )
        log.write("HISTORY_CONFIRMED", {
            "http_status": 200, "prompt_id": prompt_id, "completed": True,
            "status_str": "success", "output_count": 1, "entry_sha256": entry_sha,
        })
        marks["RESULT_READY"] = time.perf_counter_ns()

        history_path = evidence / "history" / artifact["history_name"]
        history_path.write_text(history_raw, encoding="utf-8")
        copy_path = evidence / "outputs" / artifact["output_copy_name"]
        marks["EVIDENCE_COPY_START"] = time.perf_counter_ns()
        copy_path.write_bytes(png_bytes)
        marks["EVIDENCE_COPY_DONE"] = time.perf_counter_ns()
        await terminal_task
        await ws.close()
        ws = None
        marks["EQUIVALENCE_VIEW_START"] = time.perf_counter_ns()
        async with session.get(f"{endpoint}/view", params=params) as response:
            http_bytes = await response.read()
            response.raise_for_status()
        marks["EQUIVALENCE_VIEW_DONE"] = time.perf_counter_ns()
        equivalence = {
            "local_sha256": base.sha_bytes(png_bytes),
            "http_sha256": base.sha_bytes(http_bytes),
            "bytes_equal": png_bytes == http_bytes,
        }
        if not equivalence["bytes_equal"]:
            raise ValueError("HTTP/local equivalence failed")
        (evidence / "equivalence-http" / artifact["equivalence_name"]).write_bytes(http_bytes)
        return {
            "attempt": attempt, "label": label, "arm": arm,
            "run_token": artifact["token"], "effective_strategy": effective,
            "prompt_id": prompt_id, "run_prefix": prefix,
            "marks_monotonic_ns": marks,
            "t_ms": (marks["RESULT_READY"] - marks["REQUEST_START"]) / 1e6,
            "history": {
                "exact_prompt_id_match": True, "completed": True,
                "status_str": "success", "output_count": 1,
                "raw_snapshot": str(history_path),
                "raw_sha256": base.sha_bytes(history_raw.encode("utf-8")),
                "entry_sha256": entry_sha,
            },
            "output_identity": history_image, "validation": validation,
            "result_source": "LOCAL_EXECUTED_AND_HISTORY_BOUND",
            "same_prompt_equivalence": equivalence,
            "valid": True, "utc_done": base.utc_now(),
        }
    except Exception as exc:
        for task in tasks:
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        return {
            "attempt": attempt, "label": label, "arm": arm,
            "effective_strategy": effective, "prompt_id": prompt_id,
            "marks_monotonic_ns": marks, "valid": False,
            "error": repr(exc), "utc_done": base.utc_now(),
        }
    finally:
        if ws is not None:
            await ws.close()
        log.close()

async def dispatch(*args, **kwargs):
    arm = args[7] if len(args) > 7 else kwargs["arm"]
    if arm == "A":
        return await baseline_run_once(*args, **kwargs)
    return await run_once_r2(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge-protocol")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--design", choices=["PAIRED"], default="PAIRED")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8188")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--evidence-dir", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--order-seed", type=int, required=True)
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--blocks", type=int, default=20)
    parser.add_argument(
        "--trigger", choices=["executed", "execution_success"], default="executed"
    )
    parser.add_argument(
        "--io-mode",
        choices=["parallel", "history_then_local", "local_then_history"],
        default="parallel",
    )
    parser.add_argument("--short-output-prefix", action="store_true")
    args = parser.parse_args()
    if not args.execute or args.acknowledge_protocol != "P0-MEASUREMENT-PROTOCOL-V2":
        parser.error("run requires --execute --acknowledge-protocol P0-MEASUREMENT-PROTOCOL-V2")
    global TRIGGER_ON_SUCCESS, HISTORY_THEN_LOCAL, LOCAL_THEN_HISTORY
    TRIGGER_ON_SUCCESS = args.trigger == "execution_success"
    HISTORY_THEN_LOCAL = args.io_mode == "history_then_local"
    LOCAL_THEN_HISTORY = args.io_mode == "local_then_history"
    if TRIGGER_ON_SUCCESS and LOCAL_THEN_HISTORY:
        args.strategy = "R6_SUCCESS_LOCAL_HISTORY_V2"
    elif TRIGGER_ON_SUCCESS and HISTORY_THEN_LOCAL:
        args.strategy = (
            "R5_SHORT_SUCCESS_HISTORY_LOCAL_V2"
            if args.short_output_prefix
            else "R4_SUCCESS_HISTORY_LOCAL_V2"
        )
    elif TRIGGER_ON_SUCCESS:
        args.strategy = "R3_SUCCESS_LOCAL_PARALLEL_V2"
    else:
        args.strategy = "R2_EXECUTED_LOCAL_PARALLEL_V2"
    if args.short_output_prefix:
        base.artifact_identity = short_artifact_identity
    base.run_once = dispatch
    result = asyncio.run(base.execute(args))
    evidence = Path(args.evidence_dir).resolve()
    result_path = evidence / "paired-results.json"
    summary = json.loads(result_path.read_text(encoding="utf-8"))
    summary["contract_id"] = "P0-CONTROL-V2-CANDIDATE"
    summary["adjudication_mode"] = "SEARCH_ONLY"
    summary["candidate_lock"] = "ON"
    summary["candidate_runner_sha256"] = base.sha_file(Path(__file__))
    summary["frozen_measurement_runner_sha256"] = base.sha_file(Path(base.__file__))
    result_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "contract_id": summary["contract_id"], "adjudication_mode": "SEARCH_ONLY",
        "candidate_lock": "ON",
        "candidate_runner_sha256": summary["candidate_runner_sha256"],
    }, ensure_ascii=False, indent=2))
    return result

if __name__ == "__main__":
    raise SystemExit(main())
