---
name: gpt-silver-to-premium-gold-video
description: Use when Codex needs to convert silver metal in a video or keyframe sequence into restrained premium gold using GPT-generated image keyframes, while preserving the original scene, camera, shadows, reflections, object positions, and timing. Trigger on requests like silver to gold, 高级金, 金属改色, GPT做图, keyframe image package, Gate04/Gate05/Gate06, video transition test, or user asks to package frames for GPT instead of local recolor.
---

# GPT Silver To Premium Gold Video

## Core Rule

Use GPT for visual generation. Codex must not locally recolor gold, redraw objects, Blender rerender, or silently redesign the scene unless the user explicitly asks.

Codex owns the pipeline around GPT:

1. Extract keyframes.
2. Package original frames, style references, and simple prompts for GPT.
3. Receive GPT outputs.
4. Archive outputs by frame number.
5. Generate contact sheets and reports.
6. Normalize dimensions only when needed.
7. Build preview videos for transition review.
8. Identify only the intervals that need more keyframes.

## Visual Prompt Pattern

Keep prompts simple. Avoid broad mask wording that makes GPT change the wrong regions.

Use this Chinese prompt pattern:

```text
把图中的银色金属材质改成和参考图一致的“稍亮但仍克制的高级金”，其他所有内容保持原样。

只改银色金属部分。
不要改构图、背景、桌面、键盘、显示器、屏幕文字、阴影、反射关系、物体形状、位置和线条结构。
不要重新生成整张图。
不要做拼图。
不要做 A/B/C 多版本。

金色要求：高级、真实、有金属反射；稍亮，但仍然克制；不要土黄、塑料黄、脏金、过曝金。
每张图片单独生成一个最终 gold 版本。
```

## Gate Workflow

### Gate04 - GPT Keyframe Production

1. Extract representative original frames from the source video.
2. Split large batches into small GPT packages, usually 6 images per package.
3. Include a locked style reference such as `gold_style_C_locked.png`.
4. Include accepted examples when available.
5. Ask GPT to process each image independently.
6. After user/GPT returns images, archive them as `frame_XXX_gold_gpt.png`.
7. Generate contact sheets and a Chinese review report.

Pass condition: gold style is consistent, premium, not too yellow, and environment elements are not obviously changed.

### Gate05 - Dimension Normalize And Transition Preview

Use after enough GPT keyframes pass.

1. Archive all accepted gold frames in frame order.
2. Normalize to original video size if GPT output dimensions differ but aspect ratio matches.
3. Do not crop unless explicitly requested.
4. Generate a normalized contact sheet.
5. Generate preview videos:
   - hardcut flip-through
   - timing-hold preview at original FPS
6. Report missing frames, aspect errors, and whether transition testing may continue.

Pass condition: all frames exist, dimensions match the original video, and no aspect mismatch blocks video preview.

### Gate06 - Segment Assembly Test

Use after Gate05 passes.

1. Build a timing-hold baseline video from normalized keyframes.
2. Build a crossfade reference video if simple.
3. Do not call the result a final publish video.
4. Sample frames from assembled videos into contact sheets.
5. Report video dimensions, FPS, frame count, codec, and likely jump intervals.

Pass condition: preview videos are created and obvious jumps are either acceptable or localized to specific intervals.

## Current Project State To Reuse

For the 2026-06-20 silver-to-premium-gold task:

- Source video: `C:\Users\A\Documents\xwechat_files\wxid_bq3n41o6t4o721_699b\msg\video\2026-06\55b8afced91c76b1c12f627d8cbc9f75.mp4`
- Original video size: `1080x1260`
- Original FPS: `29.97`
- Locked style: `稍亮但仍克制的高级金`
- Gate04 status: `Round1 ACCEPTED`, `Round2A PASS`, `Round2B PASS`, `Round2C PASS`
- Gate05 status: `PASS_READY_FOR_VIDEO_ASSEMBLY_TEST`
- Gate05 output: `C:\Users\A\Documents\Codex\2026-06-15\files-mentioned-by-the-user-codex\outputs\silver_to_gold_v1\gate05_video_transition_test`
- Desktop packages:
  - `C:\Users\A\Desktop\456.zip`: 25-frame archive package
  - `C:\Users\A\Desktop\123.zip`: Gate05 normalized frames, previews, and reports

Read `references/progress-log.md` before continuing this exact task.

## Bundled Scripts

- `scripts/build_round2_package.py`: create remaining-frame GPT input packages.
- `scripts/archive_25_gold_keyframes.py`: archive accepted 25 GPT gold keyframes and contact sheets.
- `scripts/gate05_transition_test.py`: normalize keyframes and generate transition preview videos.

Scripts may contain project-specific paths. Before reusing on a new project, patch the paths and frame list.

## Reporting Rule

Every gate must write:

1. Output paths.
2. Contact sheet path.
3. Chinese report path.
4. JSON metrics path when possible.
5. Status in a single explicit token, such as `PASS`, `PARTIAL`, or `BLOCKED`.
6. Next action, preferably only one step.

Also append the progress to `references/progress-log.md` when this skill is being used for a live task.
