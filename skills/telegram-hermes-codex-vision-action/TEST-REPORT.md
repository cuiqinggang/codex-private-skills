# Test Report

Task ID: `TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525`

Report time: `2026-05-25 12:31 Asia/Shanghai`

## Current Result

Status: `G01_RUNTIME_BASE_READY_WITH_STARTUP_ENTRY_MISSING`

Reason: R3 corrected G01 into runtime readiness and startup persistence checks. Runtime readiness is ready for image/video closed-loop testing; the only remaining issue is missing startup persistence, which is WARN only.

- G01A Runtime Base Readiness: PASS.
- G01B Startup Persistence Check: WARN, startup entry missing.
- Startup entry path: `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`.
- This WARN does not block `/codeximg` or `/codexvideo` testing.

Do not output `TELEGRAM_HERMES_CODEX_VISION_ACTION_SKILL_PASS` until phone Telegram image/video closed-loop gates have current PASS evidence.

## Gate Evidence

### G01A Runtime Base Readiness

Status: `PASS`

Evidence file:

- `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\G01-base-readiness.log`
- Final rerun: `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\G01-base-readiness-final.log`
- R3 rerun: `C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G01-after-G04R2B-base-readiness.txt`

Observed:

- Hermes CLI exists: PASS.
- Hermes profile exists: PASS.
- Telegram env keys exist with token redacted: PASS.
- Gateway status command: PASS.
- `gateway_state.json` api_server connected: PASS.
- `gateway_state.json` telegram connected: PASS.
- Local proxy listener `127.0.0.1:7890`: PASS.
- Hermes health endpoint: PASS.
- Hermes models endpoint: PASS.
- Open WebUI `http://127.0.0.1:3000`: PASS.
- Gateway task script exists: PASS.
- Recent logs include Telegram connected, inbound message, response ready, and Sending response.
- `ffmpeg -version`: PASS.
- `C:\Users\A\AppData\Roaming\npm\codex.cmd --version`: PASS, `codex-cli 0.133.0`.
- `C:\Users\A\AppData\Roaming\npm\codex.cmd login status`: PASS, exit code 0, logged in using ChatGPT.
- `codex.cmd exec` smoke: PASS, `G04R2B_PASS_CODEX_EXEC_OK`.
- Runtime status: `G01_RUNTIME_BASE_READY_WITH_STARTUP_ENTRY_MISSING`.

### G01B Startup Persistence Check

Status: `WARN_STARTUP_ENTRY_MISSING`

Observed:

- Startup entry exists: WARN/MISSING.
- Missing path: `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`.
- This is a persistence warning only. It does not block runtime `/codeximg` or `/codexvideo` tests.
- No startup entry was created during R3.
- Hermes current startup method was not changed.
- Telegram configuration was not changed.
- DeepSeek/New API/Open WebUI were not changed.

### G04R2B Codex Exec Smoke

Status: `G04R2B_PASS_CODEX_EXEC_OK`

Evidence:

- Log: `C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-codex-exec-smoke.txt`
- Final message: `C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-last-message.txt`
- Stdout: `C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-stdout.txt`
- Stderr: `C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-stderr.txt`
- Marker: `CODEX_EXEC_R2B_SMOKE_OK`.
- Exit code: `0`.

### G02 Image Landing

Status: `STOP_MANUAL_TELEGRAM_IMAGE_NOT_RUN`

Reason: a phone Telegram `/codeximg` image message was not sent during this run. The provided WeChat temp JPG exists and was used only as a local fixture, not as proof of Telegram landing.

### G03 Codex Image Recognition

Status: `PENDING_RERUN_AFTER_CODEX_FIX`

Reason: the earlier `Access is denied` blocker was fixed by installing the npm Codex CLI and validating `codex.cmd exec` in G04R2B. The image recognition marker check still needs a fresh run with the fixed npm CLI before this gate can be marked PASS.

Evidence file:

- `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\G03-codex-image-recognition.log`

### G04 Image Wrapper

Status: `LOCAL_DRY_RUN_PASS`

Files:

- `C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1`
- `H:\Hermes_Skills\telegram-hermes-codex-vision-action\scripts\Invoke-CodexImageExec.ps1`

Expected artifacts:

- `task.txt`
- `result.txt`
- `media-manifest.json`
- `codex-command.json`

Evidence:

- `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TEST-IMG-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\result.txt`
- Result marker: `DRY_RUN_NO_CODEX_INVOCATION`

### G05 Video Landing

Status: `STOP_MANUAL_TELEGRAM_VIDEO_NOT_RUN`

Reason: a phone Telegram `/codexvideo` video message was not sent during this run.

### G06 Video Frame Extraction

Status: `LOCAL_DRY_RUN_PASS`

Evidence:

- Fixture video: `C:\Users\A\Desktop\1\input\telegram-media\videos\TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525-fixture.mp4`
- Frames directory: `C:\Users\A\Desktop\1\input\telegram-media\frames\TEST-VID-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525`
- Extracted frames: `frame_0001.jpg`, `frame_0002.jpg`

### G07 Video Wrapper

Status: `LOCAL_DRY_RUN_PASS`

Files:

- `C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1`
- `H:\Hermes_Skills\telegram-hermes-codex-vision-action\scripts\Invoke-CodexVideoExec.ps1`

Expected artifacts:

- `task.txt`
- `result.txt`
- `media-manifest.json`
- `codex-command.json`
- `ffmpeg.log`

Evidence:

- `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TEST-VID-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\result.txt`
- Result marker: `DRY_RUN_NO_CODEX_INVOCATION`
- Frame count: `2`

### G08 Telegram Image Closed Loop

Status: `STOP_MANUAL_TELEGRAM_IMAGE_CLOSED_LOOP_NOT_RUN`

Reason: requires a real phone Telegram image send and Telegram reply verification.

### G09 Telegram Video Closed Loop

Status: `STOP_MANUAL_TELEGRAM_VIDEO_CLOSED_LOOP_NOT_RUN`

Reason: requires a real phone Telegram video send and Telegram reply verification.

### G10 Skill Save

Status: `LOCAL_VALIDATION_PASS_WITH_EXTERNAL_STOPS`

Package path:

- `H:\Hermes_Skills\telegram-hermes-codex-vision-action`

Required files:

- `README.md`
- `SKILL.md`
- `DAILY-RUN.md`
- `RECOVERY.md`
- `TEST-REPORT.md`
- `scripts\Invoke-CodexImageExec.ps1`
- `scripts\Invoke-CodexVideoExec.ps1`

Evidence:

- Skill validator: `Skill is valid!`
- Local validation log: `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\G10-local-validation.log`
- Final local validation log: `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\G10-local-validation-final.log`
- Local validation result: `TEST_PASS`

## Commands Used

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
codex --version
codex login status
ffmpeg -version
python "C:\Users\A\.codex\skills\.system\skill-creator\scripts\init_skill.py" telegram-hermes-codex-vision-action --path "H:\Hermes_Skills" --resources scripts
python "C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "H:\Hermes_Skills\telegram-hermes-codex-vision-action"
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-TELEGRAM-HERMES-CODEX-VISION-ACTION-SKILL-20260525\tests\Test-TelegramHermesCodexVisionAction.ps1"
codex --image "F:\000\xwechat_files\wxid_bq3n41o6t4o721_699b\temp\RWTemp\2026-05\0af7c60bf5b2c143d160ba3441fcefa7\21a708fd7c1ac574fad6ad5635b0ec6f.jpg" "请严格输出 CODEX_IMAGE_OK，并用一句话描述图片"
```

## R3 Commands Used

```powershell
C:\Users\A\AppData\Roaming\npm\codex.cmd exec "请严格只输出：CODEX_EXEC_R2B_SMOKE_OK" -o "C:\Users\A\Desktop\1\output\CODEX-ACCESS-DENIED-R2\G04R2B-last-message.txt"
C:\Users\A\AppData\Roaming\npm\codex.cmd --version
C:\Users\A\AppData\Roaming\npm\codex.cmd login status
ffmpeg -version
```
