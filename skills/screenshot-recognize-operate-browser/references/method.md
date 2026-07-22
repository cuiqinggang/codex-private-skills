# 截图识别并操作浏览器法

## User-Calibrated Human Visible Rule

For tasks involving visible buttons, labels, markers, screenshots, or coordinates,
also apply `human-visible-coordinate-rule-20260701.md`.

Default interpretation: if a human can see and operate the control, treat it
first as a visual human-operation task. Use the latest screenshot to locate the
target, convert it to a temporary coordinate or region only after recognition,
perform one small action, and verify from the screen before continuing.

## Purpose

This method lets an agent operate a browser from visible screen evidence instead
of relying only on DOM selectors or brittle web internals. It is useful when the
browser page is already open, the UI must be recognized visually, a web app
changes DOM structure often, or a send/copy loop must be controlled with strong
post-action verification.

The method is not permission to blindly use the user's desktop. Real desktop
mouse or keyboard input requires explicit user permission for the current task.

## One-Line Algorithm

```text
screenshot -> locate UI -> guarded browser action -> screenshot recheck -> result verification
```

## Yesterday-Replay Defaults

Mature screenshot browser control systems converge on the same rules:

- Use real visual evidence: screenshot the page/window before and after each
  action.
- Restrict search to useful regions: target window, lower composer area, modal,
  latest message toolbar, or visible viewport section.
- Match small stable visual targets: button icons, labels, enabled/disabled
  state, nearby text, and layout context. Do not depend on stale coordinates.
- Paste prepared text through the clipboard instead of typing long prompts or
  forms character by character.
- Use explicit wait conditions: image appears, image disappears, button changes
  state, page stops moving, URL changes, file appears, or clipboard changes.
- Use a sentinel before copy actions so stale clipboard contents cannot look
  like success.
- Save concise traces only when debugging or proving reliability; avoid storing
  secrets or private content.

Treat these as defaults before inventing a new route.

## Gate G01: Scope And Permission

Purpose: establish what page may be touched and what input channel is allowed.

Execution:

1. Identify the target browser window, tab, page, or local URL.
2. Confirm whether real desktop input is allowed. If not, use browser tools,
   accessibility, clipboard/UI Automation, extension control, DOM, CDP, or
   Playwright instead.
3. Define the exact success condition: sent message, copied answer, clicked
   known button, changed page state, downloaded file, filled form, or verified
   visual layout.
4. Define stop conditions before acting.

Success criteria:

- The target page is known.
- The allowed input method is known.
- The next action is low-risk and reversible or clearly intended.

Failure criteria:

- The target page is unclear.
- The action could affect account, payment, permissions, secrets, security, or
  deletion.
- Real desktop input would be required but was not explicitly allowed.

Failure recovery:

- Stop and ask for permission, a better target description, or a safer route.

## Gate G02: First Screenshot

Purpose: observe the real visible state before acting.

Execution:

1. Capture the full target viewport or active browser window.
2. Prefer a screenshot that includes the intended control and enough surrounding
   context to disambiguate it.
3. If the page is moving, wait briefly and capture again.

Success criteria:

- The intended interaction area is visible.
- UI state can be identified from pixels, visible labels, icons, layout, or
  accessibility text.

Failure criteria:

- The screenshot is blank, stale, cropped too tightly, obscured, or on the wrong
  page.

Failure recovery:

- Re-focus the target browser using a non-destructive method, capture a wider
  screenshot, or stop.

## Gate G03: Target Recognition

Purpose: locate the exact UI target before acting.

Use all available visual evidence:

- Text label or OCR text.
- Icon shape: send arrow, copy icon, menu dots, close icon, upload icon.
- Button state: enabled, disabled, loading, selected, focused.
- Position: relative to input box, latest assistant answer, toolbar, modal, or
  page edge.
- Saved image template, when available.
- Nearby context that proves the target is the intended one.

Success criteria:

- Exactly one target matches.
- The target action is consistent with the user's request.
- Dangerous adjacent controls are identified and avoided.

Failure criteria:

- Multiple targets match.
- The target is too close to a dangerous control.
- The page shows a stop/end/voice/microphone/payment/security/login/captcha
  state instead of the expected target.

Failure recovery:

- Re-screenshot, zoom in, scroll to expose context, use accessibility text, or
  stop and ask.

## Gate G04: Pre-Action Safety Check

Purpose: prevent accidental high-impact browser actions.

Check before every click or keypress:

- Is this action exactly within the user's task scope?
- Is the target visibly enabled?
- Is the target not a destructive, payment, permission, security, account, or
  privacy-sensitive action?
- Is the pointer/keyboard route allowed for this task?
- Is there a clear verification signal after the action?

Hard stops:

- Login, captcha, two-factor, password, passkey, OAuth consent, account
  recovery, payment, subscription, purchase, delete, publish, invite users,
  change permissions, expose secrets, or anything similar.
- Ambiguous control.
- Missing send arrow where send is expected.
- Stop/end/voice/microphone controls where send/copy is expected.

## Gate G05: One Small Action

Purpose: make browser operation auditable and recoverable.

Execute one action only:

- Click one recognized control.
- Paste prepared text from clipboard into a focused input.
- Press one key or one key chord.
- Scroll one viewport.
- Wait for one known visual state.

Avoid chained actions without observation between them. Do not combine focus,
paste, send, and copy into one opaque step unless a tested script already
implements the full guarded loop with internal screenshots and checks.

Success criteria:

- The action completed without triggering an unexpected prompt.

Failure criteria:

- The page changed to an unexpected state.
- A security/account/payment/login prompt appeared.
- The target action did not appear to happen.

Failure recovery:

- Stop or perform the smallest safe recovery, such as refocusing the input or
  recapturing the screenshot. Do not escalate to broader automation without a
  new plan.

## Gate G06: Screenshot Recheck

Purpose: verify that the page state changed as expected.

Execution:

1. Capture a screenshot immediately after the action.
2. Compare against the expected state change.
3. For dynamic pages, wait for completion indicators to settle and capture
   again.

Examples:

- A message bubble appears after send.
- A send arrow changes to loading and then back to send.
- A copy button appears next to the final answer.
- A modal closes.
- A selected option is visibly active.
- A URL or page title changes as expected.

Success criteria:

- The expected state is visible and stable.

Failure criteria:

- No state change.
- Unexpected prompt or navigation.
- Loading never completes.
- The page shows a stop/end control when completion was expected.

Failure recovery:

- Wait once if loading is plausible, capture again, then stop with evidence if
  still unresolved.

## Gate G07: Result Verification

Purpose: prove the browser action produced the intended outcome.

Use the strongest available verification:

- Clipboard sentinel for copied text.
- Visible page state plus OCR/accessibility text.
- URL/title check.
- Download existence and file size.
- Browser console/network check when relevant.
- Re-read page output after copy.

For send/copy loops, use a sentinel:

1. Include a unique task id in the prompt or expected result.
2. After clicking copy, read the clipboard.
3. Treat the loop as successful only if the clipboard includes the expected
   sentinel or exact output marker.

Success criteria:

- The verification signal directly matches the intended result.

Failure criteria:

- Verification is missing, stale, or mismatched.

Failure recovery:

- Re-copy once if the copy target was clearly identified. Otherwise stop and
  report the mismatch.

## ChatGPT Web Send/Copy Flow

Use this when the target is the visible ChatGPT web page and real desktop input
is explicitly allowed:

1. Screenshot the visible ChatGPT page.
2. Locate the prompt input.
3. Put the prompt on the clipboard.
4. Focus the input and paste from clipboard.
5. Screenshot and require the send arrow to be visible.
6. Click only the send arrow.
7. Wait for completion. Do not click stop/end/voice/microphone/sound-wave.
8. Screenshot the final answer area.
9. Locate the copy button for the latest assistant answer.
10. Click copy.
11. Read clipboard and verify a unique sentinel.
12. Save a concise operation trace when testing or debugging the bridge.

Fallback order when this route is blocked:

1. Clipboard plus UI Automation without real pointer movement.
2. Chrome extension or browser plugin.
3. DOM/CDP/Playwright.
4. Manual handoff.

## General Browser Use Flow

Use this when the target is any other browser page:

1. Screenshot the current page.
2. Identify one intended control from visible evidence.
3. Check hard stops and ambiguity.
4. Execute one action.
5. Screenshot again.
6. Verify the state change.
7. Continue the loop only when verification passes.

For forms, prepare all text outside the browser first, then paste field by
field with screenshots between high-risk fields. Do not submit forms involving
accounts, payment, secrets, legal commitments, medical information, government
forms, or privacy-sensitive data unless the user explicitly instructs that exact
submission and the risk is acceptable.

## Cross-Site Test Matrix

Use this matrix to make the method general instead of ChatGPT-only. A scenario
passes only when the target is unique, one guarded action runs, the page is
observed again, and the verifier directly proves the intended result.

| Lane | Scenario | Action | Verifier | Hard stop |
| --- | --- | --- | --- | --- |
| Static page | Ordinary link or button | click one visible target | URL/title/selected state changes | ambiguous duplicate target |
| Form | Text field plus low-risk submit | paste one field, then submit | confirmation text or field state | account, payment, secrets, legal forms |
| Modal/menu | Open/close dialog or dropdown | click trigger or option | modal/menu appears or disappears | close/delete/confusing adjacent controls |
| Long page | Scroll to latest item or toolbar | scroll one viewport | intended item/copy control visible | wrong section or repeated copy icons |
| Dynamic UI | Loading result or generated answer | wait for stable visual state | button/state/message stabilizes | endless loading or stop/end state |
| Copy/download | Copy button or file download | click copy/download | clipboard sentinel changes or file exists | stale clipboard or empty file |
| ChatGPT-like | Prompt send/copy loop | paste, require send arrow, click, copy | unique sentinel in copied answer | mic/voice/stop/end/login/captcha |
| Safety page | Login, payment, permissions, secrets | no action | report blocking evidence | never bypass |

Minimum maturity bar before reusing the method elsewhere:

1. Run at least one non-ChatGPT lane.
2. Run one dynamic or long-page lane.
3. Run one hard-stop lane and confirm it stops.
4. Preserve the trace format for failures.
5. Keep any page-specific rule as a small region or template hint, not a new
   one-off workflow.

## Trace Format

When preserving evidence, log concise records:

```text
TASK_ID: <unique id>
TARGET: <browser/page/tab>
INPUT_ALLOWED: <browser-tool | ui-automation | real-desktop-input>
STEP: <G02/G03/G05/etc.>
OBSERVED: <what the screenshot showed>
ACTION: <one action taken, or STOP>
VERIFY: <pass/fail signal>
NEXT: <continue/stop/retry>
```

Do not store secrets, passwords, payment data, private messages, or unnecessary
personal data in logs.

## Completion Standard

Do not report success because an action was attempted. Report success only after
the post-action screenshot and result verification pass. If verification is
skipped, state exactly why it was skipped and what residual risk remains.
