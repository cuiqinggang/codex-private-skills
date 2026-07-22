---
name: video-production-and-editing-adaptive-skill
description: Canonical local-video router for production, editing, trimming, packaging, subtitles, music replacement, phone or WeChat delivery, reference-video analysis, and AI-video post-processing. Use to select and delegate to the narrowest mature video skill; do not replace specialist HyperFrames, captioning, music, or publishing workflows.
---

# Video Production And Editing Adaptive Skill

Use this skill as the general dispatcher for:

```text
video production + video editing + trimming + subtitles + packaging + export verification
```

Chinese name, transliterated for validator-safe ASCII:

```text
shipin zhizuo yu bianji yitihua chengshu fang'an shipei jinengbao
```

## Core Rule

Do not start by listing tools.

Always route in this order:

1. Confirm the final intended result.
2. Understand the provided assets: videos, screenshots, images, audio, text,
   reference examples, platform constraints, and user dislikes.
3. Match the task to an existing mature solution, local success case, or skill
   package.
4. Adapt the mature route to the current local files.
5. Choose the minimum tools needed.
6. Execute in small steps.
7. Export and verify with visible evidence.
8. Record reusable lessons back into the appropriate skill/reference file when
   the user asks.

## Existing Skills Are Modules

Do not delete, overwrite, or replace older video skills. Reuse them as modules:

${REDACTED_SECRET}
  - AI video generation / Wan2.2 / ComfyUI baseline.
${REDACTED_SECRET}
  - PPT-style image showcase and simple slideshow video patterns.
${REDACTED_SECRET}
  - Turning video workflows and prior results into reusable skills.
${REDACTED_SECRET}
  - Poster/video publishing and campaign packaging when relevant.
${REDACTED_SECRET}
  - Fast speech-to-text for video/audio learning materials. Use before frame
    extraction when the user wants spoken content or a simple text version.
${REDACTED_SECRET}
  - Distill video transcripts, courses, podcasts, long articles, and books into
    reusable Agent Skills after the material has been converted to text.
${REDACTED_SECRET}
  - Video-derived GitHub AI resource search skill. Use when the user wants to
    find AI tools, MCP resources, Claude Code/Codex workflows, n8n templates,
    open-source tutorials, or reusable GitHub resources.

This skill is the top-level router and post-processing/editing layer.

## Routing

Read only the reference that matches the task:

- For universal mature-route selection:
  `modules/00-universal-problem-solving-logic.md`
- For video editing, trimming, subtitles, music, and export:
  `modules/10-video-editing-and-packaging-flow.md`
- For full automatic video production/editing workflow design:
  `references/auto-video-production-editing-mature-flow-20260706.md`
- For 10-15 second family/education promo rebuilding, anti-PPT checks,
  generated-hand continuity, CTA/SFX frame sync, and six-round acceptance:
  `references/ai-doctor-12s-family-promo-quality-gates-20260712.md`
- For Jianying/CapCut, Shotcut, Kdenlive, open-source replacement testing,
  and distilling editor features into reusable free workflows:
  `references/video-editor-feature-distillation-20260706.md`
- For video/audio speech-to-text:
${REDACTED_SECRET}
- For the local video-skill zone index and video-to-skill routing:
  `references/VIDEO_SKILL_ZONE_INDEX.md`
- For phone/WeChat delivery and compatibility:
  `modules/20-phone-wechat-video-acceptance.md`
- For skill-preservation and reusable workflow updates:
  `modules/30-skill-integration-and-memory.md`

## Tool-Minimization Rule

Preferred tool order:

```text
direct file processing
> scripts / FFmpeg / Python
> API / CLI tools
> desktop software scripting
> GUI automation
> manual operation
```

Use GUI apps such as Jianying, Premiere, DaVinci, or Computer Use only when the
task genuinely needs them. For simple music replacement, codec conversion,
trimming, joining, resizing, subtitles, or preview frames, prefer FFmpeg/Python.

## Mandatory Acceptance Evidence

Every video editing/export task must produce enough evidence for the user to
trust the result. At minimum, collect:

- original video info
- final export path
- final video/audio stream info
- key preview frame or contact sheet
- what changed
- what did not change
- any compatibility choices, especially H.264/AAC for phone/WeChat

Use:

```text
templates/video-acceptance-report-template.md
```

## 2026-07-08 Iterative Audit Gate Addendum

For video production tasks, do not treat "file generated" as completion.
Before final reporting, run several rounds of self-audit and record the
evidence:

- technical probe: duration, codec, resolution, frame rate, audio stream
- visual audit: contact sheet or dense frame strip, inspected by the agent
- content audit: subtitles, CTA wording, visible text, continuity, composition
- audio audit: stream check, volume/clipping check, and human-listening caveat
- gate decision: `FINAL_PASS`, `REVIEW_READY`, `PARTIAL`, or `BLOCKED`

If the agent finds meaningful issues, say so directly and continue fixing what
can be fixed. Only mark `FINAL_PASS` when repeated audit finds no blocking
issues for the user's stated final goal.

Reference:

```text
references/iterative-video-audit-gate-20260708.md
```

## Hard Boundaries

- Do not delete source videos, old skills, old workflows, models, or outputs.
- Do not overwrite an accepted output unless the user explicitly asks.
- Do not invent a large new workflow when an existing local route works.
- Do not claim success from logs alone; verify streams and at least one visible
  frame/contact sheet.
- If the user says "do not change anything else", change only the requested part.

## Common Mature Routes

- Add gentle background music while preserving the picture:
  FFmpeg audio mix, then verify video stream and extracted frame.
- Fix "only audio, no video" playback:
  transcode video to H.264 `yuv420p`, keep AAC audio, then verify.
- Phone/WeChat slideshow:
  prefer full-screen 9:16 crop, no small landscape card, no white border, no
  progress dots, no shake, no zoom unless requested.
- Remove one bad image from a slideshow:
  exclude by filename and regenerate; keep all other parameters unchanged.
- Extract text from a video:
  prefer direct audio transcription with `video-audio-transcription`; use
  frame extraction only for explicit on-screen text/OCR/key-page requests.
- Save a repeatable method:
  update the relevant skill reference, not the finished output folder only.
- Distill Jianying/CapCut-style editor features:
  use installed editors for direct GUI work, but distill script-friendly
  features into FFmpeg/Whisper/Auto-Editor/PySceneDetect/Remotion routes.
