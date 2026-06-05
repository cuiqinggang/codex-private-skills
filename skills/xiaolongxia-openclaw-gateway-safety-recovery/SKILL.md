---
name: xiaolongxia-openclaw-gateway-safety-recovery
description: Use when Xiaolongxia/OpenClaw startup, browser-open, gateway recovery, or autostart work risks opening Hermes/AiMaShi, mistaking 3011 for Xiaolongxia UI, using 18798 without proof, or needing the 2026-05-24 rollback and 18789 recovery runbook.
---

# Xiaolongxia OpenClaw Gateway Safety Recovery

## Core Rule

Treat wrong-browser launch as a safety incident, not a cosmetic mistake. If a Xiaolongxia task opens Hermes/AiMaShi, `http://localhost:3011`, or any unverified UI URL, stop browser automation and recover isolation before continuing.

Read `references/incident-20260524.md` when reconstructing the full incident, report paths, or exact evidence.
Read `references/g00-newapi-start-login-20260524.md` when a task needs the verified New API 3011 login baseline, credential-file location, or G00 evidence paths.

## Mandatory G00: New API Start And Login

Run this before any Xiaolongxia, OpenClaw, browser UI recovery, autostart redesign, or model-route confirmation task.

Purpose: independently confirm the New API/model-pool server is reachable and login works, while preventing `3011` from being mistaken for Xiaolongxia UI.

Execution location: Windows PowerShell plus Windows Chrome/Edge browser.

Required actions:

1. Check whether `127.0.0.1:3011` is listening.
2. If not listening, use existing New API skills/history to start only the New API/model-pool service.
3. Open `http://127.0.0.1:3011`.
4. Complete New API login without printing or saving credentials.
5. Read-only confirm at least one backend page is accessible, such as Channels, Models, Tokens, or Dashboard.
6. Save evidence to the current task output directory: port status, HTTP status, login/page-title or screenshot evidence, channel/model-pool page evidence, and the exact marker `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`.

Success criteria:

- `127.0.0.1:3011` is accessible.
- New API login is confirmed.
- A backend page is accessible.
- The report explicitly states `3011 = New API / model pool`.
- The report explicitly states `18789`, `18798`, or another proven URL must be discovered separately for OpenClaw/Xiaolongxia UI.
- No production model-pool channel, token, group, or route configuration is modified.
- No real message is sent.

Failure criteria:

- `3011` cannot listen or cannot be opened.
- New API login cannot be confirmed.
- A backend page cannot be reached after login.
- Any step treats `3011` as Xiaolongxia UI.

Failure recovery:

- Stop Xiaolongxia/OpenClaw UI recovery and browser testing.
- Output a failure report only.
- Use status `STOP_NEWAPI_LOGIN_NOT_CONFIRMED`.

Continue only after G00 passes.

Latest verified G00 savepoint:

- Status: `G00_NEWAPI_START_AND_LOGIN_PASS`
- Marker: `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`
- New API URL: `http://127.0.0.1:3011`
- Console URL: `http://127.0.0.1:3011/console`
- API Base: `http://127.0.0.1:3011/v1`
- Admin username: `xya6338`
- Admin credential file: `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`
- Evidence root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-G00-NEWAPI-START-LOGIN-20260524`

Do not print the password from the credential file. Use it only for local login verification when the user asks for New API browser confirmation.

## Fixed Meaning Of Ports

| Port | Meaning | Browser Rule |
| --- | --- | --- |
| `3011` | New API / model pool management | Do not treat as Xiaolongxia product UI or OpenClaw browser UI. |
| `18798` | Previously suspected Xiaolongxia UI candidate | Do not use unless a current readonly check proves it is listening and belongs to Xiaolongxia. |
| `18789` | Windows OpenClaw gateway/browser recovery path | May be used only for OpenClaw gateway/browser checks on loopback. |
| `8642` | Hermes/AiMaShi area | Do not open, modify, or reuse for Xiaolongxia. |
| `3000` | Open WebUI area on this machine | Do not reuse for Xiaolongxia. |

## Hard Stops

Stop immediately if any of these happen:

- A Xiaolongxia task opens Hermes/AiMaShi.
- A script opens `http://localhost:3011` as if it were Xiaolongxia UI.
- A task tries to enable `Xiaolongxia_Autostart_Logon` before the true UI URL is proven.
- A script would open a browser before the URL has been identified as OpenClaw/Xiaolongxia.
- Any real group chat send path, Feishu/WeChat/Telegram send function, or public bind is involved.
- Any token, API key, password, or admin credential would be printed into logs or reports.

## Recovery Workflow

1. Freeze the browser path.
   Do not open 3011, 18798, Hermes, Open WebUI, or any guessed URL.

2. Disable Xiaolongxia autostart risk.
   Check `Xiaolongxia_Autostart_Logon`. Disable it if present and active. Do not touch Hermes tasks.

3. Neutralize unsafe scripts.
   `C:\Users\A\Xiaolongxia_AutoStart\Run-Xiaolongxia-Autostart.cmd` and companion scripts must be disabled stubs or quarantined. A safe stub only prints `DISABLED_DUE_TO_ISOLATION_FAILURE` and exits.

4. Confirm Hermes isolation.
   Read only. Verify `C:\Users\A\Hermes_AutoStart`, `C:\Users\A\.hermes`, Hermes scheduled tasks, Open WebUI, old 3001, and 3011 configuration were not modified.

5. Stop looking for 18798 unless current evidence exists.
   The 2026-05-24 discovery found no 18798 listener and no product UI entry under `C:\Users\A\xiaolongxia-free-api-local`.

6. Recover OpenClaw manually on 18789 only.
   Use Windows OpenClaw, loopback binding, temporary token, and no persistent service or scheduled task.

## Safe Readonly Checks

Use these checks before any browser open:

```powershell
Get-ScheduledTask -TaskName 'Xiaolongxia_Autostart_Logon' -ErrorAction SilentlyContinue
Get-Content -Raw 'C:\Users\A\Xiaolongxia_AutoStart\Run-Xiaolongxia-Autostart.cmd' -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 18798 -ErrorAction SilentlyContinue
openclaw --version
openclaw gateway health --json --timeout 20000
```

Do not run `Run-Xiaolongxia-Autostart.cmd` during recovery. It is expected to stay disabled after the incident.

## Manual OpenClaw Gateway Recovery Pattern

Use this only after autostart is confirmed safe:

```powershell
openclaw gateway run --allow-unconfigured --bind loopback --port 18789 --auth token --token <temporary-token> --verbose
openclaw gateway health --token <temporary-token> --json --timeout 20000
Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:18789/'
```

Rules:

- Use only loopback.
- Do not install a service.
- Do not create or enable a scheduled task.
- Do not persist the temporary token.
- Do not configure models unless the user asked for model integration.
- Do not open browser unless the 18789 response is confirmed to be OpenClaw.

## Browser Open Rule

Open a browser only when all are true:

- The target URL was verified in the same task.
- The target is `http://127.0.0.1:18789/` or another proven OpenClaw/Xiaolongxia URL.
- The page is not Hermes/AiMaShi, not 3011 New API, not Open WebUI, and not an old browser-restored tab.
- There is no autostart or real-send risk.

If the browser opens a wrong page once, mark the whole browser-open/autostart path failed and return to the recovery workflow.

## Corrected Boot Replay Autostart Savepoint

After the 2026-05-24 wrong-page incident, the corrected mature boot replay and autostart path was saved as:

`xiaolongxia-boot-replay-autostart`

The later user-requested three-repeat visible verification is saved under:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-3X-VERIFY-20260524`

Final status:

`XIAOLONGXIA_BOOT_REPLAY_3X_VERIFY_PASS`

Key lesson added by that run:

- Full desktop screenshots are required when focus may be ambiguous.
- Active-window screenshots alone are not enough after a send/wait action because focus can move to Feishu, Google Docs, ChatGPT, or WeChat.
- A diagnostic screenshot that shows the wrong page, especially one containing sensitive browser content, must be rejected as pass evidence and must not be quoted.
- Continue only after the exact normal Chrome window title is `OpenClaw Control - Google Chrome` and the page address is `127.0.0.1:18789`.

Use that skill for post-boot recovery and the independent Windows logon task. Its verified task is `Xiaolongxia_BootReplay_Logon`, not the failed `Xiaolongxia_Autostart_Logon`.

Current verified chain:

1. Confirm `3011` is New API/model pool and write `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`.
2. Confirm `/v1/models` and a minimal model-pool call.
3. Run the saved Xiaolongxia internal LLM selftest, including forced fallback.
4. Confirm OpenClaw gateway health on `127.0.0.1:18789`.
5. Verify page title `OpenClaw Control`.
6. Take a full desktop screenshot and identify the exact `OpenClaw Control - Google Chrome` window before typing.
7. Only then open or refocus Chrome at `http://127.0.0.1:18789/`.
8. Complete a visible in-page marker test; the accepted marker is `XIAOLONGXIA_VISIBLE_WEB_OK`.

Important failure lesson from the visible replay:

- Active-window screenshots can be wrong when WeChat or ChatGPT steals focus.
- A screenshot of ChatGPT, WeChat, New API 3011, or Hermes is not Xiaolongxia evidence.
- Do not type until the full desktop screenshot and window title confirm the active target is `OpenClaw Control - Google Chrome`.
- The valid visible evidence path is `visible-evidence-existing-chrome\STEP4-openclaw-visible-web-test-result.png` under the verified output root.

Verified output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-TO-AUTOSTART-20260524`

Final status:

`XIAOLONGXIA_BOOT_REPLAY_TO_AUTOSTART_PASS`

## Skill Updates After Incidents

When this incident class appears again, update:

- this skill
- `xiaolongxia-3011-openclaw-connect`
- any task report under `C:\Users\A\Desktop\1\output\...`
- H drive mirrors under `H:\CodexSkills`

Never store secrets in skills. Record only paths to secret files, status codes, hashes, and redacted evidence.

## 2026-05-24 OpenClaw Stop / Exhausted Model Pool Repair

Use `references/openclaw-nvidia-switch-repair-20260524.md` when OpenClaw/Xiaolongxia shows `停止`, `assistant turn failed before producing content`, or repeated 403 balance/pre-charge failures from the 3011/OpenRouter pool.

Verified repair status:

`XIAOLONGXIA_OPENCLAW_NVIDIA_SWITCH_REPAIR_PASS`

Root cause:

- The visible OpenClaw session was pinned to `xiaolongxia-primary-temp`.
- The 3011/OpenRouter pool was failing with 403 pre-charge/balance errors.
- Fallback was only rotating inside the exhausted 3011 pool, so it needed a cross-provider NVIDIA fallback route.

Current repaired route:

- Primary after user quality correction: `nvidia-nim/meta/llama-3.1-70b-instruct`
- Fallback after user quality correction: none
- Historical repair route was 8B primary + 70B fallback, but the user later rejected 8B quality.

Required verification before claiming fixed:

1. `openclaw config validate` passes.
2. Gateway log shows `agent model: nvidia-nim/meta/llama-3.1-8b-instruct`.
3. 8B marker test returns `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_8B_RERUN_OK`.
4. 70B marker test returns `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_70B_OK`.
5. Forced/observed fallback test returns `XIAOLONGXIA_NVIDIA_AUTO_FALLBACK_70B_OK`.
6. Visible Chrome/OpenClaw page shows `xiaolongxia-nvidia-8b...` and returns `XIAOLONGXIA_DEFAULT_AFTER_REPAIR_8B_OK`.

Later correction:

- Evidence root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-SWITCH-TO-70B-20260524`
- Status: `XIAOLONGXIA_DEFAULT_MODEL_SWITCHED_TO_NVIDIA_70B_PASS`
- New visible proof: `G07-visible-70b-session-crop.png`
- Do not claim the current mature route uses 8B by default. The current mature default is NVIDIA 70B.
