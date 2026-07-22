# ChatGPT Bridge Execution Discipline

This document is the durable execution standard for GPT planning results sent back through the ChatGPT clipboard bridge.

## Core Rule

```text
默认自动执行，只有高风险才停；
Codex 不改写 GPT，只执行 GPT；
桥接只搬运，不判断。
```

## Execution Model

Wrong model:

```text
answer_raw.md -> Codex 理解 -> Codex 重写 -> Codex 执行
```

Correct model:

```text
answer_raw.md -> 结构提取 -> codex_plan.md -> 执行
```

`codex_plan.md` is not a new plan. It is a structured form of the GPT output. The steps must be 一一对应 with `answer_raw.md`.

Allowed:

- Formatting changes.
- Numbering changes.
- Splitting long lines for readability.
- Extracting explicit fields such as step, target file, command, and verification.

Forbidden:

- Adding steps.
- Removing steps.
- Rewriting meaning.
- Translating into a different intent.
- Optimizing the plan before execution.
- Adding Codex's own advice as executable steps.

## Execution Locks

### No-Rewrite Lock

If `codex_plan.md` contains a new step, deleted step, or semantic rewrite that is not present in `answer_raw.md`, STOP.

### Minimal-Diff Lock

The extracted plan must preserve the original action list. Format may differ; semantics may not.

### 执行范围锁 / Execution Range Lock

All operations must stay in:

```text
output/chatgpt-clipboard-bridge/
```

or another directory explicitly named by the GPT plan or the user. Otherwise STOP.

## Risk Levels

### Level 0

Conditions:

- Only writes inside `output/`.
- Does not delete files.
- Does not modify existing code.
- Does not call system-critical commands.
- Does not run unknown network scripts.

Action: execute automatically.

### Level 1

Examples:

- Create new files.
- Modify test output.
- Write logs.
- Write temporary files.

Action: execute automatically and write an execution log.

### Level 2

Examples:

- Modify existing code.
- Run build/test.
- Overwrite files.

Action: execute automatically only after backup, diff capture, and execution log.

### Level 3

Examples:

- Delete files.
- Batch-modify the project.
- Run unknown commands such as `curl | bash`.
- Modify system configuration.
- Operate accounts, keys, payment, secrets, or broad network permissions.

Action: STOP and ask the user.

## Bridge Boundary

The bridge only carries text:

```text
prompt -> ChatGPT website -> 复制回复 / Copy response -> answer_raw.md
```

It does not judge, rewrite, scrape page text, OCR, handle login, handle captcha, handle payment, or bypass limits.
