# GPT直连Windows执行桥 V7.0｜A 暂停，C 唯一日常入口
日期：2026-10-16
版本：7.0.0
Freeze：FREEZE-GPT-WINDOWS-BRIDGE-V7-A-PAUSED-20261016
变更来源：用户明确要求暂停 A，防止误选，并升级为 V7。

## 当前唯一生效的判路
- C = Remote Desktop Commander：默认和第一入口；先确认在线设备后直接执行授权任务。未知先核实 C，不绕过。
- A = GPT_Windows_MCP_Bridge：PAUSED_BY_USER，不进入自动或日常派单候选。即使 A 可连接或者 C 失败也不得借 A 接单。只有用户将来明确解除暂停或授权 A 独立诊断时才能重新冻结操作。
- B = GitHub Actions → Windows Runner：C 明确不可用、额度阻断或业务需要 GitHub 原生证据合同时使用；内部按现行 FAST／BOUNDED／FULL 规范分流。
- C、B 都不满足则 BLOCKED，不退回 A。副作用完成或 UNKNOWN 先对账，Exactly-once。
- 实际首选工具名：Remote_Desktop_Commander；误选过的 GPT_Windows_MCP_Bridge 为 A。

## 暂停的准确范围
- 本次暂停发生在技能包派单策略与本机判路器层：没有卸载插件，没有停止 A tunnel、client、Supervisor，也没有修改自启动任务、FlClash、Windows 代理、凭据或现有业务。
- 此级别不能让 ChatGPT 平台隐藏 A 工具，不能自动拦截不按本技能操作的其他对话，不能称为平台级硬禁用。
- V6/V5/V3 历史资料完整保留；其中 A 作为默认或 C→A→B 回退的语义全部由 V7 覆盖。已开始业务仍须遵守原 Freeze 与副作用回执。

## 实际验收
- 全程经实际 C 插件 Remote_Desktop_Commander，对在线 Windows 设备 DESKTOP-4A1EGTM 建立连接，写入、测试并回读 V7 脚本。
- 当前本地脚本：C:/AI/GPT-Windows-Bridge-B/persistence/Invoke-Three-Route-Gate-V7.ps1。原 V6 脚本保持不动，仅供历史证据。
- Windows PowerShell 5.1 Parser 错误 0；判路测试 10/10 PASS：C 默认、C down/额度阻断退 B、C 未知阻断、A ready 仍禁、DONE/UNKNOWN 禁重、GitHub 证据走 B。
- 脚本 SHA256：A01D22B210632FAB72F0AF84D6E3F360FCA531EB62A18F72D23360F8006727E2。
- 本机脚本输出 advisory_only=true、no_automatic_dispatch=true；此项 Reality 不证明平台级连接器已禁用。

## 恢复与安全
- 未经用户明确同意不得恢复 A 作为派单候选。要恢复需另行变更冻结路线并独立验收。
- C 可用时不为测试路线重复操作 A/B。不改现有网络/代理、浏览器、Runner、密钥，不重新启动任何隧道。
- Hermes 内部默认业务入口仍是已验证的原生正式 CLI；它与 GPT 连接 Windows 的通道为两个不同层级。
