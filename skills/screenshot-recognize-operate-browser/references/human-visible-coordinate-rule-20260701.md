# Human Visible Coordinate Rule

Created: 2026-07-01
Source: user correction in Codex thread about visible buttons, screenshot labels, and coordinate positioning.

## Value Judgment

This is high-value reusable material because it reduces repeated UI-operation failures, improves complex browser and desktop task quality, and turns a user-approved operating style into a reusable rule.

## Trigger Phrases

Use this rule when the task mentions:

- screenshot
- visible button
- button label
- icon or marker
- coordinate
- click position
- browser operation
- desktop UI operation
- like a human
- use your eyes
- visual positioning

## Core Rule

If a human can see a control on screen and operate it by looking, Codex should first understand the task as a visual operation problem.

The default route is:

```text
look -> locate -> confirm unique target -> perform one small human-like action -> look again -> verify
```

Do not prematurely turn the task into scripts, DOM selectors, hidden APIs, or brittle automation when a direct visible UI path is available and permitted.

## Coordinate Rule

Coordinates are easy to obtain, but they are not the real proof.

Use coordinates as a temporary execution address after visual recognition:

1. Take or inspect a screenshot.
2. Locate the target by visible evidence: text, icon, marker, state, surrounding layout, and relative position.
3. Convert the recognized target into a click point or region.
4. Execute one small action.
5. Re-check the screen and verify the intended change.

Never trust old coordinates by themselves. The current screenshot is the authority.

## Human-Operation Defaults

- Act like a careful human user: look at the page, find the intended control, click or type once, then check what changed.
- Prefer visible controls and labels over hidden implementation details.
- Use coordinate or region targeting only after visual confirmation.
- If the target is ambiguous, zoom in, crop the region, re-screenshot, or ask.
- If the action is dangerous, such as payment, deletion, permission changes, account security, publishing, or sending private data, stop and confirm.
- For long text, paste from clipboard when allowed, then visually confirm the text appeared before submitting.

## Failure Modes To Avoid

- Treating visible UI work as a code problem too early.
- Using stale coordinates without checking the latest screen.
- Clicking multiple things in a row without a screenshot between them.
- Saying success after an action attempt instead of after visual verification.
- Clicking near microphone, voice, stop, delete, payment, or security controls without explicit confirmation.

## Acceptance Checklist

Before reporting success for a visible UI operation:

- The target page or app was identified.
- The target control was visible or made visible.
- The target was uniquely recognized from screen evidence.
- One small action was performed.
- A post-action screenshot or equivalent visual check confirmed the result.
- Any dangerous or ambiguous action was stopped for confirmation.

## Next-Run Reuse Instruction

When a future task involves visible UI, screenshots, buttons, labels, markers, or coordinates, read this file together with `method.md` before acting.
