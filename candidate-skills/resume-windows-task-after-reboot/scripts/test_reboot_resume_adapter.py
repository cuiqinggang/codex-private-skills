#!/usr/bin/env python3
"""Cross-platform static and state-machine tests; never touches Task Scheduler."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "Invoke-RebootResumeAdapter.ps1"
STATE_FIELDS = {
    "schemaVersion", "runId", "status", "resumeStep", "entryPointId", "previousBootId",
    "attempt", "maxAttempts", "codeCommit", "packageSha256", "stateRevision", "updatedAt", "lastErrorCode",
}


def atomic_write(path: Path, value: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def resume(state: dict, current_boot: str) -> dict:
    assert set(state) == STATE_FIELDS
    assert state["status"] == "REBOOT_PENDING"
    if state["previousBootId"] == current_boot:
        raise ValueError("replay")
    if state["attempt"] >= state["maxAttempts"]:
        return {**state, "status": "BLOCKED"}
    return {**state, "status": "RESUMING", "attempt": state["attempt"] + 1}


def resolve_local_first(local: dict, remote: dict) -> dict:
    if local["status"] != "REBOOT_PENDING":
        return local
    for field in ("runId", "stateRevision", "codeCommit", "packageSha256", "entryPointId", "resumeStep", "previousBootId"):
        if remote[field] != local[field]:
            raise ValueError(f"stale remote {field}")
    return local


def validate_entry(entry: dict) -> None:
    assert set(entry) == {"id", "scriptPath", "sha256"}
    assert re.fullmatch(r"[A-Za-z0-9._-]{1,64}", entry["id"])
    assert entry["scriptPath"].lower().endswith(".ps1")
    assert ".." not in Path(entry["scriptPath"]).parts


def protected_layout(root: Path, paths: list[Path], writers: set[str], reparse: set[Path], bootstrap_hash_ok: bool) -> bool:
    allowed = {"SYSTEM", "BUILTIN_ADMINISTRATORS"}
    return (
        writers <= allowed
        and bootstrap_hash_ok
        and not reparse
        and all(path == root or root in path.parents for path in paths)
    )


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    required = [
        "New-ScheduledTaskTrigger -AtStartup",
        "LastBootUpTime",
        "Global\\RebootResumeAdapter",
        "Get-FileHash",
        "REBOOT_PENDING",
        "BLOCKED",
        "ShouldProcess",
        "ProgramData",
        "Set-ProtectedRootAcl",
        "Assert-ProtectedPath",
        "Source entrypoint hash mismatch",
        "Installed bootstrap hash mismatch",
        "S-1-5-18",
        "S-1-5-32-544",
    ]
    for token in required:
        assert token in text, token
    forbidden = [
        r"\bRestart-Computer\b",
        r"\bStop-Computer\b",
        r"Invoke-Expression",
        r"\biex\b",
        r"ExecutionPolicy\s+Bypass",
        r"curl.+\|\s*(?:powershell|pwsh)",
    ]
    for pattern in forbidden:
        assert not re.search(pattern, text, re.IGNORECASE), pattern

    digest = hashlib.sha256(b"entrypoint").hexdigest()
    state = {
        "schemaVersion": 1,
        "runId": "fixture",
        "status": "REBOOT_PENDING",
        "resumeStep": "after-reboot-1",
        "entryPointId": "fixture-entry",
        "previousBootId": "boot-0",
        "attempt": 0,
        "maxAttempts": 2,
        "codeCommit": "commit-1",
        "packageSha256": digest,
        "stateRevision": 1,
        "updatedAt": "fixture",
        "lastErrorCode": None,
    }
    with tempfile.TemporaryDirectory(prefix="reboot-resume-fixture-") as folder:
        path = Path(folder) / "state.json"
        atomic_write(path, state)
        loaded = json.loads(path.read_text(encoding="utf-8"))
        try:
            resume(loaded, "boot-0")
            raise AssertionError("same-boot replay was accepted")
        except ValueError:
            pass
        first = resume(loaded, "boot-1")
        assert first["attempt"] == 1 and first["status"] == "RESUMING"
        stale_remote = dict(loaded, stateRevision=0)
        try:
            resolve_local_first(loaded, stale_remote)
        except ValueError:
            pass
        else:
            raise AssertionError("stale remote checkpoint was accepted")
        assert resolve_local_first(first, loaded)["status"] == "RESUMING"
        extra = dict(loaded, command="Remove-Item C:\\*")
        try:
            resume(extra, "boot-1")
        except AssertionError:
            pass
        else:
            raise AssertionError("extra command field was accepted")
        try:
            validate_entry({"id": "fixture;whoami", "scriptPath": "entry.ps1", "sha256": digest})
        except AssertionError:
            pass
        else:
            raise AssertionError("command-like entrypoint id was accepted")
        protected_root = Path("C:/ProgramData/RebootResumeAdapter")
        critical = [protected_root / "config.json", protected_root / "state.json", protected_root / "entries" / "fixture.ps1"]
        assert protected_layout(protected_root, critical, {"SYSTEM", "BUILTIN_ADMINISTRATORS"}, set(), True)
        assert not protected_layout(protected_root, critical, {"SYSTEM", "USERS"}, set(), True)
        assert not protected_layout(protected_root, critical, {"SYSTEM"}, {protected_root / "entries"}, True)
        assert not protected_layout(protected_root, critical + [Path("C:/Temp/evil.ps1")], {"SYSTEM"}, set(), True)
        assert not protected_layout(protected_root, critical, {"SYSTEM"}, set(), False)
        first.update(status="REBOOT_PENDING", previousBootId="boot-1", resumeStep="after-reboot-2", stateRevision=2)
        second = resume(first, "boot-2")
        assert second["attempt"] == 2
        second.update(status="REBOOT_PENDING", previousBootId="boot-2")
        blocked = resume(second, "boot-3")
        assert blocked["status"] == "BLOCKED"
    print(json.dumps({"overall": "PASS", "level": "STATIC_VERIFIED", "skill": ROOT.name}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
