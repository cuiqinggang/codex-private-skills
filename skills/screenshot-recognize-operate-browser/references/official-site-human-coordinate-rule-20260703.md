# Official Site Human Coordinate Rule

Created: 2026-07-03
Source: user correction during UltraFusion 6.1B official-site test.

## Value Judgment

This is high-value reusable material because it prevents repeated failures in official AI website testing. The stable route is the simple route: use the visible page like a careful ordinary user, with coordinates derived from fresh screenshots and one verification step after each action.

## Trigger Phrases

Use this rule when the task mentions:

- official site test
- GPT / ChatGPT official site
- DeepSeek official site
- Qwen / Tongyi / 千问 official site
- coordinate test
- one screenshot per step
- like a human
- do not control the browser
- virtual mouse and keyboard
- avoid debugging / DOM / Playwright / browser control

## Core Rule

For official AI website testing, prefer:

```text
fresh screenshot -> visible target recognition -> coordinate/region action -> fresh screenshot -> visual verification
```

Do not default to methods that ordinary users do not use:

- DOM inspection
- CDP / DevTools
- Playwright page control
- browser extension control
- hidden webpage APIs
- debugging hooks
- anti-detection, stealth, or restriction-bypass methods

The purpose is reliability and respect for the website's public interface, not evasion.

## Safety Boundary

Allowed:

- Low-frequency operation through visible public UI.
- Screenshot-based location and verification.
- Clipboard or virtual input only when it does not interfere with the user and is allowed for the task.
- Honest reporting of login, captcha, rate limit, unavailable model, or blocked state.

Not allowed:

- Bypassing website limits.
- Hiding automation or making automation undetectable.
- Solving restrictions through stealth tactics.
- Using real mouse, real keyboard, foreground focus, or global clipboard while the user is actively operating the machine unless the user explicitly gives a time window for that action.

## Current Chrome Caveat

Existing user Chrome tabs are part of the active Windows desktop. Coordinate clicks and keyboard input into those tabs usually require foreground focus and can interfere with the user.

If the user is also operating the computer:

1. Do not send real desktop input.
2. Do not seize focus.
3. Use passive screenshots and planning only, or ask for an explicit time window.
4. If isolated testing is acceptable, use a separate virtual/isolated browser, knowing it may not share the user's logged-in sessions.

## UltraFusion 6.1B Test Application

For the UltraFusion 6.1B official-site test:

```text
Test A: GPT only. No DeepSeek, no Qwen, no V15, no A/B/C/D.
Test B: GPT initial frame -> DeepSeek deep/adversarial review -> Qwen third perspective -> GPT final fusion.
```

If V15_FULL is not found or not injected, mark:

```text
NON_V15_SKELETON_TEST
```

Never mark:

```text
V15_FULL_CHAIN_PASS
```

unless V15_FULL was actually found, injected, and verified.

## Acceptance Checklist

- Each action has a fresh screenshot before or after it.
- Coordinates are derived from the current screenshot, not stale memory.
- The report names the current official route.
- The report names deprecated routes separately.
- Login/captcha/rate-limit/failure states are reported honestly.
- No restriction-bypass or stealth claim is made.
