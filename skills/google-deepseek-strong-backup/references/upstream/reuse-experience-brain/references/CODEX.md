# EXP-CODEX-001｜Codex故障按层定位
版本V1；证据日期2026-10-25；状态：限定只读回归已验收，不是通用稳定规则。
触发：旧Windows CLI WebSocket重试、模型列表刷新超时、Windows MCP未监听。
旧事实：CLI0.160.0环境中三个接点分别异常；既有认证能用于HTTPS实际推理，原生MCP已安装。
采用步骤：先分传输/模型目录/MCP生命周期定位首差；复用受支持HTTPS provider、已有官方models_cache及原生stdio；保留原凭据/代理与备份，不默认重装。以当前官方支持及当前配置为准，不盲贴旧参数。
原验收摘录：cli_version=0.164.0 stable；status=ACCEPTED_LOCAL_CLI_AND_WINDOWS_MCP；9项保全检查通过；实际MCP识别3屏；T_VALID_FULL_TASK=NOT_MEASURED。
反例/边界：初次HTTP502确切来源未知；旧会话不原地升级；缓存删除或要用新模型须刷新目录；未认证全部连接器、GUI写入或长期稳定。
证据：`C:\AI\Codex-CLI-Repair\AIORG-CODEX-20261025-001\FINAL-ACCEPTANCE.json`（2026-10-27本会话前段已读回）。
继承日报：`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_DAILY\2026-10-26-DSE-INCREMENTAL.md`。
