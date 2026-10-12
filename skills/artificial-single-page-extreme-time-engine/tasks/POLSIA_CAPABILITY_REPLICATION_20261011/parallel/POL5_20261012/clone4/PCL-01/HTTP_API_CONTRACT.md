# PCL-01 → PCL-03 现有 HTTP 接口边界

来源：现有 src/services/dashboard.ts。默认请求入口 http://127.0.0.1:4317，目前全部 HTTP 探测连接拒绝；下表为源代码合同，不是线上成功回执。启动 .listen(port) 未指定 host，恢复成功后仍需回读真实监听地址，不能把 localhost 日志当作回环绑定证明。worker 配置 off。

| 方法/路径 | 合同与依赖 | 本次证据 |
|---|---|---|
| GET / | 现有 HTML | ECONNREFUSED |
| GET /api/state | JSON 公司/worker/busy/counts/任务/文档/报告；依赖 Postgres；revenue 是占位值 | ECONNREFUSED |
| GET /api/messages | JSON messages 数组；依赖 Postgres | ECONNREFUSED |
| GET /api/document?type=mission | JSON type/content；依赖 Postgres | ECONNREFUSED |
| GET /api/report?id=... | 现有报告读取；依赖 Postgres | NOT_TESTED |
| GET /fonts/pixel.woff2 | 本地字体 | ECONNREFUSED |
| GET /fonts/sans.woff2 | 本地字体 | NOT_TESTED |
| 未知路径 | 源代码返回404 | 实际连接拒绝，未验证404 |
| POST /api/chat | SSE；模型与Postgres；会写聊天并可能创建任务 | NOT_EXECUTED |
| POST /api/onboard、/api/cron 与 GET /run/:id | 可写库并执行模型/工程任务 | NOT_EXECUTED |
| POST /api/proxy/llm | 先校验公司 bearer，再调用 Anthropic；其他 Pi provider 不证明可用 | NOT_EXECUTED |
| POST /api/approve/:id、/api/reject/:id | 改写任务状态；批准后若 worker 开启可触发执行 | NOT_EXECUTED |
| POST /api/worker?on=true | 能开启旧队列自动执行 | NOT_EXECUTED；保持off |
| POST /api/reset | 删除公司业务状态的操作 | NOT_EXECUTED |

PCL-03 可消费 STATUS.json、evidence/http.json 与本合同；当前不要触发上述写接口、worker、付款、外联或云部署。未重建/修改外部监控站。
