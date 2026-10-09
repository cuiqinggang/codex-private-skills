# 《B·新页面运行模板 第23版：状态码交接》

版本=B23｜继承B22→B21→B20→B19→共同 ../../NEW_PAGE_TEMPLATE.md 第18版
适用=B路线；引擎B32、大脑B29、共同第28版和A28不变。
状态=METHOD_DEFINED｜VIRTUAL_MATURE=NO｜REAL_HANDOFF_UNVERIFIED

## 唯一修正：传定位码，不传交接正文
旧B22要求把短NEXT_PAGE_PROMPT信封粘贴到新聊天。B23以**极短、可直接定位现有任务冻结的状态码**覆盖该传输格式。任务长文本、合同、证据、下一步都继续存在原GitHub任务CURRENT/Freeze中，不通过剪贴板逐项复制；不新建码表、数据库、桥接器、调度器或全文二次核验。

**B路线交接码标准格式**：
```text
续接B|cuiqinggang/codex-private-skills|<TASK_ID>|<FREEZE_ID>
```
- 固定引导词“续接B”明确要求新GPT恢复，而非把短码当普通文本；仓库固定为权威网络工作区。
- TASK_ID唯一定位 `skills/artificial-single-page-extreme-time-engine/tasks/<TASK_ID>/CURRENT.md`；FREEZE_ID提供本次合法冻结版本防错。
- 此码不是把全部交接文字物理压缩到几十字节，**它是已持久化全文的检索地址/索引**。运行状态值10/20/30/40/100仍由完整冻结文件提供，禁止混为一谈。

## 旧页只做四动作
前提：当前任务Freeze已经真实写入、任务CURRENT更新成功且FREEZE_ID匹配，原用户授权Chrome/ChatGPT目标窗口已确定。
1. 取得已签发的**短交接状态码**（不打开/拷贝完整NEXT_PAGE_PROMPT正文）。
2. 复用已安装AutoHotkey v2 + UIA-v2：按语义控件名称“新聊天”定位并点击，不读图、不按坐标、不判断侧边栏展开/收起，也不另开浏览器。
3. 新聊天输入框控件就绪后，粘贴**短码**，不校验长任务正文；必要时只校验状态码格式/冻结标识，防误发或剪贴板截断。
4. 发送一次，即返回“提交动作已尝试”；不等待GPT生成完整回答，不自动重复未知提交。新GPT自行恢复。
原450/350毫秒固定等待不是协议必要动作，保留成熟UIA条件就绪检测和故障超时停止。

## 新GPT收到此码的唯一恢复动作
1. 解析 `续接B|仓库|TASK_ID|FREEZE_ID`，定位权威网络仓库的 `SKILL.md`→`START_HERE.md`→`routes/B/ROUTE.md`；禁止根据模型猜测制造任务数据。
2. 直接读取 `tasks/<TASK_ID>/CURRENT.md`，核对TASK_ID及FREEZE_ID完全相等，再依该CURRENT中的 `CONTRACT_PATH`/`FREEZE_PATH` 及其 `TASK_STATE_REF` 读取已保存事实；方法`METHOD_REF`与任务`TASK_STATE_REF`分开。
3. 如果码不可解析、仓库不可访问、CURRENT缺失或FREEZE_ID变更，则标记BLOCKED/STALE_CODE，不自行假设旧码有效，也不重新执行可能有副作用的步骤。
4. 恢复原目标/下一节点继续。整个业务任务达到FINAL_VALID才算完成。短码送出并不等于新会话已成功接管，完整自动交接Reality仍须实证。

## 无变化边界
当前页只执行一个合适的自然节点，完成并Freeze后接续新聊天；不引入Codex、n8n、专用浏览器、额外状态机、截图、OCR、固定坐标。K盘三日备份与每次Freeze独立。保留唯一写者、Exactly-once、UNKNOWN不盲重试、REUSE_GATE、STOP_GATE与最终T_VALID门禁。
