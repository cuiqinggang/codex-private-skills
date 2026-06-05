---
name: xiaolongxia-boot-replay-autostart
description: Use when replaying or repairing the post-boot Xiaolongxia mature startup chain: New API 3011 health/login, model-pool health, internal LLM selftest, OpenClaw 18789 browser open, and the independent Windows logon autostart task. Includes the 2026-05-24 safety rule that 3011 is New API, not Xiaolongxia UI, and must not open Hermes/AiMaShi.
metadata:
  short-description: Xiaolongxia boot replay and autostart
---

# Xiaolongxia Boot Replay Autostart

Use this skill when the machine has just booted or when the user asks to restore Xiaolongxia's mature local chain without redesign.

## Fixed Meaning

- `http://127.0.0.1:3011` is New API / model-pool management and API base only.
- `http://127.0.0.1:3011/console` is the New API console.
- `http://127.0.0.1:3011/v1` is the model-pool API base.
- `http://127.0.0.1:18789/` is the verified OpenClaw Control browser page after gateway health and title checks.
- Never treat `3011` as Xiaolongxia UI.
- Never open Hermes/AiMaShi, Open WebUI, old `3001`, or unverified ports for this flow.

## Use These First

Before this skill does browser or autostart work, also load:

- `xiaolongxia-openclaw-gateway-safety-recovery`
- `xiaolongxia-3011-openclaw-connect`
- `xiaolongxia-free-provider-expansion`

The hard G00 rule still applies: confirm New API 3011 is reachable and logged in as New API, then write `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`.

## Mature Replay Sequence

0. Visible browser safety gate:
   - Take a full desktop screenshot first, not only an active-window screenshot.
   - Identify all visible windows and window titles before typing.
   - The correct visible browser target is `OpenClaw Control - Google Chrome` with URL `http://127.0.0.1:18789/`.
   - Do not type into any window until a screenshot confirms the address bar is `127.0.0.1:18789` and the page is OpenClaw.
   - If focus lands on WeChat, ChatGPT, Hermes/AiMaShi, New API 3011, or any other page, stop and refocus by exact window title/handle.
   - Never treat "page opened" as success. Success requires a visible in-page test prompt and a visible model reply.

1. New API replay:
   - Check `127.0.0.1:3011` listener.
   - If needed, start `docker compose up -d` in `C:\Users\A\xiaolongxia-free-api-local`.
   - Confirm `http://127.0.0.1:3011/api/status`.
   - Confirm admin login with `xya6338`; password is stored only in `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`.
   - Do not print the password.

2. Model-pool replay:
   - Read token only from `C:\Users\A\xiaolongxia-free-api-local\secrets\xiaolongxia_newapi_token.txt`.
   - Call `GET http://127.0.0.1:3011/v1/models`.
   - Optional minimal chat marker uses the current primary production model.

3. Xiaolongxia internal LLM replay:
   - Use `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1`.
   - Run normal `-ModelMode auto`.
   - For fallback proof, run `-ModelMode auto -SimulatePrimaryFailure`.
   - Do not send messages or require the Xiaolongxia UI.

4. OpenClaw browser replay:
   - Start gateway on loopback only if `18789` is not listening.
   - Verify `openclaw gateway health --json --timeout 20000`.
   - Verify `GET http://127.0.0.1:18789/` has title `OpenClaw Control`.
   - Only then open Chrome at `http://127.0.0.1:18789/`.
   - Never open `3011` as a Xiaolongxia browser page.
   - If OpenClaw shows the authorization page, use the local gateway token file only for the browser login workflow and do not print it. For SecretRef-managed gateway auth, `openclaw dashboard --yes` may open the page but does not auto-fill the token.
   - Approve the visible `openclaw-control-ui` device request with `openclaw devices approve <requestId> --json` when prompted, then reopen or reconnect the existing Chrome tab.
   - After the page shows the chat UI, send a visible marker prompt and require a visible marker reply before claiming success.

5. Autostart replay:
   - Use independent directory `C:\Users\A\Xiaolongxia_BootReplay_AutoStart`.
   - Use independent task `Xiaolongxia_BootReplay_Logon`.
   - Do not reuse failed directory `C:\Users\A\Xiaolongxia_AutoStart`.
   - Keep old failed task `Xiaolongxia_Autostart_Logon` disabled.

## Current Verified Savepoint

Output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-TO-AUTOSTART-20260524`

Additional three-repeat visible verification:

- Output root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-3X-VERIFY-20260524`
- Final status: `XIAOLONGXIA_BOOT_REPLAY_3X_VERIFY_PASS`
- The user-requested normal Google Chrome path was verified three times.
- Round 1 OpenClaw evidence: `round-1\R1-normal-chrome-openclaw-after-send.png`
- Round 2 OpenClaw evidence: `round-2\R2-strict-marker-after-send.png`
- Round 3 OpenClaw evidence: `round-3\R3-openclaw-final-after-send-57s-existing-chrome.png`
- Final full desktop evidence: `R3-final-full-desktop-openclaw-pass-visible.png`
- Read `references/boot-replay-3x-verify-20260524.md` before repeating visible browser work.

Important correction from the three-repeat run:

- If Chrome focus lands on Feishu, Google Docs, ChatGPT, WeChat, New API, or any non-OpenClaw page, reject that screenshot as pass evidence.
- Do not use `Ctrl+A` or Enter until the screenshot proves the message box on `127.0.0.1:18789` is focused.
- If a screenshot accidentally contains sensitive content from another tab, do not quote it, embed it, or treat it as success evidence.
- The reliable way to recover is to open a new tab in the existing normal Google Chrome session with `chrome.exe --new-tab http://127.0.0.1:18789/`, then refocus the exact `OpenClaw Control - Google Chrome` window handle before typing.

Later strict-method retest result:

- Output root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-3X-STRICT-METHOD-20260524`
- Final status: `XIAOLONGXIA_BOOT_REPLAY_3X_STRICT_METHOD_NOT_100_STOP`
- Read `references/strict-method-retest-not-100-20260524.md` before claiming this browser method is 100% reliable.
- New lessons:
  - Do not use `Ctrl+A` in OpenClaw; it can select the page instead of the input.
  - Do not trust send-button coordinates; use Enter only after a screenshot proves marker text is inside the input.
  - Do not trust `chrome.exe --new-tab` as foreground proof.
  - After every wait, take a full desktop screenshot and verify the foreground page is still OpenClaw.
  - If focus drifts to Douyin, ChatGPT, Feishu, WeChat, Google Docs, or any other tab, the evidence is invalid and the round cannot be counted as clean PASS.

Visible browser evidence added after the user's correction:

- Full desktop screenshot before identifying the correct window: `visible-evidence-existing-chrome\STEP4-full-desktop-before-identify-correct-window.png`
- Correct OpenClaw window focused by exact title/handle: `visible-evidence-existing-chrome\STEP4-openclaw-exact-window-focused.png`
- Visible OpenClaw web test result: `visible-evidence-existing-chrome\STEP4-openclaw-visible-web-test-result.png`
- Marker returned on the visible page: `XIAOLONGXIA_VISIBLE_WEB_OK`

Status codes:

- `STEP1_NEWAPI_REPLAY_PASS`
- `STEP2_MODEL_POOL_REPLAY_PASS`
- `STEP3_XIAOLONGXIA_MODEL_LINK_REPLAY_PASS`
- `STEP4_XIAOLONGXIA_BROWSER_REPLAY_PASS`
- `STEP5_REPLAY_FLOW_SAVED_PASS`
- `STEP6_AUTOSTART_REPLAY_CREATED_PASS`
- `XIAOLONGXIA_BOOT_REPLAY_TO_AUTOSTART_PASS`

Verified task:

- `Xiaolongxia_BootReplay_Logon`
- Trigger: Windows logon
- Action: `C:\Users\A\Xiaolongxia_BootReplay_AutoStart\Run-Xiaolongxia-BootReplay.cmd`
- Manual task run result: `0`
- Latest manual run status: `BOOT_REPLAY_AUTOSTART_RUN_PASS`

## Bundled Scripts

Copies of the current scripts are bundled under `scripts\`:

- `scripts\Run-Xiaolongxia-BootReplay.cmd`
- `scripts\Start-Xiaolongxia-BootReplay.ps1`
- `scripts\Disable-Xiaolongxia-BootReplay-Task.ps1`

Operational source path:

`C:\Users\A\Xiaolongxia_BootReplay_AutoStart`

## Rollback

Disable the new task:

```powershell
C:\Users\A\Xiaolongxia_BootReplay_AutoStart\Disable-Xiaolongxia-BootReplay-Task.ps1
```

Or:

```powershell
Disable-ScheduledTask -TaskName Xiaolongxia_BootReplay_Logon
```

Do not enable or reuse `Xiaolongxia_Autostart_Logon`; it belongs to the earlier failed 3011-as-UI incident.

## Safety Rules

- Do not modify Hermes/AiMaShi.
- Do not modify Open WebUI.
- Do not modify old `3001` New API.
- Do not modify 3011 model-pool channels, groups, tokens, or production route while replaying.
- Do not print passwords, API keys, New API tokens, OpenRouter keys, or NVIDIA keys.
- Do not connect real group chats.
- Do not call Feishu, WeChat, Telegram, or any real send function.
- If any browser opens Hermes/AiMaShi, stop and switch to `xiaolongxia-openclaw-gateway-safety-recovery`.
- If a screenshot after a browser action shows WeChat or ChatGPT instead of OpenClaw, that screenshot is invalid for Xiaolongxia evidence. Stop, take a full desktop screenshot, enumerate window titles, and refocus the exact `OpenClaw Control - Google Chrome` window before testing again.

Read `references/boot-replay-20260524.md` for the exact evidence and command summary from the verified savepoint.

## 2026-05-24 Model Exhaustion Repair Addendum

If OpenClaw opens but the chat page shows `停止`, do not assume the browser flow is broken first. Check model routing.

Known failure:

- Old visible sessions may still show `xiaolongxia-primary-temp`.
- That route points into the 3011/OpenRouter model pool.
- When the 3011 pool is exhausted, the page can show `assistant turn failed before producing content`.

Repaired route:

- Current primary after user quality correction: `nvidia-nim/meta/llama-3.1-70b-instruct`
- Current fallback after user quality correction: none
- Do not use NVIDIA 8B as the mature default unless the user explicitly asks for speed/cost-saving mode.

Evidence root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-OPENCLAW-INPROGRESS-STOP-REPAIR-20260524`

Visible proof:

- `G04-openclaw-visible-window-after-refresh-crop.png`
- Model selector: `xiaolongxia-nvidia-8b...`
- Marker reply: `XIAOLONGXIA_DEFAULT_AFTER_REPAIR_8B_OK`

Before saving a boot replay as successful, verify both:

1. New or refreshed OpenClaw page is using `xiaolongxia-nvidia-70...`, not `xiaolongxia-primary-temp` and not `xiaolongxia-nvidia-8b...`.
2. A visible in-page marker reply is returned after the route repair.

Latest model switch evidence:

- Output root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-SWITCH-TO-70B-20260524`
- Status: `XIAOLONGXIA_DEFAULT_MODEL_SWITCHED_TO_NVIDIA_70B_PASS`
- Visible crop: `G07-visible-70b-session-crop.png`
