# Recovery

Use this file only after a gate fails. Do not jump layers. Do not change Hermes main model, bot token, account settings, system firewall, or startup persistence unless the user explicitly asks for that repair.

## STOP_G01_BASE_NOT_READY

Meaning: the base path is not ready.

Check in order:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
codex --version
codex login status
ffmpeg -version
```

Recovery:

- If Hermes Telegram fails, use the `hermes-telegram-persistent-bridge` runbook.
- If only startup persistence fails but live polling works, record it separately; do not repair startup unless requested.
- If Codex CLI fails, fix the Codex executable/login layer before any media route.
- If ffmpeg fails, restore ffmpeg before video gates.

## STOP_ROUTER_NOT_INSTALLED

Meaning: Hermes did not provide a saved local attachment path for `/codeximg` or `/codexvideo`.

Check:

```powershell
Get-ChildItem -LiteralPath "C:\Users\A\Desktop\1\input\telegram-media" -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 20 FullName,Length,LastWriteTime
```

Recovery:

- Keep normal Hermes messages untouched.
- Add or repair only the `/codex`, `/codeximg`, `/codexvideo` route handoff.
- The handoff must pass local file paths to the wrappers; remote Telegram file IDs are not enough.
- Stop if the change would modify broad Hermes gateway behavior.

## STOP_IMAGE_MISSING or STOP_VIDEO_MISSING

Meaning: the wrapper received a path that does not exist.

Check:

```powershell
Test-Path -LiteralPath "<path>"
```

Recovery:

- Confirm Hermes saved the attachment before wrapper invocation.
- Confirm the path is absolute.
- Confirm the attachment directory is under the fixed input path.

## STOP_IMAGE_TYPE_UNSUPPORTED

Supported image extensions:

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

Recovery: save or convert the image to a supported extension before invoking Codex.

## STOP_VIDEO_TYPE_UNSUPPORTED

Supported video extensions:

- `.mp4`
- `.mov`
- `.mkv`
- `.webm`
- `.avi`
- `.m4v`

Recovery: save or convert the video to a supported extension before frame extraction.

## STOP_FFMPEG_FAILED or STOP_FFMPEG_TIMEOUT

Check:

```powershell
ffmpeg -version
Get-Content -LiteralPath "<output dir>\ffmpeg.log" -Tail 80
```

Recovery:

- Validate the source video with `Test-Path`.
- Try a shorter video.
- Keep extraction at 1 fps or less for long videos.
- Do not delete the original video.

## STOP_NO_FRAMES

Meaning: ffmpeg completed but did not create `frame_*.jpg`.

Recovery:

- Inspect `ffmpeg.log`.
- Confirm the video is not corrupt or zero duration.
- Retry with a known short `.mp4`.

## STOP_CODEX_FAILED or STOP_CODEX_TIMEOUT

Check:

```powershell
Get-Content -LiteralPath "<output dir>\result.txt" -Raw
Get-Content -LiteralPath "<output dir>\codex-command.json" -Raw
```

Recovery:

- Confirm `codex --version` works.
- Confirm `codex login status` works.
- Confirm the exact image paths in `codex-command.json` still exist.
- Retry with one image before retrying multiple images or video frames.
- Do not switch Hermes main model as a Codex recovery step.

## Wrapper Reinstall

If the runtime wrappers are missing but the skill package is intact:

```powershell
New-Item -ItemType Directory -Force -Path "C:\Users\A\Hermes_Tools"
Copy-Item -LiteralPath "H:\Hermes_Skills\telegram-hermes-codex-vision-action\scripts\Invoke-CodexImageExec.ps1" -Destination "C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1" -Force
Copy-Item -LiteralPath "H:\Hermes_Skills\telegram-hermes-codex-vision-action\scripts\Invoke-CodexVideoExec.ps1" -Destination "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" -Force
```

Then rerun G10 validation.
