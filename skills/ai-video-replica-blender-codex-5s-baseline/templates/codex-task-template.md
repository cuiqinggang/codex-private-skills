# Codex Task Template: Blender 5 Second Replica

## Objective

Create a 5 second minimum Blender replica from the reference video. Do not attempt the full source duration in the first pass.

## Workspace

Use a new isolated workspace:

```text
H:\AI\workspaces\<TASK_NAME>
```

## Boundaries

- Use official Blender only.
- Do not install large AI video models.
- Do not start ComfyUI/Wan.
- Do not touch API keys, Hermes, Open WebUI, Xiaolongxia, or New API.
- Do not modify old skill packages.

## Gates

1. G01: environment check.
2. G01B: prepare official Blender if missing.
3. G01C: write `config/blender-path.json`.
4. G02: scene design.
5. G03: Blender Python script.
6. G04: generate `.blend`.
7. G05: render frames and MP4.
8. G06: automatic verification.
9. G07: preview frames and visual check.
10. G08: save skill package or runbook update.
11. G09: final report.

## PASS Code

```text
AI_VIDEO_REPLICA_BLENDER_CODEX_5S_VERIFY_PASS
```
