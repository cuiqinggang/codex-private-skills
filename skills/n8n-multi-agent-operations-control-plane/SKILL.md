---
name: n8n-multi-agent-operations-control-plane
version: "1.0.0"
description: n8n 多智能体运行指挥台。恢复并管理既有 Windows Docker Compose 部署，负责安全升级、备份、验收与回滚；不重造部署路线。
---

# n8n 多智能体运行指挥台技能包 v1.0.0

```ini
STATUS=REALITY_DEPLOYMENT_CONFIRMED
VERSION=1.0.0
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
