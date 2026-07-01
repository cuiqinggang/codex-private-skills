import importlib.util
import shutil
import subprocess
import sys
import time
from pathlib import Path


CODEX_HOME = Path.home() / ".codex"
HOOK_DIR = CODEX_HOME / "hooks"
HOOK_PATH = HOOK_DIR / "codex_voice_notify.py"
CONFIG_PATH = CODEX_HOME / "config.toml"


HOOK_SCRIPT = r'''import asyncio
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import winsound
from pathlib import Path

import edge_tts


CODEX_HOME = Path.home() / ".codex"
LOG_PATH = CODEX_HOME / "hooks" / "codex_voice_notify.log"
CACHE_DIR = CODEX_HOME / "hooks" / "voice-cache"


def first_existing(paths):
    for raw in paths:
        if raw and Path(raw).exists():
            return str(Path(raw))
    return None


FFMPEG = first_existing([
    shutil.which("ffmpeg"),
    Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe",
])
FFPLAY = first_existing([
    shutil.which("ffplay"),
    Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffplay.exe",
])


def log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{stamp} {message}\n")


async def synthesize(text: str, voice: str, media_path: Path) -> None:
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(str(media_path))


def play_mp3(media_path: Path) -> None:
    wav_path = media_path.with_suffix(".wav")
    if FFMPEG and not wav_path.exists():
        subprocess.run(
            [FFMPEG, "-y", "-loglevel", "quiet", "-i", str(media_path), str(wav_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )

    if wav_path.exists():
        winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)
        return

    if FFPLAY:
        subprocess.run(
            [FFPLAY, "-nodisp", "-autoexit", "-loglevel", "quiet", "-volume", "100", str(media_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
        return

    ps = (
        "$player=New-Object -ComObject WMPlayer.OCX; "
        f"$player.URL={str(media_path)!r}; "
        "$player.controls.play(); "
        "Start-Sleep -Milliseconds 250; "
        "$limit=(Get-Date).AddSeconds(10); "
        "while($player.playState -ne 1 -and (Get-Date) -lt $limit){ "
        "Start-Sleep -Milliseconds 200 }; "
        "$player.close()"
    )
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=15,
        check=False,
    )


def main() -> int:
    del sys.argv

    if os.environ.get("CODEX_VOICE_NOTIFY", "1").lower() in {"0", "false", "off", "no"}:
        log("voice_disabled")
        return 0

    text = os.environ.get("CODEX_VOICE_TEXT", "Codex \u4efb\u52a1\u5b8c\u6210\uff0c\u8bf7\u67e5\u770b\u3002")
    voice = os.environ.get("CODEX_VOICE_NAME", "zh-CN-XiaoxiaoNeural")

    try:
        if os.environ.get("CODEX_VOICE_BEEP", "0").lower() not in {"0", "false", "off", "no"}:
            winsound.Beep(880, 180)
            winsound.Beep(660, 180)

        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(f"{voice}\n{text}".encode("utf-8")).hexdigest()[:16]
        media_path = CACHE_DIR / f"{digest}.mp3"

        if not media_path.exists():
            tmp_path = Path(tempfile.gettempdir()) / f"codex-voice-notify-{os.getpid()}.mp3"
            asyncio.run(synthesize(text, voice, tmp_path))
            tmp_path.replace(media_path)
            log(f"cached voice={voice!r} text_len={len(text)}")

        play_mp3(media_path)
        log(f"played voice={voice!r} text_len={len(text)}")
        return 0
    except Exception as exc:
        log(f"voice_failed: {exc!r}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def ensure_edge_tts() -> None:
    if importlib.util.find_spec("edge_tts") is not None:
        return
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "edge-tts"],
        check=True,
    )


def toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def notify_line() -> str:
    return f"notify = [ {toml_string(sys.executable)}, {toml_string(str(HOOK_PATH))} ]"


def update_config() -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    old = CONFIG_PATH.read_text(encoding="utf-8") if CONFIG_PATH.exists() else ""
    if CONFIG_PATH.exists():
        backup = CONFIG_PATH.with_name(f"config.toml.bak-edge-tts-restore-{time.strftime('%Y%m%d-%H%M%S')}")
        backup.write_text(old, encoding="utf-8")

    lines = old.splitlines()
    replaced = False
    out = []
    for line in lines:
        if line.strip().startswith("notify ="):
            if not replaced:
                out.append(notify_line())
                replaced = True
            continue
        out.append(line)

    if not replaced:
        out.insert(0, notify_line())

    CONFIG_PATH.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ensure_edge_tts()
    HOOK_DIR.mkdir(parents=True, exist_ok=True)
    HOOK_PATH.write_text(HOOK_SCRIPT, encoding="utf-8")
    update_config()
    subprocess.run([sys.executable, "-m", "py_compile", str(HOOK_PATH)], check=True)
    print(f"Restored hook: {HOOK_PATH}")
    print(f"Updated config: {CONFIG_PATH}")
    print("Run the hook directly to test audio:")
    print(f"{sys.executable} {HOOK_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
