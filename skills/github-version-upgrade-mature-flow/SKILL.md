---
name: github-version-upgrade-mature-flow
description: Use when the user asks to publish a new version, save a version to GitHub, upgrade a project version, connect a project to GitHub, or create a durable version snapshot.
---

# GitHub Version Upgrade Mature Flow

## Purpose

This is the user's fixed version-upgrade method: search mature skill packages first, copy and reuse the best mature workflow, then publish/save the version through GitHub.

## Trigger Phrases

Use this skill when the user says or implies:

- 发布新版本
- 保存版本
- 版本升级
- 保存到 GitHub
- 推送这个版本
- 建立 GitHub 连接
- 复制成熟方案使用
- 先搜索成熟技能包

## Mature Source Adopted

Primary copied mature workflow:

- `H:\AI\skills\github-version-upgrade-mature-flow\UPSTREAM-GITHUB-YEET-SKILL.md`

Source copied from:

- `C:\Users\A\.codex\plugins\cache\openai-curated-remote\github\0.1.5\skills\yeet\SKILL.md`

Adoption decision:

- Route: `ADOPT_DIRECTLY`
- Reason: the upstream GitHub publish workflow already covers scope inspection, branch strategy, staging, commit, validation, push, and draft PR creation.

## Required Start Gate

Before version-upgrade work, run the reuse search:

```powershell
python C:\Users\A\.codex\skills\codex-video-to-usable-skill-loop\scripts\preflight_reuse_check.py "版本升级 发布新版本 GitHub 保存版本 成熟方案 复制技能包 使用"
```

Then read:

1. This `SKILL.md`.
2. `UPSTREAM-GITHUB-YEET-SKILL.md`.
3. `H:\AI\skills\github-version-save-profile\SKILL.md` when account/profile context is needed.

## Default Execution Method

1. Search mature skills and workflows first.
2. Prefer an already proven local skill package over creating a new process.
3. If a better mature source is found, copy it into this package with a source note and adoption decision.
4. Inspect the project folder and identify whether it is a git repository.
5. Check remote GitHub connection.
6. Check GitHub authentication through the connector, GitHub CLI, or system credential manager.
7. Inspect local changes before staging.
8. Stage only intended files.
9. Commit with a clear version message.
10. Push to GitHub.
11. Open a draft PR when appropriate, or report the pushed commit/branch if the user only needs a saved version.

## Safety Rules

- Do not store plaintext passwords, PATs, recovery codes, one-time codes, or other secrets.
- Do not commit secrets, local credential stores, `.env` files, token dumps, browser profiles, or unrelated user files.
- Do not silently stage unrelated changes.
- If the repository has no GitHub remote, ask for the target repository name before creating or pushing.
- If authentication is missing, use GitHub CLI login or the GitHub connector rather than writing credentials into files.

## Reuse Decision Ladder

Use this order:

1. `ADOPT_DIRECTLY`: copy and use the mature package as-is.
2. `ADAPT_LIGHTLY`: copy and make small local adjustments.
3. `TRY_LIGHTLY`: test the mature path without making it the default yet.
4. `REFERENCE_ONLY`: read it for ideas only.
5. `BUILD_FROM_SCRATCH`: only when no mature workflow fits.

## Recent Use Log

- 2026-06-27: Created as the user's fixed version-upgrade method. Copied the mature GitHub publish workflow into this package and set it as `ADOPT_DIRECTLY`.
