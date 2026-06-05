# Current Layout

Last verified: 2026-05-23

## Service

- Directory: `C:\Users\A\xiaolongxia-free-api-local`
- UI: `http://localhost:3011`
- API Base: `http://localhost:3011/v1`
- Compose file: `C:\Users\A\xiaolongxia-free-api-local\docker-compose.yml`
- README: `C:\Users\A\xiaolongxia-free-api-local\README_LOCAL.md`

## Containers

- `xiaolongxia-new-api`
- `xiaolongxia-postgres`
- `xiaolongxia-redis`

## Routing

This pool is isolated from Hermes.

- Do not connect to `localhost:3000`.
- Do not connect to Hermes `8642`.
- Do not reuse old New API `localhost:3001`.

## Current Verified Models

- `liquid/lfm-2.5-1.2b-instruct:free`
- `baidu/cobuddy:free`
- `google/gemma-4-31b-it:free`
- `openai/gpt-oss-120b:free`

Verification target reply:

```text
小龙虾测试成功。
```

Latest test reports:

- `C:\Users\A\xiaolongxia-free-api-local\reports\free-model-test-20260523-183952.md`
- `C:\Users\A\xiaolongxia-free-api-local\reports\free-model-test-expanded-20260523-190442.md`
- `C:\Users\A\xiaolongxia-free-api-local\reports\xiaolongxia-call-simulation-20260523-190745.md`
- `C:\Users\A\xiaolongxia-free-api-local\reports\model-count-diff-20260523-185736.md`
- `C:\Users\A\xiaolongxia-free-api-local\data\free-models-current.md`

Operational files:

- `C:\Users\A\xiaolongxia-free-api-local\scripts\update-free-model-pool.ps1`
- `C:\Users\A\xiaolongxia-free-api-local\scripts\test-free-models.ps1`
- `C:\Users\A\xiaolongxia-free-api-local\scripts\test-free-models-expanded.ps1`
- `C:\Users\A\xiaolongxia-free-api-local\scripts\simulate-xiaolongxia-chat-call.ps1`
- `C:\Users\A\xiaolongxia-free-api-local\config\xiaolongxia-free-routing-policy.md`
- `C:\Users\A\xiaolongxia-free-api-local\config\xiaolongxia-rate-limit-policy.md`

## Report

Current build report:

`C:\Users\A\Desktop\1\output\TASK-NEWAPI-FREE-MODEL-POOL-REBUILD-20260523\report.md`
