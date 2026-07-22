#!/usr/bin/env python3
"""Anonymous service registry for the WeChat AI free-service pilot."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("user_value", "ai_advantage", "repeatability", "remote_fit", "wechat_fit", "free_feasibility", "risk")
WEIGHTS = {"user_value": 5, "ai_advantage": 4, "repeatability": 4, "remote_fit": 3, "wechat_fit": 2, "free_feasibility": 2, "risk": -4}
ALLOWED_RESULTS = {"success", "partial", "failure"}


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def paths(state_dir: str):
    root = Path(state_dir)
    return root, root / "services.json", root / "cases.jsonl"


def score(values):
    return sum(values[key] * WEIGHTS[key] for key in FIELDS)


def grade(total, risk):
    if total >= 75 and risk <= 2:
        return "A"
    if 60 <= total <= 74 and risk <= 2:
        return "B"
    return "C"


def read_cases(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def calculate_state(service_id, cases):
    relevant = [row for row in cases if row["service_id"] == service_id]
    total = len(relevant)
    success = [row for row in relevant if row["status"] == "success"]
    incomplete = sum(row["status"] in {"partial", "failure"} for row in relevant)
    if total >= 4 and incomplete * 2 >= total:
        return "paused"
    if len(success) >= 8:
        avg_sat = sum(row["satisfaction"] for row in success) / len(success)
        avg_minutes = sum(row["minutes"] for row in success) / len(success)
        if avg_sat >= 4 and avg_minutes <= 15:
            return "priority"
    if len(success) >= 3:
        return "active"
    return "candidate"


def refresh_states(services, cases):
    for service in services:
        service["state"] = calculate_state(service["id"], cases)


def command_init(args):
    root, services_path, cases_path = paths(args.state_dir)
    root.mkdir(parents=True, exist_ok=True)
    if not services_path.exists():
        seed = Path(__file__).resolve().parent.parent / "references" / "seed-services.json"
        save_json(services_path, load_json(seed, []))
    cases_path.touch(exist_ok=True)
    print(f"REGISTRY_INIT=PASS SERVICES={len(load_json(services_path, []))} STATE_DIR={root}")


def command_list(args):
    _, services_path, cases_path = paths(args.state_dir)
    services = load_json(services_path, [])
    refresh_states(services, read_cases(cases_path))
    rows = sorted(services, key=lambda row: (-row["total_score"], row["name"]))[: args.top]
    print("ID\t分数\t类别\t状态\t名称")
    for row in rows:
        print(f'{row["id"]}\t{row["total_score"]}\t{row["class"]}\t{row["state"]}\t{row["name"]}')


def command_add(args):
    _, services_path, _ = paths(args.state_dir)
    services = load_json(services_path, [])
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.service_id):
        raise SystemExit("service-id 必须是小写字母、数字和连字符")
    if any(row["id"] == args.service_id for row in services):
        raise SystemExit("服务 ID 已存在")
    values = {key: getattr(args, key.replace("_", "-"), None) for key in ()}
    values = {key: getattr(args, key) for key in FIELDS}
    if any(not 0 <= value <= 5 for value in values.values()):
        raise SystemExit("所有评分必须在 0 到 5 之间")
    total = score(values)
    services.append({"id": args.service_id, "name": args.name, "category": args.category, "scores": values, "total_score": total, "class": grade(total, values["risk"]), "state": "candidate", "capability": args.capability})
    save_json(services_path, services)
    print(f"REGISTRY_ADD=PASS SERVICE_ID={args.service_id} SCORE={total}")


def command_record(args):
    _, services_path, cases_path = paths(args.state_dir)
    services = load_json(services_path, [])
    if not any(row["id"] == args.service_id for row in services):
        raise SystemExit("未知服务 ID")
    if args.status not in ALLOWED_RESULTS or args.minutes < 0 or not 1 <= args.satisfaction <= 5:
        raise SystemExit("案例参数不合法")
    row = {"service_id": args.service_id, "status": args.status, "minutes": args.minutes, "satisfaction": args.satisfaction, "reusable": args.reusable == "yes", "recorded_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    cases_path.parent.mkdir(parents=True, exist_ok=True)
    with cases_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"REGISTRY_RECORD=PASS SERVICE_ID={args.service_id}")


def command_report(args):
    _, services_path, cases_path = paths(args.state_dir)
    services = load_json(services_path, [])
    cases = read_cases(cases_path)
    refresh_states(services, cases)
    counts = {key: 0 for key in ("candidate", "active", "priority", "paused")}
    for row in services:
        counts[row["state"]] += 1
    print(f"REGISTRY_REPORT=PASS SERVICES={len(services)} CASES={len(cases)}")
    for key in counts:
        print(f"{key}={counts[key]}")


def parser():
    result = argparse.ArgumentParser(description="微信 AI 免费服务匿名登记与进化")
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("init", "list", "add", "record", "report"):
        item = sub.add_parser(name)
        item.add_argument("--state-dir", required=True)
        item.set_defaults(handler=globals()[f"command_{name}"])
        if name == "list":
            item.add_argument("--top", type=int, default=20)
        elif name == "add":
            item.add_argument("--service-id", required=True)
            item.add_argument("--name", required=True)
            item.add_argument("--category", required=True)
            for field in FIELDS:
                item.add_argument("--" + field.replace("_", "-"), dest=field, type=int, required=True)
            item.add_argument("--capability", default="可用能力需按具体材料确认")
        elif name == "record":
            item.add_argument("--service-id", required=True)
            item.add_argument("--status", choices=sorted(ALLOWED_RESULTS), required=True)
            item.add_argument("--minutes", type=float, required=True)
            item.add_argument("--satisfaction", type=int, choices=range(1, 6), required=True)
            item.add_argument("--reusable", choices=("yes", "no"), required=True)
    return result


if __name__ == "__main__":
    ns = parser().parse_args()
    ns.handler(ns)
