# 初始安装与部署 Reality

## 已确认的真实落地

历史 Reality 已确认：

- Windows 使用 Docker Desktop / WSL2；
- n8n 通过 Docker Compose 运行；
- 正式目录：`C:\AI\n8n`；
- Compose：`C:\AI\n8n\compose.yml`；
- 历史运行版本：`2.38.7`；
- 容器：`n8n-local`；
- 镜像路线：`n8nio/n8n:stable`；
- 本地入口：`http://localhost:5678`；
- 健康端点：`http://localhost:5678/healthz`；
- 数据卷：`n8n-local_n8n_data:/home/node/.n8n`；
- 成果目录：`C:\AI\n8n\artifacts:/files/artifacts`；
- 重启策略：`unless-stopped`。

## 原始成熟路线

原始安装选择是官方 Docker / Compose 方案，而不是 npm 全局安装。后续维护必须保持这个部署模型，除非另立迁移任务并单独 Reality 验证。

## 日常启动/查看

```powershell
Set-Location C:\AI\n8n
docker compose up -d
docker compose ps
```

查看版本：

```powershell
docker exec n8n-local n8n --version
```

健康检查：

```powershell
Invoke-WebRequest http://localhost:5678/healthz -UseBasicParsing
```

## 重要文件

- `compose.yml`：部署定义；
- `.env`：可能包含密钥，只允许备份，不允许把内容写入日志；
- `DEPLOYMENT-STATUS.md`：历史部署状态（如存在）；
- `artifacts\`：运行成果目录。
