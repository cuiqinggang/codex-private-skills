from __future__ import annotations
import argparse, json
from pathlib import Path
from common import tree_manifest, write_json


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare two trees by relative paths and SHA-256")
    ap.add_argument("tree_a")
    ap.add_argument("tree_b")
    ap.add_argument("--out", default="TREE_COMPARE.json")
    args = ap.parse_args()
    a, b = Path(args.tree_a).resolve(), Path(args.tree_b).resolve()
    ma, mb = tree_manifest(a), tree_manifest(b)
    paths = sorted(set(ma) | set(mb))
    diffs = []
    for p in paths:
        if p not in ma:
            diffs.append({"path": p, "status": "ONLY_B", "b": mb[p]})
        elif p not in mb:
            diffs.append({"path": p, "status": "ONLY_A", "a": ma[p]})
        elif ma[p] != mb[p]:
            diffs.append({"path": p, "status": "HASH_MISMATCH", "a": ma[p], "b": mb[p]})
    result = {"status": "PASS" if not diffs else "FAIL", "files_a": len(ma), "files_b": len(mb), "diffs": diffs}
    write_json(Path(args.out), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not diffs else 2

if __name__ == "__main__":
    raise SystemExit(main())
