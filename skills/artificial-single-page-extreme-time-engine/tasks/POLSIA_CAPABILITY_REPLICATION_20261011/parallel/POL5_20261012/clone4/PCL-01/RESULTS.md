# PCL-01 真实运行验收结果

TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
BATCH_ID=PCL4_20261012
PARENT_FREEZE=POLSIA-MOTHER-V008-F001
NODE_ID=PCL-01
STATUS=BLOCKED_ENVIRONMENT
FINAL_VALID=NO
MOTHER_FINAL_VALID=NO

现有网站尚未恢复运行。已修正原 guard 的意外数据库/Docker 依赖，配置本地 worker=off，完成真实编译、离线状态保护、数据库连接、启动与 HTTP 检查。没有凭据造假，没有重建/改动监控网站，也没有改代理浏览器或历史 V001–V008。

正式任务已回读 GitHub main，源 Blob 为 b69ba0dc9d7f2f1b8a9c8ac54d534ee47634007c；远端归档父目录实际为 parallel/POL5_20261012/clone4，BATCH_ID 仍为 PCL4_20261012。

| 检查 | 实际结果及边界 | 回执 |
|---|---|---|
| 修改后 pnpm typecheck | 退出码 0；工具未暴露真实子进程 PID，未以 session ID 冒充 | evidence/COMMAND_RECEIPTS.json |
| 修改后 pnpm test:guard | 退出码 0，真实 guard PID 54456，三种 engineering 状态均符合预期 | evidence/COMMAND_RECEIPTS.json |
| 同入口直接 guard | PID 1032、退出码 0；15 个内存 SQL stub、3 次内存 sandbox/release、网络尝试 0 | evidence/guard.json |
| 有界 typecheck | PID 50304，45秒后 SIGTERM，退出码 null；此超时原样保留，后续正式 pnpm 检查通过 | evidence/typecheck.json |
| 本地真实 Postgres | localhost:5433/polsia，SELECT 1 连接 ECONNREFUSED，数据库可用性未通过 | evidence/database.json |
| 首次现有 dashboard | PID 47100，20秒后 SIGTERM，退出码 null，日志为空 | evidence/dashboard.json |
| 冷加载预算复核 dashboard | PID 56892，120秒后 SIGTERM，退出码 null，日志为空；加载阻塞点未确证 | evidence/dashboard-long.json |
| HTTP | 4317 的六个请求均连接拒绝，HTTP 状态 null；无业务 PASS | evidence/http.json |
| Docker 只读 | 现有 desktop-linux 服务 HTTP500；没有创建/删除/重启/重装 Docker | evidence/COMMAND_RECEIPTS.json |
| 配置核验 | 仅检查环境存在标志和 Pi 默认三个文件存在性；未找到合法模型入口，未记录秘钥值 | evidence/configuration.json |
| git diff --check / KB health | 都退出 0；KB 未同步、未修改 | evidence/COMMAND_RECEIPTS.json |

原 guard 在沙箱运行因 esbuild spawn EPERM 退出 1；提权原动作被自动审批拒绝，理由是会写数据库并创建 Docker sandbox，涉及被禁止的 Docker 底座变更。该原动作未再次执行。安全替代仅 mock db.ts 和 sandbox factory，运行真实 engineering worker、complete_task/fail_task；覆盖未断言→needs_continuation、明确完成、明确失败，逐案验证 release。Node 模块 mock 有实验性警告，输出 integrationVerified=false，不能证明真实 DB/Docker/模型集成成功。

实际源码差分仅 package.json 与 scripts/test-guard.ts，见 evidence/open-polsia.patch。新增本地忽略文件 .env 只关闭 worker，不增加或复制任何秘钥。未运行 seed：默认数据库无法连接，且 seed 会更新 demo 文档/上下文，不能在未知原数据上无条件重种。任务诊断脚本保存在 evidence/runtime-check.mjs。

业务可用边界：离线状态完整性可验收；网站读 API、聊天/onboarding/cron、工程 Docker 集成、云部署均没有本次成功证据。未执行真实付款、外联、发布。state 的收入字段是源代码占位值，不是营收验收。已导出 HTTP_API_CONTRACT.md 供 PCL-03 读取；这只声明现有接口，未证明端点在线。

恢复所需输入：现有本地隔离 Postgres 的正式入口/容器名或本地连接配置，以及已有合法 Pi 模型配置目录；请提供路径/名称，不提供秘钥正文。Docker 修复/底座变更不能由本任务一般授权推定。

GitHub 持久化：真实证据快照已提交 932ed8b35b589f858d7eff363ca23620b7dad4dc，随后独立 Agent 对提交内容回读校验 PASS。见 evidence/GITHUB_PUBLISH.json 与 evidence/GITHUB_INDEPENDENT_READBACK.json。本状态更新和独立回执另以最终回执提交保存；该最终提交的外部本地回执为 evidence/GITHUB_FINAL_PUBLISH.json，收尾独立回读为 evidence/GITHUB_FINAL_INDEPENDENT_READBACK.json，避免文件内自引用提交哈希。环境仍 BLOCKED_ENVIRONMENT，FINAL_VALID=NO。

CodeGraph usage:
- MCP available: YES（会话工具目录可用）
- CLI available: YES（codegraph.ps1）
- .codegraph index present: NO
- status checked before work: YES
- callers/callees/impact checked where relevant: 通过定向读取检查 bootstrap/worker/guard/runtime；未修改业务 worker
- sync/refresh run after meaningful code changes: N/A，无索引
- if not used, reason: 仓库无 .codegraph，按规则回退 rg 与定向读取

Knowledge Brain usage:
- INDEX checked: YES
- ROUTING_MAP checked: YES
- Relevant indexes checked: indexes/projects-index.md
- CodeGraph used where relevant: N/A，无索引
- OpenHuman reference used where relevant: N/A，运行恢复而非记忆架构任务
- Sync run before/after: NONE，未改知识库；kb_health_check.ps1 真实退出0/PASS
- If not used, reason: 已使用 C 盘复用矩阵，SHA256 b5f1ab2893e55c107f56b316bbbead6993eb2154ffad9039e57accf607595502；无全库扫描，无 H/K 读取或备份

补充模型环境复核：PID51508、退出0，14种已知模型环境变量存在标志全false，匹配的 API_KEY/AUTH_TOKEN/ACCESS_TOKEN 名称为空；未记录值、未调用模型。见 evidence/MODEL_ENV_PRESENCE.json。
