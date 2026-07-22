from pathlib import Path
import sys

REQUIRED = [
    "TASK_ID",
    "ROUND",
    "## 本轮目标",
    "## Codex 执行步骤",
    "## 测试要求",
    "## 成功判定",
    "## 失败停止条件",
    "END_TASK_ID",
]


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [item for item in REQUIRED if item not in text]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_plan_format.py <answer_raw.md>")
        return 2

    path = Path(sys.argv[1])
    missing = validate(path)
    if missing:
        print("FAIL: missing " + ", ".join(missing))
        return 1

    print("PASS: plan format contains required fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
