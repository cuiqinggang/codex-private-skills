# Xiaolongxia Boot Replay 2026-05-24

This reference records the verified mature replay and autostart savepoint.

## Paths

- Output root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-TO-AUTOSTART-20260524`
- Operational autostart root: `C:\Users\A\Xiaolongxia_BootReplay_AutoStart`
- New API project: `C:\Users\A\xiaolongxia-free-api-local`
- OpenClaw command: `C:\Users\A\AppData\Roaming\npm\openclaw.cmd`
- OpenClaw config: `C:\Users\A\.openclaw\openclaw.json`

## Verified Commands

New API status and login:

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 3011
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3011/api/status
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3011/api/user/login -Method Post
```

Model pool:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3011/v1/models -Headers @{ Authorization = "Bearer <local-token>" }
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3011/v1/chat/completions -Method Post
```

Internal LLM replay:

```powershell
C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode auto
C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode auto -SimulatePrimaryFailure
```

OpenClaw gateway:

```powershell
openclaw gateway run --allow-unconfigured --bind loopback --port 18789 --verbose
openclaw gateway health --json --timeout 20000
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:18789/
```

Autostart manual run:

```powershell
C:\Users\A\Xiaolongxia_BootReplay_AutoStart\Run-Xiaolongxia-BootReplay.cmd
Start-ScheduledTask -TaskName Xiaolongxia_BootReplay_Logon
```

## Results

- STEP1 New API replay: PASS.
- STEP2 model pool replay: PASS.
- STEP3 internal LLM normal auto and forced fallback: PASS.
- STEP4 OpenClaw gateway 18789 health, identity, browser open, and visible in-page model reply: PASS.
- STEP6 new independent scheduled task manual trigger: PASS.
- Final status: `XIAOLONGXIA_BOOT_REPLAY_TO_AUTOSTART_PASS`.

## Key Evidence

- `STEP1-newapi-replay.json`: admin API login succeeded as `xya6338`, role `100`, password not printed.
- `STEP2-model-pool-health.json`: `/v1/models` returned 19 models; primary chat marker succeeded.
- `STEP3-internal-llm-auto-normal`: normal auto mode passed.
- `STEP3-internal-llm-auto-forced-fallback`: forced fallback mode passed.
- `STEP4-openclaw-infer-smoke.json`: OpenClaw gateway model run returned `BOOT_REPLAY_OPENCLAW_OK`.
- `visible-evidence-existing-chrome\STEP4-full-desktop-before-identify-correct-window.png`: full desktop screenshot used to identify the correct window and avoid confusing WeChat/ChatGPT with OpenClaw.
- `visible-evidence-existing-chrome\STEP4-openclaw-exact-window-focused.png`: exact `OpenClaw Control - Google Chrome` window focused, URL `127.0.0.1:18789`, model selector visible.
- `visible-evidence-existing-chrome\STEP4-openclaw-visible-web-test-result.png`: visible OpenClaw page returned `XIAOLONGXIA_VISIBLE_WEB_OK`.
- `STEP6-scheduled-task-manual-run.json`: `lastTaskResult=0`, latest run `BOOT_REPLAY_AUTOSTART_RUN_PASS`.

## Failed Paths Captured And Ruled Out

These screenshots were deliberately not accepted as success evidence:

- `visible-evidence-existing-chrome\STEP4-existing-chrome-openclaw-connected-ui-chinese-test-after-send.png`: the browser focus had switched to a ChatGPT tab, so it was not Xiaolongxia/OpenClaw evidence.
- `visible-evidence-existing-chrome\STEP4-existing-chrome-after-click-openclaw-tab-confirm-address.png`: the foreground window was WeChat, so it was a real-send risk and not valid evidence.
- `visible-evidence-existing-chrome\STEP4-existing-chrome-force-topmost-check.png`: the foreground window was still WeChat, so it was rejected.

Corrected rule: always take a full desktop screenshot, enumerate window titles, and focus the exact `OpenClaw Control - Google Chrome` window handle before typing. A visible test is not complete until the OpenClaw page itself returns a marker reply.

## Safety Evidence

- `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`.
- Browser opened only `http://127.0.0.1:18789/` after title `OpenClaw Control`.
- Visible successful page marker: `XIAOLONGXIA_VISIBLE_WEB_OK`.
- `opened_3011_as_xiaolongxia_ui=false`.
- `opened_hermes=false`.
- `real_group_send=false`.
- `key_printed=false`.
- Old failed `Xiaolongxia_Autostart_Logon` remained disabled.
- No Hermes, Open WebUI, old `3001`, or 3011 production config changes were made.
