---
name: github-version-save-profile
description: Use when the user asks to save a version, connect a project to GitHub, push a local version, create a GitHub version snapshot, or archive a project version for the user's GitHub account.
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
- GitHub login email: cuiqg.us@outlook.com
- Display name: 崔青岗

Do not store GitHub passwords, PATs, recovery codes, or 2FA codes in this skill or any report. If authentication is needed, use GitHub CLI, Git Credential Manager, or the GitHub app connector so credentials stay in the system credential store.

## Default Workflow

1. First use `H:\AI\skills\github-version-upgrade-mature-flow\SKILL.md`.
2. Run that skill's mature-skill search gate.
3. Reuse its copied mature GitHub publish workflow unless a better mature workflow is found.
4. Identify the current project folder and confirm it is a git repository.
5. Check whether `origin` points to the intended GitHub repository.
6. Check whether GitHub CLI is installed and authenticated.
7. If authentication is missing, guide the user through `gh auth login` or use the GitHub connector if available.
8. Inspect the current changes before staging.
9. If the tree has unrelated changes, ask which files belong in the version.
10. Create a branch when saving from `main` or `master`, using `codex/<short-description>`.
11. Commit with a short meaningful message.
12. Push to GitHub.
13. Open a draft PR when appropriate, or report the pushed branch/commit when the user only wants a saved version.

## Safety Rules

- Never write or repeat plaintext credentials in files, commit messages, logs, reports, or PR bodies.
- Never commit `.env`, credential files, browser profiles, token dumps, or local key stores.
- Never run `git add -A` when unrelated user changes are present.
- Prefer draft PRs unless the user explicitly asks for ready review.
- If no remote repository exists, ask for the target repository name or create only after explicit confirmation.

## Preflight Command

Before a related complex GitHub-save task, run:

```powershell
python C:\Users\A\.codex\skills\codex-video-to-usable-skill-loop\scripts\preflight_reuse_check.py "GitHub 保存版本 连接账号 提交 推送 PR 版本归档"
```

## Recent Use Log

- 2026-06-27: Created from user request to remember the GitHub version-save workflow. Secret values were intentionally not persisted.
- 2026-06-27: Bound future version-save requests to `H:\AI\skills\github-version-upgrade-mature-flow`, which first searches mature skills and then reuses the copied GitHub publish workflow.
