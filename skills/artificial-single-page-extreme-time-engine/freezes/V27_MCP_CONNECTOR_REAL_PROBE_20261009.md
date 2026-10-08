# V27 MCP连接器实际核验｜未达最终成熟门
日期 2026-10-09；ENGINE=27 BRAIN=24 NPT=17
状态：CONNECTOR_INSTALLED / PROTOCOL_CLI_PASS / END_TO_END_MCP_UNKNOWN / VIRTUAL_MATURE=NO / STOP_GATE=NO / REALITY_NOT_RUN
设备：DESKTOP-4A1EGTM，连接 Desktop Commander 当前在线。

已完成事实：
- Windows隔离目录 C:\AI\Hatchet-Isolated-V1\mcp-probe 中存在 npm 包 supergateway@4.1.0 和 @modelcontextprotocol/server-everything@2026.8.31；CLI help 实际输出，支持 --stdio、--streamableHttp、--outputTransport streamableHttp、--stateful 与超时参数。
- 原正式Playwright MCP独立进程正在运行，命令形态 node @playwright/mcp/cli.js --config C:\AI\Playwright-Native-AI-Browser\app\mcp.config.json，config使用已登录共享浏览器 profile\shared-mcp，故不能为试验另启一个竞争性 MCP/profile 进程。还存在其它MCP相关进程，必须先辨明唯一owner。
- 原 Playwright Native AI Browser 技能包明令单个有效写入者和 fencing；只有合法授权客户端可经既有 STDIO MCP 调用已审核业务入口。不能因安装协议代理就自动拥有该进程的STDIO管道。
- 既有n8n localhost健康端点20次HTTP200，中位约4.634ms/样本最大55.078ms；该数据绝非MCP链路端到端延迟。
- 原 F011 Reality 5任务总115.670s。先前离线模型在零新增连接开销、发送前全串行且发送后重叠的条件下76.824s，预计节省38.846s，33.583%；这是条件性虚拟参照，不是经端到端工具验收的 T_VIRTUAL_BEST。

关键缺口：
1 原STDIO MCP进程的所有者及安全复用入口未核实，无法直接把一个独立Supergateway接到当前进程；不创建第二个profile进程或未授权监听服务。
2 没有进行 n8n MCP Client → Supergateway → 原正式Playwright MCP tools/list 的实际端到端测试，完整开销 T_MCP 未测。
3 浏览器持有单写者范围、页面归属、发送后等待释放与崩溃恢复尚未验证，不能将模型中通过的排他规则测试冒充Reality。
下一步：从持有原STDIO MCP的授权客户端/现有进程管理入口验证可共享的官方连接方式，或在合法受控维护窗口中仅由单一owner替换当前连接为持久单实例网关；先工具发现和延迟，不发送消息；完成后重算模型、重复虚拟迭代到净收益停止，再Freeze→一次整体Reality。
本件为故障证据而非完成冻结，严格禁止VIRTUAL_MATURE=YES。
