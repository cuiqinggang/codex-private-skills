from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--output", default="SELF_TEST_RESULT.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    contract = json.loads((root / "CHANGE_CONTRACT.json").read_text(encoding="utf-8"))
    checks = []

    def add(name: str, ok: bool, detail):
        checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    for rel in contract["required_files"]:
        add(f"必需文件:{rel}", (root / rel).is_file(), str(root / rel))

    runtime_files = sorted((root / "运行提示词").glob("*.md"))
    runtime_text = "\n".join(p.read_text(encoding="utf-8") for p in runtime_files)
    runtime_names = "\n".join(p.name for p in runtime_files)

    for s in contract["required_runtime_strings"]:
        add(f"运行必需字符串:{s}", s in runtime_text, runtime_text.count(s))
    for s in contract["forbidden_runtime_strings"]:
        add(f"运行禁止字符串:{s}", s not in runtime_text and s not in runtime_names, runtime_text.count(s))

    for rel, limit in contract["prompt_char_limits"].items():
        p = root / rel
        n = len(p.read_text(encoding="utf-8")) if p.is_file() else -1
        add(f"提示词体积:{rel}", 0 <= n <= limit, {"actual": n, "limit": limit})

    a_source = root / "运行提示词/01_A层统一极限提示词.md"
    mirrors = [
        root / "桌面执行版模板/0号文件夹_源模板_不要直接测试/01_A层统一极限提示词.txt",
        root / "桌面执行版模板/1号文件夹_稳定运行母版_V9.5.1/03_A层统一极限提示词.txt",
    ]
    for m in mirrors:
        add(f"A统一提示词镜像:{m.relative_to(root).as_posix()}", m.is_file() and m.read_bytes() == a_source.read_bytes(), {"source": sha(a_source), "mirror": sha(m) if m.is_file() else None})

    a_prompt_sources = [p for p in (root / "运行提示词").glob("*A层*提示词*.md")]
    add("A源提示词唯一", len(a_prompt_sources) == 1, [p.name for p in a_prompt_sources])

    c_text = (root / "运行提示词/03_C层非回退强审核提示词.md").read_text(encoding="utf-8")
    add("C层不接收A槽位", all(x not in c_text for x in ["A_GPT_Final", "A_Qwen_Final", "A_DeepSeek_Final", "A_Initial"]), "C仅允许原始问题+B_Final")

    b_text = (root / "运行提示词/02_B层选择性强点收敛提示词.md").read_text(encoding="utf-8")
    add("B层三份A槽位齐全", all(x in b_text for x in ["A_GPT_Final", "A_Qwen_Final", "A_DeepSeek_Final"]), "三槽")

    immediate = ["00_A_Initial零流程基线提示词.md", "01_A层统一极限提示词.md", "02_B层选择性强点收敛提示词.md", "03_C层非回退强审核提示词.md", "04_最终匿名质量与成本评测提示词.md"]
    for name in immediate:
        t = (root / "运行提示词" / name).read_text(encoding="utf-8")
        add(f"立即执行启动:{name}", "立即执行命令" in t and "不要确认收件" in t, None)

    result_files = [
        "02_A_Initial结果.txt", "04_A_GPT完整回复_含Raw与Final.txt", "05_A_Qwen完整回复_含Raw与Final.txt",
        "06_A_DeepSeek完整回复_含Raw与Final.txt", "08_B层完整回复.txt", "10_C层完整回复.txt",
        "11_C_Final纯净最终答案.txt", "13_最终评测报告.txt"
    ]
    master = root / "桌面执行版模板/1号文件夹_稳定运行母版_V9.5.1"
    for name in result_files:
        p = master / name
        add(f"母版结果为空:{name}", p.is_file() and p.read_text(encoding="utf-8") == "\n", p.stat().st_size if p.exists() else None)

    overall = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    result = {"overall": overall, "root": str(root), "checks": checks, "pending": contract["pending"]}
    out = root / args.output
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall": overall, "checks": len(checks), "failed": [c["name"] for c in checks if c["status"] == "FAIL"]}, ensure_ascii=False, indent=2))
    return 0 if overall == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
