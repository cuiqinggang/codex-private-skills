# Safety Boundaries

Stop and ask before:

- API keys, cookies, tokens, passwords, or secrets,
- account login, captcha, account/security prompts,
- payment, billing, or subscription changes,
- production configuration,
- global Codex/Hermes/Cursor/Claude Code settings,
- long-lived background services or scheduled tasks,
- destructive deletes or large batch rewrites,
- remote write permissions,
- unclear repeated failures,
- changing success criteria.

Allowed with logging:

- read-only local inspection,
- public web research,
- local report generation,
- low-risk template/script creation in the workspace,
- deterministic validation commands.

Do not treat skipped risky work as PASS. Record it as blocked, needs approval, or out of scope.
