# Safe Install And Capability Check

Core principle:

Check first, then use. Read first, then write. Validate locally first, then go online. Report first, then request authorization.

## Checklist

1. Check whether the current Codex App session exposes a plugin, skill, connector, CLI, or local fallback for the required capability.
2. List already available capabilities before suggesting installation.
3. For each candidate capability, record:
   - installed or unavailable
   - connected or not connected
   - login required or not
   - extra permissions required
   - read-only test possible or not
   - local verification possible or not
4. Do not install all plugins from a tutorial or video in one batch.
5. For GitHub, Supabase, Vercel, Figma, Gmail, Drive, and other external services, start with read-only or local planning.
6. If a task involves account access, tokens, cloud writes, deployment, PR creation, issue comments, database changes, or auth policy changes, request explicit user authorization.
7. If a plugin is unavailable, continue with the closest safe local workflow and document the limitation.

## Authorization Boundary

Allowed without extra authorization:

- creating local plans and documents
- creating local demo files
- running local tests
- reading local project files
- producing visual acceptance pages

Requires separate authorization:

- installing a new plugin
- connecting an external account
- using secrets or tokens
- pushing to GitHub
- opening or editing PRs/issues
- deploying to public hosting
- connecting or changing a database
- changing auth, RLS, billing, or production settings
