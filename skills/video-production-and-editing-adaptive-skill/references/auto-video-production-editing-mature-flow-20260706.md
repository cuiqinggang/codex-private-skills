# Full Automatic Video Production And Editing Mature Flow

Date: 2026-07-06

Chinese trigger phrases:

- 全自动视频剪辑
- 全自动视频制作
- 自动成片
- 自动粗剪
- 自动字幕
- 自动配音配乐
- 自动发布前检查
- 视频制作剪辑一体化

## Positioning

This is the default mature route for repeatable automatic video work. Treat
production and editing as one pipeline:

```text
idea/assets -> script/structure -> media collection/generation -> rough cut
-> narrative edit -> subtitles/audio/music -> packaging/export -> evidence
-> optional reviewed publishing
```

The route is automation-first, but not judgment-free. Creative choices,
platform risk, account actions, paid actions, and public publishing still need
explicit review gates.

## Core Decision

Use this stack by default:

```text
FFmpeg + Python orchestration + Whisper/whisper.cpp + PySceneDetect/Auto-Editor
+ optional Remotion + local skill gates
```

Use GUI editors such as Jianying/CapCut, Premiere, or DaVinci Resolve only when
a template, proprietary effect, team handoff, or manual creative polish truly
requires the editor. They are not the default automation core.

## Workflow

### 1. Intake And Goal Lock

Collect:

- final platform: Douyin, WeChat, YouTube, Bilibili, course, internal demo
- aspect ratio: 9:16, 16:9, 1:1
- target length: short, medium, long
- source type: raw footage, images, screen recording, AI clips, voice, text
- required output: MP4 only, subtitles, cover, publish package, transcript
- forbidden actions: no public post, no account changes, no paid services

Output a `manifest.json` or simple task sheet with source files, goal, target
format, and acceptance checks.

### 2. Media Probe And Index

Run media probing before editing:

- duration
- width and height
- frame rate
- rotation
- video codec
- audio codec
- audio presence
- file size

Preferred tool: FFmpeg/ffprobe.

Acceptance: every source has a row in the media index. Do not cut blind.

### 3. Spoken Content Extraction

If the video has speech, transcribe first. This gives the editor a searchable
timeline and enables subtitle, highlight, and silence decisions.

Local preferred route:

${REDACTED_SECRET}
- local `whisper.cpp`
- model `ggml-large-v3.bin` for Chinese or reusable transcripts

Optional external/open-source routes:

- OpenAI Whisper for general ASR
- faster-whisper when speed matters
- WhisperX when word-level timestamps or speaker diarization are needed

Acceptance: TXT/SRT/JSON exist, cover full duration, and obvious ASR errors are
not ignored in user-facing text.

### 4. Automatic Rough Cut

Choose rough-cut method by material:

| Material | Default method | Tools |
|---|---|---|
| Talking head / tutorial | remove silence and dead air | Auto-Editor, FFmpeg |
| Multi-shot footage | split scenes, rank usable shots | PySceneDetect, FFmpeg |
| Screen recording | cut mistakes and idle time | transcript + silence detection |
| Image set / PPT | fixed slide timing and crossfade | ppt-showcase-video, FFmpeg |
| AI-generated clips | keep selected takes only | contact sheet + manifest |

Do not use silence removal alone for music videos, emotional pauses, interviews,
or content where pauses carry meaning. In those cases, mark silence candidates
for review instead of deleting them automatically.

Acceptance: rough cut exports to a new file; source files remain untouched.

### 5. Structure Edit

Build the story order:

```text
hook -> context -> main proof/demo -> key result -> CTA/ending
```

Automation options:

- transcript summary to find hooks and strong claims
- scene list to identify visual changes
- simple score for segments: speech density, keywords, audio level, motion,
  face/object presence if available
- template timeline for repeat formats

For deterministic social/PPT videos, reuse:

${REDACTED_SECRET}
${REDACTED_SECRET}

For generated AI video clips, reuse:

${REDACTED_SECRET}

Acceptance: a timeline plan exists before final render. It can be EDL-like JSON,
a Remotion composition, or a simple ordered clip list.

### 6. Subtitles, Voice, Music, And Sound

Subtitles:

- generate SRT from transcript
- burn in only when the target platform or visual style requires it
- keep editable SRT beside the MP4

Voice:

- keep original voice if useful
- use TTS only when the user asks or the source has no voice
- document the voice source and usage rights

Music:

- prefer user-provided music or proven local accepted soundtrack
- avoid crude generated tones unless explicitly requested
- mix as background, not foreground
- default background volume: about 0.15-0.30 of original level
- fade in/out about 1.0-1.5 seconds

Acceptance: ffprobe confirms audio stream; volume is not clipping; final file is
not accidentally silent.

### 7. Visual Package

Create:

- final MP4
- cover frame or cover image
- platform-specific caption
- optional short/full versions
- optional Douyin/WeChat separated package

Compatibility defaults:

- H.264 video
- `yuv420p`
- AAC audio
- `+faststart`
- keep portrait videos portrait

Acceptance: MP4 plays broadly on phone/WeChat; no HEVC-only surprise unless the
user requested it.

### 8. Verification Evidence

Every automatic run must produce:

- original media info
- final media info
- final path
- contact sheet or key preview frames
- transcript/subtitle path if speech exists
- what was changed
- what was not changed
- known caveats

Use the skill template:

```text
templates/video-acceptance-report-template.md
```

Acceptance: never claim PASS from logs alone. At least one visible frame or
contact sheet must exist.

### 9. Optional Publishing

Publishing is not part of automatic editing by default. It is a separate gate.

Allowed after review:

- prepare platform package
- upload through official entry
- fill title/caption
- choose cover
- click publish only if the user explicitly approved the scope

Stop conditions:

- captcha
- face verification
- SMS/security prompt
- paid promotion
- account setting changes
- violation warning
- bulk private messaging
- unknown platform risk

## Required Software And Plugins

### Default Required

| Layer | Choice | Why |
|---|---|---|
| Media engine | FFmpeg / ffprobe | stable command-line probe, cut, mux, transcode, subtitle, frame extraction |
| Orchestrator | Python / PowerShell | repeatable local automation and manifests |
| ASR | local whisper.cpp skill | fast Chinese transcription and subtitle source |
| Rough cut | Auto-Editor | mature silence/dead-air cutting for talking videos |
| Scene split | PySceneDetect | mature shot/scene detection for multi-shot footage |
| Evidence | FFmpeg contact sheet + ffprobe JSON | visible acceptance proof |

### Recommended Optional

| Layer | Choice | Use When |
|---|---|---|
| Template video | Remotion | code-driven videos, reusable branded templates, dynamic captions |
| Image/PPT showcase | ppt-showcase-video skill | image collections, static social videos, simple promo videos |
| Poster/video publish | ai-poster-video-publish-pipeline skill | platform packages and reviewed publishing |
| AI clip generation | ComfyUI Aaki video baseline | Wan/AI generated clips before editing |
| Word timestamps | WhisperX or faster-whisper | karaoke subtitles, speaker segments, transcript precision |
| GUI finish | DaVinci Resolve/Premiere/Jianying | manual color, templates, team handoff, proprietary effects |

### Not Default

| Tool Type | Reason |
|---|---|
| GUI-only editing | hard to make deterministic and harder to verify |
| random online video makers | weak reproducibility, upload/privacy risk |
| platform auto-publish without approval | account and compliance risk |
| generated music with no quality gate | previous local failure mode: technically valid but unpleasant |

## Skill Routing

Use this router:

```text
raw speech/video to text -> video-audio-transcription
image collection to vertical social video -> ppt-showcase-video
poster/campaign package -> ai-poster-video-publish-pipeline
AI generated clip/source video -> comfyui-aaki-v3-video-baseline
ordinary edit/export/subtitles/music -> video-production-and-editing-adaptive-skill
valuable lesson/workflow preservation -> codex-video-to-usable-skill-loop
```

## Output Folder Shape

Recommended per project:

```text
input/
  raw/
  audio/
  images/
work/
  probes/
  transcripts/
  scenes/
  rough_cuts/
  timeline/
output/
  final/
  platform_packages/
reports/
  contact_sheets/
  frames/
  acceptance.md
  manifest.json
```

## Pass/Fail Gates

PASS requires:

- final MP4 exists
- ffprobe confirms video stream
- ffprobe confirms expected audio stream or intentionally silent status
- compatibility is H.264/AAC/yuv420p unless otherwise requested
- contact sheet or preview frame exists
- subtitle/transcript exists when speech was used
- source files remain untouched
- report lists changes and caveats

REVIEW_READY means:

- final candidate exists but needs user creative/content review

PARTIAL means:

- usable intermediate exists, but a required output or evidence item is missing

BLOCKED means:

- missing source, missing required tool, unacceptable quality, platform risk, or
  required user approval.

## Failure Review Entry Points

When a run fails, classify it:

- ASR failure: wrong model, poor audio, no language hint, missing cleanup
- rough-cut failure: silence threshold too aggressive, pauses carried meaning
- visual failure: bad source frames, crop cut text, unstable motion, AI artifacts
- audio failure: silent export, music too loud, unpleasant generated audio
- export failure: wrong codec, no video on phone, huge file, wrong aspect ratio
- publishing failure: approval missing, platform risk, security prompt

Record the failure in the relevant skill reference before repeating the same
workflow.

## Source Notes

Current public tool references checked on 2026-07-06:

- FFmpeg documentation: https://ffmpeg.org/documentation.html
- Auto-Editor repository: https://github.com/WyattBlue/auto-editor
- PySceneDetect documentation: https://www.scenedetect.com/docs/latest/
- Remotion render docs: https://www.remotion.dev/docs/render
- OpenAI Whisper repository: https://github.com/openai/whisper
- whisper.cpp repository: https://github.com/ggerganov/whisper.cpp
- faster-whisper repository: https://github.com/SYSTRAN/faster-whisper
- WhisperX repository: https://github.com/m-bain/whisperX

