# B32 同浏览器“新聊天”薄接力适配

唯一用途：在**已完成合法Freeze**后，把 GPT 生成的唯一 `NEXT_PAGE_PROMPT` 交给现有普通 Chrome 浏览器的同一 ChatGPT 窗口，动作仅限获取信封→点击新聊天→粘贴提交。不是 n8n、不是专用浏览器9223、不是通用新状态机。

成熟底座：本机已检测存在 AutoHotkey v2 `C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe`；界面控件使用 MIT 许可的 `Descolada/UIA-v2`，上游仓库 https://github.com/Descolada/UIA-v2 ，已核对提交 `2846a9b10518a95cf26a6c43671a9512b231ccb7`，成熟的 `Lib/UIA.ahk`，不得以自行开发浏览器控制器取代。运行目录将成熟 `UIA.ahk` 与源LICENSE置于 `Lib\`，独立持久保存上游来源、提交与许可。

`B32_Handoff.ahk` 默认只读预检。传入由任务写者签发、已核验实际GitHub Freeze的UTF-8恢复信封文件，必须包含TASK_ID、FREEZE_ID和START_HERE.md。第二参数 `--commit` 才允许实际点击新聊天与提交一次，此前须经过用户授权、任务指针和当前目标ChatGPT窗口核对。输入只针对当前前台Chrome ChatGPT窗口，找不到指定UIAutomation控件即拒绝，不猜坐标，不启动其它浏览器。不支持当前非Chrome浏览器/未显示ChatGPT窗口；这是当前最小适配候选边界。

注意：**`SUBMIT_ATTEMPTED_ONCE` 不表示 ChatGPT 已收到**，必须另由实际接管确认信息验证。任何UNKNOWN均禁止盲重试；不能把脚本存在或静态语法通过当成自动接管的现实验收。此脚本不具备任务状态存储、通用事件触发、持续队列或业务重试功能。

## 2026-10-09 真实局部验证（不发送）
- 已用 Windows Desktop Commander 在线主路定位并调用现有 `C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe`，本地部署位于 `C:\AI\B32_ChatGPT_Handoff\B32_Handoff.ahk`；其`Lib/UIA.ahk`来自成熟上游锁定提交 `2846a9b10518a95cf26a6c43671a9512b231ccb7`。
- 第一次语法检查定位并修正了 AHK v2 的保留标识符 `edit`，随后 `/ErrorStdOut` 重新运行：不提供信封时 `AHK_EXIT=11`、`FAIL:NO_PROMPT_FILE`，没有语法错误。
- 准备含TEST_ONLY标记的信封，**不传`--commit`**：当前前台 Chrome 页面不是被校验的 ChatGPT 页面，脚本返回 `READ_ONLY_EXIT=14`、`BLOCKED:ACTIVE_WINDOW_NOT_CHATGPT`；没有点击、没有粘贴、没有发送。这是失败安全路径通过，**不是** ChatGPT新聊天自动接力成功。
- 当前尚未证明可在真正ChatGPT页面定位“新聊天”控件及编辑框，更未证实一次提交之后新会话准确恢复Freeze和唯一写者。实际功能继续标记`HANDOFF_AUTOMATION=UNVERIFIED`、`VIRTUAL_MATURE=NO`。
- 不使用专用浏览器9223、n8n、Playwright HTTP MCP18931，也未改 FlClash 或其它浏览器设置。
