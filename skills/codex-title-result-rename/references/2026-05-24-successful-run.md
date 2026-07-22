# 2026-05-24 成功运行证据

## 目标

用户要求把 Codex 历史会话、做过的项目、技能包相关记录改成中文长成果名：

- 名字要尽量长，能显示多少显示多少
- 一眼看出做过什么、成果是什么、能解决什么
- 重点突出“技能包”和“已保存的成果”
- New API、小龙虾、Hermes 等记录要按结果命名

## 实际完成

已改名：

- SQLite `threads.title`：75 条
- `session_index.jsonl` 侧边栏索引：9 条

重点标题示例：

```text
New API免费模型池：找到小龙虾3011免费大模型路由、接入测试、后台登录和设置保存记录
技能包：New API本地自用部署已完成，Docker三容器、数据库缓存和Token创建流程已沉淀
技能包：秋叶ComfyUI视频生成基线，Wan2.2 5B短视频测试、工作流和输出路径保存完成
Hermes修复技能包：爱马仕重启后恢复回答，重新连接Telegram和New API链路
```

## 关键经验

不要通过 PowerShell here-string 传入包含中文的 Python 代码再写 SQLite。Windows 默认代码页可能把中文写成 `?`。

正确方式：

1. 把中文映射保存到 UTF-8 文件。
2. 用 Python 直接读取 UTF-8 文件。
3. 写入 SQLite 和 JSONL。
4. 重新读取并检查 `?` 数量为 0。

## 证据路径

备份：

```text
${REDACTED_SECRET}
```

最终改名前后清单：

```text
${REDACTED_SECRET}
```

最终校验结果：

```text
SQLite 标题数量：75
session_index 标题数量：9
titles_with_question_mark：0
旧短标题命中：0
```
