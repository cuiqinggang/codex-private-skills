#!/usr/bin/env python
"""Search existing Codex skills and workspaces before starting a complex task."""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path


ROOTS = [
    Path(r"C:\Users\A\.codex\AGENTS.md"),
    Path(r"C:\Users\A\.codex\skills"),
    Path(r"C:\Users\A\.hermes\skills"),
    Path(r"K:\AI\skills"),
    Path(r"K:\AI\workspaces"),
]

TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".jsonl", ".html"}
SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".cache",
}
INTERESTING_MARKERS = (
    "skill",
    "agents",
    "sop",
    "rule",
    "checklist",
    "failure",
    "review",
    "pass",
    "usage",
    "lesson",
    "coordinate",
    "coordinates",
    "basemap",
    "sidebar",
    "browser",
    "bookmark",
    "fullscreen",
)


def configure_stdout() -> None:
    """Prefer UTF-8 stdout on Windows and degrade safely if the console rejects it."""

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        return
    except OSError:
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            return


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[\w\u4e00-\u9fff-]{2,}", text)}


def score_file(path: Path, task_tokens: set[str]) -> tuple[int, str]:
    score = 0
    snippet = ""
    name_tokens = tokenize(path.name)
    score += len(task_tokens & name_tokens) * 3
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:12000]
    except OSError:
        return score, snippet
    text_tokens = tokenize(text)
    score += len(task_tokens & text_tokens)
    lowered = text.lower()
    for token in task_tokens:
        if token in lowered:
            score += 2
    if score:
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        snippet = first_line[:180]
    return score, snippet


def has_name_interest(path: Path, task_tokens: set[str]) -> bool:
    name = path.name.lower()
    if any(marker in name for marker in INTERESTING_MARKERS):
        return True
    name_tokens = tokenize(name)
    return bool(task_tokens & name_tokens)


def iter_candidate_files(task_tokens: set[str], max_files_per_root: int) -> list[Path]:
    files: list[Path] = []
    for root in ROOTS:
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
            continue
        seen = 0
        for current, dirs, names in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in names:
                if seen >= max_files_per_root:
                    break
                path = Path(current) / name
                if path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                if not has_name_interest(path, task_tokens):
                    continue
                try:
                    if path.stat().st_size > 512_000:
                        continue
                except OSError:
                    continue
                files.append(path)
                seen += 1
            if seen >= max_files_per_root:
                break
    return files


def main() -> int:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="*", help="Task description to match against existing reusable assets.")
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--max-files-per-root", type=int, default=1200)
    args = parser.parse_args()

    task = " ".join(args.task).strip()
    task_tokens = tokenize(task)
    if not task_tokens:
        print("PREFLIGHT_REUSE_CHECK_DONE")
        print("No task text provided. Run again with a task description.")
        return 1

    scored = []
    for path in iter_candidate_files(task_tokens, args.max_files_per_root):
        score, snippet = score_file(path, task_tokens)
        if score:
            scored.append((score, path, snippet))
    scored.sort(key=lambda item: (-item[0], str(item[1]).lower()))

    print("PREFLIGHT_REUSE_CHECK_DONE")
    print("已检查技能包: C:\\Users\\A\\.codex\\skills (主用); C:\\Users\\A\\.hermes\\skills (坐标/桌面技能); K:\\AI\\skills (备份/历史参考)")
    print("已检查工作区: K:\\AI\\workspaces (备份/历史参考)")
    print("已检查规则: SKILL.md / AGENTS.md / SOP / RULE / CHECKLIST / FAILURE")
    if not scored:
        print("可复用内容: 未发现强匹配")
        print("本次采用路径: 可以新建方案；结束后判断是否沉淀为技能")
        return 0

    print("可复用内容:")
    for score, path, snippet in scored[: args.top]:
        print(f"- score={score} path={path}")
        if snippet:
            print(f"  note={snippet}")
    print("本次采用路径: 优先读取C盘高分技能；K盘命中仅作为备份/历史参考或C盘修复候选")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

