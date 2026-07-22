# Restore Continuation Checklist - 2026-07-02

## Source

Manual pasted continuation summary:
${REDACTED_SECRET}

## Value Judgment

`HIGH_VALUE`

Reasons:

- It prevents repeated false PASS claims for Cursor/Kilo UI verification.
- It preserves a live continuation state for the mature Cursor + Kilo Code + OpenRouter SuperTool route.
- It names exact passed evidence, missing evidence, and next actions.
- It can be reused as a preflight checklist before future restoration, localization, and Kilo panel work.

## Current Target

Restore and verify mature AI Coding SuperTool state:

`Cursor + Kilo Code + OpenRouter proxy + DeepSeek V4 Pro / GLM-5.2 / Qwen3-VL-235B`

This is a mature-station recovery, not a blank rebuild. Start from existing skills, reports, model matrix, Gate Review, Repair Loop, multimodal evidence, checkpoint/handoff, and Knowledge Brain.

## Confirmed Passing Evidence

${REDACTED_SECRET}
- Long-task companion skills:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
- OpenRouter live smoke passed for:
  - `deepseek/deepseek-v4-pro`
  - `deepseek/deepseek-v4-flash`
  - `z-ai/glm-5.2`
  - `qwen/qwen3-vl-235b-a22b-instruct`
- Real work test passed:
  - DeepSeek V4 Pro fixed JS logic.
  - Node output: `NODE_STATUS_TEST_PASS`.
  - Qwen3-VL screenshot analysis returned PASS.
  - GLM-5.2 Gate Review returned PASS.
- Screenshot evidence path:
${REDACTED_SECRET}
- Kilo extension installed:
${REDACTED_SECRET}
  - Version: `7.3.46`
- Kilo config exists:
${REDACTED_SECRET}
  - Current model: `openrouter/deepseek/deepseek-v4-pro`
  - Small model: `openrouter/deepseek/deepseek-v4-flash`
  - Snapshot: `false`

## Still Not Passing

- Kilo Code panel has not been screenshot-proven open.
- The captured page was Cursor Agents, not Kilo Code.
- Chinese localization is not screenshot-proven.
- Round 1 screenshot still showed English menu text: `File / Edit / View / Help / New Agent / Search / Automations / Customize`.
- Cursor was not maximized before verification.
- A few-hour long-task run has not been completed in this continuation.

## Already Tried For Localization

- Relevant skills identified:
  - `ui-setting-actual-open-self-verify-loop`
  - `screenshot`
  - `cursor-kilo-supertool-mature-stack`
- Cursor Simplified Chinese language pack exists:
${REDACTED_SECRET}
- Cursor locale file was written:
${REDACTED_SECRET}
- File content:

```json
{
  "locale": "zh-cn"
}
```

This does not count as success because the post-restart screenshot still showed English UI.

## Next-Run SOP

1. Run Knowledge Brain and skill preflight before touching UI.
2. Re-enumerate live Cursor window handles; do not reuse stale handles.
3. Maximize Cursor first.
4. Take Round 1 screenshot after maximize.
5. Verify whether the current page is Kilo Code or Cursor Agents.
6. Open Kilo Code panel explicitly using known IDs or commands.
7. Capture Kilo Code panel screenshot.
8. Open Kilo Settings.
9. Capture Kilo Settings screenshot.
10. Capture visible model selector showing OpenRouter / DeepSeek V4 Pro.
11. If Chinese localization is being repaired, run at least two screenshot rounds:
    - Round 1: current state after maximize.
    - Repair: inspect Cursor language pack, argv, locale loading, and extension activation.
    - Round 2: after restart/reload.
12. Send required screenshots into chat, not only file paths or a written report.

## Known Kilo UI Targets

- ActivityBar container: `kilo-code-ActivityBar`
- Sidebar view: `kilo-code.SidebarProvider`
- Open in Tab command: `kilo-code.new.openInTab`
- Settings command: `kilo-code.new.settingsButtonClicked`

## Required Screenshots Before PASS

- Maximized Cursor main window.
- Kilo Code panel.
- Kilo Settings page.
- Model selector showing OpenRouter / DeepSeek V4 Pro.
- Chinese localization before/after comparison.

## Acceptance Rule

Current honest status:

```text
CURSOR_KILO_OPENROUTER_SUPERTOOL_RESTORE_88_PERCENT
```

Do not upgrade to full PASS until Kilo UI opening evidence, localization evidence, and the requested long-task evidence are actually captured and reviewed.

