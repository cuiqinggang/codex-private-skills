# 完全不依赖 GPT 的强备份：如何使用

## 日常只需两个入口
1. 双击桌面「强备份-Google决策大脑」，打开 Gemini 网页与固定决策提示词。把实际任务写入 Google 对话，要求输出以 GOOGLE_BRAIN_PLAN_V1 开头的冻结执行方案。
2. 在 Google 对这段冻结方案点「复制」。双击桌面「强备份-执行Google方案」；Windows 本机直接从当前剪贴板读取一次，交给最新版 DeepSeek Harness 实际执行并记录任务身份/状态。无须打开 ChatGPT。

## 执行和复核
- 执行过程中，结果在 C:\AI\DeepSeek-Gemini-Failsafe\jobs\BACKUP-<指纹>\ 之下。
- STATUS.json 的 EXECUTING 不是成功；AWAITING_GOOGLE_REVIEW 表示执行器退出码为 0，但 Google 的独立复核未做；UNKNOWN 表示需要只读对账，不得再次运行同样方案。
- 查看 RESULT.md 和 EXECUTOR.log，与 DONE_WHEN 对照，再把必要证据提交给 Google 审核。不要把退出 0、模型说 DONE 等同于真实业务质量通过。
- 发现危险操作或超授权请求，暂停该任务，明确审批后再执行。助手不能替用户进行不可逆授权。

## 既有环境保护
- 新版 DeepSeek CLI：本目录 runtime\dsh-0.2.1-rc.2 下的隔离副本。原版 0.1.0-rc.6 未卸载。
- DeepSeek 凭据从 Windows 用户环境读取，不复制旧凭据库。
- Reasonix GUI 保留交互备用，不自动绕开文件写入批准。
- n8n 现有容器健康，但 V1 不依赖它。跨进程无人恢复需单独真实验收。
- 不改 FlClash、不改 Windows 系统代理、不改当前浏览器已有会话。

## 已知边界
- Google Gemini 网页标签存在（登录有效性尚未单独验证），但现有 9223 浏览器 Playwright attach 超时；故 V1 的 Google→DeepSeek 交接依赖人工点击“复制”，而不是无人值守自动派发。原有 ChatGPT 宕机时，以上两个桌面入口仍可使用。
- 原有状态持久化 V3 不能假设自动运行于这个新系统；这里只复用了不可重复提交、UNKNOWN 对账、轻量回执等语义。真实跨进程恢复与 n8n 联调通过前不可标称全自动强备份。
