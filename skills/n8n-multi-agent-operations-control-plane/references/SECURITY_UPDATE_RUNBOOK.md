# n8n 安全升级、备份与回滚 Runbook

## 目标

在不更换部署路线的前提下，把 `C:\AI\n8n` 的 n8n Docker Compose 实例升级到冻结的安全稳定版本，并留下可恢复证据。

## 0. 冻结目标版本

每次升级前：

1. 查询 n8n 官方 GitHub Releases 的 latest/stable；
2. 查询 n8n 官方 Security Advisories；
3. 取“稳定版”且版本号不低于所有相关漏洞修复下限；
4. 把版本号写死为本次 `TARGET_VERSION`，不要在脚本执行期间漂移。

2026-10-03 本轮冻结：

```text
TARGET_VERSION=2.41.6
```

## 1. 只读预检

必须确认：

- `C:\AI\n8n\compose.yml` 存在；
- Docker daemon 可用；
- 当前 n8n 容器可定位；
- 当前镜像/版本可读取；
- 数据卷 `n8n-local_n8n_data` 存在；
- Compose 仍把 5678 绑定到本机；
- 没有其他并发升级任务。

## 2. 备份

备份目录：

```text
C:\AI\n8n\backup\YYYYMMDD-HHmmss
```

至少保存：

- `compose.yml`；
- `.env`（只复制，不打印）；
- `DEPLOYMENT-STATUS.md`（若存在）；
- 数据卷完整 tar.gz；
- 升级前容器版本、image ID、RepoDigest、mounts、health 状态；
- 将旧 image ID 重新打本地 rollback tag。

## 3. 升级

推荐把 Compose 中 `n8nio/n8n:stable` 临时冻结为：

```text
n8nio/n8n:<TARGET_VERSION>
```

然后：

```powershell
docker compose pull
docker compose up -d
```

这样同一次升级可复验，不会因为 `stable` 指针未来变化而得到另一版本。

## 4. VALID 验收

全部满足才通过：

1. `docker compose ps` 显示 n8n Running；
2. `docker exec <container> n8n --version` = 目标版本；
3. `GET http://localhost:5678/healthz` = 200；
4. `/home/node/.n8n` 数据卷仍在；
5. `/files/artifacts` bind mount 仍在；
6. 不修改 FlClash / Windows 代理。

## 5. 自动回滚

任一关键验收失败：

1. `docker compose down`；
2. 恢复升级前数据卷快照；
3. 将 Compose 镜像切回本地 rollback tag；
4. `docker compose up -d`；
5. 再次验证旧版本与 `/healthz`；
6. 记录失败原因，不把失败升级标成成功。

## 6. 输出证据

每次升级至少输出：

- FROM_VERSION；
- TO_VERSION；
- BACKUP_DIR；
- OLD_IMAGE_ID；
- NEW_IMAGE_ID；
- HEALTH_STATUS；
- DATA_VOLUME_PRESENT；
- ARTIFACT_MOUNT_PRESENT；
- RESULT=PASS/ROLLED_BACK/FAIL。
