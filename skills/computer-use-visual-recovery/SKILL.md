---
name: computer-use-visual-recovery
description: Recover and regression-test Codex Computer Use visual operation on Windows after missing capability, broken coordinates, failed screenshot-guided actions, Desktop or plugin changes, or a capability rebuild. Do not use for ordinary healthy browser or desktop clicking; route normal operation to the canonical Computer Use skill.
---

# Computer Use Visual Recovery

Use this skill when the problem is not only "can a script run?" but "can Codex look at a real interface, locate visible controls, act like a careful human, and verify the result?"

Core principle:

```text
look -> locate -> confirm unique target -> one small action -> look again -> verify
```

## Relationship To Official Computer Use

Official Windows Computer Use is the preferred runtime engine when it is
available. This skill is the human-visible operation and acceptance layer on top
of that engine.

Use the stack this way:

1. Let official Computer Use provide desktop access, window activation,
   screenshots, typing, clicking, scrolling, dragging, and state capture.
2. Use this skill's ordinary coordinate screenshot method for real visible UI
   work: observe, recognize the target, act once, observe again, and verify.
3. If the official engine, plugin cache, Chrome native host, or native pipe path
   is broken, switch to `codex-computer-use` for repair, then return here for
   visible-operation acceptance.

See `references/computer-use-layered-routing-20260704.md` for the durable
routing table.

## Ordinary Coordinate Screenshot Method

中文名：**普通人坐标截图法**

This is the default for websites, browser pages, and desktop software when a
normal user can operate the visible UI. Codex must not prematurely switch to
DOM, CDP, debug APIs, hidden automation, window messages, or app internals just
because the first attempt misses.

Core logic:

```text
normal users can do it
-> the visible UI has stable states
-> screenshots expose those states
-> coordinates are stable inside each state
-> state changes are handled by normalization branches
-> repeated testing turns the workflow into a deterministic state machine
```

Treat "abnormal" visible UI states as state-normalization work, not as excuses
to abandon the ordinary method:

```text
app/page not open -> open it
wrong page/tab/window -> switch or open the correct one
old content visible -> start a new item/session
dirty input -> Ctrl+A / clear
focus stale -> click the visible input again or refresh once
layout changed -> screenshot, identify the current state, use that state's coordinates
small button drift -> use the normal keyboard equivalent when available
long operation still running -> wait, stop, or use the visible completion signal
```

Only treat the method as failed after ordinary repair branches have screenshot
evidence of failure. In normal network/account/app conditions, mature ordinary
state machines should target engineering-level 100% success for the tested
states.

## Start Here

1. Read `references/recovery-map.md` for the full recovery route.
2. Read `references/human-visible-operation.md` when the task involves visible buttons, labels, icons, markers, screenshots, or coordinates.
3. Read `references/acceptance-matrix.md` before claiming the capability is restored.
4. Run `scripts/check-visual-recovery.ps1` to confirm the local skill links, backups, and related Computer Use assets exist.
5. For Computer Use tasks, read `references/computer-use-layered-routing-20260704.md` before deciding whether the problem is runtime repair or visible UI operation.

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

## Coordinate Data Pages

Keep site-specific differences as lightweight coordinate data, not separate
large state machines:

- `references/ordinary-coordinate-progress-pack-20260704.md`: 普通人坐标截图法进度包。
- `references/qwen-coordinate-data-page.md`: 千问 / Qwen 坐标数据页。
- `references/deepseek-coordinate-data-page.md`: DeepSeek 坐标数据页。
- `references/web-ai-basic-flow-qwen-deepseek-20260705.md`: Qwen / DeepSeek 网页连接与答案获取 40/40 PASS 边界、100% 主张范围和轻量连接预检。

Each page records only: page state, action, coordinate, keyboard equivalent,
success count, failure repair, and evidence path.

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
