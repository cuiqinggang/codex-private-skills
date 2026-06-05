---
name: telegram-hermes-codex-vision-action
description: Use when Windows Hermes Telegram messages should route /codex, /codeximg, or /codexvideo tasks to Codex CLI, with Telegram attachments saved locally first, images passed through codex --image, videos converted to ffmpeg key frames, outputs written under C:\Users\A\Desktop\1\output, and no Codex desktop UI, mouse, keyboard, clipboard, focus, model change, commit, push, or production delete.
---

# Telegram Hermes Codex Vision Action

Use this skill to run a stable Telegram -> Hermes -> Codex CLI workflow for text, image, and video tasks.

## Non-negotiable Boundaries

- Do not use Codex desktop UI automation.
- Do not move or capture the real mouse or keyboard.
- Do not depend on window focus, clipboard, screenshot paste, or active desktop state.
- Use Codex CLI as the executor.
- Use `codex --image` for images.
- Use `ffmpeg` to extract video frames before calling Codex.
- Save every Telegram attachment to disk before invoking Codex.
- Do not change the current Hermes main model.
- Do not break the existing Hermes + Telegram polling bridge.
- Do not commit, push, or delete production files by default.
- Save all task artifacts under `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-<taskId>\`.
- If any required layer is unavailable, STOP with the narrow failing gate and do not claim success.

## Fixed Paths

- Image input: `C:\Users\A\Desktop\1\input\telegram-media\images\`
- Video input: `C:\Users\A\Desktop\1\input\telegram-media\videos\`
- Video frames: `C:\Users\A\Desktop\1\input\telegram-media\frames\<taskId>\`
- Output: `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-<taskId>\`
- Runtime wrappers: `C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1` and `C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1`
- Skill copies: `H:\Hermes_Skills\telegram-hermes-codex-vision-action\scripts\`

## Routing Rules

- Plain Telegram message: let Hermes handle it normally.
- `/codex <task>`: use Codex CLI for a text-only engineering task, saving result artifacts under output.
- `/codeximg <task>`: require at least one image attachment. Save the image first, then call `Invoke-CodexImageExec.ps1`.
- `/codexvideo <task>`: require one video attachment. Save the video first, run `Invoke-CodexVideoExec.ps1`, extract frames, then pass the frame list to Codex CLI as images.

If Hermes does not expose the saved attachment path to the agent or router, stop with `STOP_ROUTER_NOT_INSTALLED`; do not fake a local path.

## Wrapper Commands

Image:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1" `
  -RepoPath "C:\Users\A\Desktop\1" `
  -Task "Analyze this screenshot. Do not edit files." `
  -ImagePaths "C:\Users\A\Desktop\1\input\telegram-media\images\sample.jpg" `
  -TaskId "TGIMG-20260525-001"
```

Video:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" `
  -RepoPath "C:\Users\A\Desktop\1" `
  -Task "Analyze the key frames. Do not edit files." `
  -VideoPath "C:\Users\A\Desktop\1\input\telegram-media\videos\sample.mp4" `
  -TaskId "TGVID-20260525-001"
```

Use `-DryRun` only for wrapper validation. A dry run verifies paths, manifests, and video frame extraction but deliberately does not invoke Codex.

## Gate Protocol

### G01A Runtime Base Readiness

- Purpose: Confirm the live runtime can process `/codeximg` and `/codexvideo` tasks now.
- Location: `C:\Users\A\Desktop\1`
- Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
$CodexCmd = "C:\Users\A\AppData\Roaming\npm\codex.cmd"
& $CodexCmd --version
& $CodexCmd login status
& $CodexCmd exec "Output CODEX_EXEC_R2B_SMOKE_OK exactly." -o "C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-last-message.txt"
ffmpeg -version
```

- Runtime PASS conditions:
  - Hermes gateway is running.
  - `gateway_state.json` shows `api_server` connected.
  - `gateway_state.json` shows `telegram` connected.
  - Hermes health and models endpoints are healthy.
  - Open WebUI on port 3000 is reachable.
  - `C:\Users\A\AppData\Roaming\npm\codex.cmd --version` passes.
  - `C:\Users\A\AppData\Roaming\npm\codex.cmd login status` passes.
  - `codex.cmd exec` smoke writes the expected marker to the `-o` final message file.
  - `ffmpeg -version` passes.
- Success: print `G01_RUNTIME_BASE_READY_WITH_STARTUP_ENTRY_MISSING` when G01A passes and only G01B has a missing startup entry.
- Failure: Hermes gateway is not running, Telegram is disconnected, Codex CLI fails, Codex is not logged in, Codex exec smoke fails, or ffmpeg fails.
- Recovery: identify the failed runtime layer only. Do not repair Hermes model routing or startup persistence unless explicitly requested.
- Continue: after G01A passes. A G01B startup persistence warning does not block image/video closed-loop testing.

### G01B Startup Persistence Check

- Purpose: Record whether Hermes Telegram auto-start persistence is configured.
- Location: `C:\Users\A\Desktop\1`
- Check: `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`
- PASS: startup entry exists.
- WARN: startup entry is missing.
- Failure: none for runtime image/video testing.
- Recovery: do not create the startup entry unless the user explicitly asks for persistence repair.
- Continue: always continue to G02/G05/G08/G09 if G01A passed.

### G02 Image Landing

- Purpose: Confirm Telegram image attachments are saved locally.
- Location: phone Telegram plus `C:\Users\A\Desktop\1`.
- User message: send the G02 Chinese prompt from `DAILY-RUN.md` with a PNG or JPG.
- Success: file exists under `input\telegram-media\images\` and passes `Test-Path`.
- Failure: no local file path, missing file, unsupported extension, or only remote Telegram file ID.
- Recovery: fix only the attachment-save layer.
- Continue: only after local path is proven.

### G03 Codex Image Recognition

- Purpose: Confirm Codex CLI can read the saved image.
- Location: `C:\Users\A\Desktop\1`
- Command:

```powershell
codex --image "<image path>" "Output CODEX_IMAGE_OK exactly, then describe the image in one sentence."
```

- Success: output contains `CODEX_IMAGE_OK` and the description matches the image.
- Failure: Codex command fails, login missing, image unreadable, or no marker.
- Recovery: fix Codex CLI execution before touching Hermes.
- Continue: only after marker is present.

### G04 Image Wrapper

- Purpose: Create and verify the image wrapper.
- Location: `C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1`
- Success: validates repo, `.git`, image paths, image extensions, multi-image args, timeout, `task.txt`, `result.txt`, and `media-manifest.json`.
- Failure: missing repo, missing `.git`, missing image, unsupported type, Codex timeout, Codex nonzero exit.
- Recovery: wrapper must write a STOP result file and return the narrow failure.
- Continue: after dry-run validation and one real Codex image check when G03 is ready.

### G05 Video Landing

- Purpose: Confirm Telegram video attachments are saved locally.
- Location: phone Telegram plus `C:\Users\A\Desktop\1`.
- User message: send the G05 Chinese prompt from `DAILY-RUN.md` with a short video.
- Success: file exists under `input\telegram-media\videos\` and passes `Test-Path`.
- Failure: no local file path, missing file, unsupported extension, or only remote Telegram file ID.
- Recovery: fix only the attachment-save layer.
- Continue: only after local path is proven.

### G06 Video Frame Extraction

- Purpose: Convert video to reviewable frames.
- Location: `C:\Users\A\Desktop\1`
- Command:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" `
  -RepoPath "C:\Users\A\Desktop\1" `
  -Task "dry run video frame extraction" `
  -VideoPath "<video path>" `
  -TaskId "<taskId>" `
  -DryRun
```

- Success: `frame_0001.jpg` and related frames exist under `input\telegram-media\frames\<taskId>\`, with no more than 20 frames.
- Failure: ffmpeg missing, unsupported video, zero frames, or timeout.
- Recovery: fix ffmpeg/path/video layer only.
- Continue: after frames exist.

### G07 Video Wrapper

- Purpose: Run video -> frames -> Codex image list.
- Location: `C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1`
- Success: validates video, extracts frames, passes frames to Codex as repeated `--image` args, saves `result.txt`, `media-manifest.json`, and `ffmpeg.log`.
- Failure: any validation, ffmpeg, frame, timeout, or Codex error.
- Recovery: wrapper must write a STOP result file.
- Continue: after dry-run validation and one real Codex video-frame run when G01/G03 are ready.

### G08 Telegram Image Closed Loop

- Purpose: Prove phone image -> Hermes -> local save -> Codex -> Telegram reply.
- Location: phone Telegram.
- User message: send the G08 Chinese prompt from `DAILY-RUN.md` with an image.
- Success: Telegram receives analysis, output has `result.txt`, input has original image copy.
- Failure: missing reply, missing output, missing input image, or wrapper STOP.
- Recovery: check from Telegram landing to wrapper to Codex in order.
- Continue: only after evidence exists.

### G09 Telegram Video Closed Loop

- Purpose: Prove phone video -> Hermes -> local save -> frames -> Codex -> Telegram reply.
- Location: phone Telegram.
- User message: send the G09 Chinese prompt from `DAILY-RUN.md` with a short video.
- Success: Telegram receives analysis, video is saved, frames are saved, output has `result.txt`.
- Failure: missing reply, missing video, missing frames, missing output, or wrapper STOP.
- Recovery: check from Telegram landing to ffmpeg to Codex in order.
- Continue: only after evidence exists.

### G10 Skill Save

- Purpose: Save this reusable skill package.
- Location: `H:\Hermes_Skills\telegram-hermes-codex-vision-action`
- Success: required docs and scripts exist, wrappers parse, dry-run validation passes, and test report records any STOP gates honestly.
- Failure: missing files, invalid frontmatter, script parse errors, or unreported failed gates.
- Recovery: fix files and rerun validation.
- Continue: report final code only after evidence supports it.

## STOP Codes

- `STOP_G01A_RUNTIME_BASE_NOT_READY`: runtime readiness failed.
- `G01_RUNTIME_BASE_READY_WITH_STARTUP_ENTRY_MISSING`: runtime readiness passed, but startup persistence is missing and recorded as WARN only.
- `STOP_ROUTER_NOT_INSTALLED`: Hermes did not provide saved attachment paths for `/codeximg` or `/codexvideo`.
- `STOP_REPO_MISSING`: `RepoPath` does not exist.
- `STOP_REPO_GIT_MISSING`: `RepoPath\.git` does not exist.
- `STOP_IMAGE_MISSING`: an image path does not exist.
- `STOP_IMAGE_TYPE_UNSUPPORTED`: image extension is not png, jpg, jpeg, or webp.
- `STOP_VIDEO_MISSING`: video path does not exist.
- `STOP_VIDEO_TYPE_UNSUPPORTED`: video extension is unsupported.
- `STOP_FFMPEG_FAILED`: ffmpeg returned a nonzero exit.
- `STOP_FFMPEG_TIMEOUT`: ffmpeg exceeded the timeout.
- `STOP_NO_FRAMES`: frame extraction produced no images.
- `STOP_CODEX_FAILED`: Codex returned a nonzero exit.
- `STOP_CODEX_TIMEOUT`: Codex exceeded the timeout.

## Completion Rule

Use `TELEGRAM_HERMES_CODEX_VISION_ACTION_SKILL_PASS` only after G01 through G10 have current evidence. If phone Telegram sends or Codex CLI execution were not performed, report the exact STOP gate instead.
