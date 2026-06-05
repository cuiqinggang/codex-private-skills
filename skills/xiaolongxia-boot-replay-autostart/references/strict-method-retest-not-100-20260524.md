# Strict Method Retest Not 100 Percent 2026-05-24

## Status

`XIAOLONGXIA_BOOT_REPLAY_3X_STRICT_METHOD_NOT_100_STOP`

The user requested a new three-round test to verify whether the summarized method could succeed 100%. The retest found that the method was not yet reliable enough for automatic 3/3 success.

## Evidence Root

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-BOOT-REPLAY-3X-STRICT-METHOD-20260524`

## Confirmed Failures

1. `Ctrl+A` can select the OpenClaw page instead of only the input.
2. Send-button coordinates can miss or fail even when marker text is visible in the input.
3. Foreground focus can drift to Douyin or ChatGPT after waiting.
4. `chrome.exe --new-tab` is not a proof that OpenClaw is foreground.
5. Active-window screenshots after wait are not acceptable unless the full desktop or title evidence proves foreground is OpenClaw.

## Updated Rules

- Do not use `Ctrl+A` in the OpenClaw page.
- Do not rely on a send-button coordinate.
- Use Enter only after screenshot proves the marker is in the OpenClaw input field.
- After every wait, take a full desktop screenshot and confirm the foreground page.
- If foreground is not OpenClaw, reject the screenshot as evidence and do not count the round as PASS.
- Do not claim 100% browser success until three consecutive rounds complete without these failures.

## Practical Conclusion

The method is valid as a gated visual workflow, but not yet a 100% unattended automation workflow.

Future work should add a stronger foreground and tab-control mechanism for the user's normal Chrome profile before using this as an autostart or unattended test path.
