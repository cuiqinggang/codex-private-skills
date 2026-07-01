from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = ROOT / "scripts" / "chatgpt_web_attachment_bridge.py"
SAVER = ROOT / "scripts" / "chatgpt_web_result_saver.py"


def run_command(cmd: list[str], cwd: Path) -> dict:
    started = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    item = {
        "cmd": cmd,
        "returncode": proc.returncode,
        "elapsed_ms": int((time.time() - started) * 1000),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }
    try:
        item["json"] = json.loads(proc.stdout)
    except Exception:
        item["json"] = None
    return item


def attachment_result_screenshot(command_result: dict) -> str | None:
    data = command_result.get("json")
    if not isinstance(data, dict):
        return None
    screenshots = data.get("screenshots")
    if not isinstance(screenshots, dict):
        return None
    path = screenshots.get("state_result")
    if path and Path(str(path)).exists():
        return str(path)
    return None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a production-safe ChatGPT web image repair batch sequentially.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--prompt-extra", default="")
    parser.add_argument("--attachment-wait", type=float, default=35.0)
    parser.add_argument("--timeout-finish", type=float, default=420.0)
    parser.add_argument("--send-retries", type=int, default=3)
    parser.add_argument("--send-confirm-timeout", type=float, default=8.0)
    parser.add_argument("--post-send-wait", type=float, default=8.0)
    parser.add_argument("--upload-method", choices=("drag", "clipboard"), default="drag")
    parser.add_argument("--continue-on-item-fail", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    run_dir = Path(args.run_root).resolve() / f"{time.strftime('%Y%m%d-%H%M%S')}_sequential_batch"
    run_dir.mkdir(parents=True, exist_ok=True)
    output_manifest = {
        "mode": "batch-sequential",
        "source_manifest": str(manifest_path),
        "count": len(files),
        "items": [],
    }

    for item in files:
        index = int(item["index"])
        source = Path(item["local_copy"]).resolve()
        source_stem = item.get("source_stem") or source.stem
        item_dir = run_dir / f"i{index:02d}"
        item_dir.mkdir(parents=True, exist_ok=True)
        prompt = (
            "Repair this attached image as a clean production-quality video keyframe/clean plate.\n"
            "Return exactly one image. Do not add labels, captions, watermarks, or extra text inside the image.\n"
            "Preserve camera angle, object geometry, lighting, shadows, and scene composition.\n"
            "Remove visible artifacts and make the frame clean enough for downstream video reconstruction.\n"
        )
        if args.prompt_extra.strip():
            prompt += args.prompt_extra.strip() + "\n"
        prompt_path = item_dir / "prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        item_record = {
            "index": index,
            "source": str(source),
            "source_stem": source_stem,
            "prompt": str(prompt_path),
            "expected_output": str(item_dir / "result" / "local_outputs" / f"01_{source_stem}_repaired.png"),
            "attachment": None,
            "save": None,
        }
        if not args.dry_run:
            attach = run_command(
                [
                    sys.executable,
                    str(ATTACHMENT),
                    "--branch",
                    "image",
                    "--upload-method",
                    args.upload_method,
                    "--prompt-order",
                    "before",
                    "--file",
                    str(source),
                    "--prompt-file",
                    str(prompt_path),
                    "--purpose",
                    f"b{index:02d}",
                    "--run-root",
                    str(item_dir / "attachment"),
                    "--attachment-wait",
                    str(args.attachment_wait),
                    "--timeout-finish",
                    str(args.timeout_finish),
                    "--send-retries",
                    str(args.send_retries),
                    "--send-confirm-timeout",
                    str(args.send_confirm_timeout),
                ],
                ROOT,
            )
            item_record["attachment"] = attach
            attachment_screenshot = attachment_result_screenshot(attach)
            if attach["returncode"] != 0 and not attachment_screenshot and not args.continue_on_item_fail:
                item_record["save"] = None
                item_record["stopped_batch_after_item"] = True
                output_manifest["items"].append(item_record)
                output_manifest["status"] = "BATCH_FAIL"
                output_manifest["failures"] = [f"attachment:{index}"]
                output_manifest["stop_reason"] = "Attachment failed before a result screenshot existed; stopped to avoid stacking multiple unfinished ChatGPT requests."
                (run_dir / "batch_result_manifest.json").write_text(json.dumps(output_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
                print(json.dumps({"run_dir": str(run_dir), "status": output_manifest["status"], "failures": output_manifest["failures"], "stop_reason": output_manifest["stop_reason"]}, ensure_ascii=False, indent=2))
                return 2
            if args.post_send_wait > 0:
                time.sleep(args.post_send_wait)
            save_cmd = [
                    sys.executable,
                    str(SAVER),
                    "--run-root",
                    str(item_dir / "result"),
                    "--max-results",
                    "1",
                    "--require-count",
                    "1",
                    "--output-name",
                    f"01_{source_stem}_repaired.png",
            ]
            screenshot_file = attachment_screenshot
            if screenshot_file:
                save_cmd.extend(["--screenshot-file", screenshot_file])
                item_record["save_source_screenshot"] = screenshot_file
            save = run_command(
                save_cmd,
                ROOT,
            )
            item_record["save"] = save
        output_manifest["items"].append(item_record)
        (run_dir / "batch_result_manifest.json").write_text(json.dumps(output_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    failures = []
    warnings = []
    if not args.dry_run:
        for item in output_manifest["items"]:
            save_ok = bool(item.get("save") and item["save"]["returncode"] == 0)
            attachment_ok = bool(item.get("attachment") and item["attachment"]["returncode"] == 0)
            if not item.get("save") or item["save"]["returncode"] != 0:
                failures.append(f"save:{item['index']}")
            if not attachment_ok:
                if save_ok:
                    warnings.append(f"attachment_nonzero_but_output_saved:{item['index']}")
                else:
                    failures.append(f"attachment:{item['index']}")
    output_manifest["status"] = "BATCH_PASS" if not failures and not warnings else ("BATCH_PASS_WITH_WARNINGS" if not failures else "BATCH_FAIL")
    output_manifest["failures"] = failures
    output_manifest["warnings"] = warnings
    (run_dir / "batch_result_manifest.json").write_text(json.dumps(output_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), "status": output_manifest["status"], "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
