# ChatGPT Screenshot Bridge State Machine

This reference defines the simple, repeatable route for using an already logged
in ChatGPT browser session. Keep the approach visual and grounded:

```text
act -> screenshot -> classify state -> continue or jump back
```

Do not rely on brittle browser internals when a screenshot and one guarded
action is enough.

## One-Step-One-Screenshot Positioning Rule

Use the proven simple route for desktop UI coordinates:

- First take the largest relevant screenshot: the full desktop when the browser
  location is unknown, or the full ChatGPT/Chrome window when the page is
  already focused. Do not start from a guessed small crop.
- Use that broad screenshot to classify the visible state and find the
  approximate target area.
- Then crop a small screenshot around that area and locate the exact icon or
  toolbar row inside the small image.
- Treat icon pixels as a guide, not always as the clickable center. When a
  visual icon is only part of a larger clickable button, click the center of the
  button-sized candidate or make a very small nearby retry after a fresh
  screenshot.
- Perform one action at a time, then immediately screenshot again. Do not run a
  fast blind click loop.
- If the click misses but the state is still stable, retry only near the
  previous small-image target and log the screenshot. Once one coordinate works,
  preserve that rule in this skill so future runs do not re-explore it.
- If state is lost or the page jumps, return to the nearest stable state
  (`READY`, `PROMPT_PASTED`, or `ANSWER_READY`) instead of switching to another
  browser-control method.

## State Names

- `NO_BROWSER`: Chrome is not open.
- `NO_CHATGPT_TAB`: Chrome is open, but no visible ChatGPT page is found.
- `WRONG_PAGE`: The visible page is not a usable ChatGPT chat page. This also
  covers task pages that navigated away, model/account pages, blank tabs,
  error pages, or a page that jumped during a workflow.
- `LOGIN_REQUIRED`: ChatGPT asks the user to log in.
- `SECURITY_REQUIRED`: captcha, account/security prompt, payment prompt,
  privacy-sensitive form, permission prompt, or high-impact account action.
- `LIMIT_OR_EXPIRED_CHAT`: conversation time limit, stale task page, or page says
  to start a new chat.
- `READY`: ChatGPT page is visible and the composer input/action area is
  visible. An empty composer may show a voice button instead of a send arrow.
- `PROMPT_PASTED`: prompt is visible enough that the send arrow is still the
  correct action.
- `GENERATING`: response is being produced.
- `ANSWER_READY`: response area is stable and a Copy button can be found.
- `COPIED`: clipboard changed from sentinel and contains expected answer text.
- `FAILED_RETRYABLE`: transient failure; jump back to the nearest stable state.
- `FAILED_BLOCKED`: user intervention is required.

## Recovery Rules

- From `NO_BROWSER`: open the pinned/default Chrome shortcut or start the
  default browser with `https://chatgpt.com/`. Then screenshot and classify.
- From `NO_CHATGPT_TAB`: navigate the existing logged-in browser profile to
  `https://chatgpt.com/`. Do not start a new browser profile.
- From `WRONG_PAGE`: navigate the same browser/profile to `https://chatgpt.com/`,
  wait, screenshot, and reclassify.
- From `LOGIN_REQUIRED`: stop and ask the user to finish login in the visible
  browser. After the user confirms, resume from screenshot classification.
- From `SECURITY_REQUIRED`: stop. Do not solve captcha, accept security prompts,
  change account settings, pay, or bypass permission gates.
- From `LIMIT_OR_EXPIRED_CHAT`: start a new chat on the same logged-in page when
  the UI exposes a normal new-chat route; otherwise navigate to
  `https://chatgpt.com/` and reclassify.
- From `READY`: paste by clipboard, screenshot, and require the send arrow
  before clicking. Never click voice, microphone, sound-wave, stop, or end
  controls.
- From `PROMPT_PASTED`: click send only if the send-arrow classifier confirms
  the target. If not, jump back to `READY` and paste again.
- From `GENERATING`: wait for visual stability, then screenshot. If the page
  jumps, classify as `WRONG_PAGE` or `LIMIT_OR_EXPIRED_CHAT`.
- From `ANSWER_READY`: write a sentinel to the clipboard, click the bottommost
  plausible assistant toolbar row for the latest assistant message from a full
  window screenshot, crop a small screenshot around that toolbar, click the
  first icon in that small toolbar crop, and verify clipboard changed.
- From copy failure: retry copy after hover/scroll once or twice, then use the
  keyboard-copy fallback only when explicitly enabled. Otherwise report the
  copied-state failure with screenshots.

## Readiness Test

Use a no-send preflight that requires the composer:

```powershell
python "$env:USERPROFILE\.codex\skills\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt "preflight only" `
  --window-title-pattern "ChatGPT|chatgpt.com" `
  --allow-browser-window-fallback `
  --preflight-only `
  --preflight-require-composer
```

Success means the visible logged-in ChatGPT page has a usable composer region.
It does not send a prompt. The send arrow is required only after a prompt has
been pasted.

## Image Upload Boundary

The current bridge is text-only. ChatGPT web supports image/file upload, but an
automated image upload mode must be separate and explicit because it transmits a
local file to a third-party service.

Before uploading an image, require the exact local path and destination intent
from the user. The image state machine should be:

```text
READY -> attach/upload control visible -> select exact file -> screenshot
confirm file chip/thumbnail -> paste text prompt -> send -> copy answer
```

Stop for file picker confusion, wrong selected file, upload errors, login,
captcha, account/security, privacy, or payment prompts.
