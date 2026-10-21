---
name: gpt-windows-execution-bridge
description: Windows 执行桥 V12.0。A=Remote Desktop Commander（默认）；B=GPT-Windows-MCP-Bridge（A确认失败才用）；C=GitHub Actions Windows Runner（A、B确认失败才用）。
---
# Windows 执行桥 V12.0 — 唯一正式入口

**只记一条：A → B → C；能走 A 就绝不先走 B 或 C。**

- **A**：`mcp__Remote_Desktop_Commander__`（原 V11 的 C）；先 `list_devices` 动态找在线设备，再运行无副作用测试，PASS 即锁定 A。
- **B**：`mcp__GPT_Windows_MCP_Bridge__`（原 V11 的 A）；仅 A 重查及复验都确定 FAIL、有证据、业务执行结果已查清时启用。
- **C**：GitHub Actions → Windows Runner（原 V11 的 B）；仅 A、B 都确定 FAIL 后启用。
- **UNKNOWN**：先查证、不得误判或盲目重发；页面断线与业务脚本失败不等于 A 故障。

具体规则：`v12-abc-routing.md`；脚本：`route_v12.py`。V11 的 `guard_route.py` 为历史旧字母门禁，**V12 禁止调用**。旧版历史文件不改动。不可声称本地规则能物理拦截未接入的原生工具；不修改代理或系统配置。
