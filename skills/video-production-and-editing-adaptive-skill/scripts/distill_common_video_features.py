import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def find_tool(name):
    path = shutil.which(name)
    if path:
        return path
    scripts_dir = Path(os.environ.get("APPDATA", "")) / "Python" / "Python313" / "Scripts"
    suffix = ".exe" if os.name == "nt" else ""
    candidate = scripts_dir / f"{name}{suffix}"
    if candidate.exists():
        return str(candidate)
    return None


def run(cmd, timeout=120):
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return {
            "cmd": [str(x) for x in cmd],
            "returncode": p.returncode,
            "stdout": p.stdout[-3000:],
            "stderr": p.stderr[-5000:],
        }
    except Exception as exc:
        return {"cmd": [str(x) for x in cmd], "returncode": 999, "error": str(exc)}


def ffmpeg_path():
    return find_tool("ffmpeg") or "ffmpeg"


def ffprobe_path():
    return find_tool("ffprobe") or "ffprobe"


def srt_filter_path(path):
    return str(path).replace("\\", "/").replace(":", "\\:")


def record(report, feature, source_feature, decision, route, output, command, timeout=120, caveat=""):
    step = run(command, timeout=timeout)
    report["steps"].append(step)
    report["features"].append(
        {
            "feature": feature,
            "source_editor_feature": source_feature,
            "decision": decision,
            "route": route,
            "output": str(output) if output else None,
            "status": "PASS" if step.get("returncode") == 0 else "FAIL",
            "caveat": caveat,
        }
    )
    return step


def probe(media):
    return run(
        [
            ffprobe_path(),
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=index,codec_type,codec_name,width,height,pix_fmt,channels,sample_rate",
            "-of",
            "json",
            str(media),
        ],
        timeout=45,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    root = Path(args.workdir)
    root.mkdir(parents=True, exist_ok=True)

    ffmpeg = ffmpeg_path()
    auto_editor = find_tool("auto-editor")
    scenedetect = find_tool("scenedetect")

    report = {
        "status": "PASS",
        "tool_paths": {
            "ffmpeg": ffmpeg,
            "ffprobe": ffprobe_path(),
            "auto-editor": auto_editor,
            "scenedetect": scenedetect,
        },
        "steps": [],
        "features": [],
        "outputs": {},
        "probes": {},
    }

    sample = root / "sample_input.mp4"
    trimmed = root / "sample_trimmed.mp4"
    clip_a = root / "sample_clip_a.mp4"
    clip_b = root / "sample_clip_b.mp4"
    concat_list = root / "concat_list.txt"
    joined = root / "sample_joined.mp4"
    vertical = root / "sample_vertical_9x16.mp4"
    square = root / "sample_square.mp4"
    cover = root / "cover.jpg"
    sheet = root / "contact_sheet.jpg"
    srt = root / "sample.srt"
    title_ass = root / "title_overlay.ass"
    subtitled = root / "sample_subtitled.mp4"
    fade_text = root / "sample_fade_text.mp4"
    color_adjusted = root / "sample_color_adjusted.mp4"
    bg_mix = root / "sample_background_music_mix.mp4"
    normalized = root / "sample_audio_normalized.mp4"
    speed = root / "sample_speed_125.mp4"
    transition = root / "sample_transition_xfade.mp4"
    silence_input = root / "sample_silence_input.mp4"
    silence_removed = root / "sample_silence_removed.mp4"
    scene_source = root / "sample_scene_source.mp4"
    scene_dir = root / "scene_detection"
    scene_dir.mkdir(exist_ok=True)

    srt.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nVideo editor feature distillation test.\n\n"
        "2\n00:00:02,000 --> 00:00:05,000\nSubtitles, audio, trim, export and QA are reproducible.\n",
        encoding="utf-8",
    )
    title_ass.write_text(
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1280\n"
        "PlayResY: 720\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Title,Arial,54,&H00FFFFFF,&H000000FF,&HAA000000,&HAA000000,0,0,0,0,100,100,0,0,3,1,0,8,30,30,42,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        "Dialogue: 0,0:00:00.20,0:00:03.80,Title,,0,0,0,,Title Test\n",
        encoding="utf-8",
    )

    record(
        report,
        "generate representative test video",
        "local media import and preview",
        "script-distill",
        "FFmpeg synthetic video/audio asset",
        sample,
        [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc2=size=1280x720:rate=30:duration=8",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=880:duration=8",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(sample),
        ],
    )

    record(report, "trim clip", "剪切/裁剪", "script-distill", "FFmpeg -ss/-t", trimmed, [ffmpeg, "-y", "-ss", "1", "-t", "3", "-i", str(sample), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(trimmed)])
    record(report, "make join clip A", "多段素材拼接", "script-distill", "FFmpeg segment export", clip_a, [ffmpeg, "-y", "-ss", "0", "-t", "2", "-i", str(sample), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(clip_a)])
    record(report, "make join clip B", "多段素材拼接", "script-distill", "FFmpeg segment export", clip_b, [ffmpeg, "-y", "-ss", "4", "-t", "2", "-i", str(sample), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(clip_b)])
    concat_list.write_text(f"file '{clip_a.as_posix()}'\nfile '{clip_b.as_posix()}'\n", encoding="utf-8")
    record(report, "join clips", "多段素材拼接", "script-distill", "FFmpeg concat demuxer", joined, [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(joined)])

    record(report, "vertical 9:16 export", "抖音/视频号竖屏导出", "script-distill", "FFmpeg scale/pad H.264 AAC yuv420p", vertical, [ffmpeg, "-y", "-i", str(sample), "-vf", "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(vertical)])
    record(report, "square export", "社媒方形导出", "script-distill", "FFmpeg crop/scale square package", square, [ffmpeg, "-y", "-i", str(sample), "-vf", "crop=720:720:280:0,scale=1080:1080", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(square)])
    record(report, "cover frame extraction", "封面抽帧", "script-distill", "FFmpeg single-frame export", cover, [ffmpeg, "-y", "-ss", "2", "-i", str(sample), "-frames:v", "1", "-q:v", "2", str(cover)])
    record(report, "contact sheet QA", "成片预览/质检", "script-distill", "FFmpeg fps/tile preview sheet", sheet, [ffmpeg, "-y", "-i", str(sample), "-vf", "fps=1,scale=320:-1,tile=4x2", "-frames:v", "1", "-q:v", "2", str(sheet)])
    record(report, "subtitle burn-in", "字幕/文本字幕", "script-distill", "SRT + FFmpeg subtitles/libass", subtitled, [ffmpeg, "-y", "-i", str(sample), "-vf", f"subtitles='{srt_filter_path(srt)}'", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(subtitled)])

    record(report, "title text and fade", "文本标题/淡入淡出", "script-distill", "ASS title overlay + FFmpeg fade/afade", fade_text, [ffmpeg, "-y", "-i", str(sample), "-vf", f"fade=t=in:st=0:d=0.5,fade=t=out:st=7.3:d=0.7,subtitles='{srt_filter_path(title_ass)}'", "-af", "afade=t=in:st=0:d=0.5,afade=t=out:st=7.3:d=0.7", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(fade_text)])
    record(report, "color adjustment", "滤镜/调节", "script-distill", "FFmpeg eq saturation/contrast/brightness", color_adjusted, [ffmpeg, "-y", "-i", str(sample), "-vf", "eq=saturation=1.25:contrast=1.10:brightness=0.02", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(color_adjusted)])
    record(report, "background music mix", "音频导入/背景音乐/淡入淡出", "script-distill", "FFmpeg amix volume afade", bg_mix, [ffmpeg, "-y", "-i", str(sample), "-f", "lavfi", "-i", "sine=frequency=220:duration=8", "-filter_complex", "[1:a]volume=0.12,afade=t=in:st=0:d=0.5,afade=t=out:st=7.4:d=0.6[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", str(bg_mix)])
    record(report, "audio loudness normalize", "音量统一/响度标准化", "script-distill", "FFmpeg loudnorm", normalized, [ffmpeg, "-y", "-i", str(sample), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", str(normalized)])
    record(report, "speed change", "变速", "script-distill", "FFmpeg setpts/atempo", speed, [ffmpeg, "-y", "-i", str(sample), "-filter_complex", "[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(speed)])

    record(report, "transition xfade", "转场", "script-distill", "FFmpeg xfade/acrossfade", transition, [ffmpeg, "-y", "-f", "lavfi", "-i", "color=c=red:s=1280x720:r=30:d=2", "-f", "lavfi", "-i", "color=c=blue:s=1280x720:r=30:d=2", "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-f", "lavfi", "-i", "sine=frequency=660:duration=2", "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=1.5[v];[2:a][3:a]acrossfade=d=0.5[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(transition)])

    record(report, "create silence test", "智能剪口播/去静音", "script-distill", "FFmpeg synthetic loud/silent/loud audio", silence_input, [ffmpeg, "-y", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=6", "-f", "lavfi", "-i", "sine=frequency=600:duration=2", "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100:d=2", "-f", "lavfi", "-i", "sine=frequency=900:duration=2", "-filter_complex", "[1:a][2:a][3:a]concat=n=3:v=0:a=1[a]", "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(silence_input)])
    if auto_editor:
        record(report, "silence removal rough cut", "智能剪口播/去静音", "script-distill", "Auto-Editor audio detection", silence_removed, [auto_editor, str(silence_input), "-o", str(silence_removed), "--no-open", "--quiet"], timeout=180, caveat="Use FFmpeg silenceremove fallback if Auto-Editor fails on unusual audio.")
    else:
        record(report, "silence removal rough cut", "智能剪口播/去静音", "script-distill", "FFmpeg silenceremove fallback", silence_removed, [ffmpeg, "-y", "-i", str(silence_input), "-af", "silenceremove=start_periods=1:start_duration=0.2:start_threshold=-35dB:stop_periods=-1:stop_duration=0.2:stop_threshold=-35dB", "-c:v", "copy", "-c:a", "aac", str(silence_removed)], caveat="Auto-Editor not found; fallback keeps video stream length less deterministic.")

    record(report, "create scene test", "镜头/场景识别", "script-distill", "FFmpeg hard-cut scene source", scene_source, [ffmpeg, "-y", "-f", "lavfi", "-i", "color=c=red:s=1280x720:r=30:d=2", "-f", "lavfi", "-i", "color=c=green:s=1280x720:r=30:d=2", "-f", "lavfi", "-i", "color=c=blue:s=1280x720:r=30:d=2", "-f", "lavfi", "-i", "sine=frequency=500:duration=6", "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]", "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(scene_source)])
    if scenedetect:
        step = run([scenedetect, "-i", str(scene_source), "-o", str(scene_dir), "detect-content", "list-scenes", "save-images"], timeout=180)
        report["steps"].append(step)
        report["features"].append(
            {
                "feature": "scene detection list and thumbnails",
                "source_editor_feature": "镜头/场景识别",
                "decision": "script-distill",
                "route": "PySceneDetect detect-content list-scenes save-images",
                "output": str(scene_dir),
                "status": "PASS" if step.get("returncode") == 0 else "FAIL",
                "caveat": "Use GUI review for taste-based split decisions.",
            }
        )
    else:
        report["features"].append(
            {
                "feature": "scene detection list and thumbnails",
                "source_editor_feature": "镜头/场景识别",
                "decision": "script-distill",
                "route": "PySceneDetect",
                "output": str(scene_dir),
                "status": "SKIP",
                "caveat": "scenedetect executable not found.",
            }
        )

    media_outputs = [
        sample,
        trimmed,
        joined,
        vertical,
        square,
        subtitled,
        fade_text,
        color_adjusted,
        bg_mix,
        normalized,
        speed,
        transition,
        silence_input,
        silence_removed,
        scene_source,
    ]
    for media in media_outputs:
        if media.exists():
            report["outputs"][media.name] = str(media)
            report["probes"][media.name] = probe(media)
    for asset in [cover, sheet, srt, title_ass, concat_list]:
        if asset.exists():
            report["outputs"][asset.name] = str(asset)
    if scene_dir.exists():
        report["outputs"]["scene_detection_dir"] = str(scene_dir)
        report["outputs"]["scene_detection_files"] = [str(x) for x in sorted(scene_dir.glob("*"))]

    failed = [x for x in report["features"] if x["status"] == "FAIL"]
    report["status"] = "PASS" if not failed else "PARTIAL"
    report["failed_features"] = failed

    out = root / "distillation-test-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{report['status']} {out}")


if __name__ == "__main__":
    main()
