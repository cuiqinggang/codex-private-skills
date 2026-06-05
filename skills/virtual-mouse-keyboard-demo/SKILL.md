---
name: virtual-mouse-keyboard-demo
description: Use when Codex needs to update, troubleshoot, or demonstrate the local virtual mouse and keyboard workflow created for browser/desktop control. Covers Playwright virtual browser sessions, Selenium isolated Chrome desktop with noVNC, screenshot observation, and cautious real Windows mouse/keyboard simulation only with explicit user permission.
---

# Virtual Mouse Keyboard Demo

## Quick Decision

Prefer the lightest control layer that satisfies the task:

1. Use Playwright virtual browser for normal web tasks. It gives virtual mouse/keyboard control without moving the user's real pointer.
2. Use the Selenium isolated Chrome container when a visible isolated browser desktop or demo proof is needed.
3. Use real Windows mouse/keyboard simulation only when the user explicitly allows it for the current task.

For the original project recap, known pitfalls, and demo sequence, read `references/project-recap.md`.

## Playwright Virtual Browser

Use bundled `scripts/codex-virtual-browser.ps1` or run Playwright directly.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\codex-virtual-browser.ps1 -Url "https://example.com"
```

If running from this skill folder, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\codex-virtual-browser.ps1 -Url "https://example.com"
```

Use this mode for browsing, snapshots, form filling, screenshots, and UI checks where a full desktop is not required.

## Isolated Chrome Desktop

Use Docker plus Selenium's standalone Chrome image when the user wants a visual demo or isolation from the real desktop.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-start.ps1
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-test.ps1
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-stop.ps1
```

Default endpoints:

```text
WebDriver: http://127.0.0.1:4444
noVNC: http://127.0.0.1:7900/?autoconnect=1&resize=scale&password=secret
```

The proof test types `virtual mouse and keyboard`, clicks Apply, and writes a screenshot to `output/isolated-browser/isolated-browser-proof.png` relative to the current working directory.

## Desktop Observation

Use screenshots when screen pixels matter. Prefer active-window or region captures over full screen.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\codex-look.ps1 -ActiveWindow
powershell -ExecutionPolicy Bypass -File scripts\codex-look.ps1 -Region "100,200,800,600"
```

Do not capture sensitive screens unless the user explicitly asks.

## Real Windows Input

Real input affects the active desktop. Before using it, confirm the user explicitly allowed real mouse/keyboard control for this task.

Smoke test command:

```powershell
$p = Start-Process powershell -ArgumentList '-STA','-ExecutionPolicy','Bypass','-File','scripts\codex-desktop-control-test.ps1' -PassThru
Start-Sleep -Seconds 3
powershell -ExecutionPolicy Bypass -File scripts\codex-look.ps1 -ActiveWindow
Wait-Process -Id $p.Id -Timeout 20 -ErrorAction SilentlyContinue
```

Expected behavior: a temporary topmost test window opens, receives a click, pastes a short confirmation text, and closes itself.

## Update Workflow

When updating this project:

1. Locate the active workspace copy first, commonly `C:\Users\A\Desktop\1`.
2. Read `AGENTS.md`, `docs/desktop-visibility.md`, and the relevant script before changing behavior.
3. Keep real desktop control gated behind explicit user permission.
4. Run the narrowest proof command after edits.
5. Copy improved scripts or docs back into this skill and refresh the H drive backup.

