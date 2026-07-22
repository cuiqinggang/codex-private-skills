#!/usr/bin/env python3
"""验证一个可教学签名交付的证据和文件。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_STATUS = {"passed", "failed", "untested"}


def fail(message: str) -> None:
    raise SystemExit(f"验证失败：{message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="验证中文签名教学交付目录")
    parser.add_argument("--delivery-dir", required=True)
    args = parser.parse_args()
    root = Path(args.delivery_dir).resolve()
    manifest_path = root / "delivery.json"
    if not manifest_path.is_file():
        fail("缺少 delivery.json")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeError) as exc:
        fail(f"delivery.json 无法读取：{exc}")

    for key in ("name_confirmed", "character_integrity_passed", "human_three_write_status", "files", "privacy_reviewed"):
        if key not in data:
            fail(f"缺少字段 {key}")
    if data["name_confirmed"] is not True:
        fail("姓名尚未确认")
    if data["character_integrity_passed"] is not True:
        fail("字形完整性尚未通过")
    if data["privacy_reviewed"] is not True:
        fail("隐私检查尚未完成")

    status = data["human_three_write_status"]
    if status not in ALLOWED_STATUS:
        fail("human_three_write_status 必须是 passed、failed 或 untested")
    trials = data.get("trials", [])
    if status == "passed":
        if len(trials) != 3:
            fail("三写通过状态必须恰好包含 3 次记录")
        for index, trial in enumerate(trials, 1):
            if not trial.get("skeleton_consistent") or not trial.get("legible"):
                fail(f"第 {index} 次书写未同时通过骨架一致和辨识度")
            if not isinstance(trial.get("seconds"), (int, float)) or trial["seconds"] <= 0:
                fail(f"第 {index} 次耗时无效")
            if not isinstance(trial.get("pen_lifts"), int) or trial["pen_lifts"] < 0:
                fail(f"第 {index} 次抬笔数无效")

    files = data["files"]
    if not isinstance(files, list) or not files:
        fail("files 必须是非空列表")
    for relative in files:
        target = (root / relative).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            fail(f"文件路径越出交付目录：{relative}")
        if not target.is_file() or target.stat().st_size == 0:
            fail(f"交付文件不存在或为空：{relative}")

    label = "教学级交付" if status == "passed" else "视觉候选/待验证交付"
    print(f"验证通过：{label}；文件 {len(files)} 个；真人三写状态 {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
