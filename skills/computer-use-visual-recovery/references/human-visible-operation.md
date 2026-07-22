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
# 普通人坐标截图法 / Ordinary Coordinate Screenshot Method

Use this rule for any website, browser page, or desktop software where a normal
user can complete the task through the visible interface.

## Principle

If ordinary users can operate the UI reliably, Codex should first solve it with
the same visible logic:

```text
screenshot -> recognize state -> normalize state -> coordinate/key action
-> screenshot -> verify -> repeat until mature
```

The method is not "one coordinate forever". The method is:

```text
stable state + stable coordinate + screenshot gate + repair branch
```

After enough tests, each state becomes a known branch. If a coordinate changes,
the screenshot reveals the changed state; the workflow normalizes or uses that
state's coordinates.

## Do Not Escape Too Early

Do not switch to complex methods just because:

- the first click missed
- an old page was open
- focus was stale
- the input contained old text
- a page needed refresh
- the window/tab was wrong
- an answer was still generating

These are ordinary repair branches, not true blockers.

## Normalization Branches

```text
not open -> open the app/page
wrong tab/window -> switch/open the correct one
old conversation/document/state -> start a new one
dirty field -> select all and clear
focus missing -> click the target field again
small send/confirm button drift -> use keyboard equivalent if normal users do
long-running operation -> wait for visible completion or stop and restart clean
layout changed -> screenshot and bind the new state's coordinate
```

## Failure Definition

The ordinary method fails only when normal repair branches have been attempted
and screenshot evidence still shows no path forward, or when the UI presents a
true blocker such as login, captcha, account/security prompt, network outage,
service outage, or permission/payment confirmation requiring user approval.

## Maturity Target

For a tested stable UI state under normal account/network/app conditions, the
target is engineering-level 100% success. If the observed success rate is not
100%, keep testing and converting failures into explicit state branches before
declaring the workflow mature.
