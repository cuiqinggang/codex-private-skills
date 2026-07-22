# Ordinary Coordinate Text State Machine - 2026-07-04

中文技能名：**ChatGPT官网普通坐标截图发送技能**

中文别名：`ChatGPT普通人发送法`、`ChatGPT坐标截图法`、`官网文本发送状态机`、`CtrlV Enter发送法`、`普通坐标截图法`。

## Status

`PASS_WITH_BOUNDED_TEXT`: the ordinary visible coordinate + keyboard method is
validated for ChatGPT official-site text transport in the current fullscreen
state.

Validated state:

- Chrome fullscreen on `2560 x 1440`
- ChatGPT official site
- Sidebar open
- Custom black toolbar visible
- Browser zoom `100%`
- Text-only composer use

## Observed Success Rates

| Test set | Result | Observed success |
|---|---:|---:|
| Failed exploratory simple send using wrong send y-coordinate | 0/10 full PASS | 0% |
| Calibrated simple text using clear + paste + Enter | 10/10 PASS | 100% |
| Unbounded long complex answer with 45s wait | 0/10 full completion PASS | 0% full completion |
| Bounded complex short answer using clear + paste + Enter | R02-R11 = 10/10 PASS | 100% |

Evidence roots:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

## State Machine

Use this as the default for ChatGPT official-site text-only work:

```text
S0 Page visible
S1 If generation is running, click visible stop once and wait
S2 Click New Chat
S3 Screenshot-confirm clean composer before counting the run
S4 Click composer at x=1175 y=751
S5 Ctrl+A, Backspace
S6 Paste exactly one prompt with Ctrl+V
S7 Screenshot-confirm the intended prompt is visible
S8 Press Enter
S9 Wait for answer completion
S10 Screenshot-confirm expected answer or marker
```

## Coordinates

```text
New Chat row: x=60 y=203
sidebar_open composer input: x=1175 y=751
single-line send arrow if needed: about x=1768 y=751
```

For text-only work, Enter is preferred over clicking the small send arrow.

## Failure Lessons

1. The input box is large and tolerates coordinate drift; the send arrow does
   not. A click at `x=1767 y=730` left the prompt in the composer.
2. A scaled preview must not be used as the coordinate source.
3. After stopping a long generation, the next action must not be counted until
   a clean composer is screenshot-confirmed.
4. Long complex answers are not transport tests unless the workflow waits for
   completion and proves a final marker.
5. Bounded complex prompts are the right quick reliability test: they are still
   semantically complex but finish fast enough for transport verification.

## Abnormal-State Logic

Do not over-label ordinary recoverable UI states as "abnormal failures".

Repairable states are part of the ordinary method:

```text
page not open -> open chatgpt.com
old chat visible -> New Chat
dirty composer -> Ctrl+A, Backspace
generation running -> click visible stop, then require clean-composer screenshot
focus stale -> refresh once, then clean-composer screenshot
wrong/old tab -> select or open ChatGPT tab
send arrow drift -> use Enter after prompt screenshot gate
```

These branches are simple enough for an ordinary user, so Codex must treat them
as state-normalization, not as excuses to switch to complex methods.

## Rule

Do not use DOM, CDP, browser takeover, hidden debug APIs, `WM_CHAR`, `WM_PASTE`,
or window-message send paths for this workflow. If this ordinary route fails,
repair the visible state with screenshots and normal user actions first. Only
after an evidence-backed failure should the method be marked failed and
analyzed.
