"""Read-only package checks, plus one local static receipt. Not media certification."""
from pathlib import Path
import hashlib
import json
import re
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
receipt = root / "acceptance" / "static_check.json"
required = [
    "SKILL.md", "VERSION.md", "RECENT_USE_LOG.md",
    "references/METHOD_V2.md", "references/FRAME_CONTINUITY.md",
    "references/ACCEPTANCE.md", "references/FAILURE_RECOVERY.md",
    "templates/PROJECT_BRIEF.md", "templates/FINAL_TEST_RESULT.md",
    "source/LESSON_EXTRACTION.md", "source/AGENTS_PATCH_DRAFT.md",
    "source/UPSTREAM_CONTRACT.md", "acceptance/index.html",
]
errors = []
docs = {}
for relative in required:
    path = root / relative
    if not path.is_file():
        errors.append(f"MISSING: {relative}")
        continue
    try:
        docs[relative] = path.read_text(encoding="utf-8-sig")
    except UnicodeError as error:
        errors.append(f"INVALID_UTF8: {relative}: {error}")
        continue
    if not docs[relative].strip():
        errors.append(f"EMPTY: {relative}")

for relative, content in docs.items():
    targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", content)
    if relative.endswith(".html"):
        targets += re.findall(r'href="([^"]+)"', content)
    for target in targets:
        if re.match(r"^(https?://|#|[A-Za-z]:)", target):
            continue
        resolved = ((root / relative).parent / target.split("#")[0]).resolve()
        if resolved == receipt:
            continue
        if not resolved.is_relative_to(root):
            errors.append(f"LINK_OUTSIDE_PACKAGE: {relative}: {target}")
        elif not resolved.is_file():
            errors.append(f"BROKEN_LINK: {relative}: {target}")

checks = {
    "frame_count_56": "N=56" in docs.get("references/METHOD_V2.md", ""),
    "fps_24": "FPS=24" in docs.get("references/METHOD_V2.md", ""),
    "previous_accepted_and_first_reference": all(x in docs.get("SKILL.md", "") for x in ("首帧", "上一张合格", "真实输入")),
    "all_frame_gate": "56 张全部来源" in docs.get("templates/PROJECT_BRIEF.md", ""),
    "no_interpolation": "无插帧" in docs.get("references/METHOD_V2.md", ""),
    "model_not_exposed": "NOT_EXPOSED" in docs.get("SKILL.md", ""),
    "native_resolution_not_hard_gate": "非原生输出本身不判 FAIL" in docs.get("references/METHOD_V2.md", ""),
    "playback_and_listening_not_faked": all(x in docs.get("references/ACCEPTANCE.md", "") for x in ("PLAYBACK_REVIEW=NOT_DONE", "LISTEN_REVIEW=NOT_DONE")),
    "pending_reality": "REALITY_CERTIFICATION=PENDING" in docs.get("VERSION.md", ""),
    "final_valid_default_no": "FINAL_VALID=NO" in docs.get("templates/FINAL_TEST_RESULT.md", ""),
    "versioned_parent_preserved": "NEEDS_VERSIONED_UPGRADE" in docs.get("VERSION.md", ""),
    "recent_use": "下次复用" in docs.get("RECENT_USE_LOG.md", ""),
    "roi_gate_paused": "ROI 与精确标签门禁当前暂停" in docs.get("SKILL.md", ""),
    "agents_draft_not_applied": "未写入全局或项目 AGENTS" in docs.get("source/AGENTS_PATCH_DRAFT.md", ""),
}
for name, passed in checks.items():
    if not passed:
        errors.append(f"RULE_CHECK_FAILED: {name}")

upstream = root / "source" / "UPSTREAM_CONTRACT.md"
upstream_blob = None
if upstream.is_file():
    data = upstream.read_bytes()
    upstream_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    checks["upstream_contract_exact_blob"] = upstream_blob == "9f2af2701adf303ffea504f9c67e0d750f7c7a28"
    if not checks["upstream_contract_exact_blob"]:
        errors.append(f"UPSTREAM_BLOB_MISMATCH: {upstream_blob}")

files = []
for path in sorted(root.rglob("*")):
    if path.is_file() and path != receipt:
        data = path.read_bytes()
        files.append({"path": str(path.relative_to(root)).replace("\\", "/"), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

result = {
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "LOCAL_STATIC_PACKAGE_ONLY",
    "root": str(root), "status": "PASS" if not errors else "FAIL",
    "required_files": required, "checks": checks, "errors": errors,
    "files": files, "upstream_git_blob": upstream_blob,
    "github_write_performed": False,
    "media_certification_performed": False,
    "reality_certification": "PENDING", "FINAL_VALID": "NO",
}
receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": result["status"], "file_count": len(files), "errors": errors, "receipt": str(receipt), "FINAL_VALID": "NO"}, ensure_ascii=False))
raise SystemExit(0 if not errors else 1)
