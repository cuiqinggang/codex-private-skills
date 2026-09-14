#!/usr/bin/env python3
"""P0 ComfyUI control-path benchmark runner.

Dry-run is the default and never contacts ComfyUI or submits a workload.
Formal execution requires both --execute and --acknowledge-contract P0-CONTROL-V1.
No third-party package is installed by this script. Formal execution uses aiohttp
from the selected existing Python environment.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import struct
import sys
import time
import uuid
import zlib
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

CONTRACT_ID = "P0-CONTROL-V1"
WARMUP_RUNS = 3
MEASURED_RUNS = 20
FIXTURE_NAME = "p0-control-black-256.png"
EXPECTED_SIZE = (256, 256)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_png(data: bytes) -> dict[str, Any]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("invalid PNG signature")
    pos = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    saw_iend = False
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        kind = data[pos + 4 : pos + 8]
        payload_start = pos + 8
        payload_end = payload_start + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            raise ValueError("truncated PNG chunk")
        payload = data[payload_start:payload_end]
        expected_crc = struct.unpack(">I", data[payload_end:crc_end])[0]
        actual_crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"PNG CRC mismatch in {kind!r}")
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
        elif kind == b"IDAT":
            idat.extend(payload)
        elif kind == b"IEND":
            saw_iend = True
            pos = crc_end
            break
        pos = crc_end
    if not saw_iend or width is None or not idat:
        raise ValueError("PNG missing IHDR, IDAT, or IEND")
    if interlace != 0:
        raise ValueError("interlaced PNG is outside P0 contract")
    channels_by_type = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    if color_type not in channels_by_type or bit_depth not in (8, 16):
        raise ValueError("unsupported PNG color format")
    raw = zlib.decompress(bytes(idat))
    row_bits = width * channels_by_type[color_type] * bit_depth
    expected_raw = height * (1 + math.ceil(row_bits / 8))
    if len(raw) != expected_raw:
        raise ValueError(f"incomplete decoded image data: {len(raw)} != {expected_raw}")
    if (width, height) != EXPECTED_SIZE:
        raise ValueError(f"unexpected dimensions: {width}x{height}")
    return {
        "valid_png": True,
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "decoded_bytes": len(raw),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def load_workflow(run_prefix: str) -> dict[str, Any]:
    path = package_root() / "contracts" / "p0-workflow.json"
    workflow = json.loads(path.read_text(encoding="utf-8"))
    if {node["class_type"] for node in workflow.values()} != {"LoadImage", "SaveImage"}:
        raise ValueError("frozen workflow node classes changed")
    if workflow["1"]["inputs"]["image"] != FIXTURE_NAME:
        raise ValueError("frozen workflow input changed")
    if workflow["2"]["inputs"]["filename_prefix"] != "__P0_RUN_PREFIX__":
        raise ValueError("frozen workflow prefix placeholder changed")
    workflow["2"]["inputs"]["filename_prefix"] = run_prefix
    return workflow


def percentile_nearest_rank(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    rank = max(1, math.ceil(percentile * len(ordered)))
    return ordered[rank - 1]


class EventLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = path.open("w", encoding="utf-8", newline="\n")

    def write(self, kind: str, payload: Any) -> None:
        record = {
            "utc": utc_now(),
            "monotonic_ns": time.perf_counter_ns(),
            "kind": kind,
            "payload": payload,
        }
        self.handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        self.handle.flush()

    def close(self) -> None:
        self.handle.close()


async def run_once(
    session: Any,
    endpoint: str,
    client_id: str,
    label: str,
    evidence_dir: Path,
) -> dict[str, Any]:
    run_prefix = f"p0-control/{label}-{uuid.uuid4().hex[:10]}"
    workflow = load_workflow(run_prefix)
    raw_path = evidence_dir / f"{label}-raw-events.jsonl"
    log = EventLog(raw_path)
    prompt_id = None
    marks: dict[str, int] = {}
    output_record: dict[str, Any] | None = None
    try:
        ws_url = endpoint.replace("http://", "ws://").replace("https://", "wss://")
        ws = await session.ws_connect(f"{ws_url}/ws?clientId={client_id}", timeout=10)
        log.write("WS_CONNECTED", {"client_id": client_id})
        marks["REQUEST_START"] = time.perf_counter_ns()
        body = {"prompt": workflow, "client_id": client_id}
        log.write("HTTP_POST_PROMPT", body)
        async with session.post(f"{endpoint}/prompt", json=body) as response:
            response_text = await response.text()
            log.write(
                "HTTP_PROMPT_RESPONSE",
                {"status": response.status, "body": response_text},
            )
            response.raise_for_status()
            prompt_id = json.loads(response_text)["prompt_id"]
        marks["QUEUE_ACK"] = time.perf_counter_ns()

        deadline = time.monotonic() + 120.0
        while time.monotonic() < deadline:
            message = await ws.receive(timeout=10)
            if message.type.name == "TEXT":
                event = json.loads(message.data)
                log.write("WS_TEXT", event)
                data = event.get("data", {})
                event_prompt = data.get("prompt_id")
                if event_prompt != prompt_id:
                    continue
                if event.get("type") == "executing":
                    node = data.get("node")
                    if node is not None and "EXECUTION_START" not in marks:
                        marks["EXECUTION_START"] = time.perf_counter_ns()
                    if node is None:
                        marks.setdefault("SAVE_DONE", time.perf_counter_ns())
                        break
                if event.get("type") == "executed" and str(data.get("node")) == "2":
                    marks["SAVE_DONE"] = time.perf_counter_ns()
                if event.get("type") in {"execution_error", "execution_interrupted"}:
                    raise RuntimeError(f"ComfyUI execution failure: {event}")
            elif message.type.name == "BINARY":
                log.write(
                    "WS_BINARY",
                    {
                        "length": len(message.data),
                        "sha256": hashlib.sha256(message.data).hexdigest(),
                    },
                )
            elif message.type.name in {"CLOSED", "CLOSE", "ERROR"}:
                raise RuntimeError(f"WebSocket ended before completion: {message.type.name}")
        else:
            raise TimeoutError("P0 execution timed out")
        async with session.get(f"{endpoint}/history/{prompt_id}") as response:
            history_text = await response.text()
            log.write("HTTP_HISTORY_RESPONSE", {"status": response.status, "body": history_text})
            response.raise_for_status()
            history = json.loads(history_text)
        entry = history.get(prompt_id)
        if not entry:
            raise ValueError("matching history entry is missing")
        status = entry.get("status", {})
        if status.get("status_str") not in (None, "success") or status.get("completed") is False:
            raise ValueError(f"history did not complete successfully: {status}")
        images = entry.get("outputs", {}).get("2", {}).get("images", [])
        if len(images) != 1:
            raise ValueError(f"expected exactly one new image, got {len(images)}")
        image = images[0]
        params = {
            "filename": image["filename"],
            "subfolder": image.get("subfolder", ""),
            "type": image.get("type", "output"),
        }
        log.write("HTTP_VIEW_REQUEST", params)
        async with session.get(f"{endpoint}/view", params=params) as response:
            png_bytes = await response.read()
            log.write(
                "HTTP_VIEW_RESPONSE",
                {
                    "status": response.status,
                    "length": len(png_bytes),
                    "sha256": hashlib.sha256(png_bytes).hexdigest(),
                },
            )
            response.raise_for_status()
        png_validation = validate_png(png_bytes)
        output_path = evidence_dir / f"{label}-result.png"
        output_path.write_bytes(png_bytes)
        marks.setdefault("SAVE_DONE", time.perf_counter_ns())
        marks["RESULT_READY"] = time.perf_counter_ns()
        await ws.close()
        output_record = {
            "history": image,
            "evidence_copy": str(output_path),
            "validation": png_validation,
        }
    finally:
        log.close()

    required_marks = [
        "REQUEST_START",
        "QUEUE_ACK",
        "EXECUTION_START",
        "SAVE_DONE",
        "RESULT_READY",
    ]
    missing = [name for name in required_marks if name not in marks]
    if missing:
        raise ValueError(f"missing required timing marks: {missing}")

    seconds = lambda start, end: (marks[end] - marks[start]) / 1_000_000_000
    return {
        "label": label,
        "prompt_id": prompt_id,
        "run_prefix": run_prefix,
        "marks_monotonic_ns": marks,
        "timing_seconds": {
            "T_REQUEST": seconds("REQUEST_START", "QUEUE_ACK"),
            "T_QUEUE": seconds("QUEUE_ACK", "EXECUTION_START"),
            "T_EXECUTE": seconds("EXECUTION_START", "SAVE_DONE"),
            "T_RESULT": seconds("SAVE_DONE", "RESULT_READY"),
            "T_END_TO_END": seconds("REQUEST_START", "RESULT_READY"),
        },
        "output": output_record,
        "raw_events": str(raw_path),
        "result_validity_gate": "PASS",
    }


async def execute(args: argparse.Namespace) -> int:
    try:
        import aiohttp
    except ImportError as exc:
        raise RuntimeError(
            "Formal execution requires aiohttp from an existing ComfyUI Python environment; "
            "this tool will not install dependencies."
        ) from exc

    root = Path(args.comfyui_root).resolve()
    if root.drive.upper() != "C:":
        raise ValueError("only a C-drive ComfyUI root is allowed")
    if not (root / "main.py").is_file():
        raise FileNotFoundError("invalid ComfyUI root")
    fixture = package_root() / "assets" / "p0" / "black-256.png"
    fixture_bytes = fixture.read_bytes()
    fixture_validation = validate_png(fixture_bytes)

    run_id = datetime.now(timezone.utc).strftime("p0-%Y%m%dT%H%M%SZ")
    evidence_dir = Path(args.evidence_dir).resolve() if args.evidence_dir else (
        package_root() / "evidence" / "stages" / "P0" / run_id
    )
    if package_root() not in evidence_dir.parents:
        raise ValueError("evidence directory must remain inside the skill package")
    evidence_dir.mkdir(parents=True, exist_ok=False)

    endpoint = args.endpoint.rstrip("/")
    timeout = aiohttp.ClientTimeout(total=150)
    results: list[dict[str, Any]] = []
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{endpoint}/object_info") as response:
            object_info = await response.json()
            if response.status != 200:
                raise RuntimeError(f"object_info returned {response.status}")
        missing_nodes = {"LoadImage", "SaveImage"} - set(object_info)
        if missing_nodes:
            raise RuntimeError(f"P0_BLOCKED_NODE_UNAVAILABLE: {sorted(missing_nodes)}")
        form = aiohttp.FormData()
        form.add_field(
            "image",
            fixture_bytes,
            filename=FIXTURE_NAME,
            content_type="image/png",
        )
        form.add_field("type", "input")
        form.add_field("overwrite", "true")
        async with session.post(f"{endpoint}/upload/image", data=form) as response:
            upload_text = await response.text()
            if response.status != 200:
                raise RuntimeError(f"fixture upload failed: {response.status} {upload_text}")
            upload = json.loads(upload_text)
        if upload.get("name") != FIXTURE_NAME or upload.get("type") != "input":
            raise RuntimeError(f"fixture upload changed the frozen input identity: {upload}")
        (evidence_dir / "fixture-upload-response.json").write_text(
            json.dumps(
                {"response": upload, "fixture_validation": fixture_validation},
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        client_id = str(uuid.uuid4())
        for index in range(WARMUP_RUNS):
            results.append(
                await run_once(session, endpoint, client_id, f"warmup-{index + 1:02d}", evidence_dir)
            )
        for index in range(MEASURED_RUNS):
            results.append(
                await run_once(session, endpoint, client_id, f"measured-{index + 1:02d}", evidence_dir)
            )

    measured = [
        item["timing_seconds"]["T_END_TO_END"]
        for item in results
        if item["label"].startswith("measured-")
    ]
    summary = {
        "schema_version": 1,
        "experiment_id": "MINIMAL_DEFER_WEBSOCKET_CLOSE",
        "contract_id": CONTRACT_ID,
        "generated_at": utc_now(),
        "warmup_runs": WARMUP_RUNS,
        "measured_runs": MEASURED_RUNS,
        "p0_current_seconds": median(measured),
        "statistics_seconds": {
            "MIN": min(measured),
            "P50": median(measured),
            "P95": percentile_nearest_rank(measured, 0.95),
            "MAX": max(measured),
        },
        "result_validity_gate": "PASS",
        "runs": results,
    }
    (evidence_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary["statistics_seconds"], indent=2))
    return 0


def dry_run() -> int:
    fixture = package_root() / "assets" / "p0" / "black-256.png"
    workflow = load_workflow("DRY_RUN_ONLY")
    result = {
        "contract_id": CONTRACT_ID,
        "mode": "DRY_RUN",
        "warmup_runs": WARMUP_RUNS,
        "measured_runs": MEASURED_RUNS,
        "workflow_node_classes": sorted(node["class_type"] for node in workflow.values()),
        "fixture": str(fixture),
        "fixture_validation": validate_png(fixture.read_bytes()),
        "network_contacted": False,
        "workload_submitted": False,
        "p0_benchmark_executed": False,
        "p0_current": "PENDING",
        "status": "P0_TOOLING_DRY_RUN_PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P0 ComfyUI control-path benchmark runner")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="validate locally; submit nothing")
    mode.add_argument("--execute", action="store_true", help="run the frozen 3+20 protocol")
    parser.add_argument("--acknowledge-contract")
    parser.add_argument("--comfyui-root")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8188")
    parser.add_argument("--evidence-dir")
    args = parser.parse_args()
    if not args.execute:
        args.dry_run = True
    if args.execute:
        if args.acknowledge_contract != CONTRACT_ID:
            parser.error(f"--execute requires --acknowledge-contract {CONTRACT_ID}")
        if not args.comfyui_root:
            parser.error("--execute requires --comfyui-root")
    return args


def main() -> int:
    args = parse_args()
    if args.dry_run:
        return dry_run()
    return asyncio.run(execute(args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
