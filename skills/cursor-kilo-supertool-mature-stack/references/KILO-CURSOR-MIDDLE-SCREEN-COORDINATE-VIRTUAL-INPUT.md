# Kilo Cursor Middle Screen Coordinate And Virtual Input Rule

Date: 2026-07-02
Status: active rule, evidence baseline captured

## Why This Exists

The user runs a multi-monitor desktop and may be using the real mouse and keyboard while Codex is working. Future Kilo/Cursor repair must not steal the user's physical pointer or keyboard focus.

Use this rule for Cursor + Kilo model, paste, localization, settings, or new-agent repair tasks.

## Hard Boundary

- Do not use real Windows mouse or keyboard simulation for this workflow.
- Do not use PowerShell `SendKeys`, Win32 `SendInput`, `mouse_event`, or foreground click helpers unless the user explicitly allows real input for that exact step.
- Prefer read-only screenshots, config repair, Cursor/Kilo state database repair, and passive window enumeration.
- If programmatic UI operation is required, prefer a UI Automation pattern such as `InvokePattern` or `ValuePattern` when the target control exposes it. This is still state-changing and must be screenshot-verified, but it is not physical pointer movement.
- Computer Use is allowed for `list_apps` and `list_windows`.
- Computer Use `get_window_state`, `click`, `type_text`, `press_key`, `scroll`, and `activate_window` are disabled for this workflow unless re-verified in the same session and explicitly accepted, because they can request approval, activate windows, or inject input.
- If an operation would require a visible click or typed text, stop and ask or hand off a precise coordinate to the user.

## Current Target Window

Observed on 2026-07-02:

```text
Window title: Cursor Agents
Process: Cursor.exe
Win32 handle / Computer Use window id: 3934752
Win32 rectangle: X=-8, Y=-8, W=2576, H=1416
Window-handle screenshot size: 2048x1120
```

Important trap: active-window screenshot may capture Chrome even while Cursor is visually present. Use a specific window handle or title (`Cursor Agents`) for evidence.

## Evidence Baseline

Workspace evidence directory:

```text
${REDACTED_SECRET}
```

Captured files:

```text
01-full-virtual-desktop-before.png
02-middle-screen-before.png
03-cursor-foreground-full-virtual.png
```

Additional temp evidence captured during the run:

```text
${REDACTED_SECRET}
```

This screenshot proved Kilo/Cursor localization was not fully accepted yet: visible English remained in `File`, `Edit`, `View`, `Help`, `New Agent`, `Search`, `Automations`, `Customize`, `Repositories`, `No agents yet`, `Upgrade to a Pro account`, `Plan, Build`, `Composer 2.5 Fast`, `Plan New Idea`, and `Multitask`.

## Coordinate Basis

Use window-handle screenshot coordinates as the primary coordinate system:

```text
origin: top-left of the captured Cursor Agents window
size: 2048x1120
```

Use Win32 virtual desktop coordinates only as secondary evidence. The virtual desktop may use negative X/Y and DPI scaling, so absolute desktop coordinates are less stable than window-relative coordinates.

Approximate conversion from this run:

```text
virtual_x ~= win32_left + window_x * 1.2578
virtual_y ~= win32_top  + window_y * 1.2643
```

Recompute after any monitor layout, DPI, maximize/fullscreen, or window title change.

## Current Window-Relative Coordinate Map

All points are approximate centers from `codex-shot-2026-07-02_18-39-21.png` and must be revalidated by a fresh screenshot before use.

| Function | Window-relative point | Evidence label |
|---|---:|---|
| Top menu File | `(43, 21)` | `File` |
| Top menu Edit | `(78, 21)` | `Edit` |
| Top menu View | `(115, 21)` | `View` |
| Top menu Help | `(151, 21)` | `Help` |
| Left rail first icon | `(25, 51)` | panel icon |
| New Agent nav item | `(71, 80)` | `New Agent` |
| Search nav item | `(63, 109)` | `Search` |
| Automations nav item | `(82, 139)` | `Automations` |
| Customize nav item | `(78, 168)` | `Customize` |
| Repositories header | `(62, 208)` | `Repositories` |
| Repository filter button | `(160, 208)` | filter icon |
| Add/open repository icon | `(189, 208)` | folder-plus icon |
| `kilo-validation` repo row | `(86, 237)` | folder row |
| Selected `New Agent` row | `(106, 266)` | row under repo |
| Empty agents area | `(93, 334)` | `No agents yet` |
| Main project selector | `(900, 528)` | `kilo-validation / Local` |
| Main prompt input box | region `(846, 546, 560, 92)` | `Plan, Build, / for skills` |
| Add attachment button | `(865, 618)` | plus button |
| Model selector | `(942, 618)` | `Composer 2.5 Fast` |
| Voice/send-side button | `(1386, 618)` | black circular button |
| Plan New Idea chip | `(912, 670)` | `Plan New Idea` |
| Multitask chip | `(1018, 670)` | `Multitask` |
| Bottom settings gear | `(189, 1090)` | gear |
| Bottom user/account area | `(90, 1090)` | email / Free Plan |

## Coordinate Use Rule

Before any future coordinate use:

1. Capture the `Cursor Agents` window by handle/title, not active window.
2. Confirm screenshot size and title match this rule.
3. Identify the target visually from text/icon/context.
4. Use the window-relative coordinate only after the target is unique.
5. Capture a second screenshot after any user or automated action.
6. Record the before/after screenshot path and whether the coordinate still matched.

Coordinates are execution addresses, not proof. Screenshot evidence is proof.

## Model State Findings From 2026-07-02

Config/state checks found:

```text
${REDACTED_SECRET}
kilo-code.new.model.providerID = openrouter
kilo-code.new.model.modelID = deepseek/deepseek-v4-pro
kilo-code.new.language = zh

${REDACTED_SECRET}
model = openrouter/deepseek/deepseek-v4-pro
small_model = openrouter/deepseek/deepseek-v4-flash
subagent_model = openrouter/deepseek/deepseek-v4-pro
snapshot = false

${REDACTED_SECRET}
kilocode.kilo-code recentModels = [{"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}]
HAS_DEEPSEEK_V3_2 = false
HAS_KILO_PROVIDER = false
```

Interpretation: if the UI still shows DeepSeek V3.2 while these stored states are clean, treat it as runtime/webview/session/localization state until proven otherwise. Do not repeatedly rewrite `state.vscdb`.

## Paste Repair State From 2026-07-02

The terminal paste repair script rewrote:

```text
${REDACTED_SECRET}
```

Expected entries:

```json
[
  {
    "key": "ctrl+v",
    "command": "workbench.action.terminal.paste",
    "when": "terminalFocus && terminalProcessSupported"
  },
  {
    "key": "shift+insert",
    "command": "workbench.action.terminal.paste",
    "when": "terminalFocus && terminalProcessSupported"
  }
]
```

This fixes bottom integrated terminal paste routing only. It does not prove Kilo webview long-text paste.

## Localization Acceptance

Current screenshot state on 2026-07-02 is not a full localization PASS.

Required future acceptance:

- Cursor top menu is Chinese or documented as product residue after reload.
- Kilo/Cursor left navigation is Chinese or documented as product residue after reload.
- Kilo new-agent page and settings are Chinese where the extension supports localization.
- Model route remains OpenRouter / DeepSeek V4 Pro.
- At least two screenshot rounds prove before/after state.

Final status must be one of:

```text
ACTUAL_OPEN_VERIFY_PASS
PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE
FAIL_NEEDS_FURTHER_FIX
```

Do not claim localization PASS from config files alone.

## Virtual Input Research Notes

Checked on 2026-07-02:

- Microsoft UI Automation is the preferred Windows framework for programmatic UI access when controls expose automation patterns. It can access and manipulate UI elements without ordinary pointer movement.
- `InvokePattern.Invoke()` is for a single unambiguous control action; use it only when the target element is unique and enabled.
- `ValuePattern` is for controls with an intrinsic string value; use it only when the editable control exposes that pattern.
- `SendInput` inserts keyboard/mouse events into the input stream. Therefore it is classified as real desktop input for this workflow and is disabled by default.

Sources:

```text
https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32
https://learn.microsoft.com/en-us/dotnet/api/system.windows.automation.invokepattern.invoke
https://learn.microsoft.com/en-us/dotnet/api/system.windows.automation.valuepattern
https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
```
