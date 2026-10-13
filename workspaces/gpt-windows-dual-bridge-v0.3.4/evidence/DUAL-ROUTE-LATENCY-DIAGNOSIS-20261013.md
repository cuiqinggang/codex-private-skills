# GPT直连Windows双路执行桥 v0.3.4｜2026-10-13 延迟根因与最简路由冻结

## 验收边界
- 保留当前 v0.3.4，不修改 FlClash、代理、已登录浏览器或既有生产工作流。
- 目标：最短有效闭环，而非只追求 Windows 本地计算耗时。
- 证据来源：GPT_Windows_MCP_Bridge 实调用、GitHub Actions 工作流/日志、已连接的 Remote Desktop Commander 设备状态，以及 2026-10-12 仓库内既有性能证据。

## 通道 A：GPT→Windows（真实测量）
- 同一计算任务（100000 次求和、校验结果=4999950000），两次成功：端到端工具调用耗时 5.420 秒、5.882 秒；本地计算 493.322 毫秒、484.081 毫秒。
- 小文件读取三次成功：4.990 秒、6.061 秒、8.255 秒。
- 读写临时文件、回读、清除均在上一回合 PASS。
- Codex CLI 已安装并能调用：codex-cli 0.160.0；本地路径可经直连启动，不需要绕行浏览器。

## 通道 B：GitHub Actions→Windows self-hosted Runner
- 工作流：.github/workflows/windows-github-bridge-v034-smoke.yml；本机 Runner：DESKTOP-4A1EGTM-etal。
- 2026-10-13 RUN 38386260876：workflow_dispatch 正常完成；通过 GitHub 连接器**独立重运行**第 2 次也成功，证明派发无需依赖 A。
- 第 1 次创建 10:51:52 UTC、Runner 日志 10:52:07、计算标记 10:52:10、终结 10:52:19；总计约 27 秒；本机计算 928.257 毫秒。
- 第 2 次启动 10:55:42 UTC、Runner 日志 10:55:49、计算标记 10:55:52、终结 10:56:01；总计约 19 秒；本机计算 1000.225 毫秒。
- 对相同的轻计算，A 的工具往返约 5.4–5.9 秒，B 的全流程约 19–27 秒；不是吞吐量或长期 SLA 数据。
- GitHub 消耗主要在调度接单、作业初始化、状态同步和结果拉取，而非计算。
- 最简 smoke 已移除 checkout、upload-artifact 和其他外部 Action，现阶段没有证据显示继续微调该工作流能够显著消除 GitHub 平台固定调度成本。

## 生产路径区别与已知重大故障
- 2026-10-12 生产工作流 extreme-time-windows-bridge.yml Run 38264768349，contract-static PASS，windows-reality FAIL；419 秒后失败。
- 根据同期报告：在 Setup Job 获取 actions/upload-artifact@v4 的 ZIP 时三次触发 100 秒超时，业务 payload 尚未开始。
- **smoke PASS 不代表生产工作流 PASS**。需分别验收任务执行、取证返回、回调和失败恢复。

## 第三路径审查
- Remote Desktop Commander 曾显示新设备 online，ping 三次约 1.1–1.7 秒，但后续文件读取返回“月度使用额度达到上限”；**不能标为生产可用**。此额度与自建 GPT-Windows-MCP-Bridge 无关。
- Codex 浏览器自动化仅能在具有合法权限、可访问目标页面及执行端点时与 Windows 间接交互；浏览器 UI 点按不会消除 GitHub Actions 的调度耗时。若是本机 Codex CLI，优先直接使用本地文件/CLI 而非浏览器模拟 ChatGPT 对话。
- 禁止绕开权限、导出网页登录凭据、开启未经授权的公网任意命令执行端口。

## 极简路由规则（建议/冻结判断，不冒称已经部署自动切换）
1. 即时小任务：优先 A，直接执行并直接回读结果；无需上传 GitHub 再下载。
2. A 无法连接、任务需要独立追踪或可能长时间执行：选 B 的无外部 Action 最简派发路径；以 task_id/run_id/状态码核验。
3. 需文件工件/真实生产 payload：隔离走 B_FULL，不能把 smoke 当成业务完成；先修复外部 Action 下载或改为等效已验收的取证机制。
4. 避免“一小步一条 GH Action”；批量任务以一次执行节点承载多个内部步骤，并严格遵守冻结、幂等性和 Exactly-once。
5. 对失败任务不得盲目重发；先核查 run_id、回执和产物，避免双执行。
6. 不改 FlClash/代理/现有已登录浏览器；不在本次直接更改生产工作流。

## 状态
- 通道 A 基础读写与计算 PASS。
- 通道 B 独立派发＋最简计算＋日志验证 PASS。
- 通道 B 原生产任务 FAIL（历史证据），并未因本次 smoke 而自动修复。
- 重启后自动恢复、长期稳定和高并发：NOT TESTED。
- 结论：优先 A；B 做异步/备用/较长任务；Codex 直接使用本地 CLI，无需新增浏览器通道。