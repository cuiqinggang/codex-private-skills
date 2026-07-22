import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


TOOLS = [
    "ffmpeg",
    "ffprobe",
    "python",
    "auto-editor",
    "scenedetect",
    "node",
    "npm",
]


REGISTRY_NAMES = [
    "剪映",
    "Jianying",
    "CapCut",
    "Shotcut",
    "Kdenlive",
]


def run(cmd, timeout=15):
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
            "cmd": cmd,
            "returncode": p.returncode,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip(),
        }
    except Exception as exc:
        return {"cmd": cmd, "error": str(exc)}


def command_info(name):
    path = shutil.which(name)
    if not path:
        scripts_dir = Path(os.environ.get("APPDATA", "")) / "Python" / "Python313" / "Scripts"
        suffix = ".exe" if os.name == "nt" else ""
        candidate = scripts_dir / f"{name}{suffix}"
        if candidate.exists():
            path = str(candidate)
    info = {"name": name, "found": bool(path), "path": path}
    if path:
        if name in {"ffmpeg", "ffprobe"}:
            probe = run([path, "-version"])
        elif name == "scenedetect":
            probe = run([path, "version"])
        elif name == "auto-editor":
            probe = run([path, "--version"])
            if probe.get("returncode") != 0:
                probe = run([path, "-V"])
        else:
            probe = run([path, "--version"])
        info["version_probe"] = probe
    return info


def winget_list():
    items = {}
    for query in ["ByteDance.JianyingPro", "ByteDance.CapCut", "Meltytech.Shotcut", "KDE.Kdenlive"]:
        result = run(["winget", "list", "--id", query], timeout=12)
        items[query] = result
    return items


def known_paths():
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    jianying_apps = sorted((local / "JianyingPro" / "Apps").glob("*/JianyingPro.exe"))
    candidates = [
        local / "JianyingPro",
        *jianying_apps,
        local / "Programs" / "Shotcut" / "shotcut.exe",
        Path("C:/Program Files/kdenlive/bin/kdenlive.exe"),
        Path("C:/Program Files/Kdenlive/bin/kdenlive.exe"),
        local / "Programs" / "Kdenlive" / "bin" / "kdenlive.exe",
        local / "Programs" / "kdenlive" / "bin" / "kdenlive.exe",
    ]
    return [{"path": str(p), "exists": p.exists()} for p in candidates if str(p)]


def path_exists(path_status, *needles):
    lowered = [x.lower() for x in needles]
    return any(
        item["exists"] and all(needle in item["path"].lower() for needle in lowered)
        for item in path_status
    )


def decisions(tool_status, installed_status, path_status):
    found = {x["name"]: x["found"] for x in tool_status}
    shotcut_installed = "Shotcut" in installed_status.get("Meltytech.Shotcut", {}).get("stdout", "")
    kdenlive_installed = "Kdenlive" in installed_status.get("KDE.Kdenlive", {}).get("stdout", "")
    jianying_installed = "剪映" in installed_status.get("ByteDance.JianyingPro", {}).get("stdout", "")
    shotcut_ready = shotcut_installed or path_exists(path_status, "shotcut.exe")
    kdenlive_ready = kdenlive_installed or path_exists(path_status, "kdenlive.exe")
    jianying_ready = jianying_installed or path_exists(path_status, "jianyingpro")
    return [
        {
            "feature": "basic trim/join/export",
            "decision": "script-distill",
            "route": "FFmpeg for deterministic batch output; Shotcut/Kdenlive only for manual timeline polish",
            "ready": found.get("ffmpeg") and found.get("ffprobe"),
        },
        {
            "feature": "auto subtitles",
            "decision": "script-distill",
            "route": "video-audio-transcription skill / whisper.cpp -> SRT; Shotcut speech-to-text can be direct-use when configured",
            "ready": True,
        },
        {
            "feature": "manual GUI editing",
            "decision": "direct-use",
            "route": "Shotcut/Kdenlive direct use for timeline polish and preview",
            "ready": shotcut_ready or kdenlive_ready,
        },
        {
            "feature": "Jianying/CapCut paid templates and AI effects",
            "decision": "do-not-copy",
            "route": "Use only as product reference; recreate with own assets or ComfyUI/Remotion when legal",
            "ready": jianying_ready,
        },
        {
            "feature": "scene detection",
            "decision": "script-distill",
            "route": "PySceneDetect if installed; otherwise install only when needed",
            "ready": found.get("scenedetect", False),
        },
        {
            "feature": "silence removal",
            "decision": "script-distill",
            "route": "Auto-Editor if installed; otherwise install only when needed",
            "ready": found.get("auto-editor", False),
        },
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    tool_status = [command_info(x) for x in TOOLS]
    installed = winget_list()
    path_status = known_paths()
    report = {
        "status": "PASS",
        "tool_status": tool_status,
        "installed_status": installed,
        "known_paths": path_status,
        "feature_decisions": decisions(tool_status, installed, path_status),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS {out}")


if __name__ == "__main__":
    main()
