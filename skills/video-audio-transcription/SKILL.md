---
name: video-audio-transcription
description: Use when the user asks to turn video or audio into text, extract spoken content from WeChat/Douyin/phone videos, make SRT/TXT/JSON transcripts, or quickly process learning videos without expensive frame extraction. Default to direct audio transcription; use frame OCR only when the user explicitly needs on-screen text.
---

# Video Audio Transcription

## Core Rule

For simple video text extraction, use speech-to-text first.

Do not default to video frame extraction. Frame extraction is more expensive and
only needed when the user asks for exact on-screen captions, slide/page text,
visual key pages, OCR evidence, or comparison between subtitle text and spoken
words.

For ordinary video-to-text, speech-to-text, or spoken-content extraction tasks,
extract audio and run local Whisper.

## Mature Local Route

Installed tool paths:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

Verified model:

- file: `ggml-large-v3.bin`
- mirror source: `https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin`
- SHA1: `AD82BF6A9043CEED055076D0FD39F5F186FF8062`
- SHA256: `64D182B440B98D5203C4F9BD541544D84C605196C4F7B845DFA11FB23594D1E2`
- multilingual: yes
- use when accuracy matters, especially Chinese homophones, proper nouns, and
  reusable transcripts.

Use the mirror source when `huggingface.co` is blocked or slow. Never trust a
downloaded model unless the SHA1 matches.

## Standard Workflow

1. Probe the media with `ffprobe` to confirm audio exists.
2. Extract audio to mono 16 kHz WAV.
3. Run `scripts/transcribe-video.ps1`.
4. Export TXT, SRT, JSON, and `readable-transcript.html`.
5. Clean obvious ASR errors in the user-facing version.
6. Regenerate the readable HTML from the cleaned transcript when a cleaned
   transcript exists.
7. If the user wants a reusable case, save raw transcript plus cleaned analysis
   into the relevant skill or Knowledge Brain path.

## User-Facing Reading Output

When the user wants to see, copy, or reuse the transcript, provide a readable
HTML version in addition to plain text. Use:

```powershell
${REDACTED_SECRET}
```

Readable transcript HTML requirements:

- preserve a top-right `复制全文` button
- use UTF-8
- use system UI fonts first: `system-ui`, `Segoe UI`, `Microsoft YaHei UI`,
  `Microsoft YaHei`, `PingFang SC`, `Noto Sans CJK SC`
- body text: about 19px, weight 500, line-height about 1.9
- color: soft dark text such as `#202124`, not heavy pure-black display text
- do not use SimHei, 700 body weight, or text stroke for normal transcript
  reading; those make small Chinese text feel crowded and tiring
- keep a simple white background and avoid decorative styling
- if the user says the text is too faint, adjust modestly before jumping to
  very bold weights

## Parallel Chunking Guidance

Chunking can help long videos, retries, and multi-machine/multi-GPU workflows,
but it does not automatically make transcription 12x faster on one GPU.
Whisper already processes audio internally in windows, and many parallel
large-v3 jobs on the same GPU will compete for VRAM and compute.

Use chunking when:

- media is long enough that retrying the whole file is painful
- the workflow needs checkpointable partial transcripts
- multiple GPUs or machines are available
- a modest number of chunks can run without saturating VRAM

Recommended local chunking shape:

- split into 5-10 minute chunks
- keep 1-2 seconds of overlap
- transcribe chunks with large-v3
- trim overlap during merge
- preserve timestamps and chunk provenance

For short clips under about 10 minutes, direct large-v3 GPU transcription is
usually simpler and fast enough.

## Trigger Keywords

Use this skill when the user says or implies:

- "视频转文字", "语音转文字", "把视频文字摘录出来"
- "我要能复制", "直接显示出来", "给我文字稿"
- "字体看着累", "字体发虚", "字体太粗", "复制全文按钮"
- "下次都这样处理", "写入技能包", "不要落灰"

## Preflight And Failure Review

Before similar work:

1. Check this skill first.
2. Prefer `ggml-large-v3.bin` for Chinese transcripts that will be copied,
   published, or converted into reusable knowledge.
3. Confirm the final readable HTML opens and the copy button remains visible.
4. If the user complains about readability, compare against Codex chat text:
   moderate system UI font, not over-bold display font.

Failure review entry point:

- `usage-log/` records proven runs and readability lessons.
- For ASR quality failures, compare base/turbo/large-v3 terms before changing
  the workflow.
- For UI readability failures, tune font family, weight, line-height, and color
  in `scripts/export-readable-transcript-html.ps1` first.

## GPU Rule

Prefer GPU when available for large-v3. On 2026-07-06, the CUDA package detected:

```text
NVIDIA GeForce RTX 2080 Ti, 22GB VRAM
```

The standard engine selection remains:

```text
auto -> try GPU if available -> fall back to CPU -> report timing
```

## Acceptance

A run is accepted when:

- output TXT/SRT/JSON exist
- transcript covers the full media duration
- obvious model/download failures are not ignored
- final user-facing transcript is readable Chinese
- uncertain terms are marked or normalized by context
- total runtime and engine choice are reported

## Recent Proven Runs

2026-07-05:

- input: `6593f5b04aefe433128294692c6f4aef.mp4`
- duration: about 5m02s
- CPU base-q8_0 run completed and produced TXT/SRT/JSON
- CPU full run time: about 860 seconds
- GPU CUDA package detected RTX 2080 Ti; short smoke test worked but had high overhead
- lesson: keep GPU available, but choose engine by benchmark, not assumption

2026-07-06:

- input: `11808f2236c3f27e6126d71114892b6b.mp4`
- duration: about 3m10s
- base-q8_0 produced many Chinese homophone errors
- full `ggml-large-v3.bin` was downloaded and verified
- GPU large-v3 run completed in about 53 seconds on RTX 2080 Ti
- large-v3 correctly recognized Chinese technical terms and named entities
- cleaned transcript saved under this thread's outputs folder
- readable HTML was tuned with user feedback: system UI font, 19px, 500 weight,
  soft dark text, no stroke, and a persistent `复制全文` button
- lesson: for user-facing Chinese transcripts that will be copied, reused, or
  converted into skills/SOPs, prefer large-v3 and generate the readable HTML
  output by default
