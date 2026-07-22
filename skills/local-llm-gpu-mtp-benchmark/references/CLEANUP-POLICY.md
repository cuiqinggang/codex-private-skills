# Cleanup Policy

## Keep

- Verified main model GGUF files.
- Verified backend runtime.
- User-facing reports under `outputs` or Desktop benchmark folders.
- Final ZIP/report packages requested by the user.
- Scripts that reduce repeated work, after moving them into this skill.

## Delete After Recording Reason

- Draft/speculator models that failed or did not improve speed enough.
- Failed fork downloads and partial archives.
- Temporary benchmark scripts and logs after distilled copies are stored in this skill.
- Work folders from this thread that contain only intermediate probes.

## Do Not Delete Without Fresh Confirmation

- User-created reports or manually collected evidence.
- Kilo, Hermes, Open WebUI, Docker, or API-key config.
- Main 14B and 27B model files currently marked keep.
- Desktop benchmark packages unless the user explicitly asks to remove them.

## Windows Safety

Before recursive deletion, resolve the exact absolute path and confirm it is under one of:

${REDACTED_SECRET}
- a known failed model folder
- a known failed tool download folder

Use `Remove-Item -LiteralPath <path> -Recurse -Force` only on verified targets.
