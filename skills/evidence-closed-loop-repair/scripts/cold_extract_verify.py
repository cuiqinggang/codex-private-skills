from __future__ import annotations
import argparse, json, shutil, tempfile
from pathlib import Path
from common import extract_archive, sha256_file, write_json
from verify_contract import scan_one_root, markdown_report


def main() -> int:
    ap = argparse.ArgumentParser(description="Cold-extract an archive into a new directory and verify it")
    ap.add_argument("--archive", required=True)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    archive = Path(args.archive).resolve()
    out = Path(args.out_dir).resolve()
    if out.exists():
        shutil.rmtree(out)
    extract_dir = out / "extracted"
    extract_status, extractor = extract_archive(archive, extract_dir)
    result = {"archive": str(archive), "archive_sha256": sha256_file(archive), "extract_status": extract_status, "extractor": extractor}
    if extract_status == "PASS":
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
        scan = scan_one_root(extract_dir, contract, True)
        result["verification"] = scan
        result["status"] = scan["status"]
        (out / "verification.md").parent.mkdir(parents=True, exist_ok=True)
        (out / "verification.md").write_text(markdown_report(scan), encoding="utf-8")
    else:
        result["status"] = "PENDING" if extract_status.startswith("PENDING") else "FAIL"
    write_json(out / "cold_extract_report.json", result)
    print(json.dumps({"status": result["status"], "archive": str(archive), "out": str(out)}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else (3 if result["status"] == "PENDING" else 2)

if __name__ == "__main__":
    raise SystemExit(main())
