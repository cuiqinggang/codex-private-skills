"""Copy one authorized file into the existing share and verify its current public URL."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time
import urllib.parse
import urllib.request

import public_server as manager

ROOT = manager.ROOT
FULL_LIMIT = 16 * 1024 * 1024


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def run(source_name, requested_name=None):
    started = time.monotonic()
    if os.name != "nt":
        raise RuntimeError("Run this helper on the authorized Windows computer")
    source = Path(source_name).resolve(strict=True)
    if not source.is_file():
        raise ValueError("Specify one existing file")
    if source.is_relative_to(ROOT.resolve()) and not any(source.is_relative_to((ROOT / x).resolve()) for x in ("shared", "qa-source")):
        raise ValueError("Protected server files cannot be published through this helper")
    name = requested_name or source.name
    if name in (".", "..") or re.search(r'[<>:"/\\|?*\x00-\x1f]', name) or name.endswith((".", " ")) or len(name) > 200:
        raise ValueError("Use one valid Windows filename")
    state = manager.status()
    settings = manager.config()
    if state.get("status") != "RUNNING" or not state.get("public_url"):
        raise RuntimeError("Start the existing service before sharing")
    if settings.get("origin_engine") != "copyparty" or settings.get("target") != "http://[::1]:18780":
        raise RuntimeError("Unexpected origin; do not change another app's tunnel")
    shared = (ROOT / "shared").resolve(strict=True)
    expected = sha256(source)
    destination = shared / name
    if destination.exists() and (not destination.is_file() or sha256(destination) != expected):
        if requested_name:
            raise FileExistsError("A different file already uses that requested name")
        name = source.stem + "-" + expected[:8] + source.suffix
        destination = shared / name
        if destination.exists() and (not destination.is_file() or sha256(destination) != expected):
            raise FileExistsError("Conflicting destination; choose another filename")
    copied = False
    if not destination.exists():
        handle, pending = tempfile.mkstemp(prefix="publish-", dir=ROOT / "data")
        os.close(handle)
        pending = Path(pending)
        try:
            shutil.copy2(source, pending)
            if sha256(pending) != expected:
                raise RuntimeError("Source changed during copy")
            # Windows rename is atomic and refuses to replace an existing file.
            os.rename(pending, destination)
            copied = True
        finally:
            pending.unlink(missing_ok=True)
    url = state["public_url"] + "/download/" + urllib.parse.quote(name, safe="") + "?dl"
    receipt = {"skill_version": "1.0", "status": "PUBLISHED_NOT_VERIFIED", "source": str(source),
               "destination": str(destination), "download_url": url, "filename": name,
               "source_preserved": source.exists(), "copied": copied,
               "sha256": expected, "bytes": destination.stat().st_size}
    manager.save_json(ROOT / "last-share.json", receipt)
    if receipt["bytes"] <= FULL_LIMIT:
        digest = hashlib.sha256()
        with urllib.request.urlopen(url, timeout=25) as response:
            if response.status != 200:
                raise RuntimeError("Public download did not return HTTP 200")
            for part in iter(lambda: response.read(1024 * 1024), b""):
                digest.update(part)
        if digest.hexdigest() != expected:
            raise RuntimeError("Public bytes do not match the source")
        verification = "FULL_SHA256"
    else:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=25) as response:
            if int(response.headers.get("Content-Length", -1)) != receipt["bytes"]:
                raise RuntimeError("Public size does not match")
        sample = 65536
        with source.open("rb") as stream:
            for start in (0, receipt["bytes"] - sample):
                stream.seek(start)
                reference = stream.read(sample)
                req = urllib.request.Request(url, headers={"Range": "bytes={}-{}".format(start, start + sample - 1)})
                with urllib.request.urlopen(req, timeout=25) as response:
                    if response.status != 206 or response.read(sample + 1) != reference:
                        raise RuntimeError("Public range sample does not match")
        verification = "SIZE_AND_TWO_RANGE_SAMPLES"
    receipt.update(status="VERIFIED", verification=verification,
                   copy_text="这是“{}”的下载地址，点击即可下载：{}\n我的电脑开机联网时可用。".format(name, url),
                   elapsed_seconds=round(time.monotonic() - started, 3),
                   checked_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    manager.save_json(ROOT / "last-share.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--name")
    args = parser.parse_args()
    try:
        run(args.source, args.name)
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "error_type": type(exc).__name__,
                          "detail": str(exc), "reconcile": str(ROOT / "last-share.json")}, ensure_ascii=True), flush=True)
        raise SystemExit(1)
