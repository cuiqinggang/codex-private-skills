"""Install only the V1.6 adapter and exact frozen method/memory dependencies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = Path(r"C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent\skills")

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def blobsha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def sources():
    manifest = json.loads((ROOT / "references/SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        p = ROOT / item["bundled_path"]
        if blobsha(p.read_bytes()) != item["git_blob_sha"]:
            raise RuntimeError("UPSTREAM_INTEGRITY_MISMATCH:" + item["bundled_path"])
    return manifest

def install(skills, apply=False, desktop=False):
    sources()
    if not (skills / "dsh-mature-capabilities/SKILL.md").is_file():
        raise RuntimeError("Existing mature DSH installation required")
    mappings = [(ROOT, skills / "google-deepseek-strong-backup", True)]
    for name in ("ai-organization-v4-2", "reuse-experience-brain"):
        mappings.append((ROOT / "references/upstream" / name, skills / name, False))
    changes = []
    for src, dst, own in mappings:
        for p in sorted(src.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            out = dst / p.relative_to(src)
            same = out.is_file() and sha(p) == sha(out)
            if same:
                continue
            if out.exists() and not own:
                raise RuntimeError("DEPENDENCY_CONFLICT_NO_OVERWRITE:" + str(out))
            changes.append((p, out))
    receipt = {"status": "DRY_RUN", "changed": len(changes),
               "targets": [str(out) for _, out in changes], "credentials_copied": False}
    if not apply:
        return receipt
    for src, dst in changes:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            backup = dst.with_name(dst.name + ".before-v16-" + time.strftime("%Y%m%d%H%M%S"))
            shutil.copy2(dst, backup)
        shutil.copy2(src, dst)
        if sha(src) != sha(dst):
            raise RuntimeError("COPY_HASH_MISMATCH:" + str(dst))
    receipt["status"] = "INSTALLED"
    if desktop:
        import ctypes
        buf = ctypes.create_unicode_buffer(32768)
        hr = ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, buf)
        if hr != 0:
            raise RuntimeError("Cannot resolve existing Desktop")
        target = Path(buf.value) / "谷深强备-V1.6.cmd"
        launcher = skills / "google-deepseek-strong-backup/scripts/run_backup.py"
        body = '@echo off\r\nchcp 65001 >nul\r\npython "' + str(launcher) + '"\r\npause\r\n'
        if target.exists() and target.read_bytes() != body.encode("utf-8"):
            raise RuntimeError("Existing different V1.6 desktop entry; not overwritten")
        target.write_bytes(body.encode("utf-8"))
        receipt["desktop_entry"] = str(target)
    return receipt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--desktop", action="store_true")
    a = p.parse_args()
    print(json.dumps(install(DEFAULT, a.apply, a.desktop), ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
