# B33 F019｜三条无人值守自动接力候选：联通优先，拒绝人工基线充当产品
DATE=2026-10-10
MASTER_TASK=B_SINGLE_PAGE_MATURITY_20261009
PREVIOUS_FREEZE=B33-VM-F018
USER_GOAL=FULLY_AUTOMATED_EXISTING_CHROME_NEW_CHAT_SINGLE_SHORT_CODE_GITHUB_RECOVERY
EVALUATION_ORDER=REAL_CONNECTIVITY_THEN_COMPARE_FULL_T_VALID_THEN_OPTIMIZE
MANUAL_CHROME_AS_AUTO_CANDIDATE=REJECTED
AUTO_END_TO_END_PASSES=0_OF_3
REAL_AUTO_HANDOFF_VALID=NO
VIRTUAL_MATURE=NO
FINAL_VALID=NO

## 约束与曾经的选型偏差
人工T02实测382.518秒（含人为打开新聊天/等待、GPT工作与GitHub提交）是同合同人工接续的历史对照样本，不是无人值守候选，绝不据此宣称B33速度已成熟。F014原生AHK/UIA 578ms到本地固定模拟ACK也是离线局部计时，不是任何官网真实GPT恢复时间；不能把局部耗时误当完整任务。

## 不凑数的三个成熟自动候选
1. 官方OpenAI ChatGPT Chrome扩展+桌面Work/Codex浏览器控制。OpenAI官方文档确认可连接已有Chrome浏览器的标签与登录状态，无须新Profile。Windows已发现本机官方ChatGPT扩展version=1.26.901.11451且桌面ChatGPT运行；但当前聊天可调用工具没有Work Chrome控制入口，也未证明该模式获准自动对chatgpt.com自身操作并完成短码恢复，因此同合同AUTO_VALID=NOT_TESTED、T_VALID=UNKNOWN。官方文档https://learn.chatgpt.com/docs/chrome-extension、https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app。
2. B33已有Windows AutoHotkey v2+Descolada UIA-v2薄接力，原Chrome最小原生动作。离线真实UIA严格同构3/3PASS，模拟ACK中位578ms；Windows真实正式适配安全回归10/10PASS。但实际--commit自动官网交接受PROTECTED_CHAT_HARD_STOP保护exit90，先前由工具安全层明确拒绝的自动ChatGPT发送尚未获得允许，AUTO_VALID=BLOCKED、T_VALID=UNKNOWN，不允许拆解/更换执行工具去绕过。
3. A路线已通过的n8n原生MCP Client 1.1+官方Playwright MCP+现有浏览器与原业务query/send/wait_extract，必要时仅用n8n原生Remove Duplicates/Wait。A侧历史已经真实验证浏览器标签读取、可逆DOM写入、跨流程串行、去重与重启恢复；本地发现既存C:\AI\n8n部署文件和V27两节点Manual Trigger→MCP Client工作流。但没有真实new_chat+短码一次官网提交+新GPT任务恢复的同合同结果，AUTO_VALID=NOT_TESTED/NOT_CONNECTED, T_VALID=UNKNOWN；当前Docker在线状态本轮只读命令被安全审查拦截。n8n官方MCP Client文档https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcpClient/ 和Playwright官方文档https://github.com/microsoft/playwright-mcp。
以上三者的成功概率/最终时间未形成可比的统计样本，禁止声称哪一个“真实最快”，也不允许以安装状态、MCP浏览器读成功冒充正式同合同PASS。

## 联通验收唯一口径
无人工复制/切换：GPT完成自然节点→真实Freeze与CURRENT指向一致→成熟控制入口在原已登录Chrome的正确、独立归属的TEST聊天内执行新聊天→准确四字段码**仅一次提交**→真实新GPT从GitHub正确恢复→实际完成同质量测试任务→GitHub状态核验PASS。记录从合同接单到有效成果的完整T_VALID、失败/UNKNOWN三态、不允许修改FlClash/关闭用户浏览器/新造通用调度/锁。
如果既有明确平台工具安全拒绝仍在，不能以别的桥、n8n、AHK或扩展去规避拒绝的相同自动官网提交；新通道的合法性和动作权限必须明确、且是单独授权的正常产品功能。用户明确希望无人工，并不解除平台安全限制。只在获准的执行界面有真正的实时浏览器控制能力时开展一次新的隔离端到端实际验收；在此之前联通门阻塞，不再用人工T02替代成功，也不再重复离线模拟或空算最短秒数。
CURRENT_BEST_VALID_FULLY_AUTOMATED=NONE
SPEED_RANKING=NOT_POSSIBLE_0_OF_3_AUTO_VALID
