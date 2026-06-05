# Rollback

No production config is changed by this dry-run.

If this candidate route is later promoted and causes trouble:

1. Remove the candidate provider entry from OpenClaw config.
2. Remove any route selection pointing to `nvidia-nim-dryrun`.
3. Keep Xiaolongxia on the current 3011 OpenRouter production pool.
4. Do not connect real group chat until smoke tests pass again.
