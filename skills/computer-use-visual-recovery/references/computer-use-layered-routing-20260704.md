# Computer Use Layered Routing - 2026-07-04

## Core Relationship

Official Windows Computer Use, the local repair skill, and the ordinary
coordinate screenshot method are one connected capability stack.

- Official OpenAI Computer Use is the runtime engine. Prefer it for app/window
  enumeration, activation, screenshots, typing, clicking, scrolling, dragging,
  and state capture when it is available.
- `codex-computer-use` is the repair and strict-verification layer. Use it when
  the official runtime is missing, disabled, stale, or blocked by plugin cache,
  bundled marketplace, native pipe, Chrome native host, Store package copy, or
  Windows sandbox issues.
- `computer-use-visual-recovery` is the human-visible operation layer. Use it
  by default when the task depends on seeing a button, page, modal, prompt,
  icon, form field, status label, or other visible UI state.

## Default Route

```text
Need to operate UI
-> use official Computer Use as the engine when available
-> observe the current screen/window
-> apply ordinary coordinate screenshot method
-> act once
-> observe again
-> verify success
-> if engine or plugin plumbing fails, switch to codex-computer-use repair
```

## When Each Layer Leads

Use official Computer Use first when:

- apps/windows can be listed
- the target window can be activated
- screenshot/state capture works
- typing or simple key input is enough
- accessibility exposes a reliable element index

Use ordinary coordinate screenshots first when:

- a normal human would operate the visible UI
- the target is a button, modal, input field, toolbar item, browser page, or
  desktop app control
- accessibility text is incomplete but the target is visible
- the task needs proof from before/after screenshots
- a coordinate/state branch has already been tested for this UI

Use `codex-computer-use` repair first when:

- Computer Use is unavailable or not listed
- `computer-use@openai-bundled` is missing or disabled
- `browser/latest`, `chrome/latest`, or `computer-use/latest` cache is missing
- `CODEX_ELECTRON_ENABLE_WINDOWS_COMPUTER_USE` is missing
- the official client cannot list apps/windows
- Chrome native host or extension connection fails
- native pipe path is stale or unavailable
- Store package files cannot be copied or launched directly

## Acceptance Rule

Never claim restored capability from installation alone.

Minimum proof should include:

- strict verification from `codex-computer-use` when repair was touched
- official client can list apps/windows
- at least one real window operation when desktop control is being validated
- screenshot or state evidence after the action
- no leftover test windows or unsaved files

Known 2026-07-04 evidence on this machine:

- Codex Store package `26.623.13972.0`.
- Official client listed apps/windows after repair.
- Browser, Chrome, and Computer Use bundled cache were restored.
- Chrome native host and selected profile connection passed strict verify.
- Notepad smoke launched, activated, typed text, and captured screenshot/state.
- Modern Notepad close via Computer Use keypress did not close the unsaved
  window; use visual-dialog handling or explicit cleanup for that branch.
