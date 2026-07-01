from pathlib import Path
import json

import cv2
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\A\Documents\Codex\2026-06-15\files-mentioned-by-the-user-codex")
INPUT = ROOT / "outputs" / "silver_to_gold_v1" / "gate05_video_transition_test" / "normalized_25_gold_frames"
OUT = ROOT / "outputs" / "silver_to_gold_v1" / "gate06_video_assembly_test_frame000_to_360"
FRAMES = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360]
FPS = 29.97
SIZE = (1080, 1260)


def ensure_dirs():
    for name in ["assembled_videos", "sampled_frames", "contact_sheets", "reports"]:
        (OUT / name).mkdir(parents=True, exist_ok=True)


def load_images():
    missing = []
    images = {}
    for frame in FRAMES:
        path = INPUT / f"frame_{frame:03d}_gold_norm.png"
        if not path.exists():
            missing.append(frame)
            continue
        img = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if img is None or (img.shape[1], img.shape[0]) != SIZE:
            missing.append(frame)
            continue
        images[frame] = img
    return missing, images


def write_video(frames, dest):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(dest), fourcc, FPS, SIZE)
    for img in frames:
        writer.write(img)
    writer.release()


def timing_hold_frames(images):
    output = []
    for idx, key in enumerate(FRAMES):
        next_key = FRAMES[idx + 1] if idx + 1 < len(FRAMES) else 361
        hold = max(1, next_key - key)
        output.extend([images[key]] * hold)
    return output[:361]


def crossfade_frames(images):
    output = []
    for idx, key in enumerate(FRAMES):
        if idx + 1 >= len(FRAMES):
            output.append(images[key])
            continue
        next_key = FRAMES[idx + 1]
        span = next_key - key
        a = images[key].astype(np.float32)
        b = images[next_key].astype(np.float32)
        for step in range(span):
            alpha = step / span
            blended = (a * (1.0 - alpha) + b * alpha).clip(0, 255).astype(np.uint8)
            output.append(blended)
    return output[:361]


def save_sample_frames(video_frames, prefix):
    sample_points = [0, 30, 60, 90, 120, 150, 180, 195, 210, 240, 255, 270, 285, 315, 345, 360]
    saved = []
    for t in sample_points:
        idx = min(t, len(video_frames) - 1)
        path = OUT / "sampled_frames" / f"{prefix}_sample_frame_{idx:03d}.png"
        cv2.imwrite(str(path), video_frames[idx])
        saved.append((idx, path))
    return saved


def make_contact_sheet(samples, dest, title):
    cols = 4
    thumb_w, thumb_h = 250, 292
    cell_w, cell_h = 280, 342
    header_h = 62
    rows = (len(samples) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, header_h + rows * cell_h), (242, 242, 242))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, sheet.width, header_h), fill=(10, 10, 10))
    draw.text((18, 21), title, fill=(255, 220, 80))
    for i, (frame, path) in enumerate(samples):
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        x = (i % cols) * cell_w
        y = header_h + (i // cols) * cell_h
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), fill=(255, 255, 255), outline=(210, 210, 210))
        draw.rectangle((x, y, x + cell_w - 1, y + 34), fill=(30, 30, 30))
        draw.text((x + 10, y + 9), f"video frame {frame:03d}", fill=(255, 220, 80))
        sheet.paste(im, (x + (cell_w - im.width) // 2, y + 42))
    sheet.save(dest)


def video_meta(path):
    cap = cv2.VideoCapture(str(path))
    meta = {
        "path": str(path),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "duration_seconds": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / max(cap.get(cv2.CAP_PROP_FPS), 1),
        "codec": "mp4v via OpenCV VideoWriter",
    }
    cap.release()
    return meta


def main():
    ensure_dirs()
    missing, images = load_images()
    if missing:
        status = "BLOCKED_VIDEO_ASSEMBLY_ERROR"
        metrics = {"status": status, "missing_or_bad_frames": missing}
    else:
        hold = timing_hold_frames(images)
        fade = crossfade_frames(images)
        hold_video = OUT / "assembled_videos" / "01_gate06_timing_hold_baseline_frame000_to_360.mp4"
        fade_video = OUT / "assembled_videos" / "02_gate06_crossfade_reference_frame000_to_360.mp4"
        write_video(hold, hold_video)
        write_video(fade, fade_video)
        hold_samples = save_sample_frames(hold, "01_timing_hold")
        fade_samples = save_sample_frames(fade, "02_crossfade")
        hold_sheet = OUT / "contact_sheets" / "01_timing_hold_sampled_contact_sheet.png"
        fade_sheet = OUT / "contact_sheets" / "02_crossfade_sampled_contact_sheet.png"
        make_contact_sheet(hold_samples, hold_sheet, "Gate06 timing-hold sampled frames")
        make_contact_sheet(fade_samples, fade_sheet, "Gate06 crossfade sampled frames")
        status = "PASS_READY_FOR_SEGMENT_REVIEW"
        metrics = {
            "status": status,
            "input_dir": str(INPUT),
            "input_count": len(images),
            "missing_or_bad_frames": [],
            "timing_hold_video": video_meta(hold_video),
            "crossfade_video": video_meta(fade_video),
            "motion_interpolation_video": None,
            "timing_hold_contact_sheet": str(hold_sheet),
            "crossfade_contact_sheet": str(fade_sheet),
            "size_kept": "1080x1260",
            "fps": FPS,
            "local_recolor_done": False,
            "regeneration_done": False,
            "need_midframes": "review_preview_first",
            "watch_intervals": ["180-195", "240-255", "270-285", "345-360"],
        }

    (OUT / "reports" / "gate06_video_assembly_test_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        "# Gate06 0-360 段高级金视频组装测试报告",
        "",
        f"最终结论：GATE06_VIDEO_ASSEMBLY_TEST = {status}",
        "",
        f"输入 25 张 normalized 图是否齐全：{'是' if not missing else '否'}",
        f"缺失或尺寸异常帧：{missing if missing else '无'}",
        "",
        f"输出目录：{OUT}",
        f"timing hold baseline 视频：{metrics.get('timing_hold_video', {}).get('path')}",
        f"crossfade reference 视频：{metrics.get('crossfade_video', {}).get('path')}",
        "motion interpolation 视频：未生成。本轮不安装额外插帧工具。",
        f"timing hold sampled contact sheet：{metrics.get('timing_hold_contact_sheet')}",
        f"crossfade sampled contact sheet：{metrics.get('crossfade_contact_sheet')}",
        "",
        "编码说明：本轮使用 OpenCV mp4v 输出 mp4；如果后续需要 H.264/yuv420p，可在最终发布前再做转码。",
        "",
        "检查重点区间：180-195、240-255、270-285、345-360。",
        "是否建议补中间帧：先看两个预览视频；如果上述区间跳动明显，再只补对应区间。",
        "",
        "本轮没有重新生成图片，没有本地改金色，没有 Blender 重渲染。",
    ]
    (OUT / "reports" / "gate06_video_assembly_test_report_zh.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
