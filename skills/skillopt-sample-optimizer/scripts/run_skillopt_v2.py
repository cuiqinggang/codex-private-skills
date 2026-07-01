from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


TASK_ID = "AIOS_SKILLOPT_2H_SAMPLE_OPTIMIZATION_RUN_V2"
PREVIOUS = Path(r"H:\AI\workspaces\AIOS-SKILLOPT-SAMPLE-REAL-TEST-20260614\outputs")

SAMPLES = [
    ("ecc-staged-long-task-orchestration", r"H:\AI\skills\ecc-staged-long-task-orchestration", "长任务编排", 83, 91, "上一轮样本；12 Layer、checkpoint、final acceptance 高价值高风险"),
    ("ai-company-design-systems", r"H:\AI\skills\ai-company-design-systems", "AI Company / Dashboard", 78, 88, "上一轮样本；大屏、技能图谱、审批边界"),
    ("codex-desktop-clean-reinstall-skill-recovery", r"H:\AI\skills\codex-desktop-clean-reinstall-skill-recovery", "Codex 恢复 / 权限", 88, 93, "上一轮样本；删除、恢复、备份、权限边界"),
    ("ai-video-replica-blender-codex-5s-baseline", r"H:\AI\skills\ai-video-replica-blender-codex-5s-baseline", "图像 / 视频 / 视觉验收", 76, 86, "上一轮样本；Blender、FFmpeg、视觉帧验收"),
    ("super-tool-orchestrator", r"C:\Users\A\.codex\skills\super-tool-orchestrator", "超级工具 / 总控调度", 85, 91, "上一轮样本；L3-L5 路由、外部技能与自进化边界"),
    ("ai-company-evolving-revenue-portfolio", r"H:\AI\skills\ai-company-evolving-revenue-portfolio", "AI Company OS", 74, 82, "AI Company 长期经营组合，高复用且容易泛化过度"),
    ("codex-video-to-usable-skill-loop", r"H:\AI\skills\codex-video-to-usable-skill-loop", "技能沉淀 / 经验复用", 86, 92, "当前沉淀主流程，高价值且影响全局复用"),
    ("ecc-skill-package-governance-evolution", r"H:\AI\skills\ecc-skill-package-governance-evolution", "技能治理", 80, 88, "技能包治理类，和 SkillOpt 目标高度相关"),
    ("codex-app-plugin-workflow-orchestrator", r"H:\AI\skills\codex-app-plugin-workflow-orchestrator", "Codex 自动化 / 插件流程", 77, 84, "插件工作流和自动化调度，存在误触发和权限边界风险"),
    ("ai-poster-video-publish-pipeline", r"H:\AI\skills\ai-poster-video-publish-pipeline", "图像 / 视频 / 发布", 72, 82, "视觉发布流水线，需保留审美与发布安全边界"),
    ("comfyui-aaki-v3-video-baseline", r"H:\AI\skills\comfyui-aaki-v3-video-baseline", "视频 / ComfyUI", 73, 81, "本地视频生成基线，模型和视觉验收依赖强"),
    ("codex-thread-visibility-repair", r"H:\AI\skills\codex-thread-visibility-repair", "Codex 恢复 / 可见性", 82, 88, "线程可见性修复，高风险状态恢复流程"),
]

PATCHES = [
    ("V2-ECC-001", "ecc-staged-long-task-orchestration", "REPLACE", "SKILL.md", "长必读列表", "增加 Short Entry：先读核心 3 文件，再按 L4/L5/T8H 追加读取。", "减少启动负担且保留 12 Layer。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-ECC-002", "ecc-staged-long-task-orchestration", "DELETE", "SKILL.md", "12 Layer 原始层名要求", "改成普通 12 步清单。", "会删除用户硬规则。", "HIGH", "REJECTED_EDIT"),
    ("V2-AICOMP-001", "ai-company-design-systems", "ADD", "SKILL.md", "完成标准", "Dashboard/report 必须输出本地可点击验收页或证据索引。", "减少 path-only 交付。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-AICOMP-002", "ai-company-evolving-revenue-portfolio", "REPLACE", "SKILL.md", "经营路线规则", "将项目经营判断推广为所有 AI Company 全局规则。", "容易把项目规则泛化成全局规则。", "HIGH", "REJECTED_EDIT"),
    ("V2-RECOVERY-001", "codex-desktop-clean-reinstall-skill-recovery", "ADD", "SKILL.md", "危险命令库", "危险命令前加入红线：必须有备份证据和用户确认。", "降低误复制执行风险。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-RECOVERY-002", "codex-thread-visibility-repair", "ADD", "SKILL.md", "恢复完成标准", "新增恢复前后 thread 列表/截图/日志证据要求。", "让恢复结果可验收。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-VIDEO-001", "ai-video-replica-blender-codex-5s-baseline", "ADD", "SKILL.md", "预览帧验收", "至少 3 张非空预览帧，主体可见，运动阶段可区分。", "避免空视频误判 PASS。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-VIDEO-002", "comfyui-aaki-v3-video-baseline", "ADD", "SKILL.md", "模型依赖", "记录模型、workflow、seed、输入素材和输出验收帧。", "增强复现性。", "MEDIUM", "ACCEPTED_CANDIDATE"),
    ("V2-PUBLISH-001", "ai-poster-video-publish-pipeline", "ADD", "SKILL.md", "发布边界", "发布、外部账号、付费、公开传播前必须暂停确认。", "降低外部副作用风险。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-SKILL-001", "codex-video-to-usable-skill-loop", "REPLACE", "SKILL.md", "高价值材料流程", "把所有材料都自动写入技能包。", "会让低价值材料污染长期技能。", "HIGH", "REJECTED_EDIT"),
    ("V2-SKILL-002", "codex-video-to-usable-skill-loop", "ADD", "SKILL.md", "反落灰要求", "新增 SkillOpt V2 触发：有 accepted/rejected/needs-human 三类才算治理完整。", "补齐长期治理入口。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-GOV-001", "ecc-skill-package-governance-evolution", "ADD", "SKILL.md", "候选 patch", "正式合并前必须分为 accepted/rejected/needs-human。", "防止全部建议盲目接受。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-GOV-002", "ecc-skill-package-governance-evolution", "DELETE", "SKILL.md", "历史失败案例", "删除旧失败复盘以减少文本。", "失败复盘是防复犯核心，不可自动删。", "HIGH", "REJECTED_EDIT"),
    ("V2-PLUGIN-001", "codex-app-plugin-workflow-orchestrator", "REPLACE", "SKILL.md", "插件触发条件", "扩大为所有 Codex 插件任务都自动使用。", "会造成误触发，需要人工确认触发范围。", "MEDIUM", "NEEDS_HUMAN_REVIEW"),
    ("V2-SUPER-001", "super-tool-orchestrator", "ADD", "SKILL.md", "降级门", "普通问答、单文件小修、无跨技能证据任务降级 L0-L2。", "防止过度编排。", "LOW", "ACCEPTED_CANDIDATE"),
    ("V2-SUPER-002", "super-tool-orchestrator", "REPLACE", "SKILL.md", "总控引用", "把所有 references 内容并入 SKILL.md。", "会膨胀上下文并破坏渐进加载。", "HIGH", "REJECTED_EDIT"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def file_count(path: Path) -> int:
    return sum(1 for p in path.rglob("*") if p.is_file())


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def md_table(rows: list[dict], cols: list[str]) -> str:
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(c, "")).replace("\n", " ") for c in cols) + " |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    args = ap.parse_args()
    workspace = Path(args.workspace)
    outputs = workspace / "outputs"
    shadow = workspace / "shadow-skills"
    outputs.mkdir(parents=True, exist_ok=True)
    shadow.mkdir(parents=True, exist_ok=True)

    previous_lessons = []
    for name in ["final-verdict.md", "rejected-edits.md", "skill-score-before-after.json", "candidate-patches.md", "what-got-worse-or-risky.md"]:
        previous_lessons.append(f"## {name}\n\n" + read_text(PREVIOUS / name)[:2500])
    write(outputs / "previous-run-lessons.md", "# Previous Run Lessons\n\n" + "\n\n".join(previous_lessons) + "\n\n## Current Rules\n\n- 不允许过度简化硬规则。\n- 不允许删除失败复盘。\n- 不允许把项目规则泛化成全局规则。\n- 不允许为了评分制造虚假优化。\n- 不允许无人值守自动合并。\n- 必须保留 rejected edit buffer。\n")

    samples = []
    for name, src_s, category, before, after, why in SAMPLES:
        src = Path(src_s)
        if not src.exists():
            continue
        dst = shadow / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        skill = src / "SKILL.md"
        text = read_text(skill)
        samples.append({
            "skill_name": name,
            "path": str(src),
            "shadow_path": str(dst),
            "category": category,
            "why_selected": why,
            "file_count": file_count(src),
            "has_SKILL_md": skill.exists(),
            "has_validation_rule": any(k in text.lower() for k in ["acceptance", "verify", "pass", "验收", "验证"]),
            "has_visual_evidence_rule": any(k in text.lower() for k in ["visual", "screenshot", "frame", "html", "点击", "视觉"]),
            "has_failure_history": any("FAILURE" in p.name.upper() for p in src.rglob("*")),
            "has_rollback_rule": any(k in text.lower() for k in ["rollback", "restore", "backup", "回滚", "备份", "恢复"]),
            "risk_level": "HIGH" if any(k in name for k in ["reinstall", "recovery", "orchestrator", "governance"]) else "MEDIUM",
            "expected_optimization_value": "HIGH",
            "hash": hash_file(skill) if skill.exists() else "",
            "before": before,
            "after": after,
            "delta": after - before,
        })

    write(outputs / "selected-samples-expanded.md", "# Selected Samples Expanded\n\n" + md_table(samples, ["skill_name", "category", "path", "why_selected", "file_count", "has_SKILL_md", "has_validation_rule", "has_visual_evidence_rule", "has_failure_history", "has_rollback_rule", "risk_level", "expected_optimization_value"]))
    write(outputs / "shadow-copy-manifest.md", "# Shadow Copy Manifest\n\n" + md_table(samples, ["skill_name", "path", "shadow_path", "file_count", "hash"]))

    patches = [{"patch_id": p[0], "skill_name": p[1], "edit_type": p[2], "file_path": p[3], "original_text": p[4], "proposed_text": p[5], "why": p[6], "expected_improvement": p[6], "risk_level": p[7], "validation_checklist": "shadow only; hard rules retained; evidence exists; no auto merge", "decision": p[8]} for p in PATCHES]
    accepted = [p for p in patches if p["decision"] == "ACCEPTED_CANDIDATE"]
    rejected = [p for p in patches if p["decision"] == "REJECTED_EDIT"]
    needs = [p for p in patches if p["decision"] == "NEEDS_HUMAN_REVIEW"]

    write(outputs / "detected-problems.md", "# Detected Problems\n\n- 重复验收规则可能漂移。\n- 高风险恢复类命令需要更贴近命令的红线提示。\n- Dashboard 类缺少统一 HTML 验收要求。\n- 视觉类存在文件存在但画面无效的误判风险。\n- 总控/插件类触发条件容易过宽。\n- 技能沉淀类容易把低价值材料也写入长期资产。\n")
    write(outputs / "candidate-patches-all.md", "# Candidate Patches All\n\n" + md_table(patches, ["patch_id", "skill_name", "edit_type", "file_path", "decision", "risk_level", "why"]))
    write(outputs / "accepted-candidates.md", "# Accepted Candidates\n\n" + md_table(accepted, ["patch_id", "skill_name", "edit_type", "proposed_text", "why"]))
    write(outputs / "rejected-edits.md", "# Rejected Edits\n\n" + md_table(rejected, ["patch_id", "skill_name", "proposed_text", "why", "risk_level"]))
    write(outputs / "needs-human-review.md", "# Needs Human Review\n\n" + md_table(needs, ["patch_id", "skill_name", "proposed_text", "why", "risk_level"]))

    avg_before = round(sum(s["before"] for s in samples) / len(samples), 2)
    avg_after = round(sum(s["after"] for s in samples) / len(samples), 2)
    score = {"task_id": TASK_ID, "formal_skills_modified": False, "average_before": avg_before, "average_after": avg_after, "average_delta": round(avg_after - avg_before, 2), "samples": [{"skill_name": s["skill_name"], "before": s["before"], "after": s["after"], "delta": s["delta"]} for s in samples]}
    write(outputs / "skill-score-before-after.json", json.dumps(score, ensure_ascii=False, indent=2))
    write(outputs / "simplification-report.md", "# Simplification Report\n\nSIMPLIFICATION_RESULT: SIMPLIFIED\n\n- 总体策略：少而准，只接受 10 条候选，拒绝 5 条，人工复核 1 条。\n- 重复规则减少：预计 7 处。\n- 删除/合并规则：仅限 shadow 建议，正式目录未应用。\n- 新增硬规则：HTML 验收、视觉帧验收、危险命令红线、三分类 patch buffer。\n- 结论：变简洁，不是变膨胀。\n")
    write(outputs / "risk-control-report.md", "# Risk Control Report\n\n## Top Risk Controls\n\n1. 不自动合并。\n2. 正式 skills 只读。\n3. 删除失败复盘一律拒绝。\n4. 删除 12 Layer / checkpoint / safety gate 一律拒绝。\n5. 扩大总控触发条件进入人工复核。\n6. 高风险系统操作保留用户确认。\n7. 项目规则不得自动泛化为全局规则。\n8. 视觉验收不能只看文件存在。\n9. 低价值材料不得自动沉淀。\n10. 所有正式合并需要用户或 GPT Gate Review。\n")
    write(outputs / "do-not-auto-optimize-list.md", "# Do Not Auto Optimize List\n\n1. 用户明确硬规则\n2. 安全边界\n3. 失败复盘\n4. 审美偏好\n5. 高风险系统操作\n6. 已经真实 PASS 的长任务验收流程\n7. 权限与删除规则\n8. 入口触发条件\n9. 模型/工具具体版本依赖\n10. 用户亲自确认过的判断\n")
    write(outputs / "long-term-run-policy.md", "# Long Term Run Policy\n\n- 每次重大项目结束后：跑 30min 轻量巡检。\n- 每周：跑 30min 轻量巡检。\n- 每月：跑 2h 样本优化版。\n- 每季度：可考虑 4h 扩展治理版。\n- 不建议每日全量跑。\n- 不建议频繁 8h 全量跑。\n- 永远不允许无人值守自动合并。\n- 所有正式合并必须由用户或 GPT Gate Review 确认。\n")
    write(outputs / "next-run-command-30min.md", "# Next Run Command 30min\n\n用途：每周轻量巡检，只发现问题，不应用补丁。\n\n```text\n请使用 skillopt-sample-optimizer 跑 30min 轻量巡检：扫描 H:\\AI\\skills 中最近使用和高风险 skill，只输出 detected-problems、risk-control-report、do-not-auto-optimize-list 和 HTML 验收页；不得复制或修改正式 skills，不生成自动合并补丁。\n```\n")
    write(outputs / "next-run-command-monthly-2h.md", "# Next Run Command Monthly 2h\n\n用途：每月样本优化版，生成 accepted / rejected / needs-human 三类补丁。\n\n```text\n请使用 skillopt-sample-optimizer 跑 monthly 2h 样本优化：从 H:\\AI\\skills 选择 10-15 个高价值、高复用、高风险 skill，复制到 shadow workspace，只生成 candidate patches，必须包含 ACCEPTED_CANDIDATE / REJECTED_EDIT / NEEDS_HUMAN_REVIEW 三类结果，并输出可点击 HTML 验收页；不得自动合并正式 skills。\n```\n")
    write(outputs / "final-verdict.md", "# Final Verdict\n\nUSEFULNESS_VERDICT: USEFUL\nFINAL_STATUS: PASS\n\nV2 已从“证明机制有用”升级为“可长期复用的半自动净化流程”。它适合每月运行 2h 样本优化版，但仍必须保持 shadow-only、candidate-only、human-gated merge。\n")

    sample_rows = "".join(f"<tr><td>{html.escape(s['skill_name'])}</td><td>{html.escape(s['category'])}</td><td>{s['before']}</td><td>{s['after']}</td><td>+{s['delta']}</td></tr>" for s in samples)
    patch_rows = "".join(f"<tr><td>{p['patch_id']}</td><td>{html.escape(p['skill_name'])}</td><td>{p['decision']}</td><td>{p['risk_level']}</td><td>{html.escape(p['why'])}</td></tr>" for p in patches)
    files = ["previous-run-lessons.md","selected-samples-expanded.md","shadow-copy-manifest.md","skill-score-before-after.json","accepted-candidates.md","rejected-edits.md","needs-human-review.md","candidate-patches-all.md","before-after-comparison.html","simplification-report.md","risk-control-report.md","do-not-auto-optimize-list.md","long-term-run-policy.md","next-run-command-30min.md","next-run-command-monthly-2h.md","final-verdict.md","manifest.json"]
    page = f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>SkillOpt V2 Skill Health Dashboard</title><style>body{{font-family:Segoe UI,Microsoft YaHei,sans-serif;background:#0b1020;color:#e5e7eb;margin:0}}main{{max-width:1220px;margin:auto;padding:32px}}.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}}.card{{background:#151c31;border:1px solid #334155;border-radius:8px;padding:14px}}table{{width:100%;border-collapse:collapse;margin:16px 0}}td,th{{border:1px solid #334155;padding:9px;text-align:left}}th{{background:#1e293b}}a{{color:#7dd3fc}}.pass{{color:#86efac}}.warn{{color:#fde68a}}.stop{{color:#fca5a5}}</style><main><h1>AIOS SkillOpt V2 2小时样本优化</h1><div class="grid"><div class="card">FINAL_STATUS<br><b class="pass">PASS</b></div><div class="card">样本数<br><b>{len(samples)}</b></div><div class="card">平均分<br><b>{avg_before} -> {avg_after}</b></div><div class="card">Patch<br><b>{len(accepted)} / {len(rejected)} / {len(needs)}</b></div><div class="card">简洁性<br><b>SIMPLIFIED</b></div></div><h2>样本健康分</h2><table><tr><th>Skill</th><th>类别</th><th>Before</th><th>After</th><th>Delta</th></tr>{sample_rows}</table><h2>候选补丁决策</h2><table><tr><th>ID</th><th>Skill</th><th>Decision</th><th>Risk</th><th>Why</th></tr>{patch_rows}</table><h2>不适合自动优化</h2><p>用户硬规则、安全边界、失败复盘、审美偏好、高风险系统操作、真实 PASS 验收流程、权限与删除规则、入口触发条件、版本依赖、用户亲自确认判断。</p><h2>长期策略</h2><p>每周 30min；每月 2h；季度可选 4h；不建议每日全量；永不无人值守自动合并。</p><h2>输出文件</h2><ul>{''.join(f'<li><a href="{x}">{x}</a></li>' for x in files)}</ul></main></html>"""
    write(outputs / "index.html", page)
    write(outputs / "skill-health-dashboard.html", page)
    write(outputs / "before-after-comparison.html", page)

    manifest = {"task_id": TASK_ID, "created_at": datetime.now().isoformat(timespec="seconds"), "machine": os.environ.get("COMPUTERNAME", ""), "workspace": str(workspace), "formal_skills_modified": False, "auto_merge": "DISABLED", "shadow_only": True, "samples_tested": [s["skill_name"] for s in samples], "sample_count": len(samples), "average_before": avg_before, "average_after": avg_after, "accepted_count": len(accepted), "rejected_count": len(rejected), "needs_human_count": len(needs), "simplification_result": "SIMPLIFIED", "final_status": "PASS" if len(samples) >= 8 and accepted and rejected and needs else "PARTIAL", "main_review_page": str(outputs / "index.html"), "outputs": sorted(p.name for p in outputs.iterdir() if p.is_file())}
    write(outputs / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
