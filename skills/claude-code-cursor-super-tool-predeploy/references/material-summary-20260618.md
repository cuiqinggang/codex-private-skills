# Material Summary 2026-06-18

Source:

${REDACTED_SECRET}

Archived copy:

`H:\AI\inbox\codex-learning-materials\01-new\claude-code-cursor-super-tool-predeploy-v4-20260618.md`

## Value Judgment

Status: `HIGH_VALUE`

Reasons:

- It prevents a repeated high-risk mistake: treating an existing Cursor + Claude Code skeleton as if it should be deleted and rebuilt from zero.
- It gives a staged SOP: collect information, analyze blockers, eliminate blockers, then deploy.
- It defines concrete reports, task names, acceptance outputs, and safety boundaries.
- It can become triggers, checklists, scripts, and AGENTS.md guidance for future similar work.
- It touches long-term systems: skills, hooks, subagents, CCR, OpenRouter, DeepSeek, Codex, Hermes, and GPT collaboration.

## Core Lesson

The correct start state is not "install Claude Code from scratch".

The correct start state is:

`Cursor already has a partial Claude Code skeleton; preserve what works, inspect what exists, remove blockers, and upgrade it into a mature integrated toolchain.`

## Keep / Adapt / Replace / Fill

Keep:

- Cursor as the main work entry.
- Existing usable `claude` command.
- Existing OpenRouter/DeepSeek experience if still valid.
- Prior output reports, file-input helpers, `.claude` content, and verified tool-use evidence.

Adapt:

- Cursor terminal workflow.
- Git Bash or WSL as the stable terminal route.
- Claude Code launch entry.
- Provider/model configuration.
- Report and output conventions.

Replace:

- Unstable old `ccswitch_proxy.py` style routes if they are still active.
- Stale localhost `15721` proxy assumptions.
- Incomplete tool-call conversion proxies.
- Long pasted-text dependence for task input.
- Single-model execution without reviewer or fallback routes.

Fill:

- CCR routing layer.
- Multi-model strategy.
- Skills, hooks, subagents, rules, workflows, reports, evidence, rollback.
- Codex skill migration candidates.
- GPT visual/screenshot collaboration and human-assist recovery mechanism.

## Required Phase Outputs

- `ClaudeCode_Cursor_Existing_Stack_Info_Report.md`
- `ClaudeCode_Cursor_Blocker_Report.md`
- `ClaudeCode_Cursor_PreDeploy_Blocker_Elimination_Report.md`

## Evidence Note

The attachment was read successfully as UTF-8. Earlier PowerShell output rendered it as mojibake because of console encoding, but the raw file is valid enough for extraction.
