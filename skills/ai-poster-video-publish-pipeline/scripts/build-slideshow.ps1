param(
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,

    [string]$InputImageFolder,
    [string]$OutputPath,
    [string]$ReportPath,
    [int]$Crf = 18,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Resolve-ForUse {
    param(
        [Parameter(Mandatory = $true)][string]$PathValue,
        [Parameter(Mandatory = $true)][string]$BasePath
    )
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $PathValue))
}

$resolvedConfig = (Resolve-Path -LiteralPath $ConfigPath).Path
$configDir = Split-Path -Parent $resolvedConfig
$config = Get-Content -LiteralPath $resolvedConfig -Raw -Encoding UTF8 | ConvertFrom-Json

if (-not $InputImageFolder -or $InputImageFolder.Trim().Length -eq 0) {
    $InputImageFolder = 'input'
}
if (-not $OutputPath -or $OutputPath.Trim().Length -eq 0) {
    $OutputPath = $config.output
}
if (-not $ReportPath -or $ReportPath.Trim().Length -eq 0) {
    $ReportPath = Join-Path $configDir ("reports\build-slideshow-{0}.json" -f $config.mode)
}

$inputDir = Resolve-ForUse -PathValue $InputImageFolder -BasePath $configDir
$outputFile = Resolve-ForUse -PathValue $OutputPath -BasePath $configDir
$reportFile = Resolve-ForUse -PathValue $ReportPath -BasePath $configDir

if (-not (Test-Path -LiteralPath $inputDir)) {
    throw "Input image folder not found: $inputDir"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "python is required for build-slideshow.ps1"
}
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    throw "ffmpeg is required for build-slideshow.ps1"
}

$pythonCode = @'
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageEnhance, ImageFilter
except Exception as exc:
    raise SystemExit(f"Pillow is required: {exc}")


@dataclass(frozen=True)
class Slide:
    image: Path
    label: str
    seconds: float
    role: str


def fit_cover(img: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / img.width, height / img.height)
    size = (int(round(img.width * scale)), int(round(img.height * scale)))
    resized = img.resize(size, Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def fit_contain(img: Image.Image, width: int, height: int) -> Image.Image:
    scale = min(width / img.width, height / img.height)
    size = (int(round(img.width * scale)), int(round(img.height * scale)))
    return img.resize(size, Image.Resampling.LANCZOS)


def make_frame(img: Image.Image, width: int, height: int) -> Image.Image:
    bg = fit_cover(img, width, height).filter(ImageFilter.GaussianBlur(34))
    bg = ImageEnhance.Brightness(bg).enhance(0.72)
    bg = ImageEnhance.Contrast(bg).enhance(1.08)
    fg = fit_contain(img, width, height)
    frame = bg.convert("RGB")
    x = (width - fg.width) // 2
    y = (height - fg.height) // 2
    frame.paste(fg.convert("RGB"), (x, y))
    return frame


def timeline(slides: list[Slide], transition: float) -> tuple[list[float], float]:
    starts = [0.0]
    for prev in slides[:-1]:
        starts.append(starts[-1] + prev.seconds - transition)
    total = starts[-1] + slides[-1].seconds
    return starts, total


def active_frame(t: float, slides: list[Slide], starts: list[float], transition: float, frames: list[Image.Image], frame_bytes: list[bytes]) -> bytes:
    index = 0
    for i, start in enumerate(starts):
        if start <= t:
            index = i
        else:
            break

    if index + 1 < len(slides):
        next_start = starts[index + 1]
        if next_start <= t < next_start + transition:
            alpha = (t - next_start) / transition
            return Image.blend(frames[index], frames[index + 1], alpha).tobytes()

    return frame_bytes[index]


def build_ffmpeg_cmd(width: int, height: int, fps: int, crf: int, output: Path) -> list[str]:
    return [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "-",
        "-an",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.1",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", str(crf),
        str(output),
    ]


def load_slides(config: dict, input_dir: Path) -> list[Slide]:
    slides = []
    for item in config.get("slides", []):
        image = input_dir / item["file"]
        slides.append(Slide(
            image=image,
            label=str(item.get("label", item.get("role", image.name))),
            seconds=float(item.get("seconds", 4.5)),
            role=str(item.get("role", "")),
        ))
    if not slides:
        raise ValueError("config slides is empty")
    missing = [str(slide.image) for slide in slides if not slide.image.exists()]
    if missing:
        raise FileNotFoundError("Missing slide images: " + "; ".join(missing))
    return slides


def render(config: dict, input_dir: Path, output: Path, report: Path, crf: int, dry_run: bool) -> dict:
    width = int(config.get("width", 1080))
    height = int(config.get("height", 1920))
    fps = int(config.get("fps", 30))
    transition = float(config.get("transition_seconds", 0.5))
    slides = load_slides(config, input_dir)
    starts, total_seconds = timeline(slides, transition)
    total_frames = int(round(total_seconds * fps))

    result = {
        "status": "DRY_RUN" if dry_run else "PASS",
        "mode": config.get("mode", ""),
        "output": str(output),
        "width": width,
        "height": height,
        "fps": fps,
        "codec": "h264",
        "transition_seconds": transition,
        "duration_seconds": total_seconds,
        "frames": total_frames,
        "animation": "static_with_crossfade_only",
        "forbidden_animation": ["shake", "pan", "drift", "random_ken_burns", "fast_zoom", "rotate", "flip", "bounce", "vibration"],
        "slides": [
            {
                "index": i,
                "role": slide.role,
                "label": slide.label,
                "image": str(slide.image),
                "start_seconds": starts[i],
                "seconds": slide.seconds,
            }
            for i, slide in enumerate(slides)
        ],
    }

    report.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    images = [Image.open(slide.image).convert("RGB") for slide in slides]
    frames = [make_frame(img, width, height) for img in images]
    frame_bytes = [frame.tobytes() for frame in frames]
    cmd = build_ffmpeg_cmd(width, height, fps, crf, output)
    log_path = report.with_suffix(".ffmpeg.log")

    with log_path.open("w", encoding="utf-8") as log:
        log.write(" ".join(cmd) + "\n")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=log, stderr=log)
        assert proc.stdin is not None
        try:
            for frame_no in range(total_frames):
                t = frame_no / fps
                proc.stdin.write(active_frame(t, slides, starts, transition, frames, frame_bytes))
        finally:
            proc.stdin.close()
        code = proc.wait()

    for img in images:
        img.close()
    for frame in frames:
        frame.close()
    if code != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {code}; see {log_path}")

    result["ffmpeg_log"] = str(log_path)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    render(config, args.input_dir, args.output, args.report, args.crf, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'@

$tempPy = Join-Path ([System.IO.Path]::GetTempPath()) ("ai-poster-slideshow-" + [System.Guid]::NewGuid().ToString("N") + ".py")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($tempPy, $pythonCode, $utf8NoBom)

try {
    $argsList = @(
        $tempPy,
        '--config', $resolvedConfig,
        '--input-dir', $inputDir,
        '--output', $outputFile,
        '--report', $reportFile,
        '--crf', ([string]$Crf)
    )
    if ($DryRun) {
        $argsList += '--dry-run'
    }
    & python @argsList
    if ($LASTEXITCODE -ne 0) {
        throw "build-slideshow failed with exit code $LASTEXITCODE"
    }
}
finally {
    if (Test-Path -LiteralPath $tempPy) {
        Remove-Item -LiteralPath $tempPy -Force
    }
}



