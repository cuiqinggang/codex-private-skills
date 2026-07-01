# Checklists

## Safety Checklist

- [ ] No full API key printed.
- [ ] No API key modified.
- [ ] Hermes Gateway not modified.
- [ ] Qwen direct vision config not touched.
- [ ] Windows proxy/network not changed.
- [ ] No unrelated user files deleted.
- [ ] No extra agent installed unless requested.
- [ ] No Claude Code login bypass.

## Kilo Config Checklist

- [ ] Kilo installed and visible in Cursor if deployment is active.
- [ ] Default model is DeepSeek V4 Pro unless a newer verified report changes it.
- [ ] GLM-5.2 is controller route, not forced default.
- [ ] Qwen3-VL is used manually for visual tasks.
- [ ] Auto Model / Auto Free disabled.
- [ ] Kilo Gateway sign-in route not forced.
- [ ] snapshot false unless explicitly required.

## Evidence Checklist

- [ ] Report file exists.
- [ ] Evidence directory exists.
- [ ] Logs directory exists.
- [ ] Model results directory exists.
- [ ] ZIP exists and contains real files, not only directories.
- [ ] Desktop three-digit numeric folder exists.
- [ ] Desktop three-digit numeric ZIP exists.
- [ ] Desktop numeric package includes final report and evidence ZIP.
- [ ] Desktop numeric package is compact and excludes caches/node_modules/browser profiles unless explicitly requested.
- [ ] Secret scan summary exists.
- [ ] Final status string is explicit.
- [ ] Model/provider claims distinguish config, report, user decision, catalog, and live call evidence.
- [ ] `live_call_verified=true` is used only after a real provider response with non-empty assistant text.
- [ ] Output files were scanned for API key patterns after live verification.

## Vision Test Checklist

- [ ] OCR test.
- [ ] UI screenshot understanding test.
- [ ] Visual design-to-code understanding test.
- [ ] Visual debug test.
- [ ] Chart/table test.
- [ ] Video keyframe/contact-sheet test.
- [ ] Direct video input marked tested or not tested.
- [ ] Chinese output confirmed.

## Handoff Checklist

- [ ] Desktop copy made when requested.
- [ ] ZIP copy made when requested.
- [ ] Automatic desktop numeric ZIP made after completed report/task.
- [ ] Skill recent-use log updated.
- [ ] Next stage name written.
- [ ] Caveats written plainly.

## Verification Logic Checklist

- [ ] Success signals were computed.
- [ ] Failure signals were computed.
- [ ] Weighted or balanced status was used.
- [ ] Unknown was not automatically treated as FAIL.
- [ ] Rejected claims were repaired or left as explicit blockers.
- [ ] Final PASS was blocked if unresolved rejected claims remained.
