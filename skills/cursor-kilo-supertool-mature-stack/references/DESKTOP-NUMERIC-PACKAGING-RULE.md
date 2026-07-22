# Desktop Numeric Packaging Rule

## Purpose

The user often needs to send completed reports and evidence packages to another tool that cannot read the chat transcript. Therefore, every completed stage/task should produce a simple desktop ZIP handoff package with a short numeric name.

## Rule

After a task creates a final report, evidence ZIP, command package, or stage output, create:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

`NNN` must be a simple three-digit number.

## Number Selection

1. If the user specifies a number, use that exact number.
2. If the user does not specify a number, choose the next available three-digit number on the desktop.
3. Prefer numbers that are easy for the user to recognize and send.
4. If the chosen folder or ZIP already exists, rename it to a timestamped backup before creating the new package.

## Contents

Include:

- final report
- evidence ZIP
- key stage/check/report files
- a short `README_NNN.md` explaining what the package contains

Exclude by default:

- `node_modules`
- browser profiles
- cache folders
- huge source trees
- temporary scripts
- API keys or secret configs

## Final Answer

Always include the desktop numeric ZIP path, for example:

```text
桌面压缩包：
${REDACTED_SECRET}
```

