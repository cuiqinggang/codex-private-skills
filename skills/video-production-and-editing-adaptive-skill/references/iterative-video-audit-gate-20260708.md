# Iterative Video Audit Gate

Date: 2026-07-08

## Why This Exists

The user corrected a V0 promotional video workflow where the first delivery had
outputs and screenshots, but the agent still stopped too early. The required
behavior is stricter: video work must include repeated self-audit, criticism,
and repair before claiming completion.

## Required Gate

For video work, completion requires more than rendering files.

Run at least these audit passes:

1. Technical audit: verify duration, stream codecs, resolution, frame rate,
   audio stream, file size, and compatibility.
2. Visual audit: generate dense frame strips or contact sheets, inspect them,
   and record concrete observations.
3. Content audit: check subtitles, CTA wording, text legibility, scene
   continuity, composition, and whether the output matches the stated goal.
4. Audio audit: check volume/clipping and state whether human listening is still
   required.
5. Gate decision: classify honestly as `FINAL_PASS`, `REVIEW_READY`,
   `PARTIAL`, or `BLOCKED`.

## Status Meaning

- `FINAL_PASS`: repeated audit found no blocking issues for the user's final
  goal.
- `REVIEW_READY`: technically complete and useful for review, but has content,
  continuity, text, or audio issues that must be reviewed or repaired before
  final production.
- `PARTIAL`: useful artifacts exist, but one or more requested deliverables are
  missing.
- `BLOCKED`: progress requires missing assets, user decision, credentials, or
  external action.

## Anti-Pattern

Do not say "completed" immediately after rendering. Do not push the audit burden
back to the user when the agent can inspect frames, probes, and reports itself.

## Reuse Trigger Phrases

- video audit
- self review
- 挑刺
- 审计
- 反复测试
- V0粗剪
- 验收截图
- 不能只说完成

## Proven Application

${REDACTED_SECRET}

This run caught and repaired a concrete issue: support videos named `12s` were
actually longer than 12 seconds. It also flagged unresolved content risks:
possible CTA typo, a sharp KF-06 transition, small unreadable screen text, and
the need for human audio listening.
