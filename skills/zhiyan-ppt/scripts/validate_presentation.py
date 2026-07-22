#!/usr/bin/env python3
"""Structural validation for Zhiyan PPTX and fixed-stage HTML deliverables."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def result(path: Path) -> dict:
    return {"file": str(path.resolve()), "format": path.suffix.lower(), "checks": [], "warnings": [], "errors": []}


def check_pptx(path: Path) -> dict:
    out = result(path)
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            if bad:
                out["errors"].append(f"corrupt member: {bad}")
                return out
            names = set(zf.namelist())
            slide_names = sorted(n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
            if not slide_names:
                out["errors"].append("no slides found")
                return out
            pres = ET.fromstring(zf.read("ppt/presentation.xml"))
            size = pres.find("p:sldSz", NS)
            cx = int(size.get("cx", "0")) if size is not None else 0
            cy = int(size.get("cy", "0")) if size is not None else 0
            ratio = round(cx / cy, 4) if cy else None
            blank, editable, pictures, tiny_text_runs = [], 0, 0, 0
            for slide_name in slide_names:
                root = ET.fromstring(zf.read(slide_name))
                texts = [node.text.strip() for node in root.findall(".//a:t", NS) if node.text and node.text.strip()]
                shapes = root.findall(".//p:sp", NS)
                pics = root.findall(".//p:pic", NS)
                editable += len(shapes)
                pictures += len(pics)
                if not texts and not shapes and not pics:
                    blank.append(slide_name)
                for run_props in root.findall(".//a:rPr", NS) + root.findall(".//a:defRPr", NS):
                    size_value = run_props.get("sz")
                    if size_value and int(size_value) < 900:
                        tiny_text_runs += 1
            out["slides"] = len(slide_names)
            out["slide_ratio"] = ratio
            out["editable_shape_count"] = editable
            out["picture_count"] = pictures
            out["speaker_notes_parts"] = len([n for n in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)])
            out["checks"].extend(["zip_integrity", "slide_presence", "editable_object_scan"])
            if blank:
                out["warnings"].append(f"blank-looking slides: {blank}")
            if tiny_text_runs:
                out["warnings"].append(f"{tiny_text_runs} explicitly formatted text runs below 9 pt")
            if ratio and abs(ratio - (16 / 9)) > 0.03:
                out["warnings"].append(f"non-16:9 slide ratio: {ratio}")
            if editable == 0 and pictures >= len(slide_names):
                out["warnings"].append("deck may be image-based rather than natively editable")
    except (OSError, zipfile.BadZipFile, KeyError, ET.ParseError, ValueError) as exc:
        out["errors"].append(str(exc))
    return out


def check_html(path: Path) -> dict:
    out = result(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        out["errors"].append(str(exc))
        return out
    slides = len(re.findall(r'class=["\'][^"\']*\bslide\b', text, flags=re.I))
    out["slides"] = slides
    required = {
        "1920_stage": bool(re.search(r"(?:width\s*:\s*1920px|--(?:stage-)?width\s*:\s*1920)", text, re.I)),
        "1080_stage": bool(re.search(r"(?:height\s*:\s*1080px|--(?:stage-)?height\s*:\s*1080)", text, re.I)),
        "keyboard_navigation": "keydown" in text,
        "reduced_motion": "prefers-reduced-motion" in text,
    }
    for name, passed in required.items():
        (out["checks"] if passed else out["errors"]).append(name if passed else f"missing {name}")
    if slides == 0:
        out["errors"].append("no .slide elements found")
    external_scripts = re.findall(r"<script[^>]+src=[\"']https?://", text, flags=re.I)
    if external_scripts:
        out["warnings"].append("external scripts may break offline use")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("deliverable", type=Path)
    parser.add_argument("--json", action="store_true", help="retained for explicitness; output is always JSON")
    args = parser.parse_args()
    path = args.deliverable
    if not path.is_file():
        print(json.dumps({"file": str(path), "errors": ["file not found"]}, ensure_ascii=False, indent=2))
        return 2
    if path.suffix.lower() == ".pptx":
        out = check_pptx(path)
    elif path.suffix.lower() in {".html", ".htm"}:
        out = check_html(path)
    else:
        out = result(path)
        out["errors"].append("supported formats: .pptx, .html")
    out["status"] = "PASS" if not out["errors"] else "FAIL"
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
