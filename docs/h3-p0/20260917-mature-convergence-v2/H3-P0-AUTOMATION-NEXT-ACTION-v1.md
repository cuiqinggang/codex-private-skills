# H3-P0 自动化下一动作 v1

当前 H3-P0 主路径已冻结；本文件只管理自动化基础设施。

下一动作唯一为：

```text
执行 H3-P0-GPT-CODEX-AUTOMATION-PILOT-COMMAND-v2.md
```

起点必须是 Codex。用户只需把 v2 Pilot 启动命令交给 Codex 一次。

之后预期链路：

```text
Codex 000001
→ Browser wake GPT
→ GPT GitHub 000002
→ Codex GitHub 读取并执行
→ Codex GitHub 000003
→ Browser wake GPT
→ GPT GitHub 000004
→ Codex freeze
```

目标：

```text
MANUAL_COPY_PASTE_REQUIRED=NO
```

禁止重新执行 GPT-first Pilot v1。