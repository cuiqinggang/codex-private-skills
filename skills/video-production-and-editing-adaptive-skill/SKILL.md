---
name: video-production-and-editing-adaptive-skill
description: Use when the user asks for video production, video editing, trimming, packaging, subtitles, music replacement, phone/WeChat video delivery, reference-video analysis, AI-generated video post-processing, or turning a repeated video workflow into a reusable skill. Prefer mature existing routes, minimal tools, visible acceptance evidence, and do not overwrite older video skills.
metadata:
  short-description: Video production/editing mature-route adapter
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

- `H:\AI\skills\comfyui-aaki-v3-video-baseline`
  - AI video generation / Wan2.2 / ComfyUI baseline.
- `C:\Users\A\.codex\skills\ppt-showcase-video`
  - PPT-style image showcase and simple slideshow video patterns.
- `H:\AI\skills\codex-video-to-usable-skill-loop`
  - Turning video workflows and prior results into reusable skills.
- `H:\AI\skills\ai-poster-video-publish-pipeline`
  - Poster/video publishing and campaign packaging when relevant.

This skill is the top-level router and post-processing/editing layer.

## Routing

Read only the reference that matches the task:

- For universal mature-route selection:
  `modules/00-universal-problem-solving-logic.md`
- For video editing, trimming, subtitles, music, and export:
  `modules/10-video-editing-and-packaging-flow.md`
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
- Save a repeatable method:
  update the relevant skill reference, not the finished output folder only.
