# EXP-HTTP-001｜根路径302不等于服务宕机
版本V1；证据日期2026-10-23；状态：历史日报所记Ready局部通过，非当前服务健康认证。
触发：Tymeslot根路径302，探针只认可根路径HTTP200。
首差：探针条件过窄，把正常登录跳转误判宕机。
已记录修正：分别验证根路径预期302、最终`/auth/login` HTTP200、WebSocket。不能无条件把任意302都当成功；核对预期跳转目标、最终状态和实际业务。
边界：Ready探针通过不证明预约、持久化或当前服务健康。这里只读历史日报，未本次重跑HTTP。
来源：`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_DAILY\2026-10-23-DSE-INCREMENTAL.md`（2026-10-27实际读回）；原项目相关回执定位于`C:\AI\AI-Web-Replication-V1.0-20261023\`；当前使用须核对项目最新路由。
