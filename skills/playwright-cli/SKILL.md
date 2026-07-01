---
name: playwright-cli
description: Use when this Windows Codex studio needs Playwright CLI browser checks for local pages, screenshots, traces, console errors, responsive smoke tests, or reproducible UI verification. Prefer this for local apps and generated HTML when Browser plugin visibility is insufficient or terminal-driven evidence is needed.
---

# Playwright CLI Windows Studio

Use this skill for terminal-driven browser verification on Windows.

## When To Use

- Verify local frontend changes.
- Capture screenshots or traces.
- Check console errors.
- Test responsive desktop/mobile layouts.
- Reproduce a browser flow with deterministic evidence.

## Windows Studio Rules

- Use existing Playwright installation or bundled workspace dependencies when available.
- Do not install browsers or packages unless the task requires it and source is trusted.
- Use localhost/file targets only unless the user requested a remote site.
- Do not use Playwright to operate ChatGPT web planning; use the approved screenshot bridge for that route.

## Workflow

1. Identify target URL or file path.
2. Start a dev server if the app requires one; otherwise use the direct file path.
3. Run a narrow Playwright check: page load, screenshot, console capture, or one user flow.
4. Test mobile only when layout/responsiveness matters.
5. Save or report evidence: exit code, screenshot path, key console errors, and observed state.

## Verification

- PASS: target loads, expected UI is visible, and console/screenshot evidence is captured.
- FAIL: server unavailable, blank page, major console error, or layout overlap.

