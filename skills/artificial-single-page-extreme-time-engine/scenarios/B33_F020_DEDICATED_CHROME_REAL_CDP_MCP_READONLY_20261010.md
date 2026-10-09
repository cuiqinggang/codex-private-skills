# B33 F020：改用已登录专用浏览器的真实联通测试
DATE=2026-10-10
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
PARENT_FREEZE=B33-VM-F019
CONTRACT_VERSION=4
METHOD=B33/B29/B23
BROWSER=EXISTING_CHROME_FOR_TESTING_PRIVATE_PROFILE
BROWSER_CDP=127.0.0.1:9223
BROWSER_REMOTE_DEBUGGING=EXISTING_NOT_CHANGED
REAL_CHROME_CONNECTIVITY=PASS
REAL_CHATGPT_TABS_READONLY=PASS_2_TABS
REAL_AUTO_NEW_CHAT=NOT_TESTED
REAL_AUTO_SHORT_CODE_SEND=NOT_TESTED
REAL_NEW_GPT_RECOVERY=NOT_TESTED
END_TO_END_VALID=NO
VIRTUAL_MATURE=NO
FINAL_VALID=NO
PLATFORM_SAFETY_BLOCK=EXISTING_UNRESOLVED

## 当前真实执行事实
用户明确取消本轮普通Chrome路径，指定专用已登录AI浏览器；没有关闭已有浏览器、没有修改FlClash，也没有新建Profile。
Windows设备DESKTOP-4A1EGTM经Remote Desktop Commander在线。只读CIM检测专用Chrome运行进程确有--remote-debugging-port=9223及--user-data-dir；原普通Chrome没有CDP标志，不与专用混用。
本机通过127.0.0.1:9223/json/version真实请求HTTP200，CDP返回Chrome/151.0.7922.34。127.0.0.1:9223/json/list真实请求HTTP200，耗时约180ms，读取22个CDP Target；type=page且URL主机=chatgpt.com的共2个，其他含iframe、service_worker和worker。只展示host，不保存私有聊天文字。
复用本机已安装微软@playwright/mcp CLI，使用--cdp-endpoint http://127.0.0.1:9223直接附着现存专用Chrome。使用已安装的标准Model Context Protocol SDK Client和STDIO Transport仅执行browser_tabs action=list：返回PASS，发现24个MCP工具，实际列出2张真实ChatGPT标签。完整启动/连接/读取耗时45290ms，脚本随后正常结束，未执行click、send、导航或更改当前页面。
本地记录/只读探针：
C:\AI\B32_ChatGPT_Handoff\B33_DedicatedChrome_ReadonlyDiscovery.ps1
C:\AI\B32_ChatGPT_Handoff\B33_DedicatedChrome_Targets_9223.ps1
C:\AI\Hatchet-Isolated-V1\mcp-probe\b33_dedicated_playwright_readonly_20261010.mjs

## 合同与结果边界
本节点确认的是已有专用Chrome与Microsoft Playwright MCP的真实浏览器读取端到端PASS，比仅STDIO tools/list更深入。45290ms包含MCP初始附着/连接，不是ChatGPT自动发送时间或稳定热态调用时间。较快约180ms属于本机CDP HTTP只读枚举，也不是ChatGPT业务T_VALID。
此前B33官方ChatGPT自动发送的远程操作受到OpenAI平台工具预派发安全检查明确拒绝，原B33_Handoff.ahk --commit仍保护性exit90；当前不得为了证明专用浏览器可写而用新CDP/MCP通道绕过同一受限官网发送。用户更改浏览器目标并不取消平台安全规则。
本轮因此没有点击真实ChatGPT新聊天、没有提交短码，新GPT恢复未发生，FULL_AUTO_VALID=NO；属于真实联通到只读控制层、下一写入环节受限。单次测试耗时不能宣称秒级自动完整交接。
主任务合同由V3→V4仅限浏览器执行环境变更，方法引擎B33/B29/B23与其他任务/公共路由不变。真实发送需在平台允许的同浏览器控制入口且独立TEST会话所有权可证明时，才能开展恰好一次写入及新GPT接管的完整现实验收；不能重发旧UNKNOWN码。
