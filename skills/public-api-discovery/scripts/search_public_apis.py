#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, default=Path(r"C:\AI\resources\public-apis\generated\public_apis_index.json"))
    ap.add_argument("--query", default="")
    ap.add_argument("--category")
    ap.add_argument("--auth", choices=["No", "apiKey", "OAuth", "Unknown"])
    ap.add_argument("--https", choices=["Yes", "No", "Unknown"])
    ap.add_argument("--cors", choices=["Yes", "No", "Unknown"])
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()
    rows = json.loads(args.index.read_text(encoding="utf-8"))
    terms = re.findall(r"[\w+-]+", args.query.lower())
    scored = []
    for row in rows:
        if args.category and args.category.lower() not in row["category"].lower(): continue
        if args.auth and row["auth"] != args.auth: continue
        if args.https and row["https"] != args.https: continue
        if args.cors and row["cors"] != args.cors: continue
        hay = f"{row['category']} {row['name']} {row['description']}".lower()
        if terms and not any(t in hay for t in terms): continue
        score = sum((3 if t in row["category"].lower() else 0) + (2 if t in row["name"].lower() else 0) + (1 if t in row["description"].lower() else 0) for t in terms)
        score += 2 if row["https"] == "Yes" else 0
        score += 1 if row["auth"] == "No" else 0
        score += 1 if row["cors"] == "Yes" else 0
        scored.append((score, row))
    results = [row for _, row in sorted(scored, key=lambda x: (-x[0], x[1]["name"].lower()))[:max(1, min(args.limit, 8))]]
    print(json.dumps({"count": len(results), "status": "catalog_unverified", "results": results}, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
