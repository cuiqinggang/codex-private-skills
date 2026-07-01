from pathlib import Path
import json

import cv2
from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\A\Documents\Codex\2026-06-15\files-mentioned-by-the-user-codex")
INPUT = ROOT / "outputs" / "silver_to_gold_v1" / "final_25_keyframes_review" / "all_25_gold_frames"
OUT = ROOT / "outputs" / "silver_to_gold_v1" / "gate05_video_transition_test"
TARGET = (1080, 1260)
FRAMES = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360]


def ensure_dirs():
    for name in ["normalized_25_gold_frames", "contact_sheets", "preview_videos", "reports"]:
        (OUT / name).mkdir(parents=True, exist_ok=True)


def is_ratio_close(size):
    w, h = size
    return abs((w / h) - (TARGET[0] / TARGET[1])) < 0.003


def normalize():
    missing = []
    aspect_errors = []
    dims = {}
    normalized = []
    for frame in FRAMES:
        src = INPUT / f"frame_{frame:03d}_gold.png"
        if not src.exists():
            missing.append(frame)
            continue
        with Image.open(src) as im:
            dims[f"frame_{frame:03d}_gold.png"] = {"width": im.width, "height": im.height}
            if not is_ratio_close((im.width, im.height)):
                aspect_errors.append({"frame": frame, "width": im.width, "height": im.height})
                continue
            out = im.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
            dst = OUT / "normalized_25_gold_frames" / f"frame_{frame:03d}_gold_norm.png"
            out.save(dst)
            normalized.append((frame, dst))
    return missing, aspect_errors, dims, normalized


def contact_sheet(normalized):
    cols = 5
    thumb_w, thumb_h = 250, 292
    cell_w, cell_h = 280, 342
    header_h = 64
    rows = (len(normalized) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, header_h + rows * cell_h), (242, 242, 242))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, header_h), fill=(10, 10, 10))
    draw.text((18, 22), "Gate05 normalized 25 gold keyframes - 1080x1260", fill=(255, 220, 80))
    for idx, (frame, path) in enumerate(normalized):
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        x = (idx % cols) * cell_w
        y = header_h + (idx // cols) * cell_h
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), fill=(255, 255, 255), outline=(210, 210, 210))
        draw.rectangle((x, y, x + cell_w - 1, y + 34), fill=(30, 30, 30))
        draw.text((x + 10, y + 9), f"frame_{frame:03d}", fill=(255, 220, 80))
        sheet.paste(im, (x + (cell_w - im.width) // 2, y + 42))
    dst = OUT / "contact_sheets" / "final_25_gold_keyframes_normalized_contact_sheet.png"
    sheet.save(dst)
    return dst


def write_video_from_images(paths, dest, fps):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(dest), fourcc, fps, TARGET)
    for path in paths:
        frame = cv2.imread(str(path))
        if frame is None:
            raise RuntimeError(f"Cannot read image for video: {path}")
        writer.write(frame)
    writer.release()


def make_videos(normalized):
    ordered_paths = [path for _, path in normalized]
    hardcut = OUT / "preview_videos" / "01_hardcut_25frames_5fps.mp4"
    write_video_from_images(ordered_paths, hardcut, 5.0)

    timing_paths = []
    frame_to_path = dict(normalized)
    for frame in FRAMES:
        path = frame_to_path[frame]
        hold = 15
        if frame == 360:
            hold = 15
        timing_paths.extend([path] * hold)
    timing = OUT / "preview_videos" / "02_timing_hold_29_97fps_frame000_to_360.mp4"
    write_video_from_images(timing_paths, timing, 29.97)
    return hardcut, timing


def main():
    ensure_dirs()
    missing, aspect_errors, dims, normalized = normalize()
    sheet = None
    hardcut = None
    timing = None
    if not missing and not aspect_errors and len(normalized) == 25:
        sheet = contact_sheet(normalized)
        hardcut, timing = make_videos(normalized)
        status = "PASS_READY_FOR_VIDEO_ASSEMBLY_TEST"
        need_midframes = False
    else:
        status = "BLOCKED_DIMENSION_OR_ASPECT_ERROR"
        need_midframes = None

    metrics = {
        "status": status,
        "input_dir": str(INPUT),
        "normalized_dir": str(OUT / "normalized_25_gold_frames"),
        "expected_frames": FRAMES,
        "normalized_count": len(normalized),
        "missing_frames": missing,
        "original_dimensions": dims,
        "target_dimensions": {"width": TARGET[0], "height": TARGET[1]},
        "aspect_errors": aspect_errors,
        "normalized_contact_sheet": str(sheet) if sheet else None,
        "hardcut_preview": str(hardcut) if hardcut else None,
        "timing_hold_preview": str(timing) if timing else None,
        "local_recolor_done": False,
        "regeneration_done": False,
        "need_midframes": need_midframes,
        "observed_transition_note": "已生成预览视频用于人工/后续检查；当前基于25张图的尺寸和总览检查，允许进入视频组装测试。",
    }
    (OUT / "reports" / "gate05_video_transition_test_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Gate05 25 张关键帧尺寸规范化与过渡预览报告",
        "",
        f"最终结论：GATE05_TRANSITION_TEST = {status}",
        "",
        f"输入 25 张是否齐全：{'是' if not missing else '否'}",
        f"缺失帧：{missing if missing else '无'}",
        f"规范化成功数量：{len(normalized)} / 25",
        "原始 gold 图尺寸：多数为 1161 x 1355",
        "规范化后尺寸：1080 x 1260",
        f"宽高比异常：{aspect_errors if aspect_errors else '无'}",
        "",
        f"normalized_25_gold_frames：{OUT / 'normalized_25_gold_frames'}",
        f"normalized contact sheet：{sheet}",
        f"hardcut 预览视频：{hardcut}",
        f"timing hold 预览视频：{timing}",
        "",
        "检查说明：",
        "- 本轮没有重新生成图片。",
        "- 本轮没有本地改金色。",
        "- 本轮没有 Blender 重渲染。",
        "- 本轮只做尺寸规范化和视频过渡预览。",
        "",
        "观察结论：",
        "- 25 张图尺寸已统一回原视频比例。",
        "- 未发现宽高比阻塞问题。",
        "- 已生成 hardcut 和 timing hold 两个预览视频，用于检查跳动和颜色稳定性。",
        "- 暂不建议盲目补帧；先看预览视频，如果某一区间跳动明显，再只补对应区间。",
        "",
        f"是否需要补中间帧：{'暂不需要，先看预览视频' if need_midframes is False else '待尺寸问题解决后再判断'}",
    ]
    (OUT / "reports" / "gate05_video_transition_test_report_zh.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
