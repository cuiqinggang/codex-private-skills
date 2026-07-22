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

${REDACTED_SECRET}

Source copied from:

${REDACTED_SECRET}

Adoption decision:

- Route: `ADOPT_DIRECTLY`
- Reason: the upstream GitHub publish workflow already covers scope inspection, branch strategy, staging, commit, validation, push, and draft PR creation.

## Required Start Gate

Before version-upgrade work, run the reuse search:

```powershell
${REDACTED_SECRET}
```

Then read:

1. This `SKILL.md`.
2. `UPSTREAM-GITHUB-YEET-SKILL.md`.
${REDACTED_SECRET}

## Default Execution Method

1. Search mature skills and workflows first.
2. Confirm the exact target package, project folder, or single skill directory to version.
3. Prefer an already proven local skill package over creating a new process.
4. If a better mature source is found, copy it into this package with a source note and adoption decision.
5. Inspect the project folder and identify whether it is a git repository.
6. Check remote GitHub connection.
7. Check GitHub authentication through the connector, GitHub CLI, or system credential manager.
8. Inspect local changes before staging.
9. Stage only intended files.
10. Commit with a clear version message.
11. Push to GitHub.
12. Open a draft PR when appropriate, or report the pushed commit/branch if the user only needs a saved version.

## Single Skill Package Versioning Rule

2026-07-02 correction: when the user says a skill package will be made or upgraded,
do not sync or publish the entire local skills library. The intended workflow is
single-package versioning:

1. Wait until the user provides or points to the target skill package.
2. Treat the original package as one version snapshot.
3. After the user provides modifications or asks for an upgrade, create the next
   named version snapshot for that same package.
4. Include tests, verification evidence, and acceptance notes inside the matching
   version snapshot or release branch.
5. Push only the target package and its version/test artifacts.
${REDACTED_SECRET}
   explicitly asks for a full skills-library backup.

Failure review entry:

- 2026-07-01: Misread "publish the skill package version" as "sync all existing
  skills." A draft PR was closed and its remote branch was deleted. Future runs
  must ask/confirm the exact target package before publishing.

## Safety Rules

- Do not store plaintext passwords, PATs, recovery codes, one-time codes, or other secrets.
- Do not commit secrets, local credential stores, `.env` files, token dumps, browser profiles, or unrelated user files.
- Do not silently stage unrelated changes.
- Do not publish the whole local skills library when the task is about one skill package version.
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
- 2026-07-02: Added correction that version upgrades are for one target skill package at a time; full skills-library sync is only allowed when explicitly requested.
