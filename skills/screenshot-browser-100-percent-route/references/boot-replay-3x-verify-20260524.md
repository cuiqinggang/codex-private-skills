# Xiaolongxia Boot Replay 3x Visible Verification 2026-05-24

## Status

`XIAOLONGXIA_BOOT_REPLAY_3X_VERIFY_PASS`

This savepoint records the user's requested three-repeat visible verification after the wrong-window and wrong-browser corrections.

## Output Root

${REDACTED_SECRET}

## Confirmed Rule

- Use the already-open normal Google Chrome profile when visible browser evidence is required.
- Do not use the Codex in-app browser, a temporary Playwright profile, Quark, or a Chrome app window as the final visible evidence path unless the user explicitly asks for that.
- `3011` is New API/model pool only.
- `18789` is the OpenClaw visible browser target.
- A page being open is not enough; the page must visibly return the marker reply.

## Three Round Evidence

### Round 1

- New API visible page: `round-1\R1-newapi-active-window-visible.png`
- New API API check: `round-1\R1-newapi-api-models-chat-test.json`
- OpenClaw before send: `round-1\R1-normal-chrome-openclaw-before-send.png`
- OpenClaw marker result: `round-1\R1-normal-chrome-openclaw-after-send.png`

### Round 2

- New API visible page: `round-2\R2-newapi-active-window-visible.png`
- New API API check: `round-2\R2-command-and-newapi-api-test.json`
- OpenClaw strict marker result: `round-2\R2-strict-marker-after-send.png`

### Round 3

- New API visible page: `round-3\R3-newapi-active-window-visible.png`
- New API API check: `round-3\R3-command-and-newapi-api-test.json`
- OpenClaw correct new tab in existing Chrome: `round-3\R3-openclaw-opened-by-existing-chrome-command.png`
- OpenClaw before final send: `round-3\R3-openclaw-final-before-send-existing-chrome.png`
- OpenClaw marker result: `round-3\R3-openclaw-final-after-send-57s-existing-chrome.png`
- Full desktop final evidence: `R3-final-full-desktop-openclaw-pass-visible.png`

Visible returned marker:

`XIAOLONGXIA_3X_R3_STRICT_OK`

## Rejected Evidence And Cause

These files are failure/diagnostic evidence only and must not be used as pass evidence:

- `round-3\R3-openclaw-after-send.png`: foreground focus was wrong.
- `round-3\R3-openclaw-after-enter-send.png`: wrong foreground page and sensitive browser content. Do not quote or embed it.
- `round-3\R3-active-chrome-before-final-retry.png`: proved the foreground was Feishu, not OpenClaw.

## Corrected Browser Operation Pattern

1. Take a full desktop screenshot.
2. Enumerate visible windows and titles.
3. Prefer the existing normal Google Chrome process.
4. If the existing Chrome active tab is not OpenClaw, open a new tab in that same Chrome session with `chrome.exe --new-tab http://127.0.0.1:18789/`.
5. Confirm the active title is `OpenClaw Control - Google Chrome` and the address is `127.0.0.1:18789`.
6. Press Escape to close transient browser popups such as Google Translate or tab previews.
7. Click the OpenClaw message box, paste the marker prompt, screenshot before send.
8. Click the visible Send button and wait.
9. Refocus the same exact window handle before taking the result screenshot.
10. Accept success only when the OpenClaw page itself shows the marker reply.

## Safety Notes

- Do not touch Feishu/WeChat/Telegram send controls.
- Do not treat Feishu developer console as OpenClaw chat evidence.
- Do not treat Google Docs/ChatGPT screenshots as OpenClaw evidence.
- Do not quote any sensitive content accidentally visible in diagnostic screenshots.
- Leave unrelated browser tabs alone.

## Final Report

${REDACTED_SECRET}
