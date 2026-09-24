# 本地 AI 现实底座版本历程 1.1.3 → 1.1.7

## 1.1.3
- 基线：Reality Anchor 1.3.0、Exact Reality Twin 1.3.0、Browser R3/Host R2 指纹、GPU/浏览器/本地模型资产。
- 已知 Codex 约束 001–006：Temp 可执行脚本、Here-String 插值、w32tm 权限、启动告警、FETCH_HEAD 权限、只读 probe 语义优先。

## 1.1.4
- 新增 OBSERVED_CONSTRAINT_007：Windows Codex 子进程创建 `SetTokenInformation(TokenDefaultDacl) failed: 1344`。
- 规则：优先任务专属窄工作目录，不把 executor-entry failure 错判成工具缺失。
- 记录下载工具存在性：aria2c / hf / curl 可用观察。

## 1.1.5
- 固化真实工具版本：aria2c 1.37.0、hf 1.19.0、gh 2.92.0（可选）。
- `C:\AI\Mature-Download-Router-Real-Test` 窄工作目录现实子进程启动 PASS，R0≈4171ms。
- 固化进程级网络上下文继承规则；禁止改变持久代理。

## 1.1.6
- 新增 OBSERVED_CONSTRAINT_008：Windows curl / Schannel exit 35 TLS 上下文失败。
- 规则：依赖 Windows curl/Schannel 时，必须在同一执行上下文做真实 TLS 预检；不能把 exit 35 自动解释成 URL/代理/下载器失败。

## 1.1.7
- 新增 OBSERVED_CONSTRAINT_009：hf 1.19.0 + 现有进程级代理在受限 Codex 上下文真实成功。
- 实证：openai-community/gpt2/config.json，revision 607a30d..., 665 bytes，SHA256=0daed7..., T_VALID=13727.948ms，VALID_REAL=PASS。
- 该时间只是局部下载有效时间，不进入整体 T_MATURE*。

## 权威
- 当前 VERSION=1.1.7。
- 当前 manifest.version=1.1.7，previous_version=1.1.6。
- 当前 SKILL metadata 已修正为 1.1.7。
- 历史分支中个别 SKILL metadata 曾滞后一版；以各分支 VERSION + manifest + 本历程核对为准。
