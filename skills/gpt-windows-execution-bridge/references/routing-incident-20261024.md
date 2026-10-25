# 通道误选故障：2026-10-24（北京时间）

任务编号：WIN-ROUTE-20261024-001。
状态：路由技能已发布（fe57639），Windows 本机同步读回成功；独立新执行上下文真实只读验证通过。用户浏览器中另一 GPT 页面尚未完成端到端验证。

## 证据
- 用户两次截图显示 GPT-Windows-MCP-Bridge，第二次为视频任务查看 custom_nodes。截图未展示该页面此前完整 A 探测记录，不能仅凭截图断言该页面从未测过 A。
- Windows 本机 C:\Users\A\.codex\skills\gpt-windows-execution-bridge\SKILL.md 已有正确 V12 映射和失败复验条件。
- 修复前当前网上 Skills 工作区没有 gpt-windows-execution-bridge，当前会话技能目录亦未列出该入口；本机存在不等于 GPT 新页面能够自动发现。
- 网上网站能力包只写 A→B→C，缺少具体连接器映射。
- A list_devices 显示 DESKTOP-4A1EGTM 在线，设备 f6990966-5870-484b-bf79-409bc6fb963e；小文件读取及命令回执 V12_A_ROUTE_INCIDENT_PROBE_PASS 成功。
- 本机 route_v12.py 是由调用方提供探测证据的判定脚本，不探测、不代理原生调用，不能当作全局拦截器。

## 修复范围
- 发布明确可发现的 Windows 路由技能，描述覆盖视频/ComfyUI、Docker、DSH、本机文件和恢复任务。
- 网站能力包加入完整连接器映射并引用路由技能。
- Windows 本机同名技能同步网上版本；保留现有脚本、历史文件与所有业务进程。
- 不改 B 服务、不影响备用通道、不重启设备，不操作另一页面正在执行的业务。

## 验证边界
文件发布、静态规则检查和当前页面 A 命令成功只能证明本次范围。尚未对另一真实新 GPT 页面完成首次调用及 A 故障切 B 的端到端验收；已运行页面不保证热加载新技能。未获得该页完整日志，单次误选的内部推理原因仍未直接取证。

## 发布与独立验证回执
- 初次两技能合并推送被官方服务 HTTP 422 拒绝，正文明确 aggregate skills Arcade push may modify only one skill。改为每次单技能发布后，路由提交 fe57639 推送成功。
- 独立执行上下文实际通过 skills.read(e1/gpt-windows-execution-bridge) 读取 V12.0.1；动态发现 A，list_devices 后用 A list_directory 成功读取 C:\AI\ComfyUI_Aaki_v3，无 B 调用、无服务与文件写入。此为独立 agent 上下文验证，不冒充用户浏览器真实新 GPT 页面的完整验收。
- 当前用户截图对应页面的完整历史调用仍未取得；不能断言已对正在运行的所有页面施加强制路由。