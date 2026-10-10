---
name: safe-file-demo
description: 按已记录的无敏感文件演示，在指定全新 C 盘输出目录创建 UTF-8 中文演示文件并复制，验证内容与哈希；用于操作演示技能化样例验收。
metadata:
  version: "1.0.0"
---

# 安全文件演示样例

来源：`C:\AI\operation-demo-to-skill-v1\evidence\file-demo-r1\recording\desktop-events.jsonl` 与 summary.md。这是另一次独立合成桌面事件记录，不是真实人类演示。

当前 GPT/Codex 读取记录并提取：seq 3 New document → seq 4–17 两行中文 → seq 19 Save file → seq 20–32 notes/演示.txt → seq 34 Copy file → seq 35–51 archive/演示副本.txt。选择语义等价文件输出，不重放坐标。

执行：`python -B -X utf8 scripts/replay.py --out '<用户授权的全新 C 盘目录>'`。脚本只创建指定目录中的 `notes/演示.txt`、`archive/演示副本.txt` 和 manifest.json，内容为 `安全操作演示\n仅测试文件。\n`。不接受已存在的输出目录，不删除、不覆盖、不读取用户文件。

验收：退出码 0、两个文件内容与记录两行 UTF-8 相同、SHA256 一致、manifest 列出输出。重复指向既有目录必须退出非 0 且原文件哈希不变。证据为同一项目 evidence/file-demo-r1/result.json。此例证明实际文件输出和拒绝覆写，不证明真实 UI/人类操作或通用技能自动生成能力。