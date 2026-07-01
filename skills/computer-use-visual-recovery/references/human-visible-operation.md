# Human Visible Operation

Use this when a control is visible on screen and a human could operate it by looking.

## Default Interpretation

Visible UI work is first a visual operation task, not a code problem.

The agent should think:

1. What would a careful human look at?
2. Which visible label, icon, marker, state, or surrounding context proves the target?
3. Is the target unique?
4. Where is the temporary click point or input region?
5. What single action should happen next?
6. What visible change proves success?

## Coordinate Discipline

Coordinates are easy to obtain in a screenshot workflow, but they are not durable truth.

- Use coordinates only after visual recognition.
- Prefer a target region over a single pixel when a button is large enough.
- Recalculate coordinates after scrolling, resizing, focus changes, page motion, modal changes, or new screenshots.
- If the click misses, do not keep clicking the same point. Re-screenshot, re-locate, then act.

## Button And Marker Recognition

Use multiple visual clues:

- Button text or OCR text.
- Icon shape.
- Enabled or disabled state.
- Hover/focus/selected state when available.
- Nearby explanatory text.
- Position relative to form fields, message areas, modals, toolbars, or page edges.
- Dangerous adjacent controls that must be avoided.

## Human-Like Rhythm

Use this rhythm for ordinary visible UI tasks:

```text
screenshot
identify target
name the evidence
act once
screenshot again
verify result
continue or stop
```

Do not batch focus, paste, submit, copy, and close into one opaque move unless a mature tested loop already performs internal checks.

## Hard Stops

Stop and ask before:

- Payment, purchase, subscription, billing, or financial transfer.
- Delete, erase, archive, reset, publish, invite, permission changes, or public posting.
- Login, password, passkey, two-factor, OAuth consent, captcha, or account recovery.
- Security prompts, privacy-sensitive forms, government/legal/medical forms, or secrets.
- Ambiguous controls or repeated similar buttons where the target cannot be uniquely recognized.

## Success Standard

Do not report success because the action was attempted.

Report success only when a screenshot, page state, clipboard sentinel, file existence, URL/title change, or equivalent verifier proves the intended result.
