# B32 同浏览器“新聊天”薄接力适配

唯一用途：在**已完成合法Freeze**后，把 GPT 生成的唯一 `NEXT_PAGE_PROMPT` 交给现有普通 Chrome 浏览器的同一 ChatGPT 窗口，动作仅限获取信封→点击新聊天→粘贴提交。不是 n8n、不是专用浏览器9223、不是通用新状态机。

成熟底座：本机已检测存在 AutoHotkey v2 `C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe`；界面控件使用 MIT 许可的 `Descolada/UIA-v2`，上游仓库 https://github.com/Descolada/UIA-v2 ，已核对提交 `2846a9b10518a95cf26a6c43671a9512b231ccb7`，成熟的 `Lib/UIA.ahk`，不得以自行开发浏览器控制器取代。运行目录将成熟 `UIA.ahk` 与源LICENSE置于 `Lib\`，独立持久保存上游来源、提交与许可。

`B32_Handoff.ahk` 默认只读预检。传入由任务写者签发、已核验实际GitHub Freeze的UTF-8恢复信封文件，必须包含TASK_ID、FREEZE_ID和START_HERE.md。第二参数 `--commit` 才允许实际点击新聊天与提交一次，此前须经过用户授权、任务指针和当前目标ChatGPT窗口核对。输入只针对当前前台Chrome ChatGPT窗口，找不到指定UIAutomation控件即拒绝，不猜坐标，不启动其它浏览器。不支持当前非Chrome浏览器/未显示ChatGPT窗口；这是当前最小适配候选边界。

注意：**`SUBMIT_ATTEMPTED_ONCE` 不表示 ChatGPT 已收到**，必须另由实际接管确认信息验证。任何UNKNOWN均禁止盲重试；不能把脚本存在或静态语法通过当成自动接管的现实验收。此脚本不具备任务状态存储、通用事件触发、持续队列或业务重试功能。
