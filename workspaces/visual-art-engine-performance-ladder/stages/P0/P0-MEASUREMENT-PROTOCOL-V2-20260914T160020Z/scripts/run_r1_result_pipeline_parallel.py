#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "run_measurement_v2.py"

def load_base():
    spec = importlib.util.spec_from_file_location("measurement_v2_frozen", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("frozen runner import unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

base = load_base()
baseline_run_once = base.run_once

async def run_once_r1(session, endpoint, wf_path, fixture, outroot, evidence,
                      label, arm, strategy, attempt, artifact, ws_pool, client_ids):
    del fixture, outroot, ws_pool
    effective = "R1_RESULT_PIPELINE_PARALLEL"
    raw_path = evidence / "raw-events" / artifact["raw_event_name"]
    prefix = artifact["run_prefix"]
    if base.label_leak_count(prefix, raw_path.name, artifact):
        raise ValueError("TIMED_PATH_LABEL_LEAK")
    log = base.Log(raw_path, True)
    marks = {}
    prompt_id = None
    ws = None
    post_tasks = []

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

    async def fetch_and_validate(image):
        params = {"filename": image["filename"],
                  "subfolder": image.get("subfolder", ""),
                  "type": image.get("type", "output")}
        if params["type"] != "output":
            raise ValueError("unexpected output type")
        if base.label_leak_count(params):
            raise ValueError("HTTP_LABEL_LEAK")
        mark_once("VIEW_GET_START")
        deadline = time.perf_counter() + 15
        while True:
            async with session.get(f"{endpoint}/view", params=params) as response:
                mark_once("VIEW_HEADERS")
                data = await response.read()
                marks["VIEW_BODY_DONE"] = time.perf_counter_ns()
                if response.status == 200:
                    break
            if time.perf_counter() >= deadline:
                raise TimeoutError("matching new PNG not visible")
            await asyncio.sleep(0)
        marks["PNG_VERIFY_START"] = time.perf_counter_ns()
        validation = base.validate_png(data)
        marks["PNG_VERIFY_DONE"] = time.perf_counter_ns()
        return data, validation, params

    try:
        ws_url = endpoint.replace("http://", "ws://").replace("https://", "wss://")
        ws = await session.ws_connect(f"{ws_url}/ws?clientId={client_ids[arm]}", timeout=10)
        submitted_workflow = base.workflow(wf_path, prefix)
        if base.label_leak_count(submitted_workflow):
            raise ValueError("WORKFLOW_LABEL_LEAK")
        log.write("WS_READY", {"arm": arm, "effective": effective})
        marks["REQUEST_START"] = time.perf_counter_ns()
        async with session.post(
            f"{endpoint}/prompt",
            json={"prompt": submitted_workflow, "client_id": client_ids[arm]},
        ) as response:
            response_text = await response.text()
            log.write("PROMPT_RESPONSE", {"status": response.status, "body": response_text})
            response.raise_for_status()
            prompt_id = json.loads(response_text)["prompt_id"]
        marks["QUEUE_ACK"] = time.perf_counter_ns()

        executed_image = None
        while executed_image is None:
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
        history_task = asyncio.create_task(confirm_history())
        png_task = asyncio.create_task(fetch_and_validate(executed_image))
        post_tasks = [terminal_task, history_task, png_task]
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
            "result_source": "HTTP_VIEW_FROM_EXECUTED_METADATA",
            "same_prompt_equivalence": None, "valid": True, "utc_done": base.utc_now(),
        }
    except Exception as exc:
        for task in post_tasks:
            if not task.done():
                task.cancel()
        if post_tasks:
            await asyncio.gather(*post_tasks, return_exceptions=True)
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
    return await run_once_r1(*args, **kwargs)

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
    args = parser.parse_args()
    if not args.execute or args.acknowledge_protocol != "P0-MEASUREMENT-PROTOCOL-V2":
        parser.error("run requires --execute --acknowledge-protocol P0-MEASUREMENT-PROTOCOL-V2")
    args.strategy = "R1_RESULT_PIPELINE_PARALLEL"
    base.run_once = dispatch
    result = asyncio.run(base.execute(args))
    evidence = Path(args.evidence_dir).resolve()
    result_path = evidence / "paired-results.json"
    summary = json.loads(result_path.read_text(encoding="utf-8"))
    summary["adjudication_mode"] = "SEARCH_ONLY"
    summary["candidate_lock"] = "ON"
    summary["candidate_runner_sha256"] = base.sha_file(Path(__file__))
    summary["frozen_measurement_runner_sha256"] = base.sha_file(BASE_PATH)
    result_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "adjudication_mode": "SEARCH_ONLY", "candidate_lock": "ON",
        "candidate_runner_sha256": summary["candidate_runner_sha256"],
    }, ensure_ascii=False, indent=2))
    return result

if __name__ == "__main__":
    raise SystemExit(main())
