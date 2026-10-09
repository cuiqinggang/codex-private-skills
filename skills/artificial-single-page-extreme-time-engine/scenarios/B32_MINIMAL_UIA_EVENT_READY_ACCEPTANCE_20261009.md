# B32 语义控件四动作与取消固定等待：验证记录

任务：B32 单页面原聊天→新聊天交接，维持B32/B29/B22方法版本，不引入Codex/n8n/专用浏览器。
日期：2026-10-09
实际现存底座：Windows AutoHotkey v2 + Descolada UIA-v2，原普通Chrome。
状态：LOCAL_AND_GITHUB_PATCHED；VIRTUAL_RULE_TEST=16/16_PASS；REAL_READ_ONLY_PRECHECK=PASS_WHEN_CHATGPT_ACTIVE；FULL_CHAT_HANDOFF=BLOCKED_NO_VERIFIED_TARGET；VIRTUAL_MATURE=NO；FINAL_VALID=NO。

## 本轮最小修改（真实代码）
文件：`routes/B/adapter/B32_Handoff.ahk`，本机：`C:\AI\B32_ChatGPT_Handoff\B32_Handoff.ahk`
GitHub修订提交：`a2c3c99d38b034e742f81cb2292db1729b346360`。
- 用现有UIA按`Type=Button, Name=新聊天`找到可操作控件；无需区分展开/收起、尺寸、坐标、截图。
- 点击后撤销固定`Sleep 450`，使用现成UIA树的可用输入框条件检测，20ms仅在未就绪时循环，2秒仅为失败超时上限。
- 点击后先确认原聊天已经切到ChatGPT新聊天根路由，防止在旧聊天误发。
- 粘贴后撤销固定`Sleep 350`，读取输入框Value或TextPattern内容，完整匹配冻结信封才按Enter一次。未知/不匹配禁止盲发。
- 已保留信封格式验证、ChatGPT来源验证、错误窗口拒绝、无业务虚拟测试信封误带--commit直接拒绝。
- 不属于新造通用状态机或通用浏览器控制器：原成熟AutoHotkey/UIA薄适配最小修改。

## 无发送现实检查
已在正确前台普通Chrome的ChatGPT页面测试：
- 普通只读预检`DRY_RUN:NEW_CHAT_CONTROL_FOUND_NO_SEND`，退出码0，墙钟1227ms；下一次1077ms。
- 不存在信封：`FAIL:PROMPT_NOT_FOUND`（退出码12，219ms）。
- 格式不合格：`FAIL:UNVERIFIED_ENVELOPE`（退出码13，187ms）。
- 虚拟信封加--commit：`BLOCKED:TEST_ENVELOPE_COMMIT_FORBIDDEN`（退出码21，1070ms），未发送。
- 后续预检遇到普通Chrome不在前台：`BLOCKED:ACTIVE_WINDOW_NOT_CHATGPT`，退出码14，218ms；安全停止。
- 新的静态检查：固定450/350ms均不存在；20ms条件轮询、根路由门禁、全文核验、虚拟提交保护都存在。
- 同机实际脚本SHA256：`10926ACADAAE744EA7AC92151CE789B3BF13D5F036EA7CB62321BB8371D3FA64`。

## 独立真实烟雾测试准备与阻塞
独立无业务测试TASK_ID=`B32_UI_HANDOFF_SMOKE_20261009`，冻结`B32-UI-F001`及CURRENT真实存在；本机有唯一带ACK标记信封。
真正准备执行一次`--commit`前，安全只读检查发现Windows前台是`explorer.exe / Program Manager`，不是普通Chrome；普通Chrome现有活动页URL不是ChatGPT，UIA共发现14个TabItem，但不能唯一找到本任务ChatGPT标签（只读分类未发现匹配）。另一个现有`Chrome for Testing`浏览器不可替代原普通Chrome交接的事实验收。
因此**未切换任何标签、未点击新聊天、未粘贴或发送**；这不是完整交接通过。不得以找到了按钮或打印提交日志冒充成功。
真实端到端耗时、创建新聊天到可输入耗时、最终ACK均UNKNOWN。

## 冻结和下一动作
方法B32保留。当前状态：可执行代码已更新、局部只读安全验证PASS；正式虚拟成熟/完整Reality尚未通过。
只有目标普通Chrome的ChatGPT任务标签实际可确认，才允许经授权唯一无业务发信实验；否则停止。不重造浏览器进程、不擅自切换Chrome for Testing、不启动Codex或n8n、不更改代理、不恢复固定等待。无需用户手动复制复杂配置。
