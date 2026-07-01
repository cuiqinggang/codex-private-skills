---
name: ui-setting-actual-open-self-verify-loop
description: Use whenever a task involves software UI settings, plugin settings, localization, model/provider selection, workspace restoration, or opening UI panels. Requires backing up config, changing settings, restarting the target app, opening the real page, taking screenshots, inspecting evidence, fixing failures, and repeating at least two verification rounds before claiming PASS.
---

# UI Setting Actual Open Self Verify Loop

## Purpose

Prevent false completion on UI/configuration tasks. A setting is not complete just because a config file was written. It is complete only when the target software is actually opened, the target page is visible, screenshots are saved, and the screenshot evidence proves the expected state.

## Mandatory Companion Skill

For every applicable task, also use:

- `screenshot`

If the task involves browser or Electron UI automation and a more specific browser/Chrome/Playwright skill applies, use that too. The screenshot evidence remains mandatory.

## Trigger Scenarios

Use this skill for any task involving:

- software interface settings
- plugin or extension settings
- Cursor, Kilo Code, Cline, Zoo, OpenCode, Aider, Claude Code, Serena, Hermes UI panels
- Chinese localization or any display language change
- model selection
- provider selection
- OpenRouter / DeepSeek / OpenAI-compatible channel selection
- workspace restoration or opening a specific workspace
- opening a UI panel and verifying its visible state
- restoring visible sidebars, agent panels, settings pages, or extension tabs

## Non-Negotiable Rules

- Do not claim PASS from config files alone.
- Do not claim PASS from environment variables alone.
- Do not say "should work", "expected to pass", or "ask the user to open it and check".
- Do not use "configured successfully" as final proof.
- Do not make the user perform the final visual verification when automation can open and screenshot the page.
- Only screenshot-proven results can be PASS.

## Required Workflow

1. Back up relevant configuration files before editing.
2. Modify the minimal required configuration.
3. Close and restart the target software when the setting requires a reload.
4. Open the correct workspace using a command or UI automation.
5. Open the target page, panel, settings screen, model selector, provider selector, or agent page.
6. Save screenshots to an `evidence` directory named for the task.
7. Inspect screenshots before reporting.
8. If the target state is not visible, repair the issue and repeat.
9. Run at least two verification rounds.
10. Report only one final status:
    - `ACTUAL_OPEN_VERIFY_PASS`
    - `PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE`
    - `FAIL_NEEDS_FURTHER_FIX`

## Chinese Localization Acceptance

For Cursor + Kilo localization tasks, verify:

- Cursor top menu is Chinese.
- Cursor New Agent / Composer page is Chinese or clearly documented as official/product English residue.
- Kilo Code page is Chinese.
- Kilo Settings page is Chinese.
- Kilo default response is Simplified Chinese.
- The model remains OpenRouter / DeepSeek V4 Pro when that is the active route.
- Existing validation files are not damaged.

## Model / Provider Acceptance

For model or provider tasks, verify:

- The UI bottom bar or visible selector shows the target model/provider.
- Config files are not the only proof.
- A minimal real task is sent.
- A real response returns.
- Screenshot or output evidence is included in the report.

## Workspace Acceptance

For workspace tasks, verify:

- Cursor left sidebar shows the correct workspace.
- Expected files are visible.
- Kilo can read files in that workspace.
- The user is not left to find the folder manually.

## Required Report Fields

Every final report must include:

1. What was modified.
2. Which pages were opened.
3. Screenshot paths.
4. Screenshot judgment.
5. Round 1 result.
6. Round 2 result.
7. If Round 1 failed, what was fixed.
8. Final PASS/PARTIAL/FAIL status.
9. Which English residues are normal.
10. Which issues remain unresolved.
11. Whether user manual action is still needed.
12. If manual action is needed, why it cannot be automated.

## Forbidden Final Language

Do not use these as final acceptance:

- "预计通过"
- "应该生效"
- "用户打开后确认"
- "配置已写入所以完成"
- "需要用户肉眼验收"

## References

- SOP: `sop/UI_SETTING_ACTUAL_OPEN_SELF_VERIFY_LOOP_SOP.md`
- Checklist: `checklists/UI_SETTING_ACTUAL_OPEN_SELF_VERIFY_CHECKLIST.md`
- Report template: `templates/UI_SETTING_ACTUAL_OPEN_VERIFY_REPORT_TEMPLATE.md`
- Usage log: `logs/RECENT_USE.md`
- Acceptance page: `acceptance/index.html`
