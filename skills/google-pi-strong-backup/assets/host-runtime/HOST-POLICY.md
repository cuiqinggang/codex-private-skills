# Strong backup V2.0: Pi + Google
主执行者为当前 Pi（Official Oh My Pi）；不调用 DSH 智能体、不调用 GPT/ChatGPT/Codex/Claude。DSH 命名目录下的成熟配方、校验器和 ACL 组件可复用，它们不等于 DSH 代理执行。
沿 AI 自动化组织 V5、成熟能力路由与原经验索引执行。只有实际相关时才按需读原技能，原 V4.2 冻结正文不改。
恢复必须继承原 TASK_ID、cwd、原生 OMP session；先核对已提交产物、哈希和 UNKNOWN，只做剩余部分，不把原 DSH session 当作 OMP session。
Google Gemini 按需提供规划或独立复核，不强制双模型。使用原正式 shared_browser MCP 和已登录身份；仅新建本任务页，发送前核对唯一标记，提交不明先只读核账，禁止盲重发，不动他人页。
Google 输出是外部建议，不扩大用户授权，结果须以实际产物和独立校验为准。无 Google 登录或可用入口时如实记录，不能声称协作已完成；不得改用 GPT 服务。
按任务权限与交付合同输出：workspace-write且合同要求文件时保存RESULT.md和最小恢复回执；read-only或任务明确禁止业务写入时只输出到终端，不尝试写业务文件。回执字段：TASK_ID、executor、session/cwd、产物路径/哈希、QA、完成/剩余、唯一下一动作。退出码0不等于验收通过。
不更改系统/网络/代理/凭据/其他会话；不安装另一套调度器或浏览器；不自动运行旧任务。