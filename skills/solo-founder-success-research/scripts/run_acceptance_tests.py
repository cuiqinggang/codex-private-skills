from pathlib import Path
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
checks = []

def run(script):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], text=True, capture_output=True)
    checks.append((script, p.returncode == 0, (p.stdout + p.stderr).strip()))

for script in ["validate_structure.py", "validate_sources.py", "detect_stale_records.py", "build_indexes.py"]:
    run(script)

cases = {
    "test_case_01_founder.md": ["失败", "时间线", "证据等级", "https://"],
    "test_case_02_product.md": ["MRR", "上游", "竞争", "单人维护"],
    "test_case_03_comparison.md": ["| 维度 |", "Marc Lou", "Pieter Levels", "Tony Dinh", "最适合学习"],
}
for name, terms in cases.items():
    path = ROOT / "tests/outputs" / name
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    missing = [t for t in terms if t not in text]
    checks.append((name, not missing, "missing=" + ",".join(missing) if missing else "all gates present"))

ok = all(x[1] for x in checks)
stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log = ROOT / "logs" / f"acceptance-{stamp}.log"
report = ROOT / "tests" / "ACCEPTANCE_REPORT.md"
lines = ["# Acceptance Report", "", f"Run: {datetime.now().isoformat(timespec='seconds')}", "",
         "| Check | Result | Evidence |", "|---|---|---|"]
for name, passed, evidence in checks:
    clean = evidence.replace("|", "\\|").replace("\n", "<br>")
    lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {clean} |")
lines += ["", f"Final: **{'PASS' if ok else 'FAIL'}**"]
payload = "\n".join(lines) + "\n"
report.write_text(payload, encoding="utf-8")
log.write_text(payload, encoding="utf-8")
print(f"ACCEPTANCE_{'PASS' if ok else 'FAIL'} report={report} log={log}")
sys.exit(0 if ok else 1)
