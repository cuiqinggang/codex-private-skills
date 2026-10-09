# B32 现成GPT浏览器代码交接技能复用审计 V1
DATE=2026-10-09
ROUTE=B32/B29/B22
STATUS=READ_ONLY_AUDIT｜NO_REAL_CHAT_SEND｜VIRTUAL_MATURE=NO｜FINAL_VALID=NO

## 从网络权威仓库寻回的历史技能
1. `skills/chatgpt-web-plan-bridge-latest/SKILL.md`：2026-05历史备份，使用Chrome CDP 9333、WSL 9334、agent-browser snapshot/click/fill/press/send。曾验证英文与UTF-8中文实际消息送达，但使用独立调试Chrome，与B32普通Chrome“不新建专用浏览器”硬约束不相容。
2. `skills/ChatGPT官网规划桥接_让Codex读取GPT方案并执行_最新/SKILL.md`：同SHA旧技能备份。
3. `skills/absolute-time-fireworks-optimization/references/EXECUTION-BRIDGE.md`：明确指向现役 `playwright-native-ai-browser` 成熟浏览器通信桥，不需新建一套桥接系统。

## 本机现役更成熟的实际代码交付入口（已只读核验）
- `C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md`
- `C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js`
- 正式入口通过已存在专用 Playwright 的 STDIO MCP `browser_run_code_unsafe` 运行，使用 `sessionStorage.__pw_native_business_task_v1` 提交唯一任务合同。
- 该脚本操作 `query`（查询是否已提交）、`send`（定位contenteditable、fill、send-button.click、确认DOM中的用户marker）、`wait_extract`（读取对应回复、Markdown/代码/表格）。在发送前按marker去重；回执不明禁止盲重发。
- 尚不支持 `new_chat` 原生操作；现存正式技能禁止绕开入口用 ad-hoc browser_click 冒充真实业务发送。不能将“支持send”推断为完整B32新聊天接力已验收。

## 历史真实性能：`evidence\upstream-reuse-20260905\RAW-TIMING.json`
2026-09-05六轮真实ChatGPT测试：6/6结果正确，确认重复发送=0。
- B-R2直接输入`readyToSend=560ms`，随后点击到DOM确认`sendToConfirm=911ms`；即从准备填入到页面确认该轮为1471ms，**尚不含新会话创建或整任务执行**。
- 六轮`readyToSend`中位数2139.5ms，且记录了用户题目、浏览器调度、结果保存与验证等更多耗时。不能把局部代码填充或一次MCP子调用视作完整T_VALID。
- 同一历史用例的6轮完成后DOM提取延迟6-20ms；此为后处理速度，不代表新会话准备/模型首字延迟。

## 当前B32现有普通Chrome与专用调试浏览器的不同
- 本次只读CIM过程检查：普通Chrome进程PID 16036（仅测试时点）不存在 `--remote-debugging-port` 或 `--remote-debugging-pipe` 标志；另一套Chrome for Testing配置了9223，属A/专用路线，不能混用或临时打开第二浏览器。
- Playwright的 `connectOverCDP` 需要已经开放的Chromium CDP端点。普通Chrome无现存合法代码注入/扩展接管入口的证据，故现成专用浏览器脚本不能直接控制普通Chrome标签页。
- 2025-03-17 Chrome官方公告：Chrome136+的默认用户数据目录不再认可remote-debugging开关；不为了B32更改原用户浏览器profile/登录状态/代理/调试配置。

## REUSE_GATE 决策（唯一边界）
- B32仍采用已存在AutoHotkey v2+Descolada UIA-v2，当前普通Chrome中直接元素查找`新聊天`的实际只读三次查找16/31/31ms（进程总墙钟761ms）。这是基于成熟无障碍控件的**代码控制UI**，不是肉眼识别、截图或鼠标坐标猜测。
- 已存在Playwright原生代码发送/回执/幂等成熟方法：复用契约与事实，不迁移独立profile，不为单次简单交接安装整套专用浏览器，也不重造浏览器控制器。
- 如有用户授权且现有原Chrome确实提供已验证的受支持浏览器内代码连接，则优先复用上述正式入口和原文脚本，按相同Freeze、新聊天接续、错误对账、T_VALID质量标准成对测试，净收益正才采用。
- `T_B32_VALID=UNKNOWN`：未实现真实新聊天发送与GPT接管，绝不声称四动作已经毫秒完成或虚拟成熟成功。
- 本文件是复用审计，不改变B32方法版本、TASK冻结指针或已登录浏览器。

## 2026-10-09 后续 B32 最短路径选型（无需升版）
- 用户放开“必须普通浏览器”的绝对条件，允许普通/专用二选一；但当前要求**无Codex、无n8n、只在原有聊天标签中打开新聊天、四步交接**。
- 当前Windows在线只读观察：普通 Chrome 运行、未开启CDP；另有Chrome for Testing专用实例，CDP9223由其使用。现成 B32 AutoHotkey v2+UIA-v2可在普通Chrome定位唯一“新聊天”控件；窗口级 UIA 直接查找三轮为16/31/31ms，含初始化的只读进程墙钟761ms。正式脚本原有450ms+350ms固定等待，但未完整实测发送，不能将其算为必要物理极限。
- 已验证专用Playwright历史代码无需截图：`chatgpt-business-entry.js`直接DOM fill、send-button click、可选query/wait_extract，但现存正式通道使用Codex/MCP及专用浏览器所有者。历史最快一轮填入到DOM确认1471ms，不是与UIA同边界比较，也不涵盖创建新聊天。
- **当前执行选择：普通Chrome + 现成AutoHotkey/UIA控件代码，一次本机进程调用完成“复制信封→同标签新聊天→粘贴→提交”**。不增加Codex、n8n、9223/18931或新开发调度器；专用浏览器仅保留为未来同边界实测净收益更高时的候选，不强制。
- 最小安全前置：当前任务成功Freeze、正确的现有Chrome/ChatGPT标签页身份已绑定、只有一个可见新聊天入口、提交一次。侧边栏开/合使用**相同语义控件“新聊天”**，不依赖图标坐标/截图；收起状态已识别，展开状态仍未实测。发送不必等待模型完整答复或做复杂内容提取；但脚本click返回**不是服务器已经接收的证明**，如动作结果UNKNOWN不得盲重发。新标签不是要求：点击“新聊天”可在当前标签切换会话，旧聊天留在历史记录中，不会凭此被物理关闭。
- 最终四步总耗时/端到端T_VALID依然UNKNOWN；不得把局部UI定位的毫秒级速度冒充GPT自动接续成功。不可擅自干扰用户当前对话；授权后统一完整实测。
