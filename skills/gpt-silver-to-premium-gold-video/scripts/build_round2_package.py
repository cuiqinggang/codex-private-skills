from pathlib import Path
import json
import shutil

import cv2
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\A\Documents\Codex\2026-06-15\files-mentioned-by-the-user-codex")
VIDEO = Path(r"C:\Users\A\Documents\xwechat_files\wxid_bq3n41o6t4o721_699b\msg\video\2026-06\55b8afced91c76b1c12f627d8cbc9f75.mp4")
BASE = ROOT / "outputs" / "silver_to_gold_v1" / "gate04_fast_gpt_keyframes"
OUT = BASE / "round2_remaining_keyframes"
STYLE = BASE / "style_reference" / "gold_style_C_locked.png"
EXAMPLE_300 = BASE / "gpt_outputs" / "frame_300_gold_gpt.png"
EXAMPLE_360 = BASE / "gpt_outputs" / "frame_360_gold_gpt.png"

GROUPS = {
    "round2A": [15, 30, 45, 75, 90, 105],
    "round2B": [135, 150, 165, 195, 210, 225],
    "round2C": [255, 270, 285, 315, 330, 345],
}

PROMPT = """把图中的银色金属材质改成和参考图一致的“稍亮但仍克制的高级金”，
其他所有内容保持原样。

只改银色金属部分。
不要改构图、背景、桌面、键盘、显示器、屏幕文字、阴影、反射关系、物体形状、位置和线条结构。
不要重新生成整张图。
不要做拼图。
不要做 A/B/C 多版本。

金色要求：
高级、真实、有金属反射；
稍亮，但仍然克制；
不要土黄、塑料黄、脏金、过曝金。

每张图片单独生成一个最终 gold 版本。
命名规则示例：
frame_015_gold.png
frame_030_gold.png
frame_045_gold.png
以此类推。
"""


def ensure_dirs(group_dir: Path) -> None:
    for name in [
        "original_frames",
        "style_reference",
        "gpt_prompt",
        "gpt_outputs",
        "contact_sheets",
        "reports",
    ]:
        (group_dir / name).mkdir(parents=True, exist_ok=True)


def extract_frame(cap, frame_no: int, dest: Path) -> tuple[bool, tuple[int, int] | None]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ok, frame = cap.read()
    if not ok:
        return False, None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    Image.fromarray(frame).save(dest)
    h, w = frame.shape[:2]
    return True, (w, h)


def make_contact_sheet(group: str, frame_paths: list[Path], dest: Path) -> None:
    thumbs = []
    for p in frame_paths:
        im = Image.open(p).convert("RGB")
        im.thumbnail((360, 420))
        canvas = Image.new("RGB", (380, 470), "white")
        x = (380 - im.width) // 2
        canvas.paste(im, (x, 35))
        draw = ImageDraw.Draw(canvas)
        label = p.stem.replace("_original", "")
        draw.rectangle((0, 0, 379, 34), fill=(20, 20, 20))
        draw.text((12, 9), label, fill=(255, 220, 80))
        thumbs.append(canvas)

    cols = 3
    rows = 2
    sheet = Image.new("RGB", (cols * 380, rows * 470 + 60), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, 60), fill=(12, 12, 12))
    draw.text((18, 20), f"{group} original keyframes for GPT silver-to-gold", fill=(255, 220, 80))
    for i, thumb in enumerate(thumbs):
        x = (i % cols) * 380
        y = 60 + (i // cols) * 470
        sheet.paste(thumb, (x, y))
    sheet.save(dest)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(VIDEO))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {VIDEO}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    all_reports = {}

    for group, frames in GROUPS.items():
        group_dir = OUT / group
        ensure_dirs(group_dir)

        if STYLE.exists():
            shutil.copy2(STYLE, group_dir / "style_reference" / "gold_style_C_locked.png")
        if EXAMPLE_300.exists():
            shutil.copy2(EXAMPLE_300, group_dir / "style_reference" / "accepted_example_frame_300_gold.png")
        if EXAMPLE_360.exists():
            shutil.copy2(EXAMPLE_360, group_dir / "style_reference" / "accepted_example_frame_360_gold.png")

        prompt_path = group_dir / "gpt_prompt" / "GPT_SIMPLE_GOLD_C_PROMPT.txt"
        prompt_path.write_text(PROMPT, encoding="utf-8")

        extracted = []
        skipped = []
        dims = {}
        for frame_no in frames:
            out_path = group_dir / "original_frames" / f"frame_{frame_no:03d}_original.png"
            ok, size = extract_frame(cap, frame_no, out_path)
            if ok:
                extracted.append(out_path)
                dims[out_path.name] = {"width": size[0], "height": size[1]}
            else:
                skipped.append(frame_no)

        contact_path = group_dir / "contact_sheets" / f"{group}_original_keyframes_contact_sheet.png"
        if extracted:
            make_contact_sheet(group, extracted, contact_path)

        report = {
            "group": group,
            "frames_requested": frames,
            "frames_extracted": [p.name for p in extracted],
            "skipped_frames": skipped,
            "dimensions": dims,
            "contact_sheet": str(contact_path),
            "gpt_input_package": str(group_dir),
            "prompt": str(prompt_path),
            "local_recolor_done": False,
            "video": str(VIDEO),
            "video_fps": fps,
            "video_frame_count": frame_count,
            "next_step": "交给 GPT 逐张生成 gold 图，不要合图，不要本地改色。",
        }
        all_reports[group] = report

        md = [
            f"# {group} 补帧输入包报告",
            "",
            "状态：已完成输入包整理，等待 GPT 逐张生成金色图。",
            "",
            f"帧号：{', '.join(str(x).zfill(3) for x in frames)}",
            "",
            f"成功提取：{len(extracted)} 张",
            f"跳过帧：{skipped if skipped else '无'}",
            "",
            "图片尺寸：",
        ]
        for name, wh in dims.items():
            md.append(f"- {name}: {wh['width']} x {wh['height']}")
        md.extend([
            "",
            f"contact sheet：{contact_path}",
            f"GPT 输入包：{group_dir}",
            f"提示词：{prompt_path}",
            "",
            "明确限制：Codex 没有做本地改色，没有重新渲染，没有改画面内容。",
            "下一步：把 original_frames 里的图片逐张交给 GPT，按提示词生成对应 gold 版本。",
        ])
        (group_dir / "reports" / f"{group}_keyframe_package_report_zh.md").write_text("\n".join(md), encoding="utf-8")
        (group_dir / "reports" / f"{group}_keyframe_package_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    cap.release()
    (OUT / "round2_remaining_keyframes_manifest.json").write_text(
        json.dumps(all_reports, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
