# B33 极简短码交接：虚拟成熟与现实局部检测第1轮

TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
ENGINE_CANDIDATE=B33
BRAIN=B29｜TEMPLATE=B23
REALITY_SCOPE=READ_ONLY_PRECHECK_AND_INVALID_INPUT
FULL_REAL_CHAT_HANDOFF=NOT_RUN
VIRTUAL_MATURE=NO
FINAL_VALID=NO

## 成熟基线与最短原则
继承B32现有AutoHotkey v2 + Descolada/UIA-v2，同一普通Chrome窗口同标签“新聊天”语义按钮。只变更传输内容：旧全文信封→ `续接B|cuiqinggang/codex-private-skills|TASK_ID|FREEZE_ID` 四字段短码。完整Freeze由现有GitHub CURRENT索引，非新建状态数据库。无需Codex、n8n、9223、截图、坐标、额外浏览器。
现有本机B32脚本复制为B33_Handoff.ahk并仅修订短码检验；现有B32脚本未改动。GitHub新文件 `routes/B/adapter/B33_Handoff.ahk` 已创建。
旧脚本450/350ms固定等待已经在B32实现中替换为20ms条件就绪轮询（2秒为故障超时上限），B33继承成熟实现。短码可在数十字节至数百字节内完成跨页定位；这不代表完整上下文物理压缩或新GPT无需时间读取。

## 21个虚拟状态条件（规则级）
正常即时就绪、30/10ms控件、470/290ms控件、1900/1940ms控件：成功尝试一次，不带固定等待。
无效短码、Freeze未保存、TASK CURRENT不符、旧冻结码、多写者、错窗口、重复按钮、输入框超时/未就绪、粘贴超时/不一致：立即阻塞，不发送。
提交结果未知：不重发。新会话未能读GitHub或状态对不上：记录SENT_BUT_NOT_RESTORED，不伪称接管。原业务已确认执行或副作用未知时禁止重复业务执行。
本次模型化脚本断言21/21符合预期。输入场景时间为人工指定的确定性边界值，不是21次浏览器实际交接。理论固定Sleep=0ms，不能声称T_VALID=0ms。

## 实际可复核代码检测
Windows设备：DESKTOP-4A1EGTM，Desktop Commander在线。B33_Handoff.ahk已本地复制；GitHub对应新文件可读。
用B33真实AHK运行三组负输入：
- 旧不合格文本：退出13，316ms，FAIL:INVALID_STATE_CODE；
- 旧长信封：退出13，114ms，FAIL:INVALID_STATE_CODE；
- 不存在的输入文件：退出12，126ms，FAIL:PROMPT_NOT_FOUND。
三组都未访问页面控件或发送，证明短码新规则拒绝旧信封和文件缺失。**有效四字段短码输入及真实新聊天提交尚未执行。**
尝试写入本地有效测试码文件时执行工具安全检查拒绝；不能伪造完整成功。
一项原B32只读UIA控件探测启动后未返回最终结果，存在挂起现象，本轮不视为PASS；尝试仅终止本探测专属子进程同样受到工具安全检查拒绝，未触碰用户其它浏览器进程。

## 尚需Reality及时间
真实短码文件输入→原普通Chrome确定当前目标窗口→新聊天→输入框就绪→短码粘贴→提交一次→新GPT按GitHub恢复完整目标→实质结果VALID；缺任何一段不得计算完整T_B_VALID。
现已测得的是3组负例拒绝时间，不是端到端有效时间或物理极限。
ROUTE指针B33正式激活的GitHub写入遇到执行工具安全拦截，需核对当前正式ROUTE实际值；不得把B33文件已存在称作已激活。
STOP_GATE=NOT_PASSED，VIRTUAL_MATURE=NO，FINAL_VALID=NO。

## 下一步
先确保安全操作能力恢复，以现成成熟接口修复且完成明确授权的无业务短码实际一次交接，独立测量接力开始到消息提交、消息提交到新GPT读取Freeze、完整任务至VALID三段。仍按同质量T*=min(T_VALID)决策，K盘ZIP每三天独立备份。
