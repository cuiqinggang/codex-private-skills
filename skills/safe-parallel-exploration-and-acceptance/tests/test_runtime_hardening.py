from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path


def run(command: list[str], *, cwd: Path | None = None, input_bytes: bytes | None = None, env: dict[str, str] | None = None, timeout: int = 90) -> subprocess.CompletedProcess[bytes]:
    merged = os.environ.copy()
    merged.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    if env:
        merged.update(env)
    return subprocess.run(command, cwd=cwd, input=input_bytes, capture_output=True, env=merged, timeout=timeout)


def text(proc: subprocess.CompletedProcess[bytes]) -> str:
    return (proc.stdout + proc.stderr).decode("utf-8", "replace")


def json_stdout(proc: subprocess.CompletedProcess[bytes]) -> dict:
    return json.loads(proc.stdout.decode("utf-8-sig"))


def git(path: Path, *args: str, input_bytes: bytes | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    return run(["git", "-C", str(path), *args], input_bytes=input_bytes, env=env)


def commit_env() -> dict[str, str]:
    return {
        "GIT_AUTHOR_NAME": "Codex Runtime Test",
        "GIT_AUTHOR_EMAIL": "codex-test@localhost",
        "GIT_COMMITTER_NAME": "Codex Runtime Test",
        "GIT_COMMITTER_EMAIL": "codex-test@localhost",
    }


def must(proc: subprocess.CompletedProcess[bytes], label: str) -> subprocess.CompletedProcess[bytes]:
    if proc.returncode != 0:
        raise RuntimeError(f"{label} failed (exit={proc.returncode}): {text(proc)}")
    return proc


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def make_normal_repo(path: Path) -> str:
    path.mkdir(parents=True)
    must(run(["git", "init", "-b", "main", str(path)]), "git init")
    (path / "README.md").write_text("runtime fixture\n", encoding="utf-8")
    must(git(path, "add", "README.md"), "git add")
    must(git(path, "commit", "-m", "fixture", env=commit_env()), "git commit")
    return must(git(path, "rev-parse", "HEAD"), "rev-parse").stdout.decode().strip()


def make_invalid_bare_repo(path: Path) -> str:
    must(run(["git", "init", "--bare", "-b", "main", str(path)]), "git init --bare")
    blob = must(git(path, "hash-object", "-w", "--stdin", input_bytes=b"blocked\n"), "hash-object").stdout.decode().strip()
    tree_line = f"100644 blob {blob}\tBAD \0".encode("utf-8")
    tree = must(git(path, "mktree", "-z", input_bytes=tree_line), "mktree invalid path").stdout.decode().strip()
    commit = must(git(path, "commit-tree", tree, "-m", "invalid windows path", env=commit_env()), "commit-tree").stdout.decode().strip()
    must(git(path, "update-ref", "refs/heads/main", commit), "update-ref main")
    must(git(path, "symbolic-ref", "HEAD", "refs/heads/main"), "symbolic-ref")
    return commit


def add_result(results: list[dict], name: str, passed: bool, detail: object) -> None:
    results.append({"name": name, "passed": bool(passed), "detail": detail})


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", required=True, type=Path)
    parser.add_argument("--work-root", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()
    skill = args.skill_root.resolve()
    if not (skill / "SKILL.md").is_file():
        raise SystemExit(f"invalid skill root: {skill}")
    work_root = args.work_root.resolve()
    if work_root.drive.upper() != "C:":
        raise SystemExit(f"work-root must be on C drive: {work_root}")
    run_root = work_root / f"runtime-hardening-{int(time.time() * 1000)}"
    run_root.mkdir(parents=True)
    results: list[dict] = []
    ps = "powershell.exe"
    context_script = skill / "scripts" / "git" / "get-git-runtime-context.ps1"
    audit_script = skill / "scripts" / "git" / "audit-windows-git-paths.py"
    recovery_script = skill / "scripts" / "git" / "create-windows-safe-isolated-worktree.ps1"
    readiness_script = skill / "scripts" / "worktree" / "check-worktree-readiness.ps1"
    create_script = skill / "scripts" / "worktree" / "create-exploration-worktree.ps1"
    exact_script = skill / "scripts" / "acceptance" / "verify-exact-byte-assets.py"
    readonly_script = skill / "scripts" / "acceptance" / "test-readonly-sandbox-injection.py"

    try:
        empty_marker = run_root / "empty-marker"
        (empty_marker / ".git").mkdir(parents=True)
        proc = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(context_script), "-ProjectPath", str(empty_marker)])
        ctx = json_stdout(must(proc, "empty .git context"))
        add_result(results, "empty-git-marker-detected", ctx["context"] == "BROKEN_GIT_MARKER", ctx)

        plain = run_root / "plain"
        plain.mkdir()
        proc = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(context_script), "-ProjectPath", str(plain)])
        ctx = json_stdout(must(proc, "non-git context"))
        add_result(results, "non-git-detected", ctx["context"] == "NOT_GIT", ctx)

        normal = run_root / "normal-repo"
        normal_head = make_normal_repo(normal)
        proc = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(context_script), "-ProjectPath", str(normal)])
        ctx = json_stdout(must(proc, "worktree context"))
        add_result(results, "worktree-detected", ctx["context"] == "WORKTREE", ctx)
        audit = run([sys.executable, str(audit_script), "--repository", str(normal), "--revision", normal_head])
        audit_json = json_stdout(must(audit, "valid path audit"))
        add_result(results, "valid-tree-audit-pass", audit_json["status"] == "PASS", audit_json)
        ready = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(readiness_script), "-ProjectPath", str(normal)])
        ready_json = json_stdout(must(ready, "normal readiness"))
        add_result(results, "normal-worktree-ready", ready_json["status"] == "WORKTREE_READY", ready_json)
        normal_wt_root = run_root / "normal-worktrees"
        created = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(create_script), "-ProjectPath", str(normal), "-ProjectSlug", "fixture", "-Route", "positive", "-WorktreeRoot", str(normal_wt_root), "-ConfirmCreate"])
        created_json = json_stdout(must(created, "normal worktree creation"))
        add_result(results, "normal-worktree-create-pass", created_json["status"] == "WORKTREE_CREATED" and created_json["windows_path_audit"] == "PASS", created_json)

        invalid_bare = run_root / "invalid.git"
        invalid_head = make_invalid_bare_repo(invalid_bare)
        proc = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(context_script), "-ProjectPath", str(invalid_bare)])
        ctx = json_stdout(must(proc, "bare context"))
        add_result(results, "bare-repository-detected", ctx["context"] == "BARE_REPOSITORY", ctx)
        audit = run([sys.executable, str(audit_script), "--repository", str(invalid_bare), "--revision", invalid_head])
        audit_json = json_stdout(audit)
        add_result(results, "invalid-tree-audit-blocks", audit.returncode == 2 and audit_json["status"] == "WINDOWS_PATH_BLOCKED" and audit_json["blocked_count"] == 1, audit_json)
        blocked_normal = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(create_script), "-ProjectPath", str(invalid_bare), "-ProjectSlug", "fixture", "-Route", "blocked", "-WorktreeRoot", str(run_root / "blocked-normal"), "-ConfirmCreate"])
        add_result(results, "ordinary-worktree-blocked", blocked_normal.returncode != 0 and "Windows" in text(blocked_normal), {"exit": blocked_normal.returncode, "output": text(blocked_normal)[-1000:]})

        recovery_target = run_root / "isolated-recovery"
        branch = "explore/runtime/recovery"
        tag = "protect/runtime-test"
        preview = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(recovery_script), "-RepositoryPath", str(invalid_bare), "-WorktreePath", str(recovery_target), "-BranchName", branch, "-BaseRevision", "main", "-ProtectionTag", tag])
        preview_json = json_stdout(must(preview, "recovery preview"))
        add_result(results, "recovery-preview-safe", preview_json["status"] == "PREVIEW_ONLY" and preview_json["main_or_base_will_change"] is False, preview_json)
        before = must(git(invalid_bare, "rev-parse", "main"), "base before").stdout.decode().strip()
        recovery = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(recovery_script), "-RepositoryPath", str(invalid_bare), "-WorktreePath", str(recovery_target), "-BranchName", branch, "-BaseRevision", "main", "-ProtectionTag", tag, "-ConfirmCreate"])
        recovery_json = json_stdout(must(recovery, "isolated recovery"))
        after = must(git(invalid_bare, "rev-parse", "main"), "base after").stdout.decode().strip()
        parent_probe = git(invalid_bare, "rev-parse", f"{branch}^")
        recovery_ok = recovery_json["status"] == "ISOLATED_WORKTREE_CREATED" and recovery_json["base_unchanged"] and before == after and recovery_target.is_dir() and parent_probe.returncode != 0
        add_result(results, "isolated-recovery-preserves-base", recovery_ok, recovery_json)

        exact_repo = run_root / "exact-bytes"
        exact_repo.mkdir()
        must(run(["git", "init", "-b", "main", str(exact_repo)]), "exact repo init")
        must(git(exact_repo, "config", "core.autocrlf", "true"), "set autocrlf")
        locked_bytes = b"\xef\xbb\xbfline1\r\nline2\r\n"
        (exact_repo / "locked.txt").write_bytes(locked_bytes)
        (exact_repo / ".gitattributes").write_text("locked.txt -text\ndrift.txt text eol=lf\n", encoding="utf-8", newline="\n")
        (exact_repo / "drift.txt").write_bytes(b"line1\r\nline2\r\n")
        must(git(exact_repo, "add", ".gitattributes", "locked.txt", "drift.txt"), "exact git add")
        locked_manifest = exact_repo / "locked-manifest.json"
        locked_manifest.write_text(json.dumps({"assets": [{"asset_id": "locked", "path": "locked.txt", "sha256": sha(locked_bytes)}]}, indent=2), encoding="utf-8")
        verified = run([sys.executable, str(exact_script), "--manifest", str(locked_manifest), "--root", str(exact_repo), "--git-index"])
        verified_json = json_stdout(must(verified, "exact-byte locked asset"))
        add_result(results, "exact-byte-minus-text-pass", verified_json["status"] == "PASS", verified_json)
        drift_bytes = (exact_repo / "drift.txt").read_bytes()
        drift_manifest = exact_repo / "drift-manifest.json"
        drift_manifest.write_text(json.dumps({"assets": [{"asset_id": "drift", "path": "drift.txt", "sha256": sha(drift_bytes)}]}, indent=2), encoding="utf-8")
        drift = run([sys.executable, str(exact_script), "--manifest", str(drift_manifest), "--root", str(exact_repo), "--git-index"])
        drift_json = json_stdout(drift)
        add_result(results, "autocrlf-drift-detected", drift.returncode == 2 and drift_json["status"] == "EXACT_BYTE_MISMATCH", drift_json)

        readonly_source = run_root / "readonly-source.bin"
        readonly_source.write_bytes(b"LOCKED-SOURCE\r\n")
        os.chmod(readonly_source, stat.S_IREAD)
        source_before = sha(readonly_source.read_bytes())
        readonly = run([sys.executable, str(readonly_script), "--source", str(readonly_source), "--sandbox", str(run_root / "readonly-sandbox")])
        readonly_json = json_stdout(must(readonly, "readonly injection"))
        source_after = sha(readonly_source.read_bytes())
        add_result(results, "readonly-sandbox-source-unchanged", readonly_json["status"] == "PASS" and source_before == source_after, readonly_json)

        static_evidence = run_root / "installed-copy-static.json"
        static_test = run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(skill / "tests" / "run-static-tests.ps1"), "-SkillPath", str(skill), "-EvidencePath", str(static_evidence)])
        static_json = json_stdout(must(static_test, "installed-copy static test"))
        add_result(results, "non-git-installed-copy-validates", static_json["passed"] is True, {"runtime_context": "NOT_GIT_ALLOWED", "static": static_json})
    except Exception as exc:
        add_result(results, "harness-unhandled-exception", False, repr(exc))

    passed = all(item["passed"] for item in results) and len(results) >= 15
    report = {
        "schema_version": "1.0",
        "suite": "runtime-hardening",
        "status": "PASS" if passed else "FAIL",
        "skill_root": str(skill),
        "work_root": str(run_root),
        "result_count": len(results),
        "results": results,
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
