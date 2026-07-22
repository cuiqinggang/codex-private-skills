# Video Synthesis Analysis 3 Visibility Case

Thread id:

```text
019eb288-ae4b-7a32-9c46-5bd0f02812ee
```

Stable title:

```text
视频合成分析3｜文字图片视频发GPT截图法技能包
```

Observed symptoms:

- User could see the thread before shutdown.
- After restart, searching the expected title did not show it.
- The underlying rollout JSONL still existed.
- The apparent `一步一截图` project was not a separate missing thread. It was
  the same `视频合成分析3` thread after automatic title drift.

Diagnosis:

1. First failure was real archive state:
   `threads.archived = 1`, `archived_at` set, and rollout path under
   `.codex\archived_sessions`.
2. After restoring the rollout to `.codex\sessions`, restart did not rearchive
   it. Instead, title drifted to `一步一截图`.
3. Searching `一步一截图` found the thread. Searching `视频合成分析3` did not.

Conclusion:

The second disappearance was not data loss and not archive. It was title drift:
Codex Desktop regenerated or replaced the display title from conversation
content, making the original project name unsearchable.

This is a visibility defect because the user did not request archive or rename.
When it happens, do not assume deletion. Check `threads.title`,
`threads.archived`, and `threads.rollout_path` first.

Durable repair:

- Keep rollout JSONL under `.codex\sessions\2026\06\11`.
- Keep `threads.archived = 0`.
- Set an explicit stable title with the official thread title tool.
- Pin the thread with the official pin tool.
- Verify by searching multiple anchors:
  `视频合成分析3`, `文字图片视频`, and the thread id.

Post-repair verified title:

```text
视频合成分析3｜文字图片视频发GPT截图法技能包
```

Important limitation:

There is no safe evidence yet that a global "auto-hide" feature can be disabled
without changing Codex Desktop application internals. The safe prevention is to
pin important threads, set a stable explicit title, keep the rollout in active
sessions, and run the repair script if restart causes title drift or archive
state again.

Recovery backup made during the first restoration:

```text
H:\AI\recovery\codex-thread-restore-20260611-034511-019eb288-ae4b-7a32-9c46-5bd0f02812ee
```
