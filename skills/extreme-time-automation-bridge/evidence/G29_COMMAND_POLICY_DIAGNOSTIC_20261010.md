# v0.3.1 G29命令受限诊断｜2026-10-10

STATUS=PARTIAL_DIAGNOSIS
BRIDGE_VERSION=0.3.1
DEVICE=f6990966-5870-484b-bf79-409bc6fb963e

- 官方 GitHub SKILL.md 回读确认：主路Desktop Commander Remote，备路GitHub Actions self-hosted runner，主路历史真实命令PASS，备路历史Actions成功；当前不重复启动备路来规避拒绝。
- 本轮DCR list_devices Online；ping pong；成功远程读取已有自动启动脚本34行及remote.log尾部。log第一次读取返回running call_id，随后使用get_tool_result核实完成；证明只读远程文件入口有效。
- 日志记载Codex CLI在2026-10-10T12:39:49Z发生exec_command CreateProcess rejected: blocked by policy；12:39:54Z缩减为单文件Get-Content仍被同类策略拒绝。这是Codex本地命令策略拒绝，不是设备离线；不得绕过。
- G29独立PowerShell检查先前也得到平台安全检查拒绝，不能因DCR文件读取通过而宣布GPT命令执行PASS；不同调用是否同一规则UNKNOWN。
- remote.log包含其他会话、内部通信与Codex错误信息；勿将其混作本G29任务已完成的测试证据。
- 未修改Windows代理、FlClash、计划任务、Remote配置或受保护浏览器。未新建桥、未调用备路绕过拒绝。

RESULT: DCR_CONNECTIVITY=PASS; DCR_FILE_READ=PASS; CODEX_LOCAL_COMMAND=POLICY_BLOCKED; GPT_COMMAND_REALITY=UNRESOLVED; G29_FULL_VALID=NO.
