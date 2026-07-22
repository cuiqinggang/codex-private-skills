#!/usr/bin/env python3
"""Extract text, notes, and images from a PowerPoint package.

Usage:
    python extract-pptx.py <input.pptx> [output_dir]

Requires python-pptx. The CLI stages all outputs first, returns structured JSON,
and does not publish partial output when parsing or extraction fails.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import BadZipFile

from pptx import Presentation
from pptx.exc import PackageNotFoundError


def extract_pptx(file_path, output_dir="."):
    """Extract all slide data while preserving the original return contract."""
    input_path = Path(file_path)
    if input_path.suffix.casefold() != ".pptx":
        raise ValueError("input must use the .pptx extension")
    if not input_path.is_file():
        raise FileNotFoundError(f"input file not found: {input_path}")

    prs = Presentation(str(input_path))
    slides_data = []
    assets_dir = Path(output_dir) / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    for slide_num, slide in enumerate(prs.slides):
        slide_data = {
            "number": slide_num + 1,
            "title": "",
            "content": [],
            "images": [],
            "notes": "",
        }

        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    slide_data["title"] = shape.text
                else:
                    slide_data["content"].append({"type": "text", "content": shape.text})

            if shape.shape_type == 13:
                image = shape.image
                image_name = f"slide{slide_num + 1}_img{len(slide_data['images']) + 1}.{image.ext}"
                image_path = assets_dir / image_name
                image_path.write_bytes(image.blob)
                slide_data["images"].append({
                    "path": f"assets/{image_name}",
                    "width": int(shape.width),
                    "height": int(shape.height),
                })

        if slide.has_notes_slide:
            slide_data["notes"] = slide.notes_slide.notes_text_frame.text
        slides_data.append(slide_data)

    return slides_data


def _emit_error(code, category, message, input_path=None):
    payload = {
        "status": "ERROR",
        "error_code": code,
        "category": category,
        "message": message,
    }
    if input_path is not None:
        payload["input"] = str(input_path)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def run_cli(input_file, output_dir):
    """Extract via staging so failed runs leave no partial published output."""
    input_path = Path(input_file)
    target = Path(output_dir)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory(prefix="pptx-extract-", dir=str(target.parent)) as temp_root:
            stage = Path(temp_root)
            slides = extract_pptx(input_path, stage)
            (stage / "extracted-slides.json").write_text(
                json.dumps(slides, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            target.mkdir(parents=True, exist_ok=True)
            for item in stage.iterdir():
                destination = target / item.name
                if item.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                    for child in item.iterdir():
                        shutil.copyfile(child, destination / child.name)
                else:
                    # Copy into the destination directory so the published file
                    # inherits its readable workspace ACL instead of retaining
                    # a restrictive temporary-directory ACL.
                    shutil.copyfile(item, destination)
    except FileNotFoundError as exc:
        _emit_error("PPTX_INPUT_NOT_FOUND", "input", str(exc), input_path)
        return 3
    except ValueError as exc:
        _emit_error("PPTX_INPUT_INVALID", "input", str(exc), input_path)
        return 3
    except (BadZipFile, PackageNotFoundError, KeyError) as exc:
        _emit_error("PPTX_PACKAGE_INVALID", "parse", str(exc), input_path)
        return 4
    except Exception as exc:
        _emit_error("PPTX_EXTRACTION_FAILED", "runtime", f"{type(exc).__name__}: {exc}", input_path)
        return 5

    print(json.dumps({
        "status": "PASS",
        "slide_count": len(slides),
        "output": str(target / "extracted-slides.json"),
        "image_count": sum(len(slide["images"]) for slide in slides),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract-pptx.py <input.pptx> [output_dir]")
        sys.exit(2)
    sys.exit(run_cli(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."))
