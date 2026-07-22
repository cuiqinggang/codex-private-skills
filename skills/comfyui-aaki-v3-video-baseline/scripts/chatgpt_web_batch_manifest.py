from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare a ChatGPT web image repair batch folder and prompt.")
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--file", action="append", required=True)
    parser.add_argument("--purpose", default="image_repair")
    parser.add_argument("--max-files", type=int, default=10)
    parser.add_argument("--prompt-extra", default="")
    args = parser.parse_args(argv)

    files = [Path(item).resolve() for item in args.file]
    if len(files) > args.max_files:
        raise SystemExit(f"Too many files: {len(files)} > {args.max_files}")
    for path in files:
        if not path.exists() or not path.is_file():
            raise SystemExit(f"Missing file: {path}")

    root = Path(args.run_root).resolve()
    run_dir = root / f"{time.strftime('%Y%m%d-%H%M%S')}_batch_{args.purpose}"
    inputs = run_dir / "inputs"
    outputs = run_dir / "local_outputs"
    inputs.mkdir(parents=True, exist_ok=True)
    outputs.mkdir(parents=True, exist_ok=True)

    manifest_files = []
    for index, src in enumerate(files, start=1):
        stable_name = f"{index:02d}_{src.stem}{src.suffix.lower()}"
        dst = inputs / stable_name
        shutil.copy2(src, dst)
        manifest_files.append(
            {
                "index": index,
                "source": str(src),
                "local_copy": str(dst),
                "source_stem": src.stem,
                "expected_output": str(outputs / f"{index:02d}_{src.stem}_repaired.png"),
            }
        )

    manifest = {
        "purpose": args.purpose,
        "max_files": args.max_files,
        "count": len(manifest_files),
        "files": manifest_files,
    }
    manifest_path = run_dir / "input_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "Repair or regenerate each attached image as a clean production-quality frame.",
        "Return one separate image for each input, in the same order.",
        "Do not merge the images into a collage.",
        "Do not add labels, numbers, captions, watermarks, or extra text inside the images.",
        "Preserve camera angle, object geometry, lighting, shadows, and scene composition unless a defect requires local repair.",
        "For each image, remove visible artifacts and make the frame clean enough to use as a video keyframe or clean plate.",
    ]
    if args.prompt_extra.strip():
        lines.append(args.prompt_extra.strip())
    lines.append("")
    lines.append("Input order:")
    for item in manifest_files:
        lines.append(f"{item['index']:02d}. {Path(item['local_copy']).name}")
    prompt_path = run_dir / "prompt.md"
    prompt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"run_dir": str(run_dir), "manifest": str(manifest_path), "prompt": str(prompt_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
