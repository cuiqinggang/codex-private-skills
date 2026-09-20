# 现实执行环境完整采集过程 R1 → R2

版本：1.1.0

## 固定原则
不是把电脑改成测试环境，而是先完整测出现实，再让 Twin（数字孪生）复制现实。采集阶段禁止修改 Codex、AGENTS、配置、技能、代理、网络、ACL、注册表和系统设置。

## R1
锚定 Windows、PowerShell/.NET、Codex、Codex Home、全局 AGENTS、原始字节/SHA-256/编码/换行、ACL、文件系统、母技能和 Git/项目指令上下文。

R1 获得有效 Reality Anchor（现实锚点）基础，但沙盒、审批和完整运行时仍有关键未知，因此进入 R2。

## R2
扩展到主机/硬件、区域编码、进程令牌、Shell、环境变量、PATH、Codex 真正执行文件、完整实际配置与配置层、管理员强制要求、Windows 沙盒、审批、完整 instruction chain（指令链）、skills（技能）、hooks（钩子）、rules（规则）、MCP（模型上下文协议）、认证状态、Git、ACL、Windows 安全、网络/代理、进程/服务、资源快照、启动探针、漂移和秘密安全。

## TARGET / COLLECTOR 双上下文
TARGET=Codex 真正受沙盒约束的执行环境；COLLECTOR=沙盒外只读宿主采集环境。动态行为以 TARGET 为权威；COLLECTOR 不得冒充 TARGET。

## 1344 现实边界
相同只读 PowerShell 子进程创建连续 3 次：SetTokenInformation / 1344 / DENIED。
因此子进程未成功启动，PATH=NOT_REACHED，不存在运行中的子进程令牌。这是 Reality，不允许在 Twin 建立前先修掉。

## 8 个关键缺口
R2 初始：8 个关键未知，覆盖 27.27%。
先恢复 6 个：项目指令限制/备用名、完整实际配置、管理员强制要求、Windows 沙盒后端、技能运行时、Codex 真正执行文件。
最后通过 Codex 官方 execpolicy check（执行规则检查器）收口实际规则，并把 1344 结构化为已观测失败边界。

最终：
CRITICAL_UNKNOWN_COUNT_FINAL=0
CRITICAL_EXECUTION_STATE_COVERAGE_PERCENT=100.00
REALITY_ANCHOR_COMPLETE=YES
TWIN_INPUT_READY=YES

权威文件：
- snapshots/2026-09-21-r2/45-REALITY-ENVIRONMENT-ANCHOR-R2-FINAL.json
- snapshots/2026-09-21-r2/46-REALITY-FINGERPRINT-V3.json

Reality Fingerprint V3：
9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8

## 远端安全镜像
成功、部分、失败都必须保存安全远端证据，防止“本地有数据但 GPT 看不到”。秘密禁止明文上传。

## 历史
HISTORY_APPEND_ONLY=YES。未来环境变化必须新增快照和指纹，禁止覆盖 R1/R2。
