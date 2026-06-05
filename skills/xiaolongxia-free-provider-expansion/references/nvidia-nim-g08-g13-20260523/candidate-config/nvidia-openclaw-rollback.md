# NVIDIA Candidate Provider Rollback

No production config was modified in G10. Rollback is therefore:

1. Do not copy `nvidia-provider-candidate.json` into `C:\Users\A\.openclaw\openclaw.json`.
2. Keep current OpenRouter reduced pool as production.
3. If a future test temporarily applies NVIDIA provider, restore the pre-change `openclaw.json` backup and run `openclaw config validate`.
4. If NVIDIA returns 429/401/403/404, disable NVIDIA candidate route and fall back to current OpenRouter reduced pool.
