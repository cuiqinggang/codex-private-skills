# P1+P2 Stable Baseline 2026-05-22

Use this reference before adding any new restoration layer after P1+P2.

## Scope

This baseline covers only:

```text
P1: Windows native Hermes 0.14 on 127.0.0.1:8642
P2: Open WebUI on 127.0.0.1:3000
```

It explicitly does not include New API, Postgres, Redis, Telegram, Watchdog, or
AutoRecover.

## Baseline Backup

Stable backup path:

```text
H:\Hermes_Backups\HERMES-014-P1P2-HEALTH-BACKUP-20260522\stable-p1p2-20260522_185206
```

Primary report:

```text
${REDACTED_SECRET}
```

Artifacts:

```text
${REDACTED_SECRET}
```

## Passing Evidence

Required gates passed on 2026-05-22:

- `G02_PASS_HERMES_API_OK`
- `G03_PASS_OPENWEBUI_3000_OK`
- `G04_PASS_FORBIDDEN_SERVICES_NOT_RUNNING`
- `G05_PASS_SYSTEM_SNAPSHOT_CAPTURED`
- `G06_PASS_P1P2_STATE_BACKUP_SAVED`
- `G07_PASS_SKILL_UPDATED_WITH_P1P2_HEALTH_BACKUP`
- `G08_PASS_FINAL_P1P2_HEALTH_BACKUP_REPORT_CREATED`

Observed health:

- `http://127.0.0.1:8642/health` returned HTTP 200.
- `http://127.0.0.1:8642/v1/models` returned HTTP 200 with `hermes-agent`.
- chat returned `HERMES_P1P2_HEALTH_OK`.
- `http://127.0.0.1:3000` returned HTTP 200.
- Open WebUI env pointed to `http://host.docker.internal:8642/v1`.
- Docker showed `open-webui-clean` running.
- New API, Postgres, Redis, Telegram, Watchdog, and AutoRecover were not
  running.

## Rules For The Next Stage

- Do not add Telegram before New API is intentionally restored and verified.
- Do not re-enable Watchdog or AutoRecover before the full live chain is stable.
- Do not call P1+P2 a reboot-persistence baseline; Startup and scheduled task
  recovery are still intentionally disabled.
- If P1+P2 health fails later, restore or compare against the backup path above
  before adding another service.
