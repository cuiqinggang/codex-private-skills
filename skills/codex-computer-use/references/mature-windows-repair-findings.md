# Mature Windows Repair Findings

Use this reference before exploring new repair paths. Prefer these known routes
and stop re-testing paths that are already explained by OS or upstream limits.

## Verified Sources

- OpenAI/codex issue `#25220`: Store-installed Windows bundled plugins can be
  unavailable when files under `C:\Program Files\WindowsApps` cannot be copied
  by normal Node/PowerShell copy paths. The mature workaround is stream-copying
  the bundled marketplace/plugins into user-writable Codex cache paths, then
  rebuilding the local marketplace and plugin cache.
  Source: https://github.com/openai/codex/issues/25220
- OpenAI/codex issue `#25411`: Windows 10 Pro 22H2 build `19045` can reach the
  Computer Use helper and run non-screenshot operations, but screenshot capture
  fails with `SetIsBorderRequired failed: unsupported interface (0x80004002)`.
  Source: https://github.com/openai/codex/issues/25411
- Microsoft documents `GraphicsCaptureSession.IsBorderRequired` as introduced
  in Windows 10 version 2104 / `10.0.20348.0` with UniversalApiContract v12.
  Windows 10 client build `19045` is below that API requirement, so this is an
  upstream/native helper compatibility limit unless Codex skips the API at
  runtime or the OS is upgraded.
  Source: https://learn.microsoft.com/en-us/uwp/api/windows.graphics.capture.graphicscapturesession.isborderrequired
- Community alternatives such as `ezpzai/codex-computer-use-windows` and
  `iFurySt/open-codex-computer-use` provide separate Windows desktop-control
  stacks. Treat them as fallback alternatives, not as a direct repair for the
  official Codex Computer Use plugin.

## Working Overall Repair Route

1. Repair the official bundled plugin cache and local marketplace first.
   Do not start with MSIX repatching.
2. Repair Chrome native messaging separately when only Chrome control fails.
3. Apply the native pipe fallback only when the `codex-computer-use-*` pipe
   exists but `nodeRepl.nativePipe` or `SKY_CUA_NATIVE_PIPE_DIRECTORY` is not
   exposed to the official client.
4. Verify through the official `computer-use-client.mjs` by running
   `sky.list_apps()` and `sky.list_windows()`. Do not validate the current
   plugin by directly constructing old `WindowsHelperTransport` forms; current
   helper constructors require arguments and can produce false failures.
5. Use MSIX/ASAR dry-run only as a last-resort UI gate check. On Store packages
   with missing or unreadable `app.asar.unpacked` native modules, standard
   `asar extract` may fail. A dry-run target match can use internal ASAR file
   extraction and skip unpacked native files because those are not JS gate
   targets.

## Current Windows 10 19045 Capability Boundary

Important distinction:

- Official Computer Use screenshot means `codex-computer-use.exe` successfully
  returns screenshots from `sky.get_window_state({ include_screenshot: true })`.
  This path fails on Windows 10 build `19045` because the helper calls
  `SetIsBorderRequired`.
- Windows native screenshot fallback means an external OS capture route such as
  the `screenshot` skill's PowerShell helper using
  `System.Drawing.Graphics.CopyFromScreen`. This works on the same machine and
  is useful for visual diagnosis, screenshots, and human review.
- External OS screenshots do not populate the official Computer Use helper's
  internal screenshot cache. Therefore they do not make official coordinate
  `sky.click`, `sky.scroll`, or `sky.drag` pass. Treat those as separate
  capabilities unless an explicit auxiliary-control mode is implemented and
  clearly labeled as non-official Computer Use.

Expected PASS on this OS after repair:

- `sky.list_apps()`
- `sky.list_windows()`
- `sky.launch_app()`
- `sky.get_window()`
- `sky.activate_window()`
- `sky.get_window_state({ include_screenshot: false, include_text: true })`
- `sky.type_text()`
- `sky.press_key()`
- `sky.perform_secondary_action()` for stable actions such as `Raise`

Expected FAIL until upstream helper or OS support changes:

- `sky.get_window_state({ include_screenshot: true })`
- coordinate `click`
- coordinate `scroll`
- coordinate `drag`

Reason: coordinate input requires a fresh screenshot cache, and screenshot
capture fails before returning a screenshot id.

Expected PASS through OS-level fallback:

- `powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\screenshot\scripts\take_screenshot.ps1" -Mode temp -ActiveWindow`

Use this fallback for visual checks and debugging, not as evidence that official
Computer Use screenshot or coordinate APIs are fixed.

Expected PASS through the local direct-client compatibility path after the
2026-06-08 repair:

- `sky.list_apps()`
- `sky.list_windows()`
- `sky.get_window()`
- `sky.activate_window()`
- `sky.get_window_state({ include_screenshot: true, include_text: true })`
- `sky.launch_app({ app: "notepad.exe" })`
- `sky.type_text()`
- `sky.press_key()`

This path uses the official `WindowsComputerUseClientBase` but bypasses a stale
native pipe client by loading the local `helper_transport.js` directly. It also
copies official `scripts` and internal support files from the stable bundled
cache into the local compatibility plugin, then overwrites only the local helper
transport and local client entrypoint.

Known app-specific failure:

- `sky.set_value()` may fail on Notepad with
  `element no longer matches the cached target`. Prefer `type_text` plus
  `press_key` for Notepad and similar controls unless a stable editable element
  has been verified in the same app.

## Search-First Checklist For Future Failures

Before adding new repair code, search these exact symptoms:

- `SetIsBorderRequired failed 0x80004002`
- `Computer Use native pipe path is unavailable`
- `Windows Computer Use helper paths are unavailable missing-helper-path`
- `copyfile WindowsApps bundled plugins computer-use`
- `app.asar.unpacked ENOENT asar extract`
- `element no longer matches the cached target set_value`

Only implement a new workaround after confirming whether the symptom is already
covered by this reference.
