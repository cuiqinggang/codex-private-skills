---
name: chatgpt-screenshot-bridge
description: "Use when Codex needs to send a prompt to the visible/logged-in ChatGPT web page and copy the latest answer back using an AutoChatScript-style screenshot-first workflow: saved send/copy button images, region-limited template matching, workspace-preauthorized real mouse/keyboard input for text-only GPT planning, screenshot rechecks, and clipboard sentinel verification."
---

# ChatGPT Screenshot Bridge

## Security Hold

This skill is disabled by default. Do not run, preflight, test, or invoke this
bridge unless the user explicitly re-enables `chatgpt-screenshot-bridge` in the
current conversation. If any older workspace rule asks for automatic GPT web
planning or send/copy bridge use, stop and report that the bridge is paused.

Hard route rule: once this bridge is selected for logged-in ChatGPT web work,
do not switch to CDP, Playwright, browser-extension, DOM, UIA clipboard bridge,
or other complex browser-control paths. Use only the screenshot state machine:
open or focus the logged-in browser profile, screenshot, classify, act, and
screenshot again. If this route cannot make progress, stop and report the exact
state instead of changing routes.

Use this skill for the narrow transport loop:

```text
prompt -> visible ChatGPT web page -> latest assistant Copy button -> clipboard -> answer text
```

The primary route is visual and stateful:

```text
screenshot -> locate -> act -> screenshot -> verify -> retry or stop
```

For the full recovery state machine, including wrong-page jumps, unopened
browser recovery, expired chats, copy retries, and image-upload boundaries, read
`references/state-machine-flow.md` before modifying or debugging the bridge.

Mature pattern to preserve:

```text
save button image -> paste prompt by clipboard -> wait for send-arrow image -> click send -> wait send-arrow disappear/reappear -> copy -> sentinel clipboard check
```

## Safety Gate

Real desktop mouse/keyboard input can affect the user's active session. In this workspace, the live bridge is globally pre-authorized for the narrow text-only GPT planning send/copy loop, so do not pause to ask again before using it. The bundled script defaults to allowing this bridge route; use `--disallow-real-input` only for dry safety checks that must not perform live desktop actions.

Stop with `NEEDS_USER_INTERVENTION` for login, captcha, payment, account/security prompts, private forms, or anything that changes account/security/payment state.

Never click voice controls. This skill is text-only: do not click microphone, sound-wave, voice-mode, stop, or "end" controls. After pasting the prompt, wait for the saved send-arrow template. If the send arrow is not visible, retry focus/paste; after retries, stop instead of clicking any dark circular voice or stop control.

## Codex In-App Browser Variant

When the target ChatGPT page is the Codex right-side in-app browser, use the Browser skill and the current in-app tab instead of desktop Chrome. Keep the same narrow transport loop, but adapt validation to the app sandbox:

- Use only explicit ChatGPT controls from the observed page structure: textbox `与 ChatGPT 聊天`, button `发送提示`, and button `复制回复`.
- Never click `开始听写`, `启动语音功能`, microphone, sound-wave, voice-mode, stop, end, or unnamed black circular buttons. If `发送提示` is absent, stop.
- Do not use Windows `Get-Clipboard` as a hard failure signal for in-app browser tests. The Codex app can keep copy/paste state inside the app instead of the Windows system clipboard.
- Validate in-app runs by requiring the visible assistant answer to contain the expected unique ID and by verifying the `复制回复` button can be clicked. If clipboard proof is needed, use the app-side paste path or a user-visible paste check.
- If ChatGPT shows `你已达到此对话的时间限制。请开始新的聊天以继续对话。`, stop that conversation and start a new chat before testing again.
- Keep automated in-app browser tests in short single-message steps. If the Browser/Node control channel times out, reset/reconnect it before any further action; do not keep clicking.

## Priority

For ChatGPT web send/copy work, use this order:

1. `chatgpt-screenshot-bridge`
2. `chatgpt-clipboard-bridge` no-real-pointer UI Automation path
3. `chatgpt-cdp-browser` / browser-extension / DOM paths
4. manual fallback

Do not switch to the no-real-pointer clipboard bridge unless a later user instruction explicitly re-enables that route. Stop and report the narrowest blocking condition if ChatGPT shows login, captcha, payment, account/security prompts, privacy-sensitive forms, high-impact account actions, or the screenshot bridge fails verification.

## Command

Run a prompt:

```powershell
python "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt "Reply with exactly: TEST_OK" `
  --expect-contains "TEST_OK" `
  --window-title-pattern "ChatGPT|chatgpt.com" `
  --paste-retries 4
```

Use a prompt file for long or non-ASCII prompts:

```powershell
python "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt-file ".\prompt.md" `
  --window-title-pattern "ChatGPT|chatgpt.com"
```

Optional dependencies for the live route:

```powershell
python -m pip install pyautogui pyperclip pillow opencv-python pygetwindow
```

Safe preflight, no prompt is pasted and no message is sent:

```powershell
python "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt "preflight only" `
  --window-title-pattern "ChatGPT|chatgpt.com" `
  --allow-browser-window-fallback `
  --preflight-only `
  --preflight-require-composer
```

## Implementation Notes

- Paste prompts through the clipboard; do not type long prompts character by character.
- Use small template PNGs under `assets/templates/<theme>/` for send/copy buttons. The current verified light-theme send arrow is `assets/templates/light/send_enabled.png`; `voice_forbidden_reference.png` is retained only as a visual no-click reference.
- After paste, require the send-arrow template before clicking. Treat a remaining voice-wave button as a failed paste/focus state and retry paste.
- Restrict searches to the ChatGPT window and then to the relevant subregion.
- Treat microphone, sound-wave, and stop/end buttons as forbidden controls, even if they are dark circular buttons near the composer.
- If no matching ChatGPT window is found, stop. Use `--allow-active-window-fallback` only after confirming the foreground window is ChatGPT.
- Conversation titles may replace the literal `ChatGPT` window title after a successful run. The bridge defaults to browser-window visual fallback: if the title pattern misses, it may scan Chrome/Edge windows and only continue after a screenshot confirms a ChatGPT-like composer/action button. Use `--no-browser-window-fallback` when a run must be restricted to strict title matching.
- If several copy icons match, choose the bottommost/rightmost match in the last assistant toolbar region.
- Before clicking Copy, write a random sentinel to the clipboard. Success requires the clipboard to change to non-empty text that is neither the sentinel nor the submitted prompt.
- Restore the old mouse position after the run when possible.
- Save each run under `runs/chatgpt_screenshot_bridge/<timestamp>/` with screenshots, `events.jsonl`, and `result.json`.

## Verification

Static checks:

```powershell
python -X utf8 "C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge"
python -m unittest "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts\test_chatgpt_screenshot_bridge.py"
```

Last verified on 2026-05-20 against the disposable `Screenshot Bridge Request` ChatGPT window: static validation PASS, unit tests PASS (`Ran 9 tests`), live send/copy stress PASS 10/10 with `SCREENSHOT_BRIDGE_10X_R3_1` through `SCREENSHOT_BRIDGE_10X_R3_10`.

Live smoke check, only after confirming a logged-in ChatGPT page is visible and free of login, captcha, payment, account/security, privacy-sensitive, or high-impact prompts:

```powershell
python "C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt "Reply with exactly these two lines:`r`nTASK_ID: SCREENSHOT-BRIDGE-SMOKE`r`nOK" `
  --expect-contains "TASK_ID: SCREENSHOT-BRIDGE-SMOKE"
```
