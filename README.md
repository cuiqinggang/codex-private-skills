# Codex Private Skills Backup

Private backup of personal Codex/Hermes/OpenClaw skill packages collected from H: on 2026-06-05.

## Active shared fact source

This private repository is the shared long-term fact source and working area for the P0 absolute-time project:

- Skill: [absolute-time-fireworks-optimization](skills/absolute-time-fireworks-optimization/SKILL.md)
- Current state: [CURRENT STATE（当前状态）](skills/absolute-time-fireworks-optimization/references/CURRENT-STATE.md)
- Fast path: [FAST PATH（成熟最短路径）](skills/absolute-time-fireworks-optimization/references/FAST-PATH.md)
- Frozen engineering workspace: [P0-EXTREME-MINIMAL-FASTPATH](workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH/README.md)

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

## Layout

- skills/: curated skill packages, one skill per directory.
- docs/source-manifest.csv: source path for every copied skill.
- docs/all-detected-skill-dirs.csv: every H: directory found with a SKILL.md.
- docs/omitted-duplicates.csv: directories skipped because another skill had the same directory name.
- docs/excluded-files.csv: files skipped because they were archives, binaries, generated caches, logs, or larger than 50 MB.

## Backup Policy

- Keep directories that contain SKILL.md.
- Preserve useful process/output materials such as Markdown notes, scripts, JSON/CSV manifests, and image assets.
- Include the v1.5 homework keyframe image package as related output assets.
- Prefer active/custom roots before older backup roots when names duplicate.
- Exclude models, installers, archives, caches, virtual environments, build output, logs, and files over 50 MB.
- No original H: files were deleted during this backup.

