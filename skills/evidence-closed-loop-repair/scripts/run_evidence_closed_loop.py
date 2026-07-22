from __future__ import annotations
import argparse, json, subprocess, sys, shutil
from pathlib import Path
from common import write_json, sha256_file
from verify_contract import scan_one_root, markdown_report
from cold_extract_verify import main as _cold_main


def main() -> int:
    ap = argparse.ArgumentParser(description="Orchestrate full evidence-closed-loop verification")
    ap.add_argument("--root", required=True)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--archives", nargs="*", default=[])
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    contract_path = Path(args.contract).resolve()
    out = Path(args.out_dir).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    worktree = scan_one_root(root, contract, True)
    write_json(out / "worktree_verification.json", worktree)
    (out / "worktree_verification.md").write_text(markdown_report(worktree), encoding="utf-8")
    archive_results = []
    for i, a in enumerate(args.archives, 1):
        archive = Path(a).resolve()
        cold_dir = out / f"cold_{i}_{archive.suffix.lstrip('.')}"
        cp = subprocess.run([sys.executable, str(Path(__file__).with_name("cold_extract_verify.py")),
                             "--archive", str(archive), "--contract", str(contract_path), "--out-dir", str(cold_dir)])
        report = json.loads((cold_dir / "cold_extract_report.json").read_text(encoding="utf-8"))
        archive_results.append(report)
    statuses = [worktree["status"]] + [r["status"] for r in archive_results]
    final = "FAIL" if "FAIL" in statuses else ("PENDING" if "PENDING" in statuses else "PASS")
    summary = {"status": final, "worktree": worktree["status"], "archives": [{"path": r["archive"], "status": r["status"], "sha256": r["archive_sha256"]} for r in archive_results]}
    write_json(out / "FINAL_EVIDENCE_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if final == "PASS" else (3 if final == "PENDING" else 2)

if __name__ == "__main__":
    raise SystemExit(main())
