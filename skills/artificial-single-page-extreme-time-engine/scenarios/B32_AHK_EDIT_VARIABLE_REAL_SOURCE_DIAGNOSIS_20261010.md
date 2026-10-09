# B32_Handoff.ahk「edit」变量冲突｜现实源文件差分诊断
日期：2026-10-10
错误症状（用户提供截图文字）：`This Func cannot be used as an output variable. Specifically: edit`；`056: edit := 0`。
STATUS=SOURCE_CURRENT_ALREADY_USES_SAFE_VARIABLE_NAMES
REAL_CURRENT_SCRIPT_NO_ARGS_PARSE=PASS
REAL_BUSINESS_SEND=NOT_TESTED
ENGINE29_RELEASE=NOT_COMPLETE

## 不混淆的两件事
GitHub官方Contents API `update_file` 曾成功写入本技能包（提交c443c792...），与Windows本地AHK脚本能否启动没有直接依赖。
统一ENGINE29方法发布在其他独立调用中被ChatGPT/OpenAI工具预派发安全检查拒绝；当前 `ENGINE.md` 仍第28版，`SKILL.md`/ `START_HERE.md` 仍带A/B分流；不能因AHK启动成功就宣布ENGINE29上线，也不得为绕过原拒绝重复/拆分已受阻的同一发布动作。

## 当前实际核对
- Windows实盘路径：`C:\AI\B32_ChatGPT_Handoff\B32_Handoff.ahk`，160行，SHA256 `10926ACADAAE744EA7AC92151CE789B3BF13D5F036EA7CB62321BB8371D3FA64`。
- GitHub正式历史源码：`routes/B/adapter/B32_Handoff.ahk`，内容亦使用 `composerEl` 与 `candidate`，不含 `edit := 0`。这两个位置的当前源文件已排除截图中的命名冲突。
- Windows源码第56行实际为 `if (!button.IsOffscreen && button.IsEnabled) {`，不是截图显示的 `edit := 0`。
- 实测命令（无发送）：`& 'C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe' /ErrorStdOut 'C:\AI\B32_ChatGPT_Handoff\B32_Handoff.ahk'`，**不提供参数**；输出 `FAIL:NO_PROMPT_FILE`，退出码11，约275ms；符合脚本的安全输入校验设计，证明当前文件完成语法加载并到达预期入口检查，网页副作用0。
- 发现一个同路径旧AHK进程 PID 14036，启动于2026-10-09 20:29:52，本轮未结束。该进程可能持有旧内存代码，但尚未核实是否对应原截图；不能凭启动时间确定根因。
- 本轮不触发 `--commit`、不点击真实ChatGPT新聊天、不发送或替换原有浏览器/Profile。

## 后续定位原则
截图若仍弹出，先确认报错窗口的脚本绝对路径和运行进程 PID、启动时间，检查它加载的历史版本是否与当前磁盘源文件一致；同名旧进程退出并重新由**已核验入口**加载前不要声称问题彻底消失。只对真实仍存在的 `edit` 变量引用做一次完整作用域改名，避免盲改第56行。旧自动发送路径若没有合法验收仍保持未验证；已测试的无参数加载PASS不等于ChatGPT端到端handoff PASS。
