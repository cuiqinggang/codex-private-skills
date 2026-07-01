# AGENTS.md Patch Draft: UI Actual Open Verify Rule

Add this section to a workspace or global AGENTS.md after making a timestamped backup.

```markdown
## UI Setting Actual Open Self Verify Rule

For tasks involving software UI settings, plugin settings, localization, model/provider selection, workspace restoration, or opening UI panels, Codex must use:

`C:\Users\A\.codex\skills\ui-setting-actual-open-self-verify-loop`

The task is not complete from configuration alone. Codex must:

1. Back up relevant config.
2. Modify minimal config.
3. Restart the target software if needed.
4. Open the correct workspace.
5. Open the target page/panel.
6. Save screenshots to an evidence directory.
7. Inspect screenshots.
8. Repair if target state is not visible.
9. Repeat at least two verification rounds.
10. Use only one final status:
   - `ACTUAL_OPEN_VERIFY_PASS`
   - `PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE`
   - `FAIL_NEEDS_FURTHER_FIX`

Forbidden acceptance phrases:

- 预计通过
- 应该生效
- 用户打开后确认
- 配置已写入所以完成
- 需要用户肉眼验收
```
