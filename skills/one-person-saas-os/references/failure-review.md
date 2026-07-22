# Failure Review Entry Point

Use this file after any failed generation, install, build, or deployment.

## Capture

- Date:
- Request:
- Project path:
- Command that failed:
- Error summary:
- Missing env vars:
- Files changed:

## Classify

- Generator bug
- Dependency or package version drift
- Clerk integration issue
- Supabase key or client issue
- PostHog browser/client issue
- Vercel env/deploy issue
- HTTPS/custom-domain issue
- Mobile layout or tap-target issue
- Payment provider approval or payment fallback issue
- Backup/recovery gap
- Legal/trust page gap
- User-supplied product requirement outside v1

## Fix Rule

If the same failure can recur, update one of:

- `SKILL.md`
- `scripts/create_one_person_saas_os.py`
- `references/deployment-checklist.md`
- `references/v1-contract.md`
- `references/indie-site-risk-gates-video-20260706.md`
- `references/prelaunch-risk-gate-checklist-20260706.md`

Append the fix to `references/recent-use-log.md`.
