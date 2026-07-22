---
name: screenshot-recognize-operate-browser
description: "截图识别并操作浏览器法. Use when Codex needs to operate a browser or web page by taking screenshots, recognizing visible UI controls, performing one guarded browser action at a time, re-screenshoting, and verifying the result. Trigger for visual browser workflows, ChatGPT web send/copy loops, pages where DOM automation is unreliable, UI controls that must be identified from pixels, or any task that asks for screenshot-based browser operation. Do not use real desktop mouse or keyboard input unless the user explicitly allows it for that task."
---

# 截图识别并操作浏览器法

## Core Pattern

Use this method for browser work that depends on what is visibly on screen.

```text
screenshot -> locate UI -> guarded browser action -> screenshot recheck -> result verification
```

The method is intentionally simple: make one visible observation, perform one
small action, observe again, and verify before continuing.

## Mature Defaults

Borrow the proven computer-use pattern instead of improvising coordinates:

- For official AI website testing, read `references/official-site-human-coordinate-rule-20260703.md` first. Use visible public UI, fresh screenshots, coordinate/region actions, and one-step verification. Do not default to DOM/CDP/Playwright/browser-control/debugging routes for official sites.
- Limit recognition to the target window or page region; avoid full-screen blind
  searches when a smaller region is enough.
- Match small stable controls, icons, text labels, and nearby context. Never
  trust stale coordinates by themselves.
- Prefer clipboard paste for long text and clipboard sentinels for copy checks.
- Treat ChatGPT send/copy as one test lane, not the whole method. Also test
  ordinary pages, forms, modals, long pages, downloads, copy buttons, and hard
  stops.
- Pass only after a screenshot or direct verifier proves the intended result.

## Safety Gate

Before any action:

- Confirm the task scope, target browser/page, and allowed input method.
- Use browser/accessibility/DOM tools when they are reliable and available.
- Use real Windows mouse or keyboard input only when the user explicitly allows
  real desktop input for this task.
- Stop for login, captcha, payment, account/security prompts, privacy-sensitive
  forms, destructive actions, unclear controls, or any high-impact account
  operation.
- Never click voice, microphone, sound-wave, stop, end, close-account, delete,
  payment, or permission-escalation controls unless the user specifically asks
  for that exact action and the target is unambiguous.

## Workflow

1. Capture the current browser state with a screenshot or browser snapshot.
2. Identify the intended UI target from visible evidence: icon shape, button
   template, text label, location, state, and nearby context.
3. Check ambiguity. If two possible targets match, stop and ask or gather a
   better screenshot.
4. Prepare input safely. Prefer clipboard paste for long text. Keep actions
   scoped to the active browser page.
5. Execute exactly one small action: click, paste, press key, scroll, or wait.
6. Re-screenshot immediately after the action.
7. Verify the expected state change from pixels, accessibility text, copied
   output, URL, page state, or a sentinel value.
8. Continue only if verification passes. If it fails, retry only the smallest
   safe recovery step or stop with the observed evidence.

## ChatGPT Send/Copy Variant

For ChatGPT web bridge work, prefer this guarded loop when real desktop input is
allowed:

```text
screenshot -> find input/send arrow -> paste by clipboard -> wait for send arrow
-> click send -> wait for completion -> click copy -> verify clipboard sentinel
```

Use saved button images or pixel evidence when available. Require the send-arrow
state before sending. Do not click microphone, voice-mode, sound-wave, stop, or
end controls. If the send arrow is not visible after paste, retry focus/paste
once or stop.

## Fallbacks

If screenshot operation is not allowed or does not pass preflight, switch to the
safest available fallback in this order:

1. Browser/accessibility snapshot or in-app browser controls.
2. Clipboard plus UI Automation without real pointer movement.
3. Chrome extension or browser plugin control.
4. DOM/CDP/Playwright control.
5. Manual user handoff.

## Full Method

For the detailed reusable procedure, read
`references/method.md` in this skill.

## Self Check

After copying or editing this skill, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-screenshot-browser-skill.ps1
```
