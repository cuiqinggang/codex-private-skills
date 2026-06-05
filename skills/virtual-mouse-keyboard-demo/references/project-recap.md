# Virtual Mouse And Keyboard Project Recap

## Source Project

Original workspace found at `C:\Users\A\Desktop\1`.

Important files:

- `AGENTS.md`: workspace operating rules.
- `docs/codex-ops.md`: general Codex operating playbook.
- `docs/desktop-visibility.md`: desktop visibility and control workflow.
- `scripts/codex-virtual-browser.ps1`: Playwright virtual browser launcher.
- `scripts/codex-look.ps1`: wrapper around the screenshot skill helper.
- `scripts/codex-desktop-control-test.ps1`: real Windows input smoke test.
- `scripts/isolated-browser-start.ps1`: Docker Selenium Chrome startup.
- `scripts/isolated-browser-test.ps1`: WebDriver proof test for virtual typing/clicking.
- `scripts/isolated-browser-stop.ps1`: stop or remove the container.
- `output/isolated-browser/isolated-browser-proof.png`: proof screenshot produced by the isolated browser test.

## What Was Built

The project established a safe ladder for Codex-style computer control:

1. Browser automation through Playwright for most web work.
2. Full isolated browser desktop through Docker + Selenium standalone Chrome + noVNC.
3. Real Windows desktop input only as an explicit, permission-gated last resort.

The important design choice was separating "virtual mouse and keyboard" from "real mouse and keyboard". Playwright and WebDriver can type and click inside their controlled browser without moving the user's physical pointer. The Windows input test can move/click/type on the active desktop and therefore must be treated as risky.

## Working Demo Sequence

For a visible isolated browser demo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-start.ps1
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-test.ps1
```

Expected JSON includes:

```json
{
  "ok": true,
  "result": "container browser OK: virtual mouse and keyboard",
  "webdriver": "http://127.0.0.1:4444",
  "noVnc": "http://127.0.0.1:7900/?autoconnect=1&resize=scale&password=secret"
}
```

Stop it when done:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\isolated-browser-stop.ps1
```

## Troubleshooting Notes

- If Docker is missing, `isolated-browser-start.ps1` fails immediately with `Docker is not available on PATH.`
- If ports `4444` or `7900` are already used, start fails before creating the container.
- If the Selenium image is not present, Docker may need network access to pull `selenium/standalone-chrome:latest`.
- If WebDriver is slow to become ready, `isolated-browser-start.ps1` waits up to 60 seconds and then prints recent container logs.
- If screenshots fail, verify the screenshot skill exists at `%USERPROFILE%\.codex\skills\screenshot\scripts\take_screenshot.ps1`.
- If real desktop testing is requested, run PowerShell with `-STA`; Windows Forms and SendKeys need it.

## Safety Rules To Preserve

- Do not use real Windows mouse or keyboard simulation unless the user explicitly allows it for that exact task.
- Prefer isolated browser or virtual browser control for demonstrations.
- Re-observe after every meaningful click/type/navigation before claiming success.
- Avoid full-screen screenshots when active-window or region capture is enough.
- Never capture screens likely to contain passwords, recovery codes, private keys, payment details, or private conversations unless the user explicitly asks.

## Compact Update Checklist

1. Read source docs and scripts.
2. Patch the active workspace copy.
3. Run the smallest proof test.
4. Copy changed scripts/docs into this skill.
5. Validate the skill.
6. Refresh the H drive backup.

