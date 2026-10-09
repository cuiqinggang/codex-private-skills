# B33 F022｜专用浏览器直接代码联通现实冻结（无 n8n）
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
FREEZE_ID=B33-VM-F022
FREEZE_VERSION=22
PREVIOUS_FREEZE=B33-VM-F021
CONTRACT_VERSION=4
METHOD_ENGINE=B33
METHOD_BRAIN=B29
METHOD_TEMPLATE=B23
TASK_BROWSER_VARIANT=EXISTING_DEDICATED_CHROME_CDP_9223
STATUS=DIRECT_PLAYWRIGHT_CDP_READONLY_REALITY_PASS_AUTO_HANDOFF_BLOCKED
SELECTED_RUNTIME_ROUTE=GPT→Windows双路执行桥主路→现有Playwright→专用Chrome CDP9223
N8N_REQUIRED_FOR_DIRECT_PATH=NO
DESKTOP_COMMANDER_DEVICE=f6990966-5870-484b-bf79-409bc6fb963e
DESKTOP_COMMANDER_ONLINE=YES
CDP_READONLY_HTTP=200
CDP_READONLY_HTTP_WALL_S=0.001611
DIRECT_PLAYWRIGHT_CONNECT_OVER_CDP=PASS
REAL_CHATGPT_TABS=2
CHATGPT_COMPOSER_PRESENT_PER_TAB=1,1
CHATGPT_NEW_CHAT_MATCHES_PER_TAB=4,3
SEND_BUTTON_MATCHES_IN_EMPTY_COMPOSERS=0,0
REAL_NEW_CHAT_CLICK_THIS_NODE=0
REAL_AUTOMATED_CHATGPT_SEND_THIS_NODE=0
REAL_GPT_RESUME_THIS_NODE=NOT_TESTED
FULL_AUTO_CHATGPT_HANDOFF_VALID=NO
FULL_AUTO_T_VALID=UNKNOWN
VIRTUAL_MATURE=NO
STOP_GATE=NOT_PASSED
FINAL_VALID=NO

## 实际验证
2026-10-10，通过在线 Windows Desktop Commander Remote 在已安装的 C:\AI\Playwright-Native-AI-Browser\node_modules\playwright 上运行 Node 一次性只读调用，chromium.connectOverCDP(http://127.0.0.1:9223) 附着原有专用浏览器成功；不启动第二浏览器。枚举原已有两个 https://chatgpt.com 标签，在各自页面以 page.evaluate 只读查询 DOM，均找到一个 [contenteditable=true][role=textbox] 编辑框；按可见文字/aria-label 找到“新聊天”入口分别4、3处；空编辑框下未找到 data-testid=send-button。此结果不意味着发送不可用或自动发送已验收。
同轮 curl.exe 只读探测 CDP /json/list HTTP200（约1.611ms，只是接口时长）。本轮没有新聊天点击、输入、发送、导航、配置或代理变更；没有使用 n8n。
已读成熟脚本 C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js：其 send 操作已经使用真实网页编辑框 fill+submit.click；“代码直连”和“换网页模拟点击”不是绕开平台拒绝的不同许可。既有 OpenAI 预派发自动发送安全拒绝未解除，不利用 CDP/GUI/n8n 改道尝试发送。

## 决议及下一步
本任务直接路线不必经 n8n；原A n8n 业务闭环及持久化能力保留作为可选成熟资产，不重测也不拆除。
只在获得明确平台允许的 ChatGPT 自动发送会话入口和独立任务归属后，进行真实新聊天→四字段短码恰好发送一次→新GPT从GitHub读取Freeze并继续→FINAL_VALID、统一 T_VALID 验收。否则停止在平台发送授权层。Exactly-once、UNKNOWN不重试和不影响现有用户聊天继续有效。
