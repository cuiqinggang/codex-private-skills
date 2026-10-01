# Windows runner 一次性接入

目标：把目标 Windows 变成共同私库的 GitHub self-hosted runner。

## 为什么默认不是 Windows 服务

当前标准题包含桌面/用户配置/潜在剪贴板场景。
Windows 服务位于 session 0，长期更稳但不适合作为第一版交互桌面执行面。
因此 v0.1.1 默认：

```text
GitHub runner
→ 当前 Windows 用户上下文
→ 登录时由任务计划程序自动启动
→ 当前安装完成后立即启动
```

后续如果 Reality 证明不需要桌面交互，可竞争 service 模式。

## 自动令牌优先级

安装脚本依次尝试：

1. 参数 `-RegistrationToken`；
2. 环境变量 `GITHUB_RUNNER_REGISTRATION_TOKEN`；
3. 已安装且已登录的 `gh`，自动调用 GitHub API 取得短时注册 token；
4. 都不存在则 fail-closed，不伪装安装成功。

## 固定成熟组件

GitHub Actions Runner v2.337.0，Windows x64。
SHA256：
`1150692afa94e71f872017e254ea55b6eece1eece3fe7e3a6d4c93d0a1b85cfc`
