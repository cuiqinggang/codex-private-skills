---
name: github-version-save-profile
description: Use only when the user explicitly asks for a lightweight GitHub version snapshot or names `github-version-save-profile`. For mature project versioning, upgrade, replay, or release workflows, route to `github-version-upgrade-mature-flow`. Requires an existing authenticated GitHub workflow; never read or expose credentials.
---

# GitHub Version Save Profile

## Purpose

Preserve the user's preferred GitHub version-save workflow without storing secrets in plaintext.

## Trigger Phrases

Use this when the user says or implies:

- 保存版本
- 保存到 GitHub / github 上保存
- 建立 GitHub 连接
- 推送这个版本
- 版本归档
- commit / push / PR
- 把当前成果留一版

## Non-Secret Account Context

- GitHub username: cuiqinggang
${REDACTED_PERSONAL_DATA}
${REDACTED_PERSONAL_DATA}

Do not store GitHub passwords, PATs, recovery codes, or 2FA codes in this skill or any report. If authentication is needed, use GitHub CLI, Git Credential Manager, or the GitHub app connector so credentials stay in the system credential store.

## Default Workflow

${REDACTED_SECRET}
2. Run that skill's mature-skill search gate.
3. Confirm the exact target skill package, project folder, or single package directory.
4. Reuse its copied mature GitHub publish workflow unless a better mature workflow is found.
5. Identify the current project folder and confirm it is a git repository.
6. Check whether `origin` points to the intended GitHub repository.
7. Check whether GitHub CLI is installed and authenticated.
8. If authentication is missing, guide the user through `gh auth login` or use the GitHub connector if available.
9. Inspect the current changes before staging.
10. If the tree has unrelated changes, ask which files belong in the version.
11. Create a branch when saving from `main` or `master`, using `codex/<short-description>`.
12. Commit with a short meaningful message.
13. Push to GitHub.
14. Open a draft PR when appropriate, or report the pushed branch/commit when the user only wants a saved version.

## Intended Versioning Pattern

- Publish one target skill package at a time.
- Preserve the pre-upgrade package as a named version snapshot.
- After edits, tests, and verification, publish the upgraded package as the next
  named version.
- Keep tests and acceptance evidence with the corresponding version.
- Do not push all existing skills as part of a single-skill package upgrade.

## Safety Rules

- Never write or repeat plaintext credentials in files, commit messages, logs, reports, or PR bodies.
- Never commit `.env`, credential files, browser profiles, token dumps, or local key stores.
- Never run `git add -A` when unrelated user changes are present.
- Never treat the whole local skills folder as the target unless the user explicitly asks for a full skills-library backup.
- Prefer draft PRs unless the user explicitly asks for ready review.
- If no remote repository exists, ask for the target repository name or create only after explicit confirmation.

## Preflight Command

Before a related complex GitHub-save task, run:

```powershell
${REDACTED_SECRET}
```

## Recent Use Log

- 2026-06-27: Created from user request to remember the GitHub version-save workflow. Secret values were intentionally not persisted.
${REDACTED_SECRET}
- 2026-07-02: Corrected the workflow: future version saves must target one user-provided skill package and version it incrementally, not sync the full local skills library.
