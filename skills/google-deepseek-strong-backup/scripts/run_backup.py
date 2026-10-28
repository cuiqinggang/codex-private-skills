"""Thin V1.6 entry. Delegate to the existing official DSH launcher; no scheduler."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(r"C:\AI\DeepSeek-Harness-Trial")
SKILLS = BASE / "dsh-home-mature-agent" / "skills"
LAUNCH = Path(r"C:\AI\DSH-Acceleration-20261024\launch.py")
NAMES = ("google-deepseek-strong-backup", "ai-organization-v4-2",
         "dsh-extreme-effective-time", "dsh-mature-capabilities", "reuse-experience-brain")

def preflight():
    checks = {"existing_launcher": LAUNCH.is_file()}
    for name in NAMES:
        checks["skill:" + name] = (SKILLS / name / "SKILL.md").is_file()
    for name, version in (("dsh-mature-capabilities", "1.1.4"),
                          ("dsh-extreme-effective-time", "1.0.1")):
        p = SKILLS / name / "SKILL.md"
        text = p.read_text(encoding="utf-8-sig") if p.is_file() else ""
        checks["version:" + name] = bool(re.search(r"版本[：:]\s*(?:V)?" + re.escape(version) + r"\b", text))
    for resource in ("business_pack.py", "verify_order_pack.py", "run_resumable.py"):
        checks["resource:" + resource] = (SKILLS / "dsh-mature-capabilities" / "scripts" / resource).is_file()
    checks["official_runtime"] = (BASE / "dsh-0.2.1-rc.2-isolated/node_modules/@deepseek-ai/dsh/lib/bin.js").is_file()
    return {"status": "PASS" if all(checks.values()) else "BLOCKED", "checks": checks,
            "scope": "presence/version only; model and business execution separately verified"}

def main():
    p = argparse.ArgumentParser(description="谷深强备V1.6：本机DSH独立承接V4.2")
    p.add_argument("--check", action="store_true")
    p.add_argument("--task-file", type=Path)
    p.add_argument("--cwd", type=Path)
    p.add_argument("--mode", choices=["auto", "browser", "deep", "delivery", "docs", "automation"], default="auto")
    p.add_argument("--session-id")
    p.add_argument("--permission", choices=["read-only", "workspace-write"], default="workspace-write")
    a = p.parse_args()
    result = preflight()
    if a.check or result["status"] != "PASS":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 2
    task = a.task_file.read_text(encoding="utf-8-sig") if a.task_file else input("请输入本次完整任务：\n").strip()
    if not task.strip():
        p.error("任务不能为空")
    if not a.cwd and a.session_id:
        p.error("恢复必须提供原--cwd")
    if not a.cwd:
        entered = input("工作目录（回车使用DSH-Workspace）：").strip().strip('"')
        a.cwd = Path(entered or r"C:\Users\A\Documents\DSH-Workspace")
    cwd = a.cwd.resolve(strict=True)
    if not cwd.is_dir():
        p.error("--cwd必须是已存在且已授权的目录")
    instruction = ("本次使用谷深双擎强备系统V1.6，不依赖GPT/ChatGPT/Codex/Claude服务。"
        "先调用原生skill工具加载google-deepseek-strong-backup、ai-organization-v4-2、"
        "dsh-extreme-effective-time、dsh-mature-capabilities、reuse-experience-brain。"
        "按强备包HOST-BINDING显式绑定本机DSH宿主，原V4.2方法不改。"
        "读取匹配经验和原回执，完成虚拟成熟与冻结后完成实际任务，"
        "输出结果、必要QA及可恢复最小回执；workspace-write时保存RESULT.md，"
        "read-only时仅输出到终端，绝不尝试写文件；只读检查不算业务执行。"
        "禁止调用codex-cli-bridge或要求用户回GPT完成步骤。"
        "用户实际任务如下（恢复时继承已提交成果）：\n" + task)
    cmd = [sys.executable, str(LAUNCH), "--mode", a.mode, "--cwd", str(cwd),
           "--permission", a.permission]
    if a.session_id:
        cmd += ["--session-id", a.session_id]
    cmd += [instruction]
    env = dict(os.environ)
    # Child-only simulation of provider unavailability; never edit saved credentials.
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "CODEX_API_KEY"):
        env.pop(key, None)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.call(cmd, env=env, shell=False)

if __name__ == "__main__":
    raise SystemExit(main())
