# EXP-ONION-TOR-20261103-001｜Tor Browser GUI与本机MCP分层验收

版本：V1｜证据日期：2026-11-03（北京时间）｜类型：CASE + ERROR + SKILL_CANDIDATE｜证据等级：有源项目验收文字及工具返回摘要，原始截图文件未单独归档

## 触发与环境
已有Windows Tor Browser无法连接，历史V3的GUI为FAIL，独立Tor SOCKS通过不能替代浏览器自身。V4复用已连接的D插件作为远程传输、现有本机windows-mcp-v1 stdio作为桌面截图/点击工具，不重装、不修改代理、FlClash、torrc或Windows系统。

## LAST_GOOD → FIRST_DELTA → 最小修复 → 回归
- LAST_GOOD：D往返可用、本机Codex已有windows-mcp-v1配置、Tor窗口已存在。
- FIRST_DELTA：D本次命令入口按cmd解释，错误的前置&语法失败；中文stdio发生编码问题；Python SDK的is_error与序列化isError混淆；英文Tor Browser窗口名误切Chrome；GUI标题出现不代表官网正文加载完。
- 最小修复：按本轮shell选合法PowerShell调用语法，显式UTF-8和ASCII转义JSON，按序列化字段判错；先获取实际Snapshot再以精确中文窗口名操作、确认每步画面；沿原生GUI点击连接。
- 回归：V4项目记录Tor Browser内官方检测页绿色PASS及官方网站中文正文PASS；本机DisplayInventory脚本20:45退出0；前两次错误退出1均留作失败。V3 GUI FAIL不抹去，作为较早时间事实保留。

## 适用/不适用
适用：已有授权的Windows桌面、明确工具返回并可看图确认、原生GUI重试及异常定位；按当前宿主/SDK版本动态发现，不能硬编码旧插件名字。
不适用：把D传输等同MCP桌面、把独立Tor/官网普通浏览器可访问等同Tor Browser成功、自动保证下次重启/浏览器.onion/跨终端传输、在平台拒绝后换接口绕行。
未测：浏览器正常重开、整机重启、浏览器.onion、外部OnionShare传输；完整T_VALID=NOT_MEASURED。

## 权威证据
- [V4项目真实验收](../../onion-network-superpowers/references/acceptance-v4.md)
- [V4故障与修复](../../onion-network-superpowers/references/troubleshooting.md)
- [V4连接分层步骤](../../onion-network-superpowers/references/connection-runbook.md)
- 原Vault历史V3：03_SKILLS/onion-network-superpowers/STATUS-V3.md；项目本身仍为权威，不用本卡替换。
- 无新的共享EXP卡采用/拒绝业务回执，不凭空创建usage。