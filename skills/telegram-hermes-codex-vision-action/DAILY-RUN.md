# Daily Run

Run these gates in order from Windows PowerShell. Stop at the first failed gate and record the failure in `TEST-REPORT.md`.

## G01 Base Readiness

Purpose: confirm Hermes Telegram, Codex CLI, Codex login, and ffmpeg.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
codex --version
codex login status
ffmpeg -version
```

Success: output `TELEGRAM_HERMES_CODEX_BASE_READY`.

Failure: any command fails.

Recovery: fix only the failed layer. Do not change Hermes main model.

Continue: yes only after success.

## G02 Image Landing

Purpose: prove Telegram image files land locally.

Location: phone Telegram and `C:\Users\A\Desktop\1`.

Command:

```powershell
Test-Path -LiteralPath "<saved image path>"
```

Success: the saved image is under `input\telegram-media\images\` and `Test-Path` returns `True`.

Failure: no local file path or missing file.

Recovery: fix attachment saving or route handoff.

Continue: yes only after success.

## G03 Codex Image Recognition

Purpose: prove Codex CLI can inspect an image.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
codex --image "<image path>" "请严格输出 CODEX_IMAGE_OK，并用一句话描述图片"
```

Success: output contains `CODEX_IMAGE_OK` and the description matches.

Failure: Codex command fails or no marker.

Recovery: fix Codex CLI/login before Hermes integration.

Continue: yes only after success.

## G04 Image Wrapper

Purpose: verify the image wrapper.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "dry run image validation" -ImagePaths "<image path>" -TaskId "TGIMG-DRYRUN" -DryRun
```

Success: output directory contains `task.txt`, `result.txt`, `media-manifest.json`, and `codex-command.json`.

Failure: wrapper STOP code.

Recovery: fix wrapper validation error.

Continue: yes after dry run; real Codex call requires G03 success.

## G05 Video Landing

Purpose: prove Telegram video files land locally.

Location: phone Telegram and `C:\Users\A\Desktop\1`.

Command:

```powershell
Test-Path -LiteralPath "<saved video path>"
```

Success: the saved video is under `input\telegram-media\videos\` and `Test-Path` returns `True`.

Failure: no local file path or missing file.

Recovery: fix attachment saving or route handoff.

Continue: yes only after success.

## G06 Video Frame Extraction

Purpose: extract no more than 20 review frames.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "dry run video frame extraction" -VideoPath "<video path>" -TaskId "TGVID-DRYRUN" -DryRun
```

Success: `input\telegram-media\frames\TGVID-DRYRUN\frame_0001.jpg` exists, and total frames are at most 20.

Failure: ffmpeg STOP code or zero frames.

Recovery: fix ffmpeg/video path first.

Continue: yes after frames exist.

## G07 Video Wrapper

Purpose: verify video wrapper output and Codex command construction.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "dry run video validation" -VideoPath "<video path>" -TaskId "TGVID-DRYRUN" -DryRun
```

Success: output directory contains `task.txt`, `result.txt`, `media-manifest.json`, `codex-command.json`, and `ffmpeg.log`.

Failure: wrapper STOP code.

Recovery: fix the narrow failing layer.

Continue: yes after dry run; real Codex call requires G01/G03 success.

## G08 Telegram Image Closed Loop

Purpose: prove end-to-end image analysis.

Location: phone Telegram.

Command: send `/codeximg 这是一张报错截图，请分析原因，只做分析，不改文件。` with an image.

Success: Telegram receives analysis; input image and output `result.txt` exist.

Failure: missing Telegram reply, missing image, missing output, or wrapper STOP.

Recovery: inspect landing, wrapper, then Codex.

Continue: yes only with evidence.

## G09 Telegram Video Closed Loop

Purpose: prove end-to-end video analysis.

Location: phone Telegram.

Command: send `/codexvideo 这个视频里展示了一个软件操作问题，请按关键帧分析问题，只做分析，不改文件。` with a short video.

Success: Telegram receives analysis; video, frames, and output `result.txt` exist.

Failure: missing Telegram reply, missing video, missing frames, missing output, or wrapper STOP.

Recovery: inspect landing, ffmpeg, wrapper, then Codex.

Continue: yes only with evidence.

## G10 Skill Save

Purpose: verify package files.

Location: `C:\Users\A\Desktop\1`

Command:

```powershell
python "C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "H:\Hermes_Skills\telegram-hermes-codex-vision-action"
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\tests\Test-TelegramHermesCodexVisionAction.ps1"
```

Success: validation and local dry-run tests pass.

Failure: missing files, invalid skill metadata, script parse error, or wrapper dry-run failure.

Recovery: fix files and rerun G10.

Continue: report PASS only if G01-G10 are all current PASS; otherwise report the exact STOP gate.
