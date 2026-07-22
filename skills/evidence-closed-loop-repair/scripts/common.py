from __future__ import annotations
from pathlib import Path
import hashlib, json, os, re, fnmatch, shutil, subprocess, tempfile, zipfile
from dataclasses import dataclass, asdict
from typing import Iterable, Any

DEFAULT_ENCODINGS = ["utf-8-sig", "utf-8", "utf-16", "gb18030"]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def matches_any(path: str, globs: list[str]) -> bool:
    if not globs:
        return True
    # pathlib/fnmatch compatibility for root files and ** patterns
    variants = {path, "./" + path}
    if "/" not in path:
        variants.add("x/" + path)
    for pattern in globs:
        for v in variants:
            if fnmatch.fnmatch(v, pattern) or Path(v).match(pattern):
                return True
    return False


def should_exclude(rel: str, exclude_globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, p) or Path(rel).match(p) for p in exclude_globs)


def iter_files(root: Path, exclude_globs: list[str] | None = None) -> Iterable[Path]:
    exclude_globs = exclude_globs or []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = rel_posix(p, root)
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if should_exclude(rel, exclude_globs):
            continue
        yield p


def read_text_best_effort(path: Path, encodings: list[str] | None = None) -> tuple[str | None, str | None]:
    encodings = encodings or DEFAULT_ENCODINGS
    data = path.read_bytes()
    if b"\x00" in data[:4096] and not (data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff")):
        return None, None
    for enc in encodings:
        try:
            return data.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            pass
    return None, None


def count_pattern(text: str, pattern: str, mode: str, case_sensitive: bool) -> int:
    flags = 0 if case_sensitive else re.IGNORECASE
    if mode == "regex":
        return len(re.findall(pattern, text, flags))
    if case_sensitive:
        return text.count(pattern)
    return text.lower().count(pattern.lower())


def locate_pattern(text: str, pattern: str, mode: str, case_sensitive: bool, limit: int = 20) -> list[dict[str, Any]]:
    flags = 0 if case_sensitive else re.IGNORECASE
    expr = pattern if mode == "regex" else re.escape(pattern)
    out = []
    for m in re.finditer(expr, text, flags):
        line = text.count("\n", 0, m.start()) + 1
        start = max(0, m.start() - 40)
        end = min(len(text), m.end() + 60)
        out.append({"line": line, "snippet": text[start:end].replace("\n", "\\n")})
        if len(out) >= limit:
            break
    return out


def find_7z() -> str | None:
    for name in ["7z", "7zz", "7za"]:
        p = shutil.which(name)
        if p:
            return p
    return None


def extract_archive(archive: Path, out_dir: Path) -> tuple[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = archive.suffix.lower()
    if suffix == ".zip":
        with zipfile.ZipFile(archive) as z:
            z.extractall(out_dir)
        return "PASS", "zipfile"
    if suffix == ".7z":
        exe = find_7z()
        if not exe:
            return "PENDING_UNVERIFIED_7Z", "7z CLI not found"
        cp = subprocess.run([exe, "x", str(archive), f"-o{out_dir}", "-y"], capture_output=True, text=True)
        if cp.returncode != 0:
            return "FAIL", cp.stdout + "\n" + cp.stderr
        return "PASS", exe
    return "UNSUPPORTED", suffix


def tree_manifest(root: Path, exclude_globs: list[str] | None = None) -> dict[str, str]:
    return {rel_posix(p, root): sha256_file(p) for p in iter_files(root, exclude_globs)}


def write_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
