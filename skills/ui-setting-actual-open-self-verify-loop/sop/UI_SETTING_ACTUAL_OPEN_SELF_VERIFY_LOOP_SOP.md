# UI Setting Actual Open Self Verify Loop SOP

## Scope

This SOP applies to UI settings, plugin settings, localization, model/provider selection, workspace recovery, and panel-opening tasks.

## Step 1: Identify Target State

Record:

- target software
- target workspace
- target page/panel
- target setting
- expected visible result
- files that must not be changed
- secrets that must not be printed

## Step 2: Back Up Config

Before editing, copy relevant config files to a timestamped backup directory.

Examples:

- Cursor `argv.json`
- Cursor `settings.json`
- Kilo config files
- MCP config files
- plugin settings files

Do not back up or print full API keys in reports.

## Step 3: Change Minimal Config

Apply only the required setting. Preserve unrelated keys and user changes.

## Step 4: Restart Target Software

Close and reopen the target app when required for settings to load. If forced close is risky, explain why and choose a safer restart path.

## Step 5: Open Correct Workspace

Use a command or UI automation to open the intended workspace. Do not leave the user to navigate manually.

## Step 6: Open Target Page

Open the actual page or panel that proves the setting:

- settings page
- extension panel
- model selector
- provider selector
- agent/composer page
- project/file explorer

## Step 7: Screenshot Evidence

Create an evidence directory. Save screenshots with clear names:

- `round1_workspace.png`
- `round1_target_page.png`
- `round1_model_provider.png`
- `round1_response.png`
- `round2_workspace.png`
- `round2_target_page.png`
- `round2_model_provider.png`
- `round2_response.png`

## Step 8: Inspect Screenshots

Read the screenshot content before reporting. Judge:

- expected text visible
- target setting visible
- correct workspace visible
- target model/provider visible
- real response returned
- normal residue vs unresolved problem

## Step 9: Repair and Repeat

If Round 1 does not prove the target, repair and repeat. At least two rounds are required before final acceptance.

## Step 10: Final Status

Use exactly one:

- `ACTUAL_OPEN_VERIFY_PASS`
- `PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE`
- `FAIL_NEEDS_FURTHER_FIX`

Do not use expectation language as acceptance.
