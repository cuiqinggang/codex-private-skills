---
name: rea-on-demand-router
description: 按需判断是否启用已验收的 Windows REA 6.1.0 + Ghidra 12.1.4 + Codex MCP；疑难无源码原生 PE 只读逆向分析、复杂 GOOD/BAD 差分、函数调用关系定位时使用。简单问题不启动。
---

# REA 按需逆向分析路由｜v1.0.0
任务 REA-WIN-A-001；依据：《自动化 单页面极限短时间引擎第28版》。本文件是**索引与调用决策门**，不复制/修改冻结 REA 引擎，也不常驻启动 REA。

## 适用判断（先判断再执行）
- **DO / 按需调用**：有权分析的 Windows 原生、非托管 x86/x64 EXE，无源码；常规日志、源码、配置排查不能定位根因；需要反编译、调用图、交叉引用、字符串、汇编、函数或内存只读分析；复杂 GOOD/BAD 差分有明确二进制线索。
- **REFERENCE_ONLY / 只参考**：问题尚未证明需要逆向；先用成熟日志、源码分析、官方文档、普通调试器排查；可阅读本索引，但不启动 Ghidra/REA。
- **STOP / 不使用此入口**：DLL、.NET managed PE、恶意/不受信样本、未知文件授权、GUI 修改、二进制写入、非 PE 格式或当前官方 P0 未验证的范围。按官方支持矩阵转用其他已成熟方案，不暗中扩大能力声明。
- 优先级：成熟常规工具 → GOOD/BAD 的 FIRST_DELTA → REA 必要性判定 → 最小调用 → 证据/结论；分析前保留原文件哈希，不执行目标 EXE。

## 已通过的 Windows 现实基线
Windows10 19045 x64，本地 NTFS、普通非管理员/非受限宿主；Node24.14.0、REA6.1.0、Ghidra12.1.4、Temurin full JDK21.0.12.1+1。官方 Windows native 安全控制 PASS；x64/x86 原生 PE 各25/25只读操作 PASS；packaged MCP 各29/29 PASS；Codex CLI 真实5次 MCP 调用 PASS，返回 0x2a (=42)，正确 callee，close成功。官方断言和安全边界未放宽。Linux、新机器、当前既有桌面聊天的 MCP 热重载及大型/恶意样本未经现实验收。

## 最短复用路径（Windows 本机）
1. 阅读本机冻结技能：`C:\Users\A\.codex\skills\rea-windows-ghidra\SKILL.md`；实例根：`C:\Users\A\Documents\Codex\2026-10-09\a-windows-rea-win-a-codex\outputs\REA-WIN-A-001`；正式报告：`REPORT-1.0.1.md`；技能 MANIFEST/INSTANCE 和完整日志在上述目录。
2. 优先确认现有 `rea` Codex MCP 注册与实际入口，新的 CLI 会话中按需使用已注册工具；不重新安装 REA/Ghidra/JDK、不新建中间件。若当前会话未加载新服务，创建**新 Codex 会话**而非更改现有浏览器。
3. 最小业务动作：`open_binary → list_procedures → procedure_pseudo_code / procedure_callees / xrefs → close_binary`；先确认用户授权样本及其属于官方 Windows 原生支持边界；收集工具结果、错误与原始 SHA。
4. 若失败：正常退出、诊断 FIRST_DELTA；对比普通宿主与受限 Codex sandbox。出现 EPERM/EACCES 不重装、不关闭 DACL；Windows packaged verifier 的 Node Job 预初始化已由本机冻结技能管理，不能删除官方断言。
5. 恢复/重放只按本机 `references/deploy-and-rollback.md` 和 1.0.1 部署包；已有实例不再下载。Windows ZIP 不能当作 Linux 已验收安装包。

## 固定边界与交付定位
本机已冻结原技能 1.0.0，部署包 1.0.1；本索引并不取代它们。证据文件：`REPORT-1.0.1.md`、`evidence/codex-live-summary.json`、`evidence/codex-live-eof.command.json`、`skill/rea-windows-ghidra/MANIFEST.json`。官方：https://github.com/morluto/rea/tree/rea-agents-6.1.0 。避免将上游 experimental Windows P0 等同于全功能成熟。冻结技能不原位改写，需求变化通过新版本适配。
