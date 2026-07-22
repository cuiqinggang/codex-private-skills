from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, zipfile, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFY = HERE / "verify_contract.py"
COLD = HERE / "cold_extract_verify.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def make_contract(root: Path) -> Path:
    locked = root / "01_core.txt"
    contract = {
        "schema_version": "1.0",
        "task_id": "SELF-TEST",
        "root": ".",
        "exclude_globs": ["evidence/**"],
        "text_encodings": ["utf-8"],
        "required": [{"id":"qwen","pattern":"Qwen（阿里千问）","mode":"literal","case_sensitive":True,"scope_globs":["**/*.txt","**/*.py"],"min_count":2,"max_count":None,"check_filenames":True}],
        "forbidden": [{"id":"grok","pattern":"Grok","mode":"literal","case_sensitive":False,"scope_globs":["**/*"],"max_count":0,"check_filenames":True},
                      {"id":"xai","pattern":"xAI","mode":"literal","case_sensitive":False,"scope_globs":["**/*"],"max_count":0,"check_filenames":True}],
        "locked_files": [{"path":"01_core.txt","sha256":sha(locked)}],
        "mirrors": [{"left":"0/07.txt","right":"1/07.txt","mode":"bytes"}],
        "derived_relations": [{"target":"0/07.txt","sources":["01_core.txt","03_prompt.txt"],"mode":"concatenate","separator":""}],
        "deliverables": [],
        "semantic_checks": [],
        "pending_checks": []
    }
    p = root / "CHANGE_CONTRACT.json"
    p.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def build_good(root: Path):
    root.mkdir(parents=True)
    (root / "0").mkdir(); (root / "1").mkdir()
    (root / "01_core.txt").write_text("CORE\n", encoding="utf-8")
    (root / "03_prompt.txt").write_text("Qwen（阿里千问）\n", encoding="utf-8")
    data = (root / "01_core.txt").read_bytes() + (root / "03_prompt.txt").read_bytes()
    (root / "0/07.txt").write_bytes(data)
    (root / "1/07.txt").write_bytes(data)
    (root / "build.py").write_text("MODEL='Qwen（阿里千问）'\n", encoding="utf-8")


def zip_tree(root: Path, out: Path):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file() and p != out:
                z.write(p, p.relative_to(root))


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Self-test the evidence-closed-loop validator")
    ap.add_argument("--output", help="Optional JSON output path; omitted means do not modify the skill folder")
    args = ap.parse_args()
    results = {}
    with tempfile.TemporaryDirectory(prefix="eclr-selftest-") as td:
        base = Path(td)
        good = base / "good"
        build_good(good)
        contract = make_contract(good)
        cp_good = run([sys.executable, str(VERIFY), "--root", str(good), "--contract", str(contract), "--out-dir", str(base/"good_evidence"), "--no-recursive-archives"])
        results["good_fixture"] = {"returncode": cp_good.returncode, "stdout": cp_good.stdout, "stderr": cp_good.stderr, "status": "PASS" if cp_good.returncode == 0 else "FAIL"}

        bad = base / "bad"
        shutil.copytree(good, bad)
        (bad / "0/07.txt").write_text("CORE\nGrok\n", encoding="utf-8")
        # mirror intentionally stale and package intentionally bad
        bad_contract = make_contract(bad)
        cp_bad = run([sys.executable, str(VERIFY), "--root", str(bad), "--contract", str(bad_contract), "--out-dir", str(base/"bad_evidence"), "--no-recursive-archives"])
        results["bad_fixture"] = {"returncode": cp_bad.returncode, "stdout": cp_bad.stdout, "stderr": cp_bad.stderr, "status": "PASS" if cp_bad.returncode != 0 else "FAIL"}

        archive = base / "good.zip"
        zip_tree(good, archive)
        cp_cold = run([sys.executable, str(COLD), "--archive", str(archive), "--contract", str(contract), "--out-dir", str(base/"cold")])
        results["cold_zip"] = {"returncode": cp_cold.returncode, "stdout": cp_cold.stdout, "stderr": cp_cold.stderr, "status": "PASS" if cp_cold.returncode == 0 else "FAIL"}

    overall = "PASS" if all(r["status"] == "PASS" for r in results.values()) else "FAIL"
    output = {"overall": overall, "tests": results}
    if args.output:
        out = Path(args.output).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if overall == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
