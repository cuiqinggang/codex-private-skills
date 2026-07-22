---
name: new-api-local-deploy
description: Use when deploying, repairing, updating, documenting, or verifying the user's local self-use New API gateway on this Windows machine with Docker Compose, PostgreSQL, Redis, localhost-only access, token setup guidance, port separation from Hermes/Open WebUI, or Hermes/Open WebUI no-answer chain failures.
---

# New API Local Deploy

## Purpose

Use this skill for the user's first-phase New API setup: personal computer, local self-use, Docker Compose, PostgreSQL, Redis, no public exposure, and no extra platform components.

Always read `references/local-layout.md` before changing the deployment or answering from this skill.

For reboot/login persistence checks, "are New API, Hermes, Telegram connected"
questions, or skill hardening after a restart, read
`references/reboot-chain-verification.md` before reporting success.

When Hermes, Open WebUI, or the digital assistant is running but does not answer, read `references/hermes-openwebui-chain.md` before changing Open WebUI, Hermes, or New API configuration. If New API `3001` and Open WebUI `3000` are healthy but Hermes `8642` is `NOT_LISTENING`, use that reference's fast recovery pattern before any database edit. If Hermes `8642` is healthy but Docker/New API/Open WebUI are down, use the same reference's Docker/New API down recovery pattern.

## Boundary With AI Token Business

This skill is only the local New API implementation layer. It does not decide the AI token business model, low-buy/high-sell route, customer packages, provider terms, or resale strategy. Use `ai-token-business` for those questions.

Keep the routes separate:

- New API route: local self-use gateway, health, ports, Docker, setup, tokens, channels.
- AI token business route: public research, BYOK/gateway strategy, packages, cost control, risk redlines.

Do not turn this local deployment into a public or commercial service unless the user explicitly approves a separate production plan.

## Fixed Decisions

- Keep Hermes/Open WebUI on `localhost:3000`.
- Keep New API on `http://localhost:3001` and API Base `http://localhost:3001/v1` unless the user explicitly changes the port plan.
- When the user asks to view the New API server, open it in real Google Chrome, not the Codex in-app browser. The in-app browser is acceptable only for background verification.
${REDACTED_SECRET}
- Bind New API only to `127.0.0.1:3001:3000`.
- Do not expose PostgreSQL or Redis host ports.
- Hermes reads New API through `http://127.0.0.1:3001/v1`; Open WebUI reads Hermes through `http://host.docker.internal:8642/v1`.
- Treat old Open WebUI worker endpoints `http://host.docker.internal:18641-18644/v1` as stale unless those workers are explicitly running and freshly verified.
- Model routing rule: complex work must use `deepseek-v4-pro`; `deepseek-v4-flash` is only for explicit cheap, fast, low-risk, simple turns.
- Do not deploy Dify, APISIX, Keycloak, n8n, Cloudflare Tunnel, public domains, payment systems, or multi-tenant sales features in phase one.
- Never print or upload `.env` secrets.

## Long-Term Update Watch

New API is already deployed locally, so future work is mostly update awareness and safe change planning. When the user asks to keep New API updated, or when system-evolution finds important New API information:

1. Search public New API sources: Docker Hub `calciumion/new-api`, GitHub `QuantumNous/new-api`, official docs, Docker Compose examples, issues, releases/actions, and security notes.
2. Classify findings:
   - **Notify now**: security issue, breaking migration, database/env change, image/tag risk, data-loss risk, auth/token/quota behavior change.
   - **Plan only**: useful feature, channel support, billing/quota/token improvement, UI/admin change, docs improvement.
   - **Observe**: minor UI change, non-local deployment feature, public/multi-tenant feature not needed for phase one.
3. Default action is report-only. Do not pull images, restart containers, edit compose, read `.env`, create tokens, add channels, or call upstream APIs unless explicitly approved.
4. For any proposed update, generate a gated plan first: backup, current image/version, compose diff, rollback, health checks, and stop conditions.

Important local baseline to preserve:

- `http://localhost:3001`
- `http://localhost:3001/v1`
- `127.0.0.1:3001:3000`
- Hermes/Open WebUI chain: Open WebUI `3000` -> Hermes `8642` -> New API `3001/v1`.
- Model routing: complex/exploratory tasks must route to `deepseek-v4-pro`, not Flash.
- PostgreSQL and Redis with no host port exposure.
- No public domain, tunnel, payment, or multi-tenant sales feature in phase one.

Login auto recovery is installed for reboot/login repair. Read
`references/local-layout.md` before changing
${REDACTED_SECRET}
the startup fallback, or scheduled task `HermesNewApiAutoRecover_Logon`.
Use `references/reboot-chain-verification.md` for the current reboot/login
verification gates and 2026-05-22 evidence.

## Workflow

1. Check Windows, Docker daemon, `docker compose`, and the chosen host port.
${REDACTED_SECRET}
3. Generate 32-byte or stronger random local secrets for PostgreSQL, Redis, session, and crypto keys.
${REDACTED_SECRET}

```powershell
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
```

5. Verify:

- `new-api`, `new-api-postgres`, and `new-api-redis` are running.
- `new-api` is healthy or has logs showing the app started.
- `http://localhost:3001/setup` or `http://localhost:3001` opens the New API setup/login page.
- `docker port new-api` maps only `3000/tcp -> 127.0.0.1:3001`.
- `docker port new-api-postgres` and `docker port new-api-redis` return no host mappings.

For Hermes/Open WebUI no-answer failures, use `references/hermes-openwebui-chain.md`: prove each layer with direct HTTP calls, then back up Open WebUI's `webui.db` before removing stale API bases or restarting `open-webui-clean`.

For Hermes model routing or "cheap model handled a complex task" failures, use `references/model-routing-policy.md`: inspect the Hermes default model, the Telegram router plugin, and New API logs before changing routing.

## Local Balance Interpretation

If the dashboard shows a starting balance such as `$200.00`, explain that it is New API's internal local quota display, not a real recharge, not upstream provider credit, and not a minimum payment requirement.

The known first deployment showed:

```text
users.quota = 100000000
users.used_quota = 0
users.request_count = 0
top_ups rows = 0
dashboard balance = $200.00
```

Treat this as internal gateway accounting for local limits, token consumption, and statistics. Real spending happens at the upstream provider tied to the user's API key, such as OpenAI, Claude, Gemini, DeepSeek, or Qwen.

## Update And Sync Rule

${REDACTED_SECRET}

## User Handoff

After deployment, tell the user:

- Open `http://localhost:3001` in Google Chrome.
- Create the administrator account.
- Enter the backend.
- If New API exposes a server address setting, set it to `http://localhost:3001`.
- Add upstream channels such as OpenAI, Claude, Gemini, DeepSeek, or Qwen.
- Create a New API token.
- Configure clients with `API Base: http://localhost:3001/v1` and the New API token.

