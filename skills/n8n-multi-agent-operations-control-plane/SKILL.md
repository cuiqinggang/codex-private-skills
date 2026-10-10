---
name: n8n-multi-agent-operations-control-plane
version: "1.0.1"
description: n8n 多智能体运行指挥台。恢复并管理既有 Windows Docker Compose 部署，负责安全升级、备份、验收与回滚；不重造部署路线。
---

# n8n 多智能体运行指挥台技能包 v1.0.1

```ini
STATUS=REALITY_DEPLOYMENT_CONFIRMED
VERSION=1.0.1
DISPLAY_NAME=n8n 多智能体运行指挥台技能包

DEPLOYMENT_OS=Windows
DEPLOYMENT_MODE=Docker Desktop + WSL2 + Docker Compose
DEPLOYMENT_ROOT=C:\AI\n8n
COMPOSE_FILE=C:\AI\n8n\compose.yml
N8N_URL=http://localhost:5678
N8N_BIND=127.0.0.1:5678
HEALTH_URL=http://localhost:5678/healthz
CONTAINER_NAME=n8n-local
DATA_VOLUME=n8n-local_n8n_data
DATA_MOUNT=/home/node/.n8n
ARTIFACT_HOST=C:\AI\n8n\artifacts
ARTIFACT_MOUNT=/files/artifacts
HISTORICAL_VERSION=2.38.7

SECURITY_BASELINE_DATE=2026-10-03
SECURITY_TARGET_VERSION=2.41.6
TARGET_CHANNEL=stable
```

## 角色

n8n 是多智能体运行指挥台，负责任务入口、流程编排、状态观察和运行控制。既有链路可继续连接 MOA / ARO / Codex / Reasonix 等执行层；本技能包不重造这些执行器。

## 固定部署原则

1. 沿用已验证的 Docker Compose 路线，不切换成 npm 全局安装。
2. Windows 主系统与网络代理不得因升级而改变。
3. 每次升级先读取真实部署，再做备份，再升级；禁止“直接 pull 后赌结果”。
4. 生产升级目标必须是官方已发布稳定版，并记录明确版本号；不得长期依赖不可追溯的浮动结果。
5. 升级后必须同时验证：
   - 容器 Running；
   - `n8n --version` 等于目标版本；
   - `/healthz` HTTP 200；
   - 数据卷仍挂载到 `/home/node/.n8n`；
   - `C:\AI\n8n\artifacts` 仍挂载到 `/files/artifacts`。
6. 任一验收失败，进入回滚，不得宣布成功。

## 当前安全基线

2026-10-03 官方稳定版为 **2.41.6**。本次升级以 2.41.6 为固定目标。以后再次执行时，必须重新从 n8n 官方 release / security advisories 解析“当前 stable + 所有已公开漏洞的最低修复版本”，再冻结新的目标版本。

## 入口

- 初始部署说明：`references/INSTALL_DEPLOYMENT.md`
- 安全升级流程：`references/SECURITY_UPDATE_RUNBOOK.md`
- 可复用升级脚本：`scripts/Update-N8nSecure.ps1`

## 安全边界

- 不修改 FlClash。
- 不修改 Windows 网络代理。
- 不删除 Windows 系统。
- 不输出 `.env`、凭据或密钥内容。
- 备份文件只保存在本机部署目录的 `backup\<timestamp>`。


## v1.0.1 现场复核与隔离测试事故（2026-10-11）

### 真实可回读基线
- 原生产容器 `n8n-local` 仍 `Up (healthy)`；实际 `n8n --version=2.38.7`；`127.0.0.1:5678/healthz` 返回HTTP200。
- 原生产7个工作流经 `docker exec n8n-local n8n list:workflow --all` 成功列出，未发现被新测试替换：`gzenqhusv2wKoWAF`、`PY9w2v8FnZmj7nff`、`n8nDeploy03E2E`、`n8nNativeE2E01`、`n8nNativeE2E02`、`n8nNativeE2E03`、`v27McpReadonly20261009`。
- 通过 `docker inspect n8n-local` 核验：`n8n-local_n8n_data:/home/node/.n8n` 与 `C:/AI/n8n/artifacts:/files/artifacts` 仍正确挂载。本轮未重装、不改生产容器和FlClash。

### 临时隔离测试事故与恢复原则
- 临时测试容器 `engine29-n8n-isolated` 曾完成创建、单流程导入、发布命令返回成功，但随后 `docker restart` 报 `No such container`。
- `docker ps -a` 只显示生产 `n8n-local` 等其他容器，临时容器不在；Docker事件出现 `kill → die → destroy`，**操作来源和消失根因仍未知**，不能虚构是谁删除，也不能断言平台、n8n本体或生产数据损坏。
- 独立测试定义文件仍在 `C:\Users\A\Documents\Codex\ENGINE29_STATE_CANDIDATES\n8n_isolated_webhook.json`，不等于容器中导入的工作流运行结果已经持久保存。
- 该测试没有获取 `Webhook → 节点执行 → HTTP最终回执`，所以 `ISOLATED_N8N_E2E=NOT_VALIDATED`。导入/发布、容器健康只算前置检查。
- 原 `N8N-MCP-SHARED-20261009` 的任务合同第1版与 `N8N-MCP-SHARED-F002` 冻结第2版仍为历史GOOD基线；其中已完成MCP读写、跨工作流串行、去重与Wait恢复等，不等于完整共享浏览器生产入口已经FINAL_VALID。

### 最短复验方法（只对未完成差分）
1. **先只读确认原生产环境**：`docker ps`、`n8n --version`、`/healthz`、7个工作流、数据卷；正常就禁止重装或无故调整生产配置。
2. **隔离实验必须有持久测试目录/卷和唯一名称**，与生产容器及原7工作流严格分开；事先确认容器删除/清理策略，异常消失先核对Docker事件、生命周期与残存卷，不将新容器成功创建误判为已稳定运行。临时容器丢失时，从现存合法测试定义重建仅该隔离实验，不重装整个n8n。
3. **正式成功必须有同一测试任务的真实入口请求、执行记录与最终结果**；结果UNKNOWN时先查执行日志，禁止盲目二次触发，确保Exactly-once。
4. 原有n8n CLI在运行中的容器内执行`n8n execute`曾遇Task Broker端口5679冲突，优先调用正常Webhook入口；已知业务Webhook不能当无副作用测试接口。
5. 本次只更新技能包方法和实测事实；不改生产n8n版本。软件安全升级须独立遵循备份→当前稳定版/漏洞确认→升级→回滚流程，不能把技能包版本升级误称软件已升级。

STATUS_REALITY_20261011=PRODUCTION_N8N_HEALTHY_COMPONENTS_CONFIRMED
STATUS_ISOLATED_E2E=NOT_VALIDATED
STATUS_SHARED_BROWSER_END_TO_END=NOT_VALIDATED
