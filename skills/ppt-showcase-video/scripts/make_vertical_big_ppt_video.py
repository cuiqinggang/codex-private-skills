from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_AUDIO = SKILL_DIR / "assets" / "calm-piano-background-music-free-orange-free-sounds.mp3"
DEFAULT_FFMPEG = Path(
    r"C:\Users\A\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
)

W, H = 1080, 1920
FPS = 30


def fit_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def fit_contain(img: Image.Image, max_size: tuple[int, int]) -> Image.Image:
    copy = img.copy()
    copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    return copy


def make_slide(src: Path, out: Path) -> None:
    img = Image.open(src).convert("RGB")

    bg = fit_cover(img, (W, H)).filter(ImageFilter.GaussianBlur(30))
    bg = ImageEnhance.Brightness(bg).enhance(0.62)
    bg = ImageEnhance.Color(bg).enhance(0.86)

    if img.width / img.height < 0.72:
        fg = fit_contain(img, (1060, 1888))
    else:
        fg = fit_contain(img, (1060, 1620))

    x = (W - fg.width) // 2
    y = (H - fg.height) // 2

    shadow = Image.new("RGBA", (fg.width + 56, fg.height + 56), (0, 0, 0, 0))
    box = Image.new("RGBA", (fg.width, fg.height), (0, 0, 0, 120))
    shadow.alpha_composite(box, (28, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    bg.paste(shadow.convert("RGB"), (x - 28, y - 18), shadow)

    edge = Image.new("RGB", (fg.width + 8, fg.height + 8), (248, 246, 241))
    bg.paste(edge, (x - 4, y - 4))
    bg.paste(fg, (x, y))
    bg.save(out, quality=96)


def render_video(
    ffmpeg: Path,
    slides: list[Path],
    audio: Path,
    output: Path,
    seconds_per_slide: float,
    fade_seconds: float,
    crf: int,
) -> None:
    inputs: list[str] = []
    for slide in slides:
        inputs.extend(["-loop", "1", "-t", str(seconds_per_slide), "-i", str(slide)])
    inputs.extend(["-i", str(audio)])

    filters: list[str] = []
    for i in range(len(slides)):
        filters.append(f"[{i}:v]fps={FPS},format=rgba,setpts=PTS-STARTPTS[v{i}]")

    current = "v0"
    for i in range(1, len(slides)):
        offset = i * (seconds_per_slide - fade_seconds)
        out = f"x{i}"
        filters.append(
            f"[{current}][v{i}]xfade=transition=fade:duration={fade_seconds}:offset={offset:.3f},format=rgba[{out}]"
        )
        current = out

    filters.append(f"[{current}]format=yuv420p[vout]")
    total_duration = len(slides) * seconds_per_slide - (len(slides) - 1) * fade_seconds

    cmd = [
        str(ffmpeg),
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[vout]",
        "-map",
        f"{len(slides)}:a:0",
        "-t",
        f"{total_duration:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        str(crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(cmd, check=True)


def image_files(folder: Path) -> list[Path]:
    exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a vertical big-image PPT-style showcase video.")
    parser.add_argument("--images", required=True, type=Path, help="Folder containing source images.")
    parser.add_argument("--output", required=True, type=Path, help="Output MP4 path.")
    parser.add_argument("--audio", type=Path, default=DEFAULT_AUDIO, help="Music file. Defaults to bundled light music.")
    parser.add_argument("--workdir", type=Path, default=None, help="Intermediate slide folder.")
    parser.add_argument("--ffmpeg", type=Path, default=DEFAULT_FFMPEG, help="ffmpeg executable path.")
    parser.add_argument("--seconds-per-slide", type=float, default=4.0)
    parser.add_argument("--fade-seconds", type=float, default=0.6)
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()

    images = image_files(args.images)
    if not images:
        raise SystemExit(f"No supported image files found in {args.images}")
    if not args.audio.exists():
        raise SystemExit(f"Missing audio file: {args.audio}")
    if not args.ffmpeg.exists():
        ffmpeg = Path(shutil.which("ffmpeg") or "")
        if not ffmpeg.exists():
            raise SystemExit("ffmpeg not found. Pass --ffmpeg.")
        args.ffmpeg = ffmpeg

    temp_ctx = None
    if args.workdir is None:
        temp_ctx = tempfile.TemporaryDirectory(prefix="ppt_showcase_video_")
        workdir = Path(temp_ctx.name)
    else:
        workdir = args.workdir
        workdir.mkdir(parents=True, exist_ok=True)

    slides: list[Path] = []
    for i, src in enumerate(images):
        out = workdir / f"slide_{i + 1:02d}.png"
        make_slide(src, out)
        slides.append(out)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    render_video(
        args.ffmpeg,
        slides,
        args.audio,
        args.output,
        args.seconds_per_slide,
        args.fade_seconds,
        args.crf,
    )
    print(f"VIDEO={args.output}")
    print(f"IMAGES={len(images)}")
    print(f"AUDIO={args.audio}")

    if temp_ctx is not None:
        temp_ctx.cleanup()


if __name__ == "__main__":
    main()
