---
name: video-editor-feature-distillation
description: Use when the user asks to evaluate Jianying/CapCut, Shotcut, Kdenlive, or other video editors, find free/open-source alternatives, test which video editing features can be used directly, distill paid or GUI-only video editor capabilities into FFmpeg/Whisper/Auto-Editor/PySceneDetect/Remotion workflows, or create reusable video editing skills from software feature research.
---

# Video Editor Feature Distillation

## Purpose

Use this skill to turn mature video editor capabilities into the user's own
reusable Codex workflows. Do not recreate an installed editor when direct use is
better. Distill only the parts that are paid, unstable, hard to automate, or
better handled by scripts.

## Decision Rule

Route every feature into one of four buckets:

```text
direct-use       -> use installed editor as a tool
script-distill   -> implement with FFmpeg / Whisper / Python / PowerShell
hybrid           -> script first, GUI for final manual polish
do-not-copy      -> proprietary, licensed, account-risk, or unclear rights
```

## Default Tool Order

```text
FFmpeg/ffprobe
> local video-audio-transcription skill / whisper.cpp
> Auto-Editor / PySceneDetect / Python scripts
> Remotion templates
> Shotcut / Kdenlive GUI
> Jianying/CapCut as product reference or manual tool
```

## When To Read References

- Read `references/FEATURE-MAP.md` before mapping Jianying/CapCut features to
  free/open-source alternatives.
- Read `references/TEST-MATRIX.md` before doing a software evaluation run.
- Read `references/DISTILLATION-RUNBOOK.md` before creating or updating scripts
  from editor features.

## Standard Workflow

1. Check installed editors and CLI tools.
2. Create or locate small representative test assets.
3. Test direct-use ability: launchable app, import/export support, obvious free
   vs paid gates, and whether automation is practical.
4. Map each useful editor feature to a free/open-source route.
5. Distill script-friendly features first.
6. Keep GUI editors only for timeline polish, preview, or manual template work.
7. Produce an evidence report with:
   - installed versions
   - tested features
   - direct-use vs distilled decisions
   - missing tools
   - next scripts to add

Run the local scanner:

```powershell
${REDACTED_SECRET}
```

## Boundaries

- Do not crack, bypass payment, copy proprietary code, copy paid templates, or
  scrape private assets.
- Do not claim a GUI feature is automated unless it was actually tested or has a
  stable CLI/project-file route.
- Do not install third-party repacks or unofficial "VIP unlocked" packages.
- If a free/open-source app works well directly, use it directly and only save a
  small adapter rule.

## Acceptance

A distillation is accepted only when it includes:

- feature name and source editor
- decision bucket
- free/open-source replacement
- command/script route when applicable
- compatibility/export checks
- preview frame or contact sheet for rendered video outputs
- caveats and when to fall back to GUI

