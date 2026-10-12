# Polsia clone4｜派发链路根因与第一路真实启动回执
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
BATCH_ID=PCL4_20261012
PARENT_FREEZE=POLSIA-MOTHER-V008-F001
MOTHER_FINAL_VALID=NO
CHECKPOINT_KIND=PARTIAL_LIVE_EXECUTION

## 原因
GitHub 四任务合同创建与回读确实成功，但当时仅有 ASSIGNED_NOT_YET_STARTED，未实际触发 Windows Codex。原 GPT-Windows Bridge 一度返回 MCP server is not initialized，重试后的同一桥已执行成功；备用 Remote Desktop Commander 连接正常但本月额度用完。故前一次“全部无法启动”不代表 Codex 程序不可用。

## 真实启动
2026-10-12 22:04:55 +08:00，经 GPT-Windows-MCP-Bridge 调用 Start-Process，PCL-01 本机启动器 PID=7392；多次 Get-Process 核验存活。日志 C:\AI\Polsia-V5-Parallel-20261012\clone4\PCL-01\CODEX.log 已出现 Codex session id=01a1306e-4d0e-73b1-98c0-24cac3efa9d9、实际任务输入及 Codex 模型答复，证明真实接单，非仅合同发布。
启动早期 wss://chatgpt.com/backend-api/codex/responses 收到 os error 10061 并自动重试；之后出现真实 Codex 模型输出，不能将该网络错误判定为完全失败。两份本地 Codex SKILL.md 的 YAML frontmatter 缺失和一个旧配置项被忽略，均需后续另行排查，但尚不能断言阻断此次运行。

## 当前进度与边界
PCL-01=RUNNING_VERIFIED_PROCESS_AND_CODEX_REPLY; business outcome pending.
PCL-02/PCL-03/PCL-04=ASSIGNED_NOT_YET_STARTED; 出于同一源码目录写入冲突，待使用隔离工作树后独立启动。
保留 V001-V008 冻结，不改代理/浏览器/已有监控网站；新成果必须真实提交 GitHub 回读；网站端到端 FINAL_VALID=NO。不能将 PCL-01 启动成功宣布为网站复刻成功。
