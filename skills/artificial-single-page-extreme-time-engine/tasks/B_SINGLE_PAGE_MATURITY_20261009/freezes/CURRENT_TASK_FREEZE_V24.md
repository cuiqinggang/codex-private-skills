# B33 F024｜恢复原有专用浏览器网页界面自动化主线（路线明确）
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
FREEZE_ID=B33-VM-F024
FREEZE_VERSION=24
PREVIOUS_FREEZE=B33-VM-F023
CONTRACT_VERSION=4
METHOD_ENGINE=B33
METHOD_BRAIN=B29
METHOD_TEMPLATE=B23
TASK_BROWSER_VARIANT=EXISTING_DEDICATED_CHROME_CDP_9223
CURRENT_DECISION=REUSE_MATURE_NATIVE_BROWSER_GUI_UIA_NO_N8N
BROWSER_CONTROL_ROUTE=原有专用浏览器真实网页界面控件（AutoHotkey v2 + Descolada UIA-v2；优先原有正式入口）
N8N_REQUIRED=NO
SECOND_BROWSER_REQUIRED=NO
CHATGPT_API_DIRECT_SEND_REQUIRED=NO
NATIVE_GUI_ASSETS=C:\AI\B32_ChatGPT_Handoff\B33_Handoff.ahk
SKILL_REFERENCE=C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\references\MATURE-OPERATIONS-CONTRACT.md
STATE_SOURCE=GitHub主任务CURRENT + 最新合法Freeze
GUI_ACTIONS=验证目标浏览器窗口和聊天归属→新聊天控件→输入框聚焦→剪贴板粘贴四字段码→读回校验→恰好一次提交→官网回执验证
EXACTLY_ONCE=REQUIRED
UNKNOWN_RESEND=FORBIDDEN
EXISTING_COMMIT_HARD_STOP=PRESERVED
PLATFORM_PRIOR_BLOCK_SCOPE=此前为自动发送准备脚本的工具调用遭预派发安全拒绝；不可推断所有正常网页操作均被禁止，亦不得换工具规避同一具体拒绝
REAL_GUI_OFFLINE_NATIVE_3_OF_3=PASS_HISTORICAL
REAL_DEDICATED_BROWSER_NEW_CHAT_NO_SEND=PASS_F023
REAL_CHATGPT_AUTO_SEND_THIS_NODE=0
NEW_GPT_GITHUB_FREEZE_RESUME=NOT_TESTED
FULL_AUTO_HANDOFF_VALID=NO
FULL_AUTO_T_VALID=UNKNOWN
VIRTUAL_MATURE=NO
STOP_GATE=NOT_PASSED
FINAL_VALID=NO

## 依据
用户明确要求恢复过去长期使用的网页控件复制、粘贴、发送路线，而不是把“代码对代码/CDP调用”作为主线。2026-10-10读取Windows现有C:\AI\B32_ChatGPT_Handoff\B33_Handoff.ahk：已完整具备UIA选中Chrome标签/Doc、验证chatgpt.com域名、按目标HWND/URL绑定、寻找New chat控件、SetFocus、ClipboardAll与Ctrl+V、粘贴读回核验、Enter一次的成熟实现；其 --commit 当前最先触发PROTECTED_CHAT_HARD_STOP且返回90，保护不得绕过。本机B33_F013_NativeThreeTiming.json：原生本地离线页面3/3 PASS（593/578/578ms内部计时）；不是官网发送。
上一F023已在现有专用Chrome中使用Playwright完成真实新测试标签、新聊天点击和编辑框就绪，16.887秒，无消息发送，清理后标签数量恢复2；该事实不等于AHK正式网页交接成功。
历史安全诊断表明OpenAI预派发拒绝发生在准备真实发送相关脚本的工具调用；拒绝具体策略原因未公开。普通用户在官网手动复制粘贴没有经此记录被禁止的证据，但“真人手动网页操作允许”亦不等于“程序自动发送获得许可”。不更换CDP/UIA以绕过同一安全拒绝，不自行移除保护锁。

## 下一门
仅在正式获准的自动发送入口及独立测试聊天归属/唯一短码得到证明后，复用原有GUI动作完成官网发送、回执与新GPT真正读取GitHub CURRENT/Freeze、继续任务和统一T_VALID一次验收。其余已PASS连接/离线动作不重测。保持原专用浏览器和FlClash不变，不新增n8n层或自研框架。
