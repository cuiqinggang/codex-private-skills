# 2026-07-06 Large-v3 Readable Transcript Run

## Material Value

HIGH_VALUE.

Reasons:

- User explicitly said this was a good result and asked to write it into a
  skill package for next time.
- The run improved repeated video-to-text work: better ASR model, cleaner
  transcript delivery, readable HTML, and one-click copy.
- The outcome creates reusable rules, workflow steps, template CSS, and a
  script.

## Source

- Input video: `11808f2236c3f27e6126d71114892b6b.mp4`
- Topic: Codex prompting tips, first-principles thinking, adversarial review
${REDACTED_SECRET}

## Lessons Deployed

1. Prefer `ggml-large-v3.bin` for Chinese user-facing transcripts that will be
   copied, reused, or converted into skills/SOPs.
2. Keep only the final large-v3 model after segmented download succeeds; delete
   partial turbo/base models and segment folders to avoid duplicated GB usage.
3. Generate `readable-transcript.html` in addition to TXT/SRT/JSON.
4. Preserve a visible `复制全文` button.
5. Match Codex chat readability: system UI fonts, about 19px, weight 500,
   line-height about 1.9, soft dark text, no SimHei body text, no 700 body
   weight, and no text stroke.
6. Do not expect 12-way local chunking to be 12x faster on one GPU. Use chunking
   mostly for long-video retryability or multi-GPU/multi-machine distribution.

## Trigger Phrases

- 视频转文字
- 语音转文字
- 把视频内容摘录出来
- 我要能复制
- 字体看着累 / 发虚 / 太粗
- 复制全文按钮
- 下次都这样处理

## Verification

- Full large-v3 model verified by SHA1 and SHA256.
- GPU large-v3 run on RTX 2080 Ti completed a 3m10s video in about 53 seconds.
- User confirmed the final font felt comfortable.
- Skill now includes `scripts/export-readable-transcript-html.ps1`.

## Next-Run Instruction

For similar tasks, run the video transcription skill first, use large-v3, clean
obvious ASR errors, then generate or regenerate readable HTML from the cleaned
transcript. Keep the copy button and Codex-like readable font settings.
