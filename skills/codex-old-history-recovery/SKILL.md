---
name: codex-old-history-recovery
description: Use when Codex Desktop history, old chats, task threads, session records, or project conversations disappear after relogin/account changes, or when the user asks to recover/search "旧历史", "旧任务", "历史任务包", "以前 Codex 记录", "重新登录后聊天消失", DeepSeek/Codex++/config/model-routing old records. Provides a safe read-only recovery, backup, parse, knowledge-base, and search workflow.
---

# Codex Old History Recovery

## Purpose

Recover and search old Codex Desktop chats/tasks after relogin, profile/account changes, Codex++/DeepSeek/model-route changes, or missing UI history.

This skill preserves a strict safety boundary:

- Read and copy only.
- Prefer backup copies over originals.
- Never delete, move, overwrite, clean caches, reinstall, restore UI, or modify account/config files unless the user explicitly requests a separate high-risk task.
- Never expose or copy access tokens, refresh tokens, API keys, or secrets into reports.

## First Checks

Always load workspace `AGENTS.md` and `yesterday-replay-controlled-coding` first if the workspace requires it.

Classify:

- **Search existing old-history knowledge base**: user says "搜索旧历史", "查旧任务", "找历史任务包", "找以前 Codex 记录", or asks for a topic from prior Codex work.
- **Recovery scan**: user says Codex Desktop history/chats/tasks disappeared, especially after relogin/account/model-route changes.
- **Parse/export**: user has a recovery backup and wants readable catalogs/previews/search files.

## Known Fixed Pointer

On this Windows machine, first try the fixed pointer:

```text
H:\AI\CODEX_OLD_HISTORY_SEARCH入口.md
```

If it exists, read it first. It points to the current old-history knowledge base, currently:

```text
H:\AI\recovery\codex-chat-history-recovery-20260609-165244\knowledge_base
```

For search tasks, prefer:

```text
knowledge_base\START_HERE.md
knowledge_base\TOP_50_LIKELY_IMPORTANT_SESSIONS.md
knowledge_base\KEYWORD_HITS.md
knowledge_base\ALL_SESSIONS_CATALOG.md
knowledge_base\ALL_SESSIONS_CATALOG.csv
knowledge_base\previews
knowledge_base\session_index_table.csv
```

## Search Workflow

When the user asks to search old history:

1. Read `H:\AI\CODEX_OLD_HISTORY_SEARCH入口.md`.
2. Read `knowledge_base\START_HERE.md`.
3. Use `rg -n -i` over the knowledge base for the user's keywords.
4. Rank results by:
   - direct keyword match in title/first user message;
   - hits in `TOP_50_LIKELY_IMPORTANT_SESSIONS.md`;
   - hits in `KEYWORD_HITS.md`;
   - user message count and assistant message count;
   - recency and file size when relevance is otherwise tied.
5. Output the top 3 to 5 sessions with:
   - session/topic title if available;
   - Markdown/catalog path;
   - backup `rollout-*.jsonl` path if relevant;
   - short summary;
   - suggested next action.

Do not modify the knowledge base during search.

Useful search patterns:

```powershell
rg -n -i "DeepSeek|Codex\+\+|CodexPlusPlus|config\.toml|模型路由|provider|route" "H:\AI\recovery\codex-chat-history-recovery-20260609-165244\knowledge_base"
```

## Recovery Scan Workflow

Use this when no knowledge base exists or the user asks to recover missing history.

Create a timestamped recovery directory:

```text
H:\AI\recovery\codex-chat-history-recovery-YYYYMMDD-HHMMSS
```

Scan these roots read-only:

```text
C:\Users\A\.codex
C:\Users\A\AppData\Roaming
C:\Users\A\AppData\Local
C:\Users\A\AppData\LocalLow
```

Search for:

```text
codex openai chatgpt conversation thread session history sqlite db json jsonl log
```

Prioritize:

```text
.db .sqlite .sqlite3 .json .jsonl .log sessions threads conversations history
```

Copy only non-sensitive suspected history files to:

```text
<recovery>\files
```

Do not copy or print secrets from names like:

```text
auth token secret credential key oauth
```

For sensitive account files, record only path, size, modified time, and sanitized hints such as email/account/workspace/user-id digest if safely extractable. Never print token values.

Required scan report:

```text
<recovery>\RECOVERY_REPORT.md
```

Include:

- current account assessment, sanitized;
- discovered history-related files;
- suspected chat/task files;
- old-account/profile traces;
- whether recoverable content exists;
- next steps;
- explicit safety statement: no delete, no overwrite, no reinstall, no cache cleanup, no `auth.json` change, no config change.

## Parse And Export Workflow

Use this when a backup exists and the user wants readable catalogs/previews.

Read only from backup copies, usually:

```text
<recovery>\files\C\Users\A\.codex\session_index.jsonl
<recovery>\files\C\Users\A\.codex\sessions
```

Never read or write original:

```text
C:\Users\A\.codex
```

Write outputs only under:

```text
<recovery>\parsed
```

Parse `session_index.jsonl` into:

```text
parsed\session_index_summary.md
parsed\session_index_table.csv
parsed\session_index_raw_preview.txt
```

Scan all:

```text
rollout-*.jsonl
```

Extract:

- source path, size, modified time;
- possible session id and timestamps;
- counts of user/assistant/system/developer/tool messages;
- whether `content`, `message`, or `text` fields exist;
- first user/assistant message summaries;
- keyword hits.

Generate:

```text
parsed\ALL_SESSIONS_CATALOG.md
parsed\ALL_SESSIONS_CATALOG.csv
parsed\KEYWORD_HITS.md
parsed\TOP_50_LIKELY_IMPORTANT_SESSIONS.md
parsed\previews\preview_001.md ... preview_020.md
parsed\PARSE_REPORT.md
```

Report must state:

- rollout count;
- parsed success/failure count;
- whether `session_index.jsonl` is readable;
- whether real user messages and assistant replies were confirmed;
- top likely old task files;
- next 5 full reads;
- safety statement that only `parsed` was written and no backup source/original was modified.

## Knowledge Base Workflow

Use this after parsed outputs exist and the user wants long-term search.

Create:

```text
<recovery>\knowledge_base
```

Copy or organize:

```text
PARSE_REPORT.md
TOP_50_LIKELY_IMPORTANT_SESSIONS.md
ALL_SESSIONS_CATALOG.md
ALL_SESSIONS_CATALOG.csv
KEYWORD_HITS.md
session_index_summary.md
session_index_table.csv
previews\
```

Create:

```text
knowledge_base\README.md
knowledge_base\START_HERE.md
```

Update the fixed pointer only if the user asks:

```text
H:\AI\CODEX_OLD_HISTORY_SEARCH入口.md
```

Do not modify `config.toml` for long-term memory unless the user explicitly asks and accepts backup/test/rollback. Prefer the fixed pointer file over config changes.

## Output Style

For recovery/search tasks, answer in Chinese unless the user asks otherwise.

Always include:

- what was read;
- what was written, if anything;
- top findings;
- exact paths;
- PASS/FAIL verification;
- skipped checks and residual risk;
- safety statement.

For search-only tasks, keep it concise: top 3 to 5 results and paths.

## Hard Stops

Stop and ask before:

- deleting anything;
- overwriting originals;
- restoring files into `C:\Users\A\.codex`;
- changing `auth.json`, `config.toml`, account state, payment state, proxies, DNS, firewall, VPN, or system security;
- exposing tokens/API keys;
- cleaning AppData/cache;
- reinstalling Codex Desktop;
- attempting UI recovery.
