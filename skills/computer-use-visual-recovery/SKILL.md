---
name: computer-use-visual-recovery
description: Restore and verify Codex Computer Use visual operation ability on Windows. Use when tasks mention computer use, Any App, visible buttons, screenshots, coordinates, click positions, human-like UI operation, visual browser/desktop control, screenshot-guided clicks, or when these abilities need repair, recovery, reorganization, regression testing, or a complete capability rebuild after Codex/Desktop/plugin changes.
---

# Computer Use Visual Recovery

Use this skill when the problem is not only "can a script run?" but "can Codex look at a real interface, locate visible controls, act like a careful human, and verify the result?"

Core principle:

```text
look -> locate -> confirm unique target -> one small action -> look again -> verify
```

## Start Here

1. Read `references/recovery-map.md` for the full recovery route.
2. Read `references/human-visible-operation.md` when the task involves visible buttons, labels, icons, markers, screenshots, or coordinates.
3. Read `references/acceptance-matrix.md` before claiming the capability is restored.
4. Run `scripts/check-visual-recovery.ps1` to confirm the local skill links, backups, and related Computer Use assets exist.

## Recovery Order

Use the smallest route that restores the missing capability:

1. **Rule recovery**: restore the human-visible operation rule and trigger phrases.
2. **Screenshot recovery**: confirm screenshots work for active windows and target regions.
3. **Recognition recovery**: identify visible text, icons, nearby context, and enabled/disabled state from the current screenshot.
4. **Coordinate recovery**: convert the recognized target into a temporary point or region only after recognition.
5. **Action recovery**: execute one small click, paste, keypress, scroll, or wait.
6. **Verification recovery**: capture a second screenshot or state signal and verify the expected change.
7. **Computer Use repair**: if the official Computer Use tool path is broken, switch to `codex-computer-use` for plugin/cache/native-host repair, then return here for visual capability acceptance.

## Operating Rules

- Treat the latest screenshot as the authority. Never trust stale coordinates alone.
- Prefer visible UI evidence before DOM selectors, hidden APIs, or scripts when the user expects human-like operation.
- Use coordinates as an execution address, not as proof.
- Perform one action between observations.
- Do not click payment, delete, publish, permission, login, security, microphone, voice, stop, or ambiguous controls without explicit confirmation.
- For long text, prepare it outside the UI, paste it when allowed, and visually confirm it appeared before submitting.
- Report success only after post-action verification passes.

## Related Skills

- `codex-computer-use`: repair Computer Use, Any App, browser, Chrome native host, plugin cache, and Windows control plumbing.
- `screenshot-recognize-operate-browser`: operate visible browser pages with screenshot-based recognition.
- `screenshot-browser-100-percent-route`: gated screenshot browser operation route with screenshot-after-each-step discipline.
- `screenshot`: OS-level screenshot capture fallback.
- `ui-setting-actual-open-self-verify-loop`: actual-open verification for UI settings and app panels.

## Failure Review Entry

When visual operation fails, preserve only non-secret evidence:

```text
TASK:
TARGET APP/PAGE:
EXPECTED CONTROL:
SCREENSHOT STATE:
RECOGNITION RESULT:
ACTION ATTEMPTED:
POST-ACTION STATE:
FAILURE MODE:
NEXT RECOVERY STEP:
```

Put durable lessons back into `references/human-visible-operation.md` or `references/acceptance-matrix.md` if they generalize.
