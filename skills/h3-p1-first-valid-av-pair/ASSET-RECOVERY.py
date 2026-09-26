"""H3-P1 v1.0.0: exact-path, read-only source recovery; NEVER generates media."""
import hashlib
import json
import os
import re
import stat
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
SCOPE = "H3_P1_ASSET_RECOVERY_ONLY"
MAX_TEXT_BYTES = 2 * 1024 * 1024
OUTPUT_ROOT = r"C:\AI\H3-P1-Acceptance\v1.0.0"
ASSETS = (
    ("parent_skill", r"C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\SKILL.md", "text", None),
    ("quality_sop", r"C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\references\H3-05-QUALITY-GATE-SOP.md", "text", None),
    ("failure_review", r"C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\FAILURE_REVIEW.md", "text", None),
    ("factory_sop", r"C:\Users\A\.codex\skills\h3-high-fidelity-local-video-recreation\references\AI-FILM-FACTORY-IMPLEMENTATION-SOP-V2.md", "text", None),
    ("canonical_workflow", r"C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json", "json", "89b6a40b13485a6633191f1350db472556359cdb6407e5272c9ed109698fd0f5"),
    ("diffusion_model", r"C:\AI\MiniMax-H3\ComfyUI\models\diffusion_models\minimax_h3_fl2va_pruned_int8_convrot.safetensors", "metadata", None),
    ("text_encoder", r"C:\AI\MiniMax-H3\ComfyUI\models\text_encoders\qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "metadata", None),
    ("video_vae", r"C:\AI\MiniMax-H3\ComfyUI\models\vae\minimax_h3_video_vae_fp16.safetensors", "metadata", None),
    ("existing_python", r"C:\AI\MiniMax-H3\.venv\Scripts\python.exe", "metadata", None),
)
SECRET_PATTERN = re.compile(
    r"sk-[A-Za-z0-9_-]{16,}|(?:authorization\s*[:=]\s*['\"]?\s*bearer\s+)\S+|"
    r"(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"\r\n]{16,}['\"]",
    re.IGNORECASE,
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def inspect_asset(asset, fixture_root=None):
    key, original, kind, expected = asset
    path = Path(original) if fixture_root is None else Path(fixture_root) / key
    result = {"id": key, "declared_path": original, "kind": kind, "status": "UNKNOWN"}
    try:
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            return dict(result, status="NOT_REGULAR_FILE")
        result.update(bytes=before.st_size, mtime_ns=before.st_mtime_ns)
        if before.st_size == 0:
            return dict(result, status="EMPTY")
        if kind == "metadata":
            return dict(result, status="PRESENT_METADATA_ONLY", content_verified=False)
        if before.st_size > MAX_TEXT_BYTES:
            return dict(result, status="TOO_LARGE")
        with path.open("rb") as handle:
            raw = handle.read(MAX_TEXT_BYTES + 1)
        after = path.stat()
        if len(raw) > MAX_TEXT_BYTES:
            return dict(result, status="TOO_LARGE")
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            return dict(result, status="CHANGED_DURING_READ")
        result["sha256"] = sha256(raw)
        text = raw.decode("utf-8-sig")
        if SECRET_PATTERN.search(text):
            return dict(result, status="POTENTIAL_SECRET_CONTENT_OMITTED")
        if kind == "json":
            graph = json.loads(text)
            if not isinstance(graph, dict) or not graph:
                return dict(result, status="INVALID_GRAPH")
            result["node_classes"] = sorted({str(v.get("class_type")) for v in graph.values() if isinstance(v, dict) and v.get("class_type")})
        result["content"] = text
        result["content_sha256"] = sha256(text.encode("utf-8"))
        result["status"] = "HASH_MISMATCH" if expected and expected.lower() != result["sha256"] else "READ_OK"
        return result
    except FileNotFoundError:
        return dict(result, status="MISSING")
    except PermissionError:
        return dict(result, status="ACCESS_DENIED")
    except UnicodeError:
        return dict(result, status="INVALID_UTF8")
    except json.JSONDecodeError:
        return dict(result, status="INVALID_JSON")
    except OSError as error:
        return dict(result, status="READ_ERROR", error_type=type(error).__name__)


def run_verifier(snapshot):
    """Integrity/scope verifier only, NOT an image/audio semantic verifier."""
    if not isinstance(snapshot, dict) or snapshot.get("scope") != SCOPE:
        return False
    if snapshot.get("version") != VERSION or snapshot.get("context") not in ("GPT_FIXTURE", "WINDOWS_REAL_ASSET_RECOVERY"):
        return False
    if snapshot.get("p1_virtual_complete") is not False or type(snapshot.get("p1_real_generation_runs")) is not int or snapshot["p1_real_generation_runs"] != 0:
        return False
    if snapshot.get("p1_t_valid_ms") is not None:
        return False
    records = snapshot.get("assets")
    if not isinstance(records, list) or len(records) != len(ASSETS):
        return False
    for asset, record in zip(ASSETS, records):
        if not isinstance(record, dict) or record.get("id") != asset[0] or record.get("declared_path") != asset[1] or record.get("kind") != asset[2]:
            return False
        if record.get("status") not in {"READ_OK", "PRESENT_METADATA_ONLY", "MISSING", "EMPTY", "TOO_LARGE", "NOT_REGULAR_FILE", "CHANGED_DURING_READ", "POTENTIAL_SECRET_CONTENT_OMITTED", "HASH_MISMATCH", "ACCESS_DENIED", "INVALID_UTF8", "INVALID_GRAPH", "INVALID_JSON", "READ_ERROR"}:
            return False
        if record["status"] in {"READ_OK", "HASH_MISMATCH"}:
            if not isinstance(record.get("content"), str) or not re.fullmatch(r"[0-9a-f]{64}", record.get("sha256", "")):
                return False
            if record.get("content_sha256") != sha256(record["content"].encode("utf-8")):
                return False
            if SECRET_PATTERN.search(record["content"]):
                return False
        if record["status"] == "POTENTIAL_SECRET_CONTENT_OMITTED" and "content" in record:
            return False
    return True


def recover(output_dir, fixture_root=None):
    """Internal fixture hook; production caller must use run_reality()."""
    context = "GPT_FIXTURE" if fixture_root is not None else "WINDOWS_REAL_ASSET_RECOVERY"
    start_utc, start_ns = stamp(), time.perf_counter_ns()
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=False)
    snapshot = {"version": VERSION, "scope": SCOPE, "context": context,
                "p1_virtual_complete": False, "p1_real_generation_runs": 0,
                "p1_t_valid_ms": None,
                "assets": [inspect_asset(a, fixture_root) for a in ASSETS]}
    if not run_verifier(snapshot):
        raise RuntimeError("SNAPSHOT_SCOPE_OR_SHAPE_INVALID")
    raw = (json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target = output / "ASSET-SNAPSHOT.json"
    with target.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    recovered = target.read_bytes()
    if recovered != raw or not run_verifier(json.loads(recovered)):
        raise RuntimeError("SNAPSHOT_READBACK_FAILED")
    end_ns, end_utc = time.perf_counter_ns(), stamp()
    issues = [{"id": x["id"], "status": x["status"]} for x in snapshot["assets"] if x["status"] not in ("READ_OK", "PRESENT_METADATA_ONLY")]
    receipt = {"version": VERSION, "scope": SCOPE, "context": context,
               "inventory_capture": "PASS", "asset_issues": issues,
               "real_start_utc": start_utc, "real_end_utc": end_utc,
               "real_start_ns": start_ns, "real_end_ns": end_ns,
               "asset_recovery_elapsed_ms": (end_ns - start_ns) / 1e6,
               "timing_boundary": "before_output_creation_to_snapshot_fsync_and_readback; receipt_reporting_excluded",
               "snapshot_sha256": sha256(recovered), "snapshot_path": str(target),
               "p1_virtual_complete": False, "p1_real_generation_runs": 0,
               "p1_t_valid_ms": None, "next_action": "STOP_RETURN_TO_GPT"}
    with (output / "RECOVERY-RECEIPT.json").open("x", encoding="utf-8") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2)
    return receipt


def run_reality():
    if os.name != "nt":
        raise RuntimeError("WINDOWS_TARGET_REQUIRED")
    directory = Path(OUTPUT_ROOT) / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    return recover(directory)
