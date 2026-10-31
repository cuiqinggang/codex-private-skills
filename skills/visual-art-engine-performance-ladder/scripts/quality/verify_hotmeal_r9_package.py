#!/usr/bin/env python3
"""Verify the frozen R9 package without submitting GPU or network work."""
import argparse, hashlib, json, pathlib, subprocess, tempfile, zipfile

def verify(package):
    root = pathlib.Path(__file__).resolve().parents[2]
    release = json.loads((root / "references/RELEASE-V3.json").read_text(encoding="utf-8"))
    data = pathlib.Path(package).read_bytes()
    expected = release["artifacts"]["package"]
    assert len(data) == expected["bytes"], "PACKAGE_SIZE_MISMATCH"
    assert hashlib.sha256(data).hexdigest() == expected["sha256"], "PACKAGE_SHA_MISMATCH"
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None, "ZIP_CRC_FAILURE"
        names = archive.namelist()
        assert len(names) == len(set(names)), "DUPLICATE_ARCHIVE_PATH"
        assert all(not pathlib.PurePosixPath(n).is_absolute() and ".." not in pathlib.PurePosixPath(n).parts for n in names), "UNSAFE_ARCHIVE_PATH"
        manifest = json.loads(archive.read("file-manifest.json"))
        for name, item in manifest.items():
            value = archive.read(name)
            assert len(value) == item["bytes"], "FILE_SIZE_MISMATCH:" + name
            assert hashlib.sha256(value).hexdigest() == item["sha256"], "FILE_SHA_MISMATCH:" + name
        state = json.loads(archive.read("R9/delivery-state.json"))
        assert state["human_approval"] is False and state["final_approval"] is False, "APPROVAL_BOUNDARY_CHANGED"
        video = archive.read("R9/FINAL/HotMeal-R9-15s-Human-Review.mp4")
        assert hashlib.sha256(video).hexdigest() == release["artifacts"]["video"]["sha256"], "VIDEO_SHA_MISMATCH"
        with tempfile.TemporaryDirectory(prefix="hotmeal-r9-verify-") as temp:
            file = pathlib.Path(temp) / "candidate.mp4"
            file.write_bytes(video)
            probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-of", "json", str(file)], timeout=90))
        visual = next(s for s in probe["streams"] if s["codec_type"] == "video")
        audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
        assert (visual["width"], visual["height"]) == (768, 640), "DIMENSION_MISMATCH"
        assert visual["r_frame_rate"] == "24/1" and int(visual["nb_read_frames"]) == 360 and float(visual["duration"]) == 15, "TIMELINE_MISMATCH"
        assert visual["codec_name"] == "h264" and visual["pix_fmt"] == "yuv420p", "VIDEO_CODEC_MISMATCH"
        assert audio["codec_name"] == "aac" and audio["sample_rate"] == "48000", "AUDIO_CODEC_MISMATCH"
    return {"integrity": "PASS", "manifest_files": len(manifest), "frames": 360, "seconds": 15, "status": state["state"], "human_approval": False, "final_approval": False, "gpu_submissions": 0, "scope": "file integrity and stream structure only; no artistic or universal-control certification"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=pathlib.Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.package), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"integrity": "FAIL", "reason": str(error), "gpu_submissions": 0}, ensure_ascii=False))
        raise SystemExit(1)

