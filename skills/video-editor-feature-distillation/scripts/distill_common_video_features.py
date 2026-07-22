import argparse
import json
import subprocess
from pathlib import Path


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": p.returncode,
        "stdout": p.stdout[-2000:],
        "stderr": p.stderr[-4000:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    root = Path(args.workdir)
    root.mkdir(parents=True, exist_ok=True)
    report = {"steps": []}

    sample = root / "sample_input.mp4"
    trimmed = root / "sample_trimmed.mp4"
    vertical = root / "sample_vertical.mp4"
    cover = root / "cover.jpg"
    sheet = root / "contact_sheet.jpg"
    srt = root / "sample.srt"
    subtitled = root / "sample_subtitled.mp4"

    srt.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nVideo editor feature distillation test.\n\n"
        "2\n00:00:02,000 --> 00:00:04,000\nFFmpeg subtitle burn-in and export check.\n",
        encoding="utf-8",
    )

    report["steps"].append(run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=6",
        "-f", "lavfi", "-i", "sine=frequency=880:duration=6",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", str(sample),
    ]))

    report["steps"].append(run([
        "ffmpeg", "-y", "-ss", "1", "-t", "3", "-i", str(sample),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(trimmed),
    ]))

    report["steps"].append(run([
        "ffmpeg", "-y", "-i", str(sample),
        "-vf", "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(vertical),
    ]))

    report["steps"].append(run([
        "ffmpeg", "-y", "-ss", "2", "-i", str(sample),
        "-frames:v", "1", "-q:v", "2", str(cover),
    ]))

    report["steps"].append(run([
        "ffmpeg", "-y", "-i", str(sample),
        "-vf", "fps=1,scale=320:-1,tile=3x2",
        "-frames:v", "1", "-q:v", "2", str(sheet),
    ]))

    safe_srt = str(srt).replace("\\", "/").replace(":", "\\:")
    report["steps"].append(run([
        "ffmpeg", "-y", "-i", str(sample),
        "-vf", f"subtitles='{safe_srt}'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(subtitled),
    ]))

    probes = {}
    for media in [sample, trimmed, vertical, subtitled]:
        probes[media.name] = run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size:stream=index,codec_type,codec_name,width,height,pix_fmt",
            "-of", "json", str(media),
        ])
    report["probes"] = probes
    report["outputs"] = {x.name: str(x) for x in [sample, trimmed, vertical, cover, sheet, srt, subtitled]}

    status = "PASS"
    for step in report["steps"]:
        if step["returncode"] != 0:
            status = "PARTIAL"
    report["status"] = status

    out = root / "distillation-test-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{status} {out}")


if __name__ == "__main__":
    main()
