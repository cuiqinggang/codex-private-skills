# UltraFusion Sites 测试页面部署 SOP

## 1. 冻结范围

记录用户要求的唯一改动、禁止项、时间门禁、最终状态词和能力边界。若用户中途收窄范围，先撤回尚未提交的扩大改动，再按新范围继续。

## 2. 定位真实站点

必须形成四项闭环证据：

1. 原网址；
2. 真实源码绝对路径；
3. Git remote、当前分支和 HEAD；
4. .openai/hosting.json 的现有 project_id。

再用 Sites get_site 验证 slug、live URL、版本号和访问模式。任一对应不上，状态为 MINIMAL_PATCH_BLOCKED，不得另建页面代替。

## 3. 建立隔离候选

- 记录正式源码基线和已有未跟踪文件。
- 从当前正式 HEAD 创建独立 Worktree 和 RC 分支。
- 不修改旧 RC 目录，不合并本地主分支。
- 若仓库无 .codegraph，记录原因并用 rg/人工调用链检查；有索引则 CodeGraph-first。

## 4. 最小集成

- 移动或复用既有 question、fullReply 等 DOM ID，避免同页重复 ID。
- Q0 可使用独立轻量字段；不得复制 calculateAll、evaluateGates、collect 等核心逻辑。
- 新按钮只调用既有装配、解析、保存函数或薄包装函数。
- 详细业务面板使用 details/dialog 默认折叠，不删除原字段。
- 对夹具方括号和正式中文方括号的兼容，只扩展同一个解析器。
- 正式提示词不编辑；同时验证字符、部署字节和 SHA-256。注意 Windows CRLF 可能让工作树字节数不同，必须以构建/部署资产和正式合同为准，禁止凭感觉重写原文。

## 5. 本地验收

1. npm run build。
2. 原业务测试 10/10。
3. VT-01～VT-05 浏览器测试 5/5。
4. 截图严格为每套 3 张；测试输出目录区分 local 与 postdeploy，防止线上复验覆盖本地证据。
5. 保存 JSON、Markdown、断言 JSON、控制台日志。
6. 验证截图 15、导出数量、控制台错误 0、真实样本 0、L3、REVISE。

未发布时只能报告 LOCAL_MINIMAL_PATCH_PASS_READY_FOR_DEPLOY。

## 6. 精确发布

1. 确认 tracked tree clean、测试通过、HEAD 已提交。
2. 使用 Sites 源凭证按单命令 HTTP header 推送同一 HEAD；不得把 token 写入 remote、文件或输出。
3. 验证远端目标分支 SHA 等于本地 HEAD。
4. 用 Sites 官方打包脚本从该提交的构建产物生成 archive。
5. save_site_version(project_id, commit_sha, archive)。
6. 对 owner-only 站点使用 deploy_private_site_version。
7. 若连接器出现一次参数转发型瞬时错误，可用完全相同的精确参数重试一次；不得换建新站。
8. 轮询 deployment 到终态。

## 7. 线上复验

- 从原根网址进入，确认仍是同一域名并落到真实入口。
- 首屏存在 3 个粘贴框，详细面板折叠，旧长页不再是默认操作入口。
- 1366×768 与 1920×1080 检查滚动要求。
- 线上执行 VT-01 完整流程；VT-02～05 执行关键路径。
- 再跑原业务回归 10/10 或等价生产断言。
- 控制台/Page Error 为 0。
- 核对 Sites 最新版本号、版本 commit、远端 commit、本地 commit。

## 8. 收尾

- 保存生产截图、断言 JSON、日志和版本 ID。
- 关闭浏览器/开发服务器，清理仅由本次产生的临时 Playwright 缓存。
- 不删除证据、用户文件或旧版本。
- 运行 Knowledge Brain Health Check；新增技能/记录时只对显式文件 Hot Sync。
- 最终仍声明真实样本 0、L3、REVISE、下一关口 L4。

