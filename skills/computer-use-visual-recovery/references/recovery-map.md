# Recovery Map

Use this file to recover the whole visual Computer Use capability after settings drift, plugin breakage, skill loss, or unreliable UI operation.

## Layer 1: Skill And Rule Presence

Confirm these C-drive runtime skills exist:

- `C:\Users\A\.codex\skills\computer-use-visual-recovery`
- `C:\Users\A\.codex\skills\codex-computer-use`
- `C:\Users\A\.codex\skills\screenshot-recognize-operate-browser`
- `C:\Users\A\.codex\skills\screenshot-browser-100-percent-route`
- `C:\Users\A\.codex\skills\screenshot`

K-drive copies are backup/history/reference unless the user asks to restore from them.

## Layer 2: Screenshot Ability

Use the `screenshot` skill or tool-specific screenshot ability.

Pass means:

- A current screenshot is captured.
- The target app/page is visible.
- The screenshot is not blank, stale, cropped wrong, or on the wrong window.

## Layer 3: Recognition Ability

Pass means:

- The target control can be identified from visible evidence.
- Ambiguous duplicate controls are ruled out or clarified.
- Dangerous adjacent controls are noticed.

If recognition fails:

1. Capture a wider screenshot.
2. Capture a smaller region around the suspected target.
3. Scroll or zoom only when it helps expose context.
4. Ask the user if the target remains ambiguous.

## Layer 4: Coordinate Ability

Pass means:

- Coordinates or a target region are derived from the current screenshot.
- The point is inside the recognized control.
- The coordinate basis is clear: full screen, active window, browser viewport, or screenshot image.

If coordinates fail:

1. Re-screenshot.
2. Recalculate from the current image.
3. Prefer the center of the recognized button/region.
4. Avoid edges and nearby dangerous controls.

## Layer 5: Action Ability

Pass means one small action changes the target state as expected.

Allowed low-risk actions:

- Click one recognized control.
- Paste prepared text into a focused field.
- Press one safe key or key chord.
- Scroll one viewport.
- Wait for a known visual state.

If official Computer Use action APIs fail, use `codex-computer-use` to repair plugin/cache/native-host paths before declaring the capability restored.

## Layer 6: Verification Ability

Pass means the result is proven by:

- Post-action screenshot.
- URL or title change.
- Visible selected state.
- Confirmation text.
- Clipboard sentinel.
- Download/file existence and size.
- Other direct state signal.

No verification means no success claim.

## Full Restoration Pass

The capability is fully restored only when:

- Skill trigger and reference files are present.
- Screenshots work.
- A visible target is uniquely recognized.
- A coordinate/region is calculated from the current screenshot.
- One low-risk action works.
- A second observation proves the result.
- A hard-stop scenario is recognized and blocked.
