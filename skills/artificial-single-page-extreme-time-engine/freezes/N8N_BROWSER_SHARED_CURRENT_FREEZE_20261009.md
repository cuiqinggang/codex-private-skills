# 《n8n 原生 MCP 与共享浏览器｜当前任务冻结状态 第1版》
日期：2026-10-09
冻结标签：N8N-MCP-SHARED-F001
任务：n8n 原生 MCP 接入、跨客户端共享浏览器、资源级协调与故障恢复
权威方法版本：自动化单页面极限短时间引擎 第28版；极限短时间执行大脑 第25版；新页面运行模板 第17版。
性质：现状冻结，不代表生产成熟或 FINAL_VALID。
## 已确定结论
- 用户所有获许可工具共同使用原有浏览器。不得因一个业务独占浏览器、阻止其他合法工具使用、擅自改代理或启动第二浏览器。
- 无冲突任务应并行；冲突操作只按实际的会话、标签页及共享上下文协调。全局并发=1 是隔离测试基线，不是正式协作规范。
- 成熟方案复用 n8n 原生 MCP Client、Remove Duplicates、Wait、官方 Playwright MCP 与原有 chatgpt-business-entry.js；禁止重造通用调度器、锁、持久化与发送器。
- 三态：CONFIRMED_COMMITTED 不重试；CONFIRMED_NOT_EXECUTED 经资源协调后允许恢复；UNKNOWN 不自动重试，不阻塞无关任务。
- REUSE_GATE→整体虚拟成熟→STOP_GATE→Freeze→仅一次Reality。无同边界完整时间对照不得宣称 VIRTUAL_MATURE=YES。
## 已验收、可直接复用
- 正式 n8n-local 原有7条工作流（其中 Reasonix 闭环激活）；隔离测试 n8n-v27-sandbox。
- 原生 MCP browser_tabs 只读调用与原浏览器可逆 DOM 写入 PASS，无真实发送。
- 隔离 n8n 跨工作流三任务执行串行 PASS（#23-25）。
- 原生去重跨重启 PASS（#18-20、#22）；Wait 持久等待同编号跨重启恢复 PASS（#21）。
- 写入成功后强制失败 #26；同键重试 #27 未再次写入。
- n8n 实写 #28 与独立 MCP 客户端只读同时共存 PASS。
- 虚拟资源规则15项离线测试通过，但不是生产级资源协调的实现证据。
## 尚未完成（本次不进行新的Reality）
1. 跨 n8n/Codex/其他客户端同一资源的最小冲突域协调，正式生产尚未部署。
2. 不同资源跨客户端实际并行、共享上下文互扰隔离、异常释放与无饥饿尚未验收。
3. UNKNOWN 状态的端到端业务证据对账与失败恢复未接入统一生产路径。
4. 原 Reasonix/n8n 业务流程与多客户端共享规范尚未完成正式整合。
5. T_BASE_REAL、T_VIRTUAL_BEST、DELTA_T、GAIN_PERCENT、SPEEDUP 的完整同边界对照仍 UNKNOWN。
## 下一自然节点
以已保存的 ENGINE 28/BRAIN 25 及本冻结状态为唯一方法/任务恢复入口；先核查最成熟的可复用资源协调方案，完成全链路时间、故障、用户并行成本虚拟成熟；STOP_GATE 过后才安排一次现实闭环验收。
## 当前状态
ENGINE=28
BRAIN=25
FREEZE_VERSION=1
BASIC_REALITY=PASS
SHARED_BROWSER_POLICY=FROZEN
MULTI_CLIENT_COORDINATION=PENDING
VIRTUAL_MATURE=NO
REAL_SEND=PROHIBITED
FINAL_VALID=NO
