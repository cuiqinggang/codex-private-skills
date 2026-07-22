# Feature Map

## Core Jianying/CapCut-Style Features

| Feature | Direct Tool | Distilled Route | Decision |
|---|---|---|---|
| Import, cut, join clips | Shotcut/Kdenlive | FFmpeg concat/trim | script-distill for batches; GUI for manual timeline |
| Auto subtitles | Shotcut if enabled, Jianying reference | whisper.cpp / Whisper / faster-whisper -> SRT | script-distill |
| Burn subtitles | Shotcut/Kdenlive | FFmpeg subtitles filter | script-distill |
| Remove silence/dead air | Jianying reference | Auto-Editor + FFmpeg | script-distill |
| Scene detection | GUI review | PySceneDetect + contact sheet | script-distill |
| Background music mix | Any editor | FFmpeg audio filters | script-distill |
| Fade in/out | Any editor | FFmpeg filters | script-distill |
| Vertical social export | Any editor | FFmpeg scale/pad/crop; ppt-showcase-video | script-distill |
| Image slideshow | Jianying templates, Shotcut/Kdenlive | ppt-showcase-video / Remotion / FFmpeg | script-distill |
| Cover image | Any editor | FFmpeg frame extract + Pillow/HTML template | script-distill |
| Templates/stickers/effects | Jianying/CapCut | only recreate with own assets/templates | hybrid or do-not-copy |
| Beauty/portrait enhancement | Jianying/CapCut | limited open-source route; manual review | hybrid |
| AI generated effects | Jianying/CapCut paid/reference | ComfyUI/video generation skill when legal assets exist | hybrid |
| Color correction | Shotcut/Kdenlive | FFmpeg filters for simple cases | hybrid |
| Manual fine cut | Shotcut/Kdenlive | not worth scripting | direct-use |
| Platform package | Jianying/CapCut reference | ai-poster-video-publish-pipeline | script-distill |

## Recommended Product Roles

| Product | Role |
|---|---|
| Jianying/CapCut | Product reference, optional manual editor, paid/free boundary probe |
| Shotcut | Lightweight open-source GUI editor, quick manual verification |
| Kdenlive | More capable open-source timeline editor when installed |
| FFmpeg | Main deterministic media engine |
| whisper.cpp / Whisper | Subtitle and transcript engine |
| Auto-Editor | Rough cut for talking videos |
| PySceneDetect | Shot/scene segmentation |
| Remotion | Repeatable code-driven templates |

