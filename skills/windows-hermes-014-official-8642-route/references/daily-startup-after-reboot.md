# 重启后打开 Windows 原生爱马仕页面

## 直接双击的文件

日常推荐双击：

```text
H:\Hermes_Windows_Native_014\明天重启后打开爱马仕页面.cmd
```

如果中文文件名在某台机器上不稳定，双击纯英文备用入口：

```text
H:\Hermes_Windows_Native_014\START-HERMES-WEBUI.cmd
```

不要把 `.md` 当作启动文件。`.md` 是说明文档；Windows 没有关联 Markdown 阅读器时，双击可能没有反应。

## 实际脚本

两个 `.cmd` 都调用这个 ASCII 路径脚本：

```text
H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1
```

技能包内保存了参考副本：

```text
scripts/start-hermes-openwebui.ps1
scripts/明天重启后打开爱马仕页面.cmd
scripts/START-HERMES-WEBUI.cmd
references/使用说明-明天重启后打开爱马仕页面.txt
```

## 启动顺序

脚本按这个顺序等待：

```text
Hermes 8642 health
-> /v1/models contains hermes-agent
-> Docker Desktop API ready
-> Open WebUI 3000 health
-> Open http://127.0.0.1:3000
```

这个顺序来自实测：Open WebUI 依赖 Hermes 后端 `http://host.docker.internal:8642/v1`，所以必须先等 Hermes 8642 正常，再打开页面。

## 启动时间预期

- Hermes 已经运行：通常几秒内通过。
- Hermes 冷启动：一般几十秒内通过。
- Docker Desktop 冷启动：可能需要 1 到 5 分钟。
- Open WebUI 容器启动：Docker 就绪后通常几十秒内通过。

脚本会等待，不需要重复点击。

## 成功标志

窗口最后看到：

```text
FINAL_PASS Windows native Hermes page is ready
```

然后浏览器打开：

```text
http://127.0.0.1:3000
```

## 日志位置

每次运行会写日志：

```text
H:\Hermes_Windows_Native_014\reports\daily-start-YYYYMMDD-HHMMSS.log
```

## 安全边界

脚本不会：

- 修改 Open WebUI 配置
- 修改 Hermes 配置
- 迁移 memory 或 sessions
- 打印 API key、token、password
- 随机停止进程
- 创建系统开机自启动项

如果失败：

- `G01_FAIL`: Hermes 8642 没有健康，查看 `C:\Users\A\.hermes\logs\gateway-8642-stderr.log`
- `G02_FAIL`: Docker Desktop 没有启动好，手动打开 Docker Desktop 后再运行脚本
- `G03_FAIL`: Open WebUI 3000 没有健康，查看 Docker Desktop 容器状态
