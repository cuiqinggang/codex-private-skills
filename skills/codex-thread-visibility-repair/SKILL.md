---
name: codex-thread-visibility-repair
description: "Use when a Codex Desktop thread, task, project, or chat appears to disappear, becomes hidden, is archived unexpectedly, cannot be found by its old title, or needs safe restoration from .codex sessions/archived_sessions."
---

# Codex Thread Visibility Repair

## Purpose

Safely diagnose and repair Codex Desktop threads that appear to disappear after
restart, relogin, archive/unarchive, title changes, or UI cache refresh.

Use this skill before direct database edits. The common failure is not always
data loss. Separate these causes first:

1. **Archived thread**: `threads.archived = 1`, rollout path points to
   `.codex\archived_sessions`.
2. **Title drift**: thread is still active, but the title changed, so the old
   project name no longer searches.
3. **Rollout path mismatch**: database points to a missing file or to archive
   while the UI expects `.codex\sessions\YYYY\MM\DD`.
4. **UI cache/list refresh**: backend tools can find the thread but the visible
   app list has not refreshed yet.

## Safety Rules

- Always back up `state_5.sqlite`, `state_5.sqlite-wal`,
  `state_5.sqlite-shm`, `session_index.jsonl`, and the rollout JSONL before
  any repair.
- Never delete archived rollout files. Copy back to active sessions instead.
- Never edit `auth.json`, `config.toml`, account state, secrets, or payment
  state for a visibility repair.
- Prefer official thread tools first:
  `list_threads`, `read_thread`, `set_thread_archived`,
  `set_thread_title`, and `set_thread_pinned`.
- If official tools cannot repair an unloaded thread, use the local repair
  script with one explicit `--thread-id`.

## Workflow

1. Run diagnosis:

```powershell
${REDACTED_SECRET}
```

2. If the thread is archived or title drifted, repair with backup:

```powershell
${REDACTED_SECRET}
```

3. Verify with both:

```powershell
${REDACTED_SECRET}
```

and `list_threads(query="stable title")` when the Codex thread tool is
available.

4. For important threads, add a title lock in
   `references/title-locks.json`, then enforce it:

```powershell
${REDACTED_SECRET}
```

This neutralizes title drift for known important threads by restoring the
stable title and clearing accidental archive state after making a backup.

5. To protect all currently active projects, refresh the lock list:

```powershell
${REDACTED_SECRET}
```

This records every active, unarchived thread as protected. The enforcement
script can then restore any protected thread that is accidentally archived or
sent to `archived_sessions`.

## Known Case

On 2026-06-11, thread `019eb288-ae4b-7a32-9c46-5bd0f02812ee` appeared to
disappear twice.

Root cause sequence:

- First disappearance: archived state was set, with rollout under
  `.codex\archived_sessions`.
- After manual database recovery, the thread was active again, but the visible
  title drifted to `一步一截图`, so searching `视频合成分析3` no longer found it.
- The durable fix was to restore the active rollout path, set `archived=0`, and
  then use the official title tool to set a stable title:
  `视频合成分析3｜文字图片视频发GPT截图法技能包`.
- A title lock was added in `references/title-locks.json`.

See `references/video-synthesis-analysis-3-20260611.md`.

## Automatic Guard

For ongoing prevention, run these two commands on a schedule:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

This does not modify Codex Desktop internals. It creates a local protection
layer: newly active threads are added to the lock list, and protected threads
are restored if Codex Desktop moves them to archive state or changes their
stable title.
