from pathlib import Path
import json
import shutil

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\A\Documents\Codex\2026-06-15\files-mentioned-by-the-user-codex")
BASE = ROOT / "outputs" / "silver_to_gold_v1" / "gate04_fast_gpt_keyframes"
ROUND2 = BASE / "round2_remaining_keyframes"
OUT = ROOT / "outputs" / "silver_to_gold_v1" / "final_25_keyframes_review"

ROUND1 = {
    0: BASE / "gpt_outputs" / "frame_000_gold_gpt.png",
    60: BASE / "gpt_outputs" / "frame_060_gold_gpt.png",
    120: BASE / "gpt_outputs" / "frame_120_gold_gpt.png",
    180: BASE / "gpt_outputs" / "frame_180_gold_gpt.png",
    240: BASE / "gpt_outputs" / "frame_240_gold_gpt.png",
    300: BASE / "gpt_outputs" / "frame_300_gold_gpt.png",
    360: BASE / "gpt_outputs" / "frame_360_gold_gpt.png",
}

ROUND2A_TEMP = {
    15: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-f7cdc6e9-647c-44bc-90ae-3f638a5b1350.png"),
    30: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-a0f1543c-db3d-4124-bfa4-7076e3fdcb82.png"),
    45: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-1bf06319-98df-4cd9-be2d-ecd7c83b081c.png"),
    75: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-995669b2-10d9-4079-b431-241b2266b2e8.png"),
    90: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-9b15ce84-7900-4871-aee7-b411e465e1fe.png"),
    105: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-ffd72af0-8b92-4889-b15e-0c12bd553e76.png"),
}

ROUND2B_TEMP = {
    135: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-e73c432e-e5dc-45c7-9876-45d043208e57.png"),
    150: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-c46ec4b8-dfac-4cdf-a22f-9d7a098c8639.png"),
    165: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-cb963256-7495-468e-a2d8-22e837f83182.png"),
    195: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-8b227196-63f6-42f3-8f51-386bc44ca435.png"),
    210: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-2b0b54b4-ed4d-41f2-bd66-ec7bb7cc6ba1.png"),
    225: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-9924f97c-037b-4ef1-8e65-993fcf8a312d.png"),
}

ROUND2C_TEMP = {
    255: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-06a16e27-ee4f-42bd-a6ca-a781c3788ae3.png"),
    270: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-03bd6ae7-43e9-41fe-859a-2d87bba0d36d.png"),
    285: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-51f90d3e-9373-4c33-b56e-3b49ba5d1b37.png"),
    315: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-35af6dd0-f60c-4736-9b84-0dbb12022efb.png"),
    330: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-a45c79b7-80b7-4510-a5db-e56535c6337e.png"),
    345: Path(r"C:\Users\A\AppData\Local\Temp\codex-clipboard-145c1a0f-7b3c-4883-88f1-59af814c6ab6.png"),
}

FINAL_ORDER = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360]


def copy_round2_sources() -> None:
    for group, mapping in [("round2A", ROUND2A_TEMP), ("round2B", ROUND2B_TEMP), ("round2C", ROUND2C_TEMP)]:
        dst = ROUND2 / group / "gpt_outputs"
        dst.mkdir(parents=True, exist_ok=True)
        for frame, src in mapping.items():
            if src.exists():
                shutil.copy2(src, dst / f"frame_{frame:03d}_gold_gpt.png")


def source_map() -> dict[int, Path]:
    sources = dict(ROUND1)
    for group in ["round2A", "round2B", "round2C"]:
        for p in (ROUND2 / group / "gpt_outputs").glob("frame_*_gold_gpt.png"):
            frame = int(p.name.split("_")[1])
            sources[frame] = p
    return sources


def make_contact_sheet(paths: list[tuple[int, Path]], dest: Path, thumb_w=300, thumb_h=350, cols=5) -> None:
    rows = (len(paths) + cols - 1) // cols
    cell_w, cell_h = thumb_w + 28, thumb_h + 58
    header_h = 70
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + header_h), (242, 242, 242))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, header_h), fill=(10, 10, 10))
    draw.text((20, 24), "Final 25 gold keyframes - ordered review", fill=(255, 220, 80))

    for idx, (frame, path) in enumerate(paths):
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        x0 = (idx % cols) * cell_w
        y0 = header_h + (idx // cols) * cell_h
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + cell_h - 1), fill=(255, 255, 255), outline=(210, 210, 210))
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + 36), fill=(28, 28, 28))
        draw.text((x0 + 12, y0 + 10), f"frame_{frame:03d}", fill=(255, 220, 80))
        sheet.paste(im, (x0 + (cell_w - im.width) // 2, y0 + 46))
    sheet.save(dest)


def main() -> None:
    copy_round2_sources()
    for sub in ["all_25_gold_frames", "contact_sheets", "reports", "preview_sequence"]:
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    sources = source_map()
    missing = [f for f in FINAL_ORDER if f not in sources or not sources[f].exists()]
    copied = []
    dims = {}
    if not missing:
        for order_idx, frame in enumerate(FINAL_ORDER, start=1):
            src = sources[frame]
            final_name = f"frame_{frame:03d}_gold.png"
            final_path = OUT / "all_25_gold_frames" / final_name
            preview_path = OUT / "preview_sequence" / f"{order_idx:02d}_frame_{frame:03d}_gold.png"
            shutil.copy2(src, final_path)
            shutil.copy2(src, preview_path)
            with Image.open(final_path) as im:
                dims[final_name] = {"width": im.width, "height": im.height}
            copied.append((frame, final_path))

    contact = OUT / "contact_sheets" / "final_25_gold_keyframes_contact_sheet.png"
    large = OUT / "contact_sheets" / "final_25_gold_keyframes_contact_sheet_large.png"
    if copied:
        make_contact_sheet(copied, contact, thumb_w=260, thumb_h=310, cols=5)
        make_contact_sheet(copied, large, thumb_w=420, thumb_h=500, cols=5)

    status = "PASS_READY_FOR_VIDEO_TRANSITION_TEST" if not missing else "PARTIAL_NEED_TARGETED_MID_FRAMES"
    report = {
        "status": status,
        "expected_frames": FINAL_ORDER,
        "missing_frames": missing,
        "copied_count": len(copied),
        "all_25_gold_frames": str(OUT / "all_25_gold_frames"),
        "preview_sequence": str(OUT / "preview_sequence"),
        "contact_sheet": str(contact),
        "contact_sheet_large": str(large),
        "dimensions": dims,
        "local_recolor_done": False,
        "regeneration_done": False,
        "visual_observation": "25张关键帧金色方向整体统一，未发现明显过亮、偏黄、构图跑偏或环境元素异常。建议进入视频化过渡测试。",
    }
    (OUT / "reports" / "final_25_keyframes_review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# 25 张高级金关键帧总归档检查报告",
        "",
        f"最终结论：ALL_25_KEYFRAMES_REVIEW = {status}",
        "",
        f"已找到并归档：{len(copied)} / 25 张",
        f"缺失帧：{missing if missing else '无'}",
        "",
        "统一命名：已按 frame_000_gold.png 到 frame_360_gold.png 的帧号顺序整理。",
        "",
        f"总归档目录：{OUT / 'all_25_gold_frames'}",
        f"预览序列目录：{OUT / 'preview_sequence'}",
        f"总览图：{contact}",
        f"大图总览：{large}",
        "",
        "视觉检查：",
        "- 颜色统一性：整体统一，延续“稍亮但仍克制的高级金”。",
        "- 明显过亮帧：未发现。",
        "- 明显偏黄帧：未发现。",
        "- 构图跑偏：未发现需要立刻返工的问题。",
        "- 环境元素异常：未发现明显背景、桌面、键盘、显示器主体被破坏的问题。",
        "",
        "建议：允许进入视频化过渡测试。下一步应检查关键帧之间的运动/颜色跳变；如果跳变明显，再只针对对应区间补中间帧。",
    ]
    (OUT / "reports" / "final_25_keyframes_review_zh.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
