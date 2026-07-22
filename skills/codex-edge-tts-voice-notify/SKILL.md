---
name: codex-edge-tts-voice-notify
description: Use when restoring, repairing, documenting, or redeploying the local Windows Codex voice notification setup that uses edge-tts after Codex task completion. Covers Codex notify wrapping, stale runtime paths, no-audio playback fixes, cached MP3/WAV playback, and removing the leading beep.
---

# Codex Edge TTS Voice Notify

Use this skill when the user wants Codex to speak after a task finishes, or when the existing voice reminder stops working after a Codex restart/reinstall.

## Current Known-Good Design

- Python package: `edge-tts`.
- Hook script path: `%USERPROFILE%\.codex\hooks\codex_voice_notify.py`.
- Config entry: `notify` in `%USERPROFILE%\.codex\config.toml`.
- Default voice: `zh-CN-XiaoxiaoNeural`.
- Default spoken text: `Codex task complete, please check.` in Chinese, stored in the script with Unicode escapes to avoid Windows encoding damage.
- Audio flow: synthesize MP3 with `edge-tts`, cache by text and voice, convert to WAV with `ffmpeg` when available, then play with Python `winsound`.
- Beep is disabled by default. Enable only by setting `CODEX_VOICE_BEEP=1`.

## What Failed In The Original Attempt

1. `edge-playback.exe` reported `edge-tts is not installed` even though the Python package worked. Avoid relying on that launcher.
2. A hardcoded Codex runtime path became stale after Codex restarted and runtime folder changed.
3. Codex Desktop may wrap `notify` as:
   `codex-computer-use.exe turn-ended --previous-notify "[python, hook]"`
   This is normal. The previous notify script can still run.
4. `ffplay` could execute and report successful playback while the user heard nothing.
5. Windows console encoding damaged direct Chinese text in the script once. Store the default Chinese phrase as Unicode escapes.
6. The two leading `winsound.Beep` tones were useful for debugging but should remain off for normal use.

## Fast Recovery

Run:

```powershell
${REDACTED_SECRET}
```

Then restart Codex Desktop if the current session does not pick up the new `notify` value.

## Verification

Run the hook directly:

```powershell
${REDACTED_SECRET}
```

Check the log:

```powershell
${REDACTED_SECRET}
```

Healthy log lines include `cached` on first generation and `played` after playback.

## Troubleshooting

- If the log time does not change after Codex finishes a turn, Codex did not call the notify hook. Re-run the restore script and restart Codex Desktop.
- If the log says `played` but the user hears nothing, test Windows sound with `[console]::beep(880,500)` and check the default output device or app volume.
- If `edge-tts` synthesis fails, verify network access and run `python -m pip install --user edge-tts`.
- If the user hears two beeps before speech, set `CODEX_VOICE_BEEP=0` or restore the script; the final baseline disables beep by default.

## Useful Environment Overrides

- `CODEX_VOICE_NOTIFY=0` disables voice.
- `CODEX_VOICE_TEXT="..."` changes the spoken text.
- `CODEX_VOICE_NAME="zh-CN-YunyangNeural"` changes the voice.
- `CODEX_VOICE_BEEP=1` temporarily enables the two debug beeps.

## 2026-06-13 Baseline

The working fix was confirmed when the user heard the spoken reminder without the two beeps. Preserve the cached MP3/WAV approach and avoid reintroducing direct `edge-playback.exe` or stale Codex runtime paths.
