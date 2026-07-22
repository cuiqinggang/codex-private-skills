---
name: codex-title-result-rename
description: Use when the user wants Codex history, saved project names, task titles, or skill-related records renamed into long, clear Chinese result-based titles so they can find past work by outcome. Also use when preserving the renaming workflow as backups, before/after lists, and verification evidence.
---

# Codex历史标题按成果长中文命名

## 什么时候用

当用户说这些话时使用本技能：

- 历史项目、会话、保存项“从名字看不出来做了什么”
- 要把名字改成“中文、简单明了、尽量长、一眼看出成果”
- 要把做过的项目、技能包、New API、Hermes、小龙虾、ComfyUI 等工作按结果命名
- 要保留重命名过程、备份、改名前后清单和校验记录

本技能默认处理 Codex 桌面版当前工作区的历史会话标题：

${REDACTED_SECRET}
${REDACTED_SECRET}
- 会话正文：只读，不改
- 技能包目录：只在用户明确要求时才改

## 命名原则

标题必须用中文长成果名，优先让用户在列表里直接看出“这件事最终做成了什么”。

推荐格式：

```text
类型：对象/系统 + 已完成成果 + 关键用途/端口/保存位置/验证结果
```

常用类型：

- `技能包：`
- `New API免费模型池：`
- `Hermes修复技能包：`
- `小龙虾接入：`
- `ComfyUI视频技能包：`
- `标题整理：`
- `备份包：`
- `系统体检：`

好标题示例：

```text
New API免费模型池：找到小龙虾3011免费大模型路由、接入测试、后台登录和设置保存记录
技能包：Codex历史会话按成果长中文标题重命名，75条已改，备份清单和校验流程已保存
Hermes修复技能包：爱马仕重启后恢复回答，重新连接Telegram和New API链路
```

避免：

- 只写“查找文件”“修复问题”“项目整理”
- 只写英文缩写，用户看不懂
- 只复述用户第一句话，不写最终成果
- 标题太短，列表里看不出内容

## 安全流程

1. 先读取当前 `AGENTS.md` 和 `yesterday-replay-controlled-coding`。
2. 判断范围：只改标题字段，不改会话正文、不改技能包内容、不删除文件。
3. 备份 `state_5.sqlite` 和 `session_index.jsonl`。
4. 读取线程 ID、旧标题、首条用户消息、必要时读最终报告。
5. 生成 `id -> 中文长成果名` 映射。
6. 先 dry-run 检查映射是否覆盖所有目标 ID。
7. 正式写入 SQLite 的 `threads.title` 和 `session_index.jsonl` 的 `thread_name`。
8. 生成改名前后清单。
9. 重新读取校验：
   - 目标标题数量正确
   - 没有 `?` 乱码替代字符
   - 旧短标题不再命中
   - New API、技能包等重点词能搜到

## 脚本

优先使用：

```powershell
${REDACTED_SECRET}
```

脚本支持：

- `--mapping`：JSON 文件，格式为 `{ "thread-id": "中文长成果名" }`
- `--cwd-like`：限定工作区，默认匹配 `Desktop\1`
- `--dry-run`：只检查不写入
- `--apply`：写入标题
- `--out-dir`：输出备份和清单目录

不要通过 PowerShell here-string 直接传中文 Python 脚本。Windows 默认代码页可能把中文写成 `?`。如果要写中文映射，必须保存为 UTF-8 文件后再运行。

## 当前成功案例

本技能由 2026-05-24 的一次成功整理沉淀而来：

- 已改 SQLite 历史标题：75 条
- 已改 `session_index.jsonl` 索引：9 条
- 重点成果名示例：`New API免费模型池：找到小龙虾3011免费大模型路由、接入测试、后台登录和设置保存记录`
${REDACTED_SECRET}
${REDACTED_SECRET}

详细证据见 `references/2026-05-24-successful-run.md`。
