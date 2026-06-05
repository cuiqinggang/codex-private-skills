---
name: ai-learning-material-pack
description: "Use when creating, updating, verifying, or packaging the user's free AI学习资料包: a WeChat-sendable Chinese AI learning material pack with video-first links, text backups, beginner/intermediate/advanced levels, discussion summary, update plan, and H-drive backup."
---

# AI学习资料包

Use this skill when the user asks to create, update, verify, package, or continue improving the free **AI学习资料包**.

## Core Positioning

Keep the public name exactly:

```text
AI学习资料包
```

This is a free learning material pack, not a paid course, training class, website, or server project.

The first version is a lightweight document that can be sent directly through WeChat. Its body is curated learning links, not a newly written long tutorial.

Use a conversational Chinese style: simple, direct, easy to understand, and a little urgent. Do not write like a formal manual.

## Non-Negotiable Rules

- Do not rename it to "链接型教材", "导航包", "入口包", or similar technical wording.
- Do not mention Telegram, 电报, or platform-sensitive implementation details.
- Do not write "付费咨询".
- For complex human help, use soft wording like: `请老师喝杯奶茶表示感谢`.
- Put video links before text links.
- For each learning point, try to provide at least 2 video links and 2 text links.
- Prefer links that are public, mature, Chinese-friendly, and easy for ordinary users.
- Keep the pack lightweight. Do not turn it into a long original course.
- Keep the update path simple: replace failed links, add better videos, remove low-quality resources.

## Required Public Opening

Use this idea, keeping it short:

```text
现在 AI 已经不是加分项，是基本能力。
你不会用 AI，别人会用 AI，最后被淘汰的一定是你。
现在被裁掉、被替代的人，很多不是不努力，而是不会用 AI。
```

## Learning Levels

Use three levels:

1. **初级**: 小学生、初中生、零基础成年人。认识 AI、简单提问、学习辅助、查资料、写简单内容。
2. **中级**: 已经会一点 AI 的人。写作、总结、办公、PPT、表格、图片、音频、视频、学习计划、效率提升。
3. **高级**: 学生、商家、个体户、企业主、想解决实际问题的人。学习提升、文案、获客、短视频、经营分析、客户沟通、方案制定、智能体和自动化。

## Workflow

1. Load [discussion-summary.md](references/discussion-summary.md) to preserve the user's confirmed positioning.
2. Load [wechat-pack.md](references/wechat-pack.md) when creating or updating the public WeChat-sendable document.
3. Load [update-and-verification.md](references/update-and-verification.md) before checking links or publishing a refreshed version.
4. Search the web when links may be stale. Prefer official docs, stable open-source tutorials, mature public videos, and Chinese-friendly resources.
5. Update the WeChat document first, then mirror changes into this skill's references.
6. Save a copy under `H:\Hermes_Skills\AI学习资料包` when the user asks for H-drive backup.
7. Verify with the skill validator and a basic link extraction/check where feasible.

## Output Files

For a normal refresh, produce or update:

- `AI学习资料包.md`
- `讨论总结和后续计划.md`
- `链接验证记录.md`
- `codex_plan.md` when an execution plan is needed
- Skill references under `references/`
- H-drive backup under `H:\Hermes_Skills\AI学习资料包`

## Verification

Validate the skill:

```powershell
python "C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\A\.codex\skills\ai-learning-material-pack"
```

Check generated files exist:

```powershell
Test-Path "C:\Users\A\.codex\skills\ai-learning-material-pack\SKILL.md"
Test-Path "C:\Users\A\.codex\skills\ai-learning-material-pack\references\wechat-pack.md"
Test-Path "H:\Hermes_Skills\AI学习资料包"
```

If link checks fail because a platform blocks automated requests, record the failure in `链接验证记录.md` and use manual browser verification or user feedback before deleting the link.
