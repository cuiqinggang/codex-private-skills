# G00 New API Start And Login Baseline - 2026-05-24

## Status

`G00_NEWAPI_START_AND_LOGIN_PASS`

Required marker:

`3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`

## Meaning

- `http://127.0.0.1:3011` is New API / model-pool management.
- `http://127.0.0.1:3011/v1` is the New API API base.
- `3011` is not Xiaolongxia product UI.
- OpenClaw/Xiaolongxia UI must be verified separately, such as OpenClaw gateway/browser on `18789`.

## Current Login Baseline

- Login URL: `http://127.0.0.1:3011/login`
- Console URL: `http://127.0.0.1:3011/console`
- Admin username: `xya6338`
- Admin credential file: `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`

Do not print the password from the credential file in chat, reports, skills, logs, or screenshots.

## What Was Done

1. Confirmed `3011` was listening.
2. Confirmed HTTP `200` and page title `New API`.
3. Tried the previously remembered `xya6338` login and observed the page error "用户名或密码错误，或用户已被封禁".
4. Inspected the database and found the 3011 instance had existing users including an old admin `xllxadmin`.
5. Took a PostgreSQL custom-format backup before changing login state.
6. Created/reset `xya6338` as an administrator for this 3011 New API instance.
7. Stored the new password only in the local credential file.
8. Logged into New API successfully as `xya6338`.
9. Read-only confirmed Dashboard, Channels, Models, Tokens, and Settings pages.
10. Left production channels, models, tokens, groups, routing, Docker Compose, and `.env` unchanged.

## Service Baseline

- Container: `xiaolongxia-new-api`
- Image: `calciumion/new-api:latest`
- Port mapping: `127.0.0.1:3011 -> 3000/tcp`
- PostgreSQL: `xiaolongxia-postgres`
- Redis: `xiaolongxia-redis`

## Backend Readonly Confirmation

Confirmed pages:

- Dashboard: `http://127.0.0.1:3011/console`
- Channels: `http://127.0.0.1:3011/console/channel`
- Models: `http://127.0.0.1:3011/console/models`
- Tokens: `http://127.0.0.1:3011/console/token`
- Settings: `http://127.0.0.1:3011/console/setting?tab=operation`

Confirmed channel page fields:

- Channel: `openrouter-free`
- Group: `xiaolongxia-free-pool`
- Type: `OpenRouter`
- Status: enabled

## Evidence

Evidence root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-G00-NEWAPI-START-LOGIN-20260524`

Key files:

- `final-report.md`
- `G00-port-http-precheck.md`
- `G00-port-http-precheck.json`
- `G00-db-backup-before-admin-reset.json`
- `G00-admin-account-created-redacted.json`
- `G00-newapi-login-success.png`
- `G00-newapi-login-success.txt`
- `G00-console-route-probe.json`
- `G00-newapi-current-channel-page.png`
- `G00-newapi-current-channel-page.txt`

Database backup before admin reset:

- File: `xiaolongxia-newapi-before-admin-reset-20260524-033858.dump`
- SHA256: `818762B6290AA3F029D58BCC937205C4191D406A69AC48DC587F070AB01F3D0E`

## Future Use

Any later Xiaolongxia/OpenClaw/browser/autostart task must first either:

1. Reuse this baseline if it is still current and explicitly acceptable for the task, or
2. Rerun G00 and save new evidence.

If New API cannot open, cannot login, or cannot show a backend page, stop with:

`STOP_NEWAPI_LOGIN_NOT_CONFIRMED`
